
# termaudio v0.2
A lightweight YouTube audio player for the linux terminal.

## Install
### Ubuntu/Debian Install
* Go to the [releases](https://github.com/othema/termaudio/releases/) tab and download latest version.
* Open a terminal and enter `./termaudio`. Termaudio will then open.

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
