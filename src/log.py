#!/usr/bin/env python3
import logging
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG

_logger = None
def __init(projname):
    global _logger
    _logger = logging.getLogger(projname)
    if not _logger.handlers:
        _loggerHandler = logging.StreamHandler()
        _loggerHandler.setLevel(logging.DEBUG)
        _loggerHandler.setFormatter(logging.Formatter('[%(asctime)s - %(levelname)s - %(module)s] %(message)s'))
        _logger.addHandler(_loggerHandler)
        _logger.setLevel(logging.INFO)

def getChild(*args, **kwargs):
    return _logger.getChild(*args, **kwargs)

__init('ngwallpaper')

if __name__ == '__main__':
    log = _logger.getChild('logtest')
    log.setLevel(logging.DEBUG)
    log.info('Info test')
    log.warn('Warn test')
    log.error('Error test')
    log.critical('Critical test')
    log.debug('debug test')
    try:
        def __ex_test():
            raise Exception('exception test')
        __ex_test()
    except Exception as ex:
        log.exception(ex)
