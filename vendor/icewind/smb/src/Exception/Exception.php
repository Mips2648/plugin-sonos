<?php
/**
 * Copyright (c) 2014 Robin Appelman <icewind@owncloud.com>
 * This file is licensed under the Licensed under the MIT license:
 * http://opensource.org/licenses/MIT
 */

namespace Icewind\SMB\Exception;

class Exception extends \Exception {
	static public function unknown($path, $error) {
		$message = 'Unknown error (' . $error . ')';
		if ($path) {
			$message .= ' for ' . $path;
		}

		return new Exception($message, $error);
	}
}
