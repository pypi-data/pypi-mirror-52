# -*- coding: utf-8 -*-
import asyncio, platform
from . import config
class SyncAsync(object):
	def __init__(self, _coroutine):
		self.loop = asyncio.get_event_loop().run_until_complete
		self._coroutine = _coroutine
		
	def run(self):
		return self.loop(self._coroutine)

class ApplicationHeader(object):
	MAP = {
		'ios': {
			'UA': "Line/9.15.1", # "Line/7.14.0"
			'LA': "IOSIPAD\t9.15.1\t{}\t7.0.0".format(config.LOGIN_DEVICE_NAME),
		},
		'ios2': {
			'UA': "Line/8.2.0",
			'LA': "IOS\t8.2.0\t{}\t8.2.0".format(config.LOGIN_DEVICE_NAME),
		},
		'desktop': {
			'UA': "DESKTOP:MAC:10.9.4-MAVERICKS-x64(5.1.2)", #"DESKTOP:MAC:10.10.2-YOSEMITE-x64(4.5.0)",
			'LA': "DESKTOPMAC\t10.9.4-MAVERICKS-x64\tMAC\t5.1.2", #"DESKTOPWIN\t10.9.4-MAVERICKS-x64\tMAC\t5.1.2" #"DESKTOPMAC 10.10.2-YOSEMITE-x64    MAC 4.5.0",
		},
		'chrome': {
			'UA': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
			'LA': "CHROMEOS\t1.4.11\tChrome_OS\t1",
		},
		'android': {
			'UA': "Line/9.15.1",
			'LA': "ANDROID\t9.15.1\tAndroid\tOS\t7.0",
		},
		'androidlite': {
			'UA':"androidapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)" ,
			'LA': "ANDROIDLITE\t8.2.4\tAndroid\tOS\t6.0",
		},
		'tizen': {
			'UA': "Mozilla/5.0 (Linux; Tizen 2.3; SAMSUNG SM-Z130H) AppleWebKit/537.3 (KHTML, like Gecko) Version/2.3 Mobile Safari/537.3",
			'LA': "TIZEN\t8.2.4\tLine\t6.8.2",
		},
		# LINE@
		'biz': {
			'UA': "androidapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
			'LA': 'BIZANDROID\t1.7.2\tAndroid OS\t7.1.2',
		},
		'bizweb': {
			'UA': "Mozilla/5.0 (Linux; Tizen 2.3; SAMSUNG SM-Z130H) AppleWebKit/537.3 (KHTML, like Gecko) Version/2.3 Mobile Safari/537.3",
			'LA': 'BIZWEB\t1.0.22\tWEB\t1',
		},
		'bizbot': {
			'UA': "androidapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
			'LA': 'BIZBOT\t1.7.2\tAndroid OS\t7.1.2',
		},
		'bizios': {
			'UA': "androidapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
			'LA': "BIZIOS\t1.7.2\tAndroid OS\t7.1.2",
		},
		'bot': {
			'UA': "androidapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
			'LA': 'BOT\t1.7.2\tLinux Kernel\t3.14.7',
		},
		'internal': {
			'UA': "androidapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
			'LA': 'INTERNAL\t1.7.2\tINTERNAL\t3.14.7',
		},
		'square': {
			'UA': "androidapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
			'LA': 'SQUARE\t1.7.2\tINTERNAL\t3.14.7',
		},
		'web': { # Weird
			'UA': "Line/2017.0731.2132 CFNetwork/758.6 Darwin/15.0.0",
			'LA': 'WEB\t8.2.4\tiPhone\tOS\t1',
		},
		'web2': {
			'UA': "Line/2017.0731.2132 CFNetwork/758.6 Darwin/15.0.0",
			'LA': 'WEB\t8.2.4\tFirefox_OS\t1',
		},
		'android2': {
			'UA': "Line/7.7.0",
			'LA': 'ANDROID\t8.2.4\tAndroid\tOS\t4.4.4',
		},

		's40': {
			'UA': "Line/8.2.4",
			'LA': 'S40\t8.2.4\tAndroid\tOS\t4.4.4',
		},
		'virtual': {
			'UA': 'Virtual.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)',
			'LA': 'VIRTUAL\t8.2.4\tLINE_VIRTUAL\t7.5.0',
		},
		'chrono': {
			'UA': 'Chronoapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)',
			'LA': 'CHRONO\t8.2.4\tiPhone\tOS\t1',
		},
		'wap': {
			'UA': 'WAPapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)',
			'LA': 'WAP\t8.2.4\tiPhone\tOS\t1',
		},

		'win10': {
			'UA': 'DESKTOP:WIN10:10.9.4-MAVERICKS-x64(1.0.1)',
			'LA': 'WIN10\t8.2.4\tPhone\tOS\t1',
		},
		'winphone': {
			'UA': 'WINPHONEapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)',
			'LA': 'WINPHONE\t8.2.4\tiPhone\tOS\t1',
		},
		'winphone_rc': {
			'UA': 'WINPHONEapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)',
			'LA': 'WINPHONE_RC\t8.2.4\tiPhone\tOS\t1',
		},
		'win10_rc': {
			'UA': 'DESKTOP:WIN10:10.9.4-MAVERICKS-x64(1.0.1)',
			'LA': 'WIN10_RC\t8.2.4\tiPhone\tOS\t1',
		},
		'clova': {
			'UA': 'X:CLOVAFRIENDS:10.9.4-MAVERICKS-x64(1.0.1)',
			'LA': 'CLOVAFRIENDS\t8.2.4\tiPhone\tOS\t1',
		},
		'channelcp': {
			'UA': 'X:CHANNELCP:10.9.4-MAVERICKS-x64(1.0.1)',
			'LA': 'CHANNELCP\t8.2.4\tiPhone\tOS\t1',
		},
		'channelgw': {
			'UA': 'X:CHANNELGW:10.9.4-MAVERICKS-x64(1.0.1)',
			'LA': 'CHANNELGW\t8.2.4\tiPhone\tOS\t1',
		},
	}
	def __init__(self, client_name, line_app='', useragent="Line/8.2.4 iPad4,1 10.0.2"):
		
		if client_name == 'custom':
			self.LA = line_app
			self.UA = useragent
		else:
			sets = self.MAP.get(client_name, None)
			if not sets:
				raise Exception('Client not in the list [ %s ] ' % (', '.join(list(self.MAP.keys()) )) )
			else:
				self.LA, self.UA = sets['LA'], sets['UA']
				
	def get(self):
		return self.LA, self.UA
