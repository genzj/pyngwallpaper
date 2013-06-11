#!/usr/bin/env python3
import argparse
from sys import argv, exit as sysexit, platform
import os
from os.path import expanduser, join as pathjoin, isdir, splitext, basename
import log
import webutil
import ngphoto
import record

NAME = 'pyngwallpaper'
REV  = '1.0.0'
LINK = 'https://github.com/genzj/pyngwallpaper'
HISTORY_FILE = pathjoin(expanduser('~'), 'ng-wallpaper-history.json')

_logger = log.getChild('main')

def load_setters():
    if platform == 'win32':
        return ['no', 'win']
    else:
        return ['no', 'gnome3', 'gnome2']

def parseargs(args):
    setters = load_setters()
    parser = argparse.ArgumentParser(prog=NAME,
            description='Download the wallpaper offered by National Geographic'
            +'photography website and set it current wallpaper background.')
    parser.add_argument('-v', '--version', action='version',
            version='%(prog)s-{} ({})'.format(REV, LINK),
            help='show version information')
    parser.add_argument('-d', '--debug', default=0,
            action='count',
            help='''enable debug outputs. 
            The more --debug the more detailed the log will be''')
    parser.add_argument('-f', '--force', default=False,
            action='store_true',
            help='''adopt this photo even if its size may
                    be strange to be wallpaper. Disabled by
                    default''')
    parser.add_argument('-k', '--keep-file-name', default=False,
            action='store_true',
            help='''keep the original filename. By default
            downloaded file will be renamed as 'wallpaper.jpg'.
            Keep file name will retain all downloaded photos
            ''')
    parser.add_argument('--persistence', type=int, default='7',
            help='''go back for at most N-1 pages if photo of today isn\'t for
            wallpaper. Backward browsing will be interrupted before N-1 pages
            tried if either a downloaded page found or a wallpaper link read''')
    parser.add_argument('-s', '--setter', choices=setters,
            default=setters[1],
            help='''specify interface to be called for
                    setting wallpaper. 'no'
                    indicates downloading-only; 'gnome2/3'
                    are only for Linux with gnome; 'win' is
                    for Windows only. Customized setter can
                    be added as dev doc described. Default: {}
            '''.format(setters[1]))
    parser.add_argument('--setter-args', default=[], action='append',
            help='''go back for at most N-1 pages if photo of today isn\'t for
            ''')
    parser.add_argument('-t', '--output-folder', default=pathjoin(expanduser('~'), 'MyNgWallpapers'),
            help='''specify the folder to store photos.
                    Use '~/MyNgWallpapers' folder in Linux or
                    'My Documents/MyNgWallpapers' in Windows by default
                ''')
    parser.add_argument('URL', nargs='*',
            default=['http://photography.nationalgeographic.com/photography/photo-of-the-day/',],
            help='''starts with this URL instead of today's photo if specified
            ''')
    config = parser.parse_args(args)
    config.setter_args = ','.join(config.setter_args).split(',')
    return config

def prepare_output_dir(d):
    os.makedirs(d, exist_ok=True)
    if isdir(d):
        return True
    else:
        _logger.critical('can not create output folder %s', d)

def download_wallpaper(config):
    p = config.persistence
    s = ngphoto.NgPhotoPage(config.URL[0])
    while True:
        _logger.debug(repr(s))
        s.load()
        _logger.debug(str(s))
        if not s.loaded():
            _logger.fatal('can not load url %s. aborting...', s.url)
            sysexit(1)
        if not s.isphoto():
            _logger.fatal('%s is not a valid NG photo page.', s.url)
            sysexit(1)
        wplink = s.wallpaper_link()
        if not wplink and config.force:
            _logger.info('in force mode')
            wplink = s.img_link()

        if wplink:
            outfile = get_output_filename(config, wplink)
            rec = record.default_manager.get(wplink, None)

            if rec and outfile == rec['local_file']:
                _logger.info('file has been downloaded before, exit')
                sysexit(0)
                return None

            with open(outfile, 'wb') as of:
                _logger.info('download photo of "%s"', s.title())
                of.write(webutil.loadurl(wplink))
            _logger.info('file saved %s', outfile)
            r = record.DownloadRecord(wplink, outfile)
            return r
        p -= 1
        if p <= 0:
            _logger.info('bad luck, no wallpaper today:(')
            break
        _logger.debug('no wallpaper, try previous')
        s.update(s.prev_link())
    return None

def get_output_filename(config, link):
    filename = basename(link)
    if not config.keep_file_name:
        filename = 'wallpaper{}'.format(splitext(filename)[1])
    return pathjoin(config.output_folder, filename)

def load_history():
    try:
        f = open(HISTORY_FILE, 'r')
    except Exception:
        _logger.warning('error occurs when recover downloading history', exc_info=1)
    else:
        record.default_manager.load(f)
        f.close()

def save_history(r, keepold=False):
    if not keepold:
        record.default_manager.clear()
    record.default_manager.add(r)
    try:
        f = open(HISTORY_FILE, 'w')
        f.truncate(0)
    except Exception:
        _logger.warning('error occurs when recover downloading history', exc_info=1)
    else:
        record.default_manager.save(f)
        f.close()

def set_debug_details(level):
    if not level:
        l = log.INFO
    elif level == 1:
        l = log.DEBUG
    elif level >= 2:
        l = log.PAGEDUMP
    _logger.setLevel(l)
    webutil._logger.setLevel(l)
    log._logger.setLevel(l)
    ngphoto._logger.setLevel(l)


if __name__ == '__main__':
    config = parseargs(argv[1:])
    set_debug_details(config.debug)
    _logger.debug(config)

    prepare_output_dir(config.output_folder)

    load_history()
    filerecord = download_wallpaper(config)

    save_history(filerecord)
    if not filerecord or config.setter == 'no':
        _logger.info('nothing to set')
    else:
        pass #set wallpaper
    sysexit(0)
