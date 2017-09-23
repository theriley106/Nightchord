#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tesserocr import PyTessBaseAPI, RIL
import pyautogui
import json
import os
import bs4
import subprocess
import pytesseract
import base64
from moviepy.editor import VideoFileClip
import billboard
import time
import random
import difflib
import csv
import re
from PyLyrics import *
import Image, ImageChops, ImageDraw, ImageFont, ImageFilter
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import glob
import threading
import sys
import itertools
reload(sys)
sys.setdefaultencoding('utf8')
###THIS IS ONLY FOR PRINTING STUFF
lock = threading.Lock()
APIKEY = open('apiKey.txt','r').read()
def GenerateBackground():
	return random.choice(glob.glob("src/backgrounds/*.jpg"))

def stripExtension(filename):
	return filename[:filename.rfind('.')]

def stripPath(filename):
	return filename[filename.rfind('/') + 1:]

def findPath(filename):
	return filename[:filename.rfind('/') + 1]

def convertBase(image):
	return base64.b64encode(open(image, "rb").read())

def GetDuration(clip):
	if '.mp4' in str(clip):
		return VideoFileClip(clip).duration
	elif '.mp3' in str(clip):
		return eyed3.load('{}'.format(clip)).info.time_secs

def csvToList(filename):
	file = [row for row in csv.reader(open(filename, 'r'))]
	a = [l[0] for l in file]
	return a

def shuffleList(listname):
	return random.shuffle(listname)

def genReqJson(image):
	a = open("Request.json", "r").read()
	a = a.replace('BASE', convertBase(image))
	return str(json.dumps(a))
	

def genCurl(basefile):
	a = 'curl -v -s -H "Content-Type: application/json" https://vision.googleapis.com/v1/images:annotate?key={} --data-binary @{}'.format(APIKEY, basefile)
	return a

def ocrImage(image):
	inpu = open('Request.json', 'r')
	out = open('Request.tmp', 'w')
	out.write(inpu.read().replace('BASE', convertBase(image)))
	out.close()
	a = genCurl("Request.tmp")
	os.system("{} > tmp.json".format(a))
	with open('tmp.json') as json_data:
	    d = json.load(json_data)
	    return d

def LoadHeader():
	UserAgentCSV = open('UserAgent.csv', 'r')
	UserAgentList = csv.reader(UserAgentCSV)
	UserAgentList = [row for row in UserAgentList]
	UserAgentList = [l[0] for l in UserAgentList]
	random.shuffle(UserAgentList)
	return {'User-Agent': random.choice(UserAgentList)} 

def genYoutubeURL(string):
	string = string.replace(' ', '+')
	return 'https://www.youtube.com/results?search_query={}'.format(string)

def grabYoutubeID(result):
	return str(result.select('.overflow-menu-choice')[0]).partition('data-video-ids="')[2].partition('" onclick="')[0]

def generateOCR(jsondict):
	with open('{}Transcript.json'.format(Words[1]), 'w') as f:
		json.dump(Information, f)

def findSong(artist, song):
	return genYoutube('{} {} lyrics'.format(artist, song))

def genYoutube(string):
	URL = genYoutubeURL(string)
	res = requests.get(URL, headers=LoadHeader())
	page = bs4.BeautifulSoup(res.text, "lxml")
	Result = page.select('.item-section > li .clearfix')
	Results = []
	for number in Result:
		if 'Duration' in str(number):
			Results.append(number)
	VideoID = grabYoutubeID(Results[0])
	URL = 'https://www.youtube.com/watch?v={}'.format(VideoID)
	return URL

def ocrList(image):
	response = pytesseract.image_to_string(Image.open(image)).encode('utf-8','replace')
	if len(response) > 5:
		response = response.replace('\n', ' ').replace('  ', ' ').split(' ')
	return response

def ExtractAudio(filename):
	filename = stripExtension(filename)
	os.system('ffmpeg -i {}.mp4 -y {}.mp3'.format(filename, filename))
	return '{}.mp3'.format(filename)

