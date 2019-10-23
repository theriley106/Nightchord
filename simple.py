import os
from moviepy.editor import *
import requests
import bs4
import random
import csv
import time

TMP_DIR = "musicFiles"

SOX_COMMAND = "sox -S {0}/{1} {0}/{2} speed 1.35 pitch +200 bass +10 vol 1.0 silence 1 0.1 1% && rm {0}/{1}"

if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

def check_sox():
	os.system("which sox > tmp")
	if len(open("tmp").read()) == 0:
		print("SOX is not installed")
		print("Please install the SOX command line utility to continue")
		raise Exception("SOX NOT INSTALLED")

def check_youtube_dl():
	os.system("which youtube-dl > tmp")
	if len(open("tmp").read()) == 0:
		print("youtube-dl is not installed")
		print("Please install the youtube-dl command line utility to continue")
		raise Exception("YOUTUBE-DL NOT INSTALLED")

def check_dependencies():
	check_sox()
	check_youtube_dl()

check_dependencies()

def LoadHeader():
	UserAgentCSV = open('UserAgent.csv', 'r')
	UserAgentList = csv.reader(UserAgentCSV)
	UserAgentList = [row for row in UserAgentList]
	UserAgentList = [l[0] for l in UserAgentList]
	random.shuffle(UserAgentList)
	return {'User-Agent': random.choice(UserAgentList)}

def ExtractAudio(filename):
	#This receives a .mp4 file but it removes .mp4 because the alternative seemed confusing af
	#filename = str(filename).replace('.mp4', '')
	#os.system('ffmpeg -i {}.mp4 -y {}.mp3'.format(filename, filename))
	video = VideoFileClip(filename.replace(".mp4", "") + ".mp4")
	video.audio.write_audiofile(filename + ".mp3")
	return '{}.mp3'.format(filename)

def DownloadVideo(url, saveas='Vid.mp4'):
	os.system("youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' --output {} {} 2> /dev/null".format(saveas, url))
	return saveas

def genYoutube(string):
	string = string.replace(' ', '+')
	URL = 'https://www.youtube.com/results?search_query={}'.format(string)
	res = requests.get(URL, headers=LoadHeader())
	page = bs4.BeautifulSoup(res.text, "lxml")
	Result = page.select('.item-section > li .clearfix')
	Results = []
	for number in Result:
		if 'Duration' in str(number):
			Results.append(number)
	VideoID = str(Results[0].select('.overflow-menu-choice')[0]).partition('data-video-ids="')[2].partition('" onclick="')[0]
	URL = 'https://www.youtube.com/watch?v={}'.format(VideoID)
	return URL

def findSong(artist, song):
	return genYoutube('{} {} lyrics'.format(artist, song))

def createYoutubeCLI(artist, song):
	listOfInputs = []
	listOfInputs.append({"artist": artist, "song": song})
	for val in listOfInputs:
		#URL = findSong(val['artist'], val['song'])
		# filename = '{}_{}'.format(val['artist'].replace(' ', '_'), val['song'].replace(' ', '_'))
		# val['filename'] = filename
		# DownloadVideo(URL, saveas=filename)
		# a = ExtractAudio('{}.mp4'.format(filename))
		a = "{0}_{1}.mp3".format(artist.replace(" ", "_"), song.replace(" ", "_"))
		wavVersion = a.replace(".mp3", ".wav")
		os.system('youtube-dl --extract-audio --audio-format mp3 -o "{}" "ytsearch:{} {} lyrics"'.format(a, artist, song))
		os.system("ffmpeg -i {} {}".format(a, wavVersion))
		time.sleep(3)
		os.system("cp {} {}/{}".format(wavVersion, TMP_DIR, wavVersion))
	# raw_input(SOX_COMMAND.format(TMP_DIR, a, a.partition('.')[0] + "_final.mp3"))
	os.system(SOX_COMMAND.format(TMP_DIR, wavVersion, a.partition('.')[0] + "_final.mp3"))
	os.system("rm {} && rm {}".format(wavVersion, a))
	return "{}/{}".format(TMP_DIR, a.partition('.')[0] + "_final.mp3")

if __name__ == '__main__':
	print("\n_____ NIGHTCORE GENERATOR ______\n")
	artist = raw_input("Artist: ")
	song = raw_input("Song: ")
	createYoutubeCLI(artist, song)
