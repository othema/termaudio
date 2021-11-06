import sys
from termcolor import colored
from art import text2art
import platform
from youtubesearchpython import VideosSearch
import mpv
import time
import tabulate
import os

search = None  # type: dict
player = None  # type: mpv.MPV


def main(argv):
    global search

    os.system("title termaudio")

    print(colored(text2art("termaudio"), "red"))
    print("creator: Daniel George")
    print("version: v0.3")
    print("date of release: 25 Oct 2021")
    print("platform: " + platform.platform())
    print("\n")

    loop = False
    volume = 100

    # command loop
    while True:
        action = input(colored("termaudio (? for help)", "grey", "on_white") + " ").strip()

        if action == "": continue

        try:
            if action == "exit":
                sys.exit()

            elif action.startswith("/"):
                # search query
                query = action[1:]

                if query == "":
                    error("please specify a search query.\n")
                    continue

                search = search_query(query)[0]
                play_url(search, loop, volume)

            elif action.startswith("s/"):
                # search query and ask which result to choose
                query = action[2:]

                if query == "":
                    error("please specify a search query")
                    continue

                results = search_query(query, limit=10)

                d = []
                for index, r in enumerate(results):
                    title = colored(r["title"], "yellow")
                    d.append([
                        colored(str(index), "red"),
                        title[:75] + "..." if len(title) > 75 else title,
                        colored(r["duration"], "green")
                    ])

                print(tabulate.tabulate(d, tablefmt="plain"), end="\n\n")

                while True:
                    try:
                        user = input(colored("choose search index (blank to quit)", "grey", "on_white") + " ").strip()

                        if user == "":
                            break

                        choice = int(user)
                        if choice < 10:
                            search = results[choice]
                            play_url(search, loop, volume)
                            break
                    except ValueError:
                        pass

            elif action.startswith("?"):
                command = action[1:]

                if command == "":
                    print("?                  show the help menu")
                    print("/[query]           search youtube for query")
                    print("s/[query]          search youtube for query and choose video from results")
                    print("?current           show current video and attributes")
                    print("?stop              stop/pause the current video")
                    print("?resume            resume the paused video")
                    print("?volume            gets the current volume")
                    print("?volume [percent]  sets the volume of the video (max. 500)")
                    print("?seek [h]:[m]:[s]  seeks playback to specified time")
                    print("?loop              cycle loop mode")
                    print("exit               exits the program")

                    print()

                else:
                    if player is not None:
                        if player.core_idle and not player.pause:
                            search = None
                            player.stop()

                    if command.startswith("volume"):
                        split = command.split(" ")
                        no_spaces = [value for value in split if value != " "]

                        if len(no_spaces) == 1:
                            # they are getting the volume, not setting it
                            print(colored("volume", "red") + ": " + str(int(player.volume)) + "\n")
                            continue

                        # no_spaces[0] is 'volume' and no_spaces[1] is volume percentage
                        vol = int(no_spaces[1])
                        if 0 <= vol <= 500:
                            volume = vol
                            try:
                                player.volume = vol
                            except AttributeError:
                                pass
                        else:
                            error("invalid volume.\n")

                        continue
                    elif command == "loop":
                        loop = not loop
                        try:
                            player.loop = loop
                        except AttributeError:
                            pass
                        print(colored("loop mode", "red") + ": " + (
                            colored("on", "green") if loop else colored("off", "yellow")) + ".\n")
                        continue

                    if search is None:
                        error("no audio is being played right now.\n")
                        continue

                    elif command == "stop":
                        player.pause = True

                    elif command == "resume":
                        player.pause = False

                    elif command == "current":
                        print("now playing " + colored(search["title"], "red"))
                        print(f"({search['link']})\n")
                        try:
                            print(colored("duration", "red") + ": " + search["duration"])
                            print(colored("uploaded", "red") + ": " + search["publishedTime"])
                            print(colored("views", "red") + ": " + search["viewCount"]["short"])

                            tp = player.time_pos
                            print(colored("playback time", "red") + ": " + seconds_to_seek(tp))
                        except TypeError:
                            # its a live stream
                            print(colored("type", "red") + ": livestream")

                        print()

                    elif command.startswith("seek"):
                        split = command.split(" ")
                        no_spaces = [value for value in split if value != " "]

                        # no_spaces[0] is 'seek' and no_spaces[1] is h:m:s

                        try:
                            seek = seek_to_seconds(no_spaces[1])
                        except ValueError:
                            error("seek format is " + colored("?seek [h]:[m]:[s]", "green") + ".\n")
                            continue

                        duration = search["duration"]
                        if duration is None:
                            # its a livestream
                            error("cannot seek in a livestream.\n")
                            continue

                        total = seek_to_seconds(duration)

                        if total >= seek >= 0:
                            player.seek(seek - player.time_pos, precision="exact")
                            while player.core_idle:
                                time.sleep(0.1)
                        else:
                            error("seek time exceeds video duration.\n")

                    else:
                        error("unknown command " + colored(command, "yellow") + ".\n")
                        continue

            else:
                error("unknown action " + colored(action, "yellow") + ".\n")
        except Exception as e:
            # for any unhandled exceptions, we dont want the program to quit
            print(colored("error", "red") + ": there was an error.")

            if input("type " + colored("e", "yellow") + " to see the message. ") == "e":
                print()
                error(str(e))

            print()


def search_query(query, limit=1):
    results = VideosSearch(query, limit)
    return results.result()["result"]


def seek_to_seconds(seek: str, separator=":"):
    time_seek = seek.replace(" ", "").split(separator)

    h = int(time_seek[-3]) if len(time_seek) == 3 else 0
    m = int(time_seek[-2]) if len(time_seek) > 1 else 0
    s = int(time_seek[-1])
    seek = s + (m * 60) + (h * 3600)

    return seek


def play_url(yt_search, loop, volume):
    global player

    if player is not None:
        player.stop()
    else:
        player = mpv.MPV(ytdl=True, video=False)

    player.play(yt_search["link"])
    player.pause = False
    player.volume = volume
    player.loop = loop

    while player.core_idle:
        time.sleep(0.1)

    print("playing " + colored(yt_search["title"], "red"))
    print(f"({yt_search['link']})\n")


def seconds_to_seek(seconds: int, separator=":"):
    return time.strftime(f"%H{separator}%M{separator}%S", time.gmtime(seconds))


def error(message):
    print(colored("error", "red") + ": " + message)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit()
