# PyNgWallpaper

### What pyngwallpaper does

Download the wallpaper offered by National Geographic photography website and set it current wallpaper background.

Another bash script for the same purpose can be found [here]()

----------

### How does it work

1.  Read and parse National Geographic photography *photo-of-today* [website](http://photography.nationalgeographic.com/photography/photo-of-the-day/)

1.  If there is a wallpaper download link:
    * if it's same as last downloaded photo, exit
    * download it to **specified** folder and overwrite last downloaded photo
    * record the downloading URL in a text file, which locates in current user's personal folder
    * use it as wallpaper unless in **download-only** mode
    * exit

1. If there isn't a wallpaper link, which means the photo may have  resolution improper to be wallpaper:
    * if the **force** switch is on, do same as step 2
    * reduce **persistence** counter by 1; if it's 0, exit
    * go to the previous *Photo of The Day*, then do things again

----------

### Usage

    Usage: pyngwallper [OPTIONS]
    Download the wallpaper offered by National Geographic photography website and set it current wallpaper background.

    -f, --force                 adopt this photo even if its size may
                                be strange to be wallpaper. Disabled by 
                                default
    --persistence=N             go back for at most N-1 pages if photo of
                                today isn't for wallpaper. Backward 
                                browsing will be interrupted before N-1
                                pages tried if either a downloaded page
                                found or a wallpaper link read
    -s, --setter={no|gnome2|gnome3|win|...}
                                specify interface to be called to set 
                                the downloaded photo wallpaper. 'no' 
                                indicates downloading only; 'gnome2/3'
                                are only for Linux with gnome; 'win' is
                                for Windows only. Customized setter can 
                                be added as dev doc described
    --setter-args=comma-sep-args
                                additional arguments for wallpaper setter.
                                Varies with wallpaper setter. Read dev doc
                                for more
    -t, --output-folder         specify the folder to store photos.
                                Use '~/Pictures' folder in Linux or 
                                'My Pictures' in Windows by default
    

----------

### Devolopment

#### Customized wallpaper setter
(TBD)

----------