import threading
import os
import bs4
import requests

def loadSongs():
	songFile = raw_input("Song File: ")
	return open(songFile).read().split("\n")

def DownloadVideo(url, saveas='Vid.mp4'):
	os.system("youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' --output {} {} 2> /dev/null".format(saveas, url))
	return saveas

def ExtractAudio(filename):
	#This receives a .mp4 file but it removes .mp4 because the alternative seemed confusing af
	filename = str(filename).replace('.mp4', '')
	os.system('ffmpeg -i {}.mp4 -y {}.mp3'.format(filename, filename))
	return '{}.mp3'.format(filename)
	#I don't know why this returns anything.  ideally it should just be a boolean depending on if it worked or not


def createYoutube(URL=None, Speed=None, SaveAs=None):
	if URL == None:
		artist = raw_input('Artist: ')
		song = raw_input('Song: ')
		URL = findSong(artist, song)
	filename = '{}_{}'.format(artist.replace(' ', '_'), song.replace(' ', '_'))
	DownloadVideo(URL, saveas=filename)
	ExtractAudio('{}.mp4'.format(filename))
	applyChain('{}.mp3'.format(filename))
	CombineAudioandImage('{}.mp3'.format(filename))



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

def multiThreadedDownload():

