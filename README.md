
# termaudio
A lightweight YouTube audio player for your terminal.

## Install
### Debian Install
* `sudo apt install termaudio` to install
* `termaudio` to run

## Runtime Dependencies
* `mpv` for streaming through `youtube-dl`

## Python Packages
* `termcolor` for printing colored text to the terminal 
* `art` for printing ASCII art to the terminal
* `youtube-search-python` for searching YouTube's api

## Usage
* `?` show the help menu
* `/[query]` search YouTube for a query
* `?current` show current video and attributes
* `?stop` stop/pause the current video
* `?resume` resume the paused video
* `?volume` displays the current volume
* `?volume [percent]` sets the volume of the video (max. 200)
* `seek [h]:[m]:[s] seeks playback to specified time`