def ReturnAll(folder, extension='mp3'):
	return glob.glob("{}/*.{}".format(folder, extension))

def CombineAudioandImage(audio, image=GenerateBackground(), output=None):
	if output == None:
		output = stripExtension(str(audio))
	os.system("ffmpeg -loop 1 -i {} -i {} -y -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest -strict -2 {}.mp4".format(image, audio, output))

def GenerateNewMusic():
	return billboard.ChartData('hot-100')

def calcSpaces(image):
	response = pytesseract.image_to_string(Image.open(image)).encode('utf-8','replace')
	print response
	response = response.replace('\n', '').split(' ')
	return len(response)

def getClosestMatch(string, listofstrings):
	return difflib.get_close_matches(string, listofstrings)[0]

def removeNoise(listofwords, largerlistofwords):
	#this essentially finds the correct words for a list of words (lyrics)
	incorrect = 0
	ReturnVals = []
	for words in listofwords:
		try:
			newword = getClosestMatch(words, largerlistofwords)
			if levenshtein(words, newword) > (len(words) / 2):
				incorrect = incorrect + 1
				newword = words
			ReturnVals.append(newword)
		except:
			pass
	if incorrect < len(listofwords) / 2:
		return ReturnVals
	else:
		return []
		
def genAmazonURL(search):
	return 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Ddigital-music&field-keywords={}'.format(search.replace(' ', '+'))

def grabSongs(artist):
	url = genAmazonURL(artist)
	res = requests.get(url, headers=headers)
	page = bs4.BeautifulSoup(res.text)
	songs = []
	e = page.select(".songTitle")
	for a in e[1:]:
		songs.append(str(a.getText()))
	return songs

def levenshtein(s1, s2):
	if len(s1) < len(s2):
		return levenshtein(s2, s1)
	if len(s2) == 0:
		return len(s1)

	previous_row = range(len(s2) + 1)
	for i, c1 in enumerate(s1):
		current_row = [i + 1]
		for j, c2 in enumerate(s2):
			insertions = previous_row[j + 1] + 1
			deletions = current_row[j] + 1
			substitutions = previous_row[j] + (c1 != c2)
			current_row.append(min(insertions, deletions, substitutions))
		previous_row = current_row
	return previous_row[-1]

def genNC(image=None, listofwords=[], artist=None, song=None):
	threads = []
	Words = {}
	
	def batchExtract(listofimages):
		for image in listofimages:
			try:
				extractText(image)
			except Exception as exp:
				print(exp)
				pass

	def doCommand(image, listofwords):
		a = pytesseract.image_to_string(Image.open(image)).encode('utf-8','replace').split(' ')
		for a in a:
			if len(a) > 3:
				print difflib.get_close_matches(str(a), listofwords)[0]

	Information = {}
	listofwords = GrabSongLyrics(artist, song)
	d = []

	for i in range(len(image) / 5):
		t = threading.Thread(target=batchExtract, args=([image[i*5:(i*5) + 4]]))
		d.append(t)
		t.start()

	for t in d:
		t.join()

	for i, image in enumerate(image):
		t = threading.Thread(target=doCommand, args=(image, i))
		threads.append(t)
		t.start()

	for t in threads:
		t.join()
	Information["GuessedWords"] = Words
	Information["Real_Lyrics"] = listofwords
	with open('{}Transcript.json'.format(Words[1]), 'w') as f:
		json.dump(Information, f)


