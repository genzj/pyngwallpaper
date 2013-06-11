# PyNgWallpaper

### What pyngwallpaper does

Download the wallpaper offered by National Geographic photography website and set it current wallpaper background.

Another bash script for the same purpose can be found [here](https://github.com/genzj/ubuntu-ng-wallpaper)

----------

### Auto startup

#### Linux with Gnome
You just need to add a startup application:

    gnome-session-properties

then *add* a startup program with:

    Name: pyngwallpaper
    Command: /path/to/pyngwallpaper/src/main.py
    Comment: download and update wallpaper!

You can also append arguments in *Command* box.

#### Windows
TBD

----------

### How it works

1.  Read and parse National Geographic photography *Photo of Today* [website](http://photography.nationalgeographic.com/photography/photo-of-the-day/)

1.  If there is a wallpaper download link:
    * if both its URL and target file name are same as last downloaded photo's, exit without error
    * download it to **specified** folder
    * record the downloading URL, location of saved photo and downloading time in a text file, which locates in current user's personal folder
    * use it as wallpaper unless in **download-only** mode
    * exit

1. If there isn't a wallpaper link, which means the photo may have  resolution improper to be wallpaper:
    * if the **force** switch is on, do same as step 2
    * reduce **persistence** counter by 1; if it's 0, exit
    * go to the previous *Photo of The Day*, then do things again

----------

### Usage

    usage: pyngwallpaper [-h] [-v] [-d] [-f] [--redownload] [-k]
                         [--persistence PERSISTENCE] [-s {no,gnome3,gnome2}]
                         [--setter-args SETTER_ARGS] [-t OUTPUT_FOLDER]
                         [URL [URL ...]]

    Download the wallpaper offered by National Geographicphotography website and
    set it current wallpaper background.

    positional arguments:
      URL                   starts with this URL instead of today's photo if
                            specified

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show version information
      -d, --debug           enable debug outputs. The more --debug the more
                            detailed the log will be
      -f, --force           adopt this photo even if its size may be strange to be
                            wallpaper. Disabled by default
      --redownload          do not consider history records. Download must be
                            done. But this download will be recorded in history
                            file.
      -k, --keep-file-name  keep the original filename. By default downloaded file
                            will be renamed as 'wallpaper.jpg'. Keep file name
                            will retain all downloaded photos
      --persistence PERSISTENCE
                            go back for at most N-1 pages if photo of today isn't
                            for wallpaper. Backward browsing will be interrupted
                            before N-1 pages tried if either a downloaded page
                            found or a wallpaper link read
      -s {no,gnome3,gnome2,win}, --setter {no,gnome3,gnome2,win}
                            specify interface to be called for setting wallpaper.
                            'no' indicates downloading-only; 'gnome2/3' are only
                            for Linux with gnome; 'win' is for Windows only.
                            Customized setter can be added as dev doc described.
                            Default: gnome3
      --setter-args SETTER_ARGS
                            go back for at most N-1 pages if photo of today isn't
                            for
      -t OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                            specify the folder to store photos. Use
                            '~/MyNgWallpapers' folder in Linux or 'My
                            Documents/MyNgWallpapers' in Windows by default

----------

### Devolopment

#### Customized wallpaper setter
(TBD)

----------
