#!/usr/bin/env python3
import log
import sys
import subprocess

loglevel = log.INFO

class WallpaperSetter:
    def __init__(self):
        self._logger = log.getChild(self.__class__.__name__)
        self._logger.setLevel(loglevel)

    def set(self, path, args):
        raise NotImplementedError()

class RegisterWallpaperSetter(WallpaperSetter):
    pass

class ShellWallpaperSetter(WallpaperSetter):
    TIMEOUT_SEC = 5
    def _cmd(self, path, args):
        raise NotImplementedError()

    def _cb(self, status, out, err, ex):
        self._logger.debug('cmd exit code: %s, OUT:\n%s\nERR:\n%s',
                    str(status), repr(out), repr(err))
        if ex:
            self._logger.exception(ex)
        return status == 0 and not ex

    def set(self, path, args):
        p = None
        cmd = self._cmd(path, args)
        try:
            self._logger.debug('about to execute %s', cmd)
            p = subprocess.Popen(cmd,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate(timeout = self.TIMEOUT_SEC)
        except Exception as ex:
            if p:
                p.kill()
                return self._cb(p.poll(), p.stdout.read(), p.stderr.read(), ex)
            else:
                return self._cb(None, None, None, ex)
        else:
            return self._cb(p.poll(), out, err, None)

class Gnome2Setter(ShellWallpaperSetter):
    def _cmd(self, path, args):
        return ["gconftool-2", "--type=string",
                "--set", "/desktop/gnome/background/picture_filename",
                '"{}"'.format(path)]

class Gnome3Setter(ShellWallpaperSetter):
    def _cmd(self, path, args):
        return ["gsettings", "set",
                "org.gnome.desktop.background", "picture-uri",
                '"file://{}"'.format(path)]

class WallpaperSetterFactory:
    def __init__(self, name):
        self.registered = dict()
        self.name = name

    def register(self, name, c):
        if name in self.registered \
            and c is not self.registered[name]:
            raise NameError(
                    '{} has been registered by {}'.format(name, self.registered[name]))
        self.registered[name] = c

    def get(self, name):
        if name not in self.registered:
            raise NameError(
                    'unregistered setter {}'.format(name))
        return self.registered[name]

_default_wallpaper_factory = WallpaperSetterFactory('default')

register = _default_wallpaper_factory.register
get = _default_wallpaper_factory.get

if sys.platform == 'linux':
    register('gnome2', Gnome2Setter)
    register('gnome3', Gnome3Setter)
if sys.platform == 'win32':
    pass
