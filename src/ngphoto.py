#!/usr/bin/env python3
import re
import log
import webutil
from urllib.parse import urljoin

_logger = log.getChild('ngphoto')

def _property_need_loading(f):
    def wrapper(*args, **kwargs):
        args[0]._assert_load(f.__name__)
        return f(*args, **kwargs)
    return wrapper

class NgPhotoPage:
    def __init__(self, url):
        self.update(url)

    def update(self, url):
        if hasattr(self, 'url') and self.url == url:
            return
        self.reset()
        self.url = url

    def reset(self):
        self.__loaded = False
        self.__isphoto = False
        self.content = ''
        self.__title = ''
        self.__img_link = None
        self.__wallpaper_link = None
        self.__prev_link = None

    def _parse(self):
        image_offset = self.content.find('class="primary_photo"')

        if image_offset > 0:
            self.__isphoto = True
        else:
            return

        prev_pat = re.compile(r'<a[^>]+href="([^"]+)"[^>]*title="[^"]+previous[^"]+"[^>]*>')
        img_pat = re.compile(r'<img[^>]+src="([^"]+)"[^>]*alt="([^"]+)"')

        prevs = prev_pat.findall(s.content[image_offset:])
        imgs = img_pat.findall(s.content[image_offset:])

        if not prevs or not imgs:
            _logger.warn('no prev or no imgs: %s, %s', prevs, imgs)

        self.__img_link, self.__title = imgs[0]
        self.__prev_link = urljoin(self.url, prevs[0])

        wp_pat = re.compile(r'<div[^>]+class="download_link"[^>]*>\s*<a[^>]+href="([^"]+)"[^>]*>\w*\s*Wallpaper')
        wpl = wp_pat.findall(self.content)
        if not wpl:
            _logger.info('wallpaper link not found')
            self.__wallpaper_link = None
        else:
            self.__wallpaper_link = wpl[0]
            if len(wpl) > 1:
                _logger.warn('more than one wallpaper link found: %s', wpl)

        return True

    def load(self):
        self.reset()
        _logger.info('loading from %s', self.url)
        self.content = webutil.loadpage(self.url)
        if self.content:
            _logger.info('%d bytes loaded', len(self.content))
            self.__loaded = True
            self._parse()
        else:
            _logger.error('can\'t download photo page')

    def loaded(self):
        return self.__loaded

    @_property_need_loading
    def isphoto(self):
        return self.__isphoto

    @_property_need_loading
    def img_link(self):
        return self.__img_link

    @_property_need_loading
    def wallpaper_link(self):
        return self.__wallpaper_link

    @_property_need_loading
    def prev_link(self):
        return self.__prev_link

    @_property_need_loading
    def title(self):
        return self.__title

    def _assert_load(self, propname):
        if not self.loaded():
            raise Exception('use property "{}" before loading'.format(propname))

    def __str__(self):
        s_basic = '<url="{}", loaded={}'.format(self.url, self.loaded())
        if not self.loaded():
            return s_basic + '>'
        s_loaded = s_basic + ', isphoto={}'.format(self.isphoto())
        if not self.isphoto():
            return s_loaded + '>'
        s_all   = s_loaded + ', img_link="{}", wallpaper_link="{}", prev_link="{}", title="{}">'.format(
                self.img_link(), self.wallpaper_link(), self.prev_link(), self.title())
        return s_all

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self.url))

from sys import argv
if __name__ == '__main__':
    _logger.setLevel = log.DEBUG
    s = NgPhotoPage(argv[1])
    _logger.info(repr(s))
    _logger.info(str(s))
    s.load()
    _logger.info(str(s))
