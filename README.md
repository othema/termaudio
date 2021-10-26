
# termaudio
A lightweight YouTube audio player for the linux terminal.

## Install
### Ubuntu/Debian Install
#### Portable Install
* Go to the [releases](https://github.com/othema/termaudio/releases/latest) tab and download the binary file.
* Open a terminal and enter `./termaudio`. Termaudio will then open.
#### Installer (Recommended)
 * Open a terminal and enter enter these commands:
 ```bash
 wget https://github.com/othema/termaudio/releases/latest/download/termaudio.deb
 sudo dpkg -i termaudio.deb
 ```

## Runtime Dependencies
* `mpv` for streaming through `youtube-dl`

## Python Packages
* `termcolor` for printing colored text to the terminal 
* `art` for printing ASCII art to the terminal
* `youtube-search-python` for searching YouTube's api
* `python-mpv` for interacting with `libmpv`

## Usage
* `?` show the help menu
* `/[query]` search YouTube for a query
* `?current` show current video and attributes
* `?stop` stop/pause the current video
* `?resume` resume the paused video
* `?volume` displays the current volume
* `?volume [percent]` sets the volume of the video (max. 200)
* `seek [h]:[m]:[s]` seeks playback to specified time