def applyChain(file):
	p = subprocess.Popen(["audacity", "./{}".format(file)])
	time.sleep(7)
	try:
		pyautogui.click(pyautogui.locateCenterOnScreen('src/images/discard.png'))
		time.sleep(1)
		pyautogui.click(pyautogui.locateCenterOnScreen('src/images/yes.png'))
	except:
		pass

	time.sleep(1)
	if len(list(pyautogui.locateAllOnScreen('src/images/audacity_fileButton.png'))) > 1:
		pyautogui.keyDown('alt')
		pyautogui.press('f10')
		pyautogui.keyUp('alt')
	time.sleep(1)
	pyautogui.click(pyautogui.locateCenterOnScreen('src/images/audacity_fileButton.png'))
	time.sleep(2)
	pyautogui.click(pyautogui.locateCenterOnScreen('src/images/audacity_applyChain.png'))
	time.sleep(2)
	pyautogui.click(pyautogui.locateCenterOnScreen('src/images/audacity_applyToCurrentFile.png'))
	time.sleep(10)
	p.terminate()
	print('Done')



def DownloadVideo(url, saveas='Vid.mp4'):
	os.system("youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' --output {} {} 2> /dev/null".format(saveas, url))
	return saveas

def ExtractFrames(video, folder=None):
	#this is the one that disables the keyboard use
	#this function converts the mp4 into a folder filled with pictures
	threads = []
	def doCommand(videourl, folder, i):
		print('Frame {} Completed'.format(i))
		os.system("ffmpeg -loglevel panic -ss {} -i {}.mp4 -y {}/{}.jpg".format(i, videourl, folder, i))
	if folder == None:
		folder = str(random.randint(1, 10000))
	os.system('mkdir {}'.format(folder))
	videourl = video.replace('.mp4', '')
	for i in range(1, int(GetDuration('{}.mp4'.format(videourl)))):
		t = threading.Thread(target=doCommand, args=(videourl, folder, i))
		threads.append(t)
		t.start()
	for t in threads:
		t.join()	

def ExtractAudio(filename):
	#This receives a .mp4 file but it removes .mp4 because the alternative seemed confusing af
	filename = str(filename).replace('.mp4', '')
	os.system('ffmpeg -i {}.mp4 -y {}.mp3'.format(filename, filename))
	return '{}.mp3'.format(filename)
	#I don't know why this returns anything.  ideally it should just be a boolean depending on if it worked or not

def returnSimilarWord(word, listofwords):
	return difflib.get_close_matches(word, listofwords)[0]

def GrabSongLyrics(artist, song):
	return str(PyLyrics.getLyrics(artist, song)).replace('\n', ' ').replace('\t', '').split(' ')

def extractText(image):
	print('{} Extracted'.format(image))
	filename = image
	filename = filename[:filename.rfind('/') + 1] + 'tmp' + filename[filename.rfind('/') + 1:]
	os.system('python extract_text.py {} {}'.format(image, filename))
	os.remove(image)
	os.system('mv {} {}'.format(filename, image))
	return image

def epicAudioCollab(audio):
	#work on this to get this to work
	saveas = stripExtension(audio) + '.mp4'
	os.system('./genVideos.sh epic {} {}'.format(audio, saveas))

def applySpectogram(audio):
	saveas = stripExtension(audio) + '.mp4'
	os.system('./genVideos.sh spectogram {} {}'.format(audio, saveas))

def applyAvectorscope(audio):
	saveas = stripExtension(audio) + '.mp4'
	os.system('./genVideos.sh avectorscope {} {}'.format(audio, saveas))

def applyMandelbrot(audio):
	saveas = stripExtension(audio) + '.mp4'
	os.system('./genVideos.sh mandelbrot {} {}'.format(audio, saveas))

def convertFramesToVid(saveas, folder=None):
	if folder != None:
		folder = folder + '/'
	os.system('ffmpeg -r 60 -f image2 -s 1920x1080 -i {}%07d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p {}'.format(folder, saveas))

if __name__ == "__main__":
	#genNC(image=ReturnAll('beware_of_darkness_all_who_remain', 'jpg'), listofwords=[], artist='beware of darkness', song='all who remain')
	'''lyrics = GrabSongLyrics('beware of darkness', 'all who remain')
	for image in ReturnAll('beware_of_darkness_all_who_remain', 'jpg'):
		words = ocrList(image)
		a = removeNoise(words, lyrics)
		print(a)'''
	print str(APIKEY)
	print ocrImage('test.jpg')