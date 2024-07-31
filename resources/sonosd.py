import asyncio
from typing import List

from soco import SoCo, discover, events_asyncio
import soco.config as soco_config
from soco.data_structures import SearchResult

from jeedomdaemon.base_daemon import BaseDaemon
from jeedomdaemon.base_config import BaseConfig

from sonos.data import SonosData
from sonos.speaker import SonosSpeaker

class SonosConfig(BaseConfig):
    def __init__(self):
        super().__init__()

class SonosDaemon(BaseDaemon):
    def __init__(self) -> None:
        self._config = SonosConfig()
        super().__init__(self._config, self._on_start, self._on_message, self._on_stop)

        soco_config.EVENTS_MODULE = events_asyncio
        self._speakers:dict[str, SonosSpeaker] = {}
        self._sonos_data = SonosData()

        self._favorites = List[dict]
        self._radios: SearchResult

    async def _on_start(self):
        await self._discover_and_sync()

    async def _on_message(self, message: list):
        if 'action' not in message:
            self._logger.error('No action in message: %s', message)
            return

        if 'ip' in message:
            if message['ip'] not in self._speakers:
                self._logger.warning('No speaker with ip: %s', message['ip'])
                return

            speaker = self._speakers[message['ip']]
            coordinator = speaker if speaker.is_coordinator else speaker.coordinator

            if message['action'] == 'mute':
                speaker.soco.mute = True
            elif message['action'] == 'unmute':
                speaker.soco.mute = False
            elif message['action'] == 'volume':
                speaker.soco.volume = message['slider']
            elif message['action'] == 'switch_to_line_in':
                speaker.soco.switch_to_line_in()
            elif message['action'] == 'switch_to_tv':
                speaker.soco.switch_to_tv()

            elif message['action'] == 'repeat':
                coordinator.soco.repeat = not coordinator.soco.repeat
            elif message['action'] == 'shuffle':
                coordinator.soco.shuffle = not coordinator.soco.shuffle
            elif message['action'] == 'play_mode':
                coordinator.soco.play_mode = message['select']
            elif message['action'] == 'play':
                coordinator.soco.play()
            elif message['action'] == 'pause':
                coordinator.soco.pause()
            elif message['action'] == 'stop':
                coordinator.soco.stop()
            elif message['action'] == 'previous':
                coordinator.soco.previous()
            elif message['action'] == 'next':
                coordinator.soco.next()

            elif message['action'] == 'join':
                try:
                    master = next(item for item in self._speakers.values() if item.zone_name==message['title'])
                    master = master if master.is_coordinator else master.coordinator
                    speaker.soco.join(master)
                except StopIteration:
                    self._logger.warning("No zone '%s'", message['title'])
            elif message['action'] == 'unjoin':
                speaker.soco.unjoin()

            elif message['action'] == 'play_favorite':
                try:
                    # fav = next(f for f in self.__sonos_data.favorites if f.title == message['title'])
                    fav = next(f for f in self._favorites if f['title'] == message['title'])
                    # self._logger.warning(vars(fav))
                    self._logger.info("playing favorite %s in %s", fav, coordinator.zone_name)
                    # coordinator.soco.play_uri(fav['uri'], fav['meta'], fav['title'])
                    # # coordinator.soco.play_uri(fav['uri'], '', fav['title'])
                    coordinator.soco.clear_queue()
                    # # coordinator.soco.add_to_queue(fav)
                    # todo: try to fix this so we can use soco.music_library.get_sonos_favorites() and avoid warning in log
                    coordinator.soco.avTransport.AddURIToQueue(
                        [
                            ("InstanceID", 0),
                            ("EnqueuedURI", fav['uri']),
                            ("EnqueuedURIMetaData", fav['meta']),
                            ("DesiredFirstTrackNumberEnqueued", 0),
                            ("EnqueueAsNext", 0),
                        ]
                    )

                    coordinator.soco.play_from_queue(0)
                except StopIteration:
                    self._logger.error("Favorite '%s' not found, cannot play on %s", message['title'], speaker.zone_name)
            elif message['action'] == 'play_playlist':
                playlist = coordinator.soco.get_sonos_playlist_by_attr('title', message['title'])
                coordinator.soco.clear_queue()
                coordinator.soco.add_to_queue(playlist)
                self._logger.info("playing playlist %s in %s", playlist, coordinator.zone_name)
                coordinator.soco.play_from_queue(0)
            elif message['action'] == 'play_radio':
                radio = next(r for r in self._radios if r.title == message['title'])
                coordinator.soco.clear_queue()
                coordinator.soco.add_to_queue(radio)
                self._logger.info("playing radio %s in %s", radio, coordinator.zone_name)
                coordinator.soco.play_from_queue(0)

            elif message['action'] == 'tts':
                coordinator.snapshot(False)
                coordinator.soco.play_mode = 'NORMAL'
                speaker.soco.mute = False
                try:
                    speaker.soco.volume = int(message['title'])
                except ValueError:
                    pass
                coordinator.soco.play_uri(f"x-file-cifs:{message['file']}", '', 'text-to-speech')
                await asyncio.sleep(1)
                while coordinator.media.playback_status == 'PLAYING':
                    await asyncio.sleep(0.5)
                await asyncio.sleep(0.5)
                coordinator.restore()

            else:
                self._logger.error("Unknown action '%s' for speaker %s", message['action'], message['ip'])
            return
        if message['action'] == 'sync':
            await self._discover_and_sync()
        else:
            self._logger.error('Unknown action: %s', message['action'])

    async def _on_stop(self):
        for speaker in self._speakers.values():
            await speaker.async_unsubscribe()

    async def _discover_and_sync(self):
        await self.__discover_controllers()

        for speaker in self._speakers.values():
            await self.__send_speaker(speaker)

        random_speaker = next(iter(self._speakers.values()))
        coordinator = random_speaker if random_speaker.is_coordinator else random_speaker.coordinator
        self._logger.debug(f"use {coordinator.zone_name} to get favorites, playlists & radios")
        await self.__get_favorites(coordinator)
        await self.__get_playlists(coordinator)
        await self.__get_radios(coordinator)

    async def __discover_controllers(self):
        socos: List[SoCo]
        socos = list(discover())
        for soco in socos:
            self._logger.info(f"found speaker {soco.player_name}")
            new_speaker = SonosSpeaker(self._sonos_data, soco, self.__on_speaker_change)
            self._sonos_data.discovered[soco.uid] = new_speaker
            self._speakers[soco.ip_address] = new_speaker
            await self.add_change(f'controllers::{new_speaker.ip_address}', new_speaker.get_info())

    async def __get_favorites(self, speaker: SonosSpeaker):
        result = speaker.soco.get_sonos_favorites()
        self._logger.info("get %s favorites out of %s", result['returned'], result['total'])
        self._logger.debug('favorites: %s', result['favorites'])
        self._favorites = result['favorites']

        results = speaker.soco.music_library.get_sonos_favorites()
        self._logger.info("get %s favorites out of %s", results.number_returned, results.total_matches)

        # self._logger.debug('favorites: %s', result['favorites'])
        self._sonos_data.favorites = results
        await self.add_change('favorites', list({r.title for r in results}))

    async def __get_playlists(self, speaker: SonosSpeaker):
        results = speaker.soco.get_sonos_playlists()
        self._logger.info("get %s playlists out of %s", results.number_returned, results.total_matches)
        await self.add_change('playlists', list({r.title for r in results}))

    async def __get_radios(self, speaker: SonosSpeaker):
        self._radios = speaker.soco.music_library.get_favorite_radio_stations()
        self._logger.info("get %s radios out of %s", self._radios.number_returned, self._radios.total_matches)
        await self.add_change('radios', list({r.title for r in self._radios}))

    async def __send_speaker(self, speaker: SonosSpeaker):
        await self.add_change(f'speakers::{speaker.ip_address}', speaker.to_dict())

    def __on_speaker_change(self, speaker: SonosSpeaker):
        self._loop.create_task(self.__send_speaker(speaker))
        for s in speaker.sonos_group:
            self._loop.create_task(self.__send_speaker(s))


SonosDaemon().run()