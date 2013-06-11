from cx_Freeze import setup, Executable
import sys
sys.path.append('src')
from main import REV

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = {'packages': ['urllib', 'PIL'],
                'includes': ['win32.win32gui', 'log', 'record', 
                              'webutil', 'setter', 'ngphoto'],
                 'excludes': ['tkinter'],
                 'compressed':1,
                 'include_files': [('src/winsetter.py','')],
                 'bin_includes': ['pywintypes33.dll']
               }

executables = [
    Executable('./src/main.py', base='Win32GUI', targetName='NgWallpaper.exe'),
    Executable('./src/main.py', base='Console', targetName='NgWallpaper-cli.exe')
]

setup(name='PyNgWallpaper.exe',
      version = REV,
      description = 'National Geography Wallpaper Downloader',
      options = {'build_exe': buildOptions},
      executables = executables)
