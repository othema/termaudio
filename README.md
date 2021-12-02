
# termaudio
A lightweight YouTube audio player for the linux terminal.

## Install
### Ubuntu/Debian Install
#### Installer (Recommended)
 * Open a terminal and enter enter these commands:
 ```bash
 wget https://github.com/othema/termaudio/releases/latest/download/termaudio.deb
 sudo dpkg -i termaudio.deb
 sudo apt install libmpv1
 ```
#### Portable Install
* Go to the [releases](https://github.com/othema/termaudio/releases/latest) tab and download the binary file (called `termaudio`).
* Open a terminal and enter `./termaudio`. Termaudio will then open.
* **Note: you will need to install the dependencies manually (see 'Runtime Dependencies')**

## Runtime Dependencies
* `mpv` for streaming through `youtube-dl`
* `libmpv1` to help with `mpv`

## Python Packages
* `termcolor` for printing colored text to the terminal 
* `art` for printing ASCII art to the terminal
* `youtube-search-python` for searching YouTube's api
* `python-mpv` for interacting with `libmpv`

## Usage
* `?` show the help menu
* `/[query]` search YouTube for a query
* `/[query]` search YouTube for a query and choose a video from the results
* `?current` show current video and attributes
* `?stop` stop/pause the current video
* `?resume` resume the paused video
* `?volume` displays the current volume
* `?volume [percent]` sets the volume of the video (max. 200)
* `seek [h]:[m]:[s]` seeks playback to specified time
