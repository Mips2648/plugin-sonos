"""Const for Sonos."""

from __future__ import annotations

import datetime

UPNP_ST = "urn:schemas-upnp-org:device:ZonePlayer:1"

DOMAIN = "sonos"
DATA_SONOS = "sonos_media_player"
DATA_SONOS_DISCOVERY_MANAGER = "sonos_discovery_manager"

SUB_FAIL_ISSUE_ID = "subscriptions_failed"
SUB_FAIL_URL = "https://www.home-assistant.io/integrations/sonos/#network-requirements"

SONOS_ARTIST = "artists"
SONOS_ALBUM = "albums"
SONOS_PLAYLISTS = "playlists"
SONOS_GENRE = "genres"
SONOS_ALBUM_ARTIST = "album_artists"
SONOS_TRACKS = "tracks"
SONOS_COMPOSER = "composers"
SONOS_RADIO = "radio"
SONOS_OTHER_ITEM = "other items"

SONOS_STATE_PLAYING = "PLAYING"
SONOS_STATE_TRANSITIONING = "TRANSITIONING"

SONOS_TYPES_MAPPING = {
    "A:ALBUM": SONOS_ALBUM,
    "A:ALBUMARTIST": SONOS_ALBUM_ARTIST,
    "A:ARTIST": SONOS_ARTIST,
    "A:COMPOSER": SONOS_COMPOSER,
    "A:GENRE": SONOS_GENRE,
    "A:PLAYLISTS": SONOS_PLAYLISTS,
    "A:TRACKS": SONOS_TRACKS,
    "object.container.album.musicAlbum": SONOS_ALBUM,
    "object.container.genre.musicGenre": SONOS_GENRE,
    "object.container.person.composer": SONOS_COMPOSER,
    "object.container.person.musicArtist": SONOS_ALBUM_ARTIST,
    "object.container.playlistContainer.sameArtist": SONOS_ARTIST,
    "object.container.playlistContainer": SONOS_PLAYLISTS,
    "object.item": SONOS_OTHER_ITEM,
    "object.item.audioItem.musicTrack": SONOS_TRACKS,
    "object.item.audioItem.audioBroadcast": SONOS_RADIO,
}

LIBRARY_TITLES_MAPPING = {
    "A:ALBUM": "Albums",
    "A:ALBUMARTIST": "Artists",
    "A:ARTIST": "Contributing Artists",
    "A:COMPOSER": "Composers",
    "A:GENRE": "Genres",
    "A:PLAYLISTS": "Playlists",
    "A:TRACKS": "Tracks",
}

SONOS_CHECK_ACTIVITY = "sonos_check_activity"
SONOS_CREATE_ALARM = "sonos_create_alarm"
SONOS_CREATE_AUDIO_FORMAT_SENSOR = "sonos_create_audio_format_sensor"
SONOS_CREATE_BATTERY = "sonos_create_battery"
SONOS_CREATE_FAVORITES_SENSOR = "sonos_create_favorites_sensor"
SONOS_CREATE_MIC_SENSOR = "sonos_create_mic_sensor"
SONOS_CREATE_SWITCHES = "sonos_create_switches"
SONOS_CREATE_LEVELS = "sonos_create_levels"
SONOS_CREATE_MEDIA_PLAYER = "sonos_create_media_player"
SONOS_FALLBACK_POLL = "sonos_fallback_poll"
SONOS_ALARMS_UPDATED = "sonos_alarms_updated"
SONOS_FAVORITES_UPDATED = "sonos_favorites_updated"
SONOS_MEDIA_UPDATED = "sonos_media_updated"
SONOS_SPEAKER_ACTIVITY = "sonos_speaker_activity"
SONOS_SPEAKER_ADDED = "sonos_speaker_added"
SONOS_STATE_UPDATED = "sonos_state_updated"
SONOS_REBOOTED = "sonos_rebooted"
SONOS_VANISHED = "sonos_vanished"

SOURCE_AIRPLAY = "AirPlay"
SOURCE_LINEIN = "Line-in"
SOURCE_SPOTIFY_CONNECT = "Spotify Connect"
SOURCE_TV = "TV"

MODELS_LINEIN_ONLY = (
    "CONNECT",
    "CONNECT:AMP",
    "PORT",
    "PLAY:5",
)
MODELS_TV_ONLY = (
    "ARC",
    "BEAM",
    "PLAYBAR",
    "PLAYBASE",
)
MODELS_LINEIN_AND_TV = ("AMP",)

AVAILABILITY_CHECK_INTERVAL = datetime.timedelta(minutes=1)
AVAILABILITY_TIMEOUT = AVAILABILITY_CHECK_INTERVAL.total_seconds() * 4.5
BATTERY_SCAN_INTERVAL = datetime.timedelta(minutes=15)
SCAN_INTERVAL = datetime.timedelta(seconds=10)
DISCOVERY_INTERVAL = datetime.timedelta(seconds=60)
SUBSCRIPTION_TIMEOUT = 1200
