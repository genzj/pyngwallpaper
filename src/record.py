#!/usr/bin/env python3
import log
import json
import time
from os.path import isfile
from collections import UserDict

_logger = log.getChild('record')
#_logger.setLevel(log.DEBUG)

class DownloadRecord(dict):
    def __init__(self, url, local_file, download_time=None):
        UserDict.__init__(self)
        if download_time is None:
            download_time = time.localtime()
        timestr = time.strftime('%Y-%m-%dT%H:%M:%S%z', download_time)

        self['url'] = url
        self['local_file'] = local_file
        self['time'] = timestr[:-2]+':'+timestr[-2:]

class DownloadRecordManager(dict):
    def __init__(self, name):
        dict.__init__(self)
        self.name = name
        self.clear()

    def save(self, f):
        json.dump(self, f)

    def load(self, f):
        self.clear()
        content = json.load(f)
        _logger.debug('json file loaded:\n%s', str(content))
        for r in content.values():
            try:
                exists = isfile(r['local_file'])
            except:
                _logger.debug('error occurs when detecting saved file', exc_info=1)
                exists = False
            if exists:
                self.add(r)
            else:
                _logger.debug('%s doesn\'t exist any more', r)
        _logger.debug('history %s loaded', self)
    
    def add(self, r):
        self[r['url']] = r

default_manager = DownloadRecordManager('default')
