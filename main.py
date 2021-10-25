import sys
from termcolor import colored
from art import text2art
import platform
from youtubesearchpython import VideosSearch
import mpv
import time

global search


def main(argv):
	global search

	print(colored(text2art("termaudio"), "red"))
	print("creator: Daniel George")
	print("version: v0.2")
	print("date of release: null")
	print("platform: " + platform.platform())
	print("\n")

	player = None
	search = None

	# command loop
	while True:
		action = input(colored("termaudio (? for help)", "grey", "on_white") + " ")

		try:
			if action.startswith("/"):
				# search query
				query = action[1:]
	
				if query == "":
					error("please specify a search query.\n")
					continue
	
				search = search_query(query)
				url = search["link"]
				title = search["title"]
				
				if player is not None:
					player.stop()
				else:
					player = mpv.MPV(ytdl=True, video=False)
				player.play(url)
				
				while player.core_idle:
					time.sleep(0.1)
				
				print("playing " + colored(title, "red"))
				print(f"({url})\n")
			
			elif action.startswith("?"):
				command = action[1:]
				
				if command == "":
					print("?                  show the help menu")
					print("/[query]           search youtube for query")
					print("?current           show current video and attributes")
					print("?stop              stop/pause the current video")
					print("?resume            resume the paused video")
					print("?volume            gets the current volume")
					print("?volume [percent]  sets the volume of the video (max. 200)")
					print("?seek [h]:[m]:[s]  seeks playback to specified time\n")
	
				else:
					if player is not None:
						if player.core_idle:
							search = None
							player.stop()
	
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
	
					elif command.startswith("volume"):
						split = command.split(" ")
						no_spaces = [value for value in split if value != " "]
	
						if len(no_spaces) == 1:
							# they are getting the volume, not setting it
							print(colored("volume", "red") + ": " + str(int(player.volume)) + "\n")
							continue
	
						# no_spaces[0] is 'volume' and no_spaces[1] is volume percentage
						volume = int(no_spaces[1])
						if volume >= 0 and volume <= 200:
							player.volume = volume
						else:
							error("invalid volume.\n")
	
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
						
						if seek <= total and seek >= 0:
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
		except:
			# for any unhandled exceptions, we dont want the program to quit
			print(colored("error", "red") + ": there was an error.\n")
	
	
def	search_query(query):
	search = VideosSearch(query, limit=1)
	return search.result()["result"][0]


def seek_to_seconds(seek: str, separator=":"):
	time_seek = seek.replace(" ", "").split(":")
	
	h = int(time_seek[-3]) if len(time_seek) == 3 else 0
	m = int(time_seek[-2]) if len(time_seek) > 1 else 0
	s = int(time_seek[-1])
	seek = s + (m * 60) + (h * 3600)

	return seek


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
