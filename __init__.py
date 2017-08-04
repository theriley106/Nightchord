#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tesserocr import PyTessBaseAPI, RIL
import pyautogui
import json
import os
import bs4
import pytesseract
from moviepy.editor import VideoFileClip
import billboard
import time
import random
import difflib
import csv
import subprocess
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

def GetDuration(clip):
	if '.mp4' in str(clip):
		return VideoFileClip(clip).duration
	elif '.mp3' in str(clip):
		return eyed3.load('{}'.format(clip)).info.time_secs


def LoadHeader():
	UserAgentCSV = open('UserAgent.csv', 'r')
	UserAgentList = csv.reader(UserAgentCSV)
	UserAgentList = [row for row in UserAgentList]
	UserAgentList = [l[0] for l in UserAgentList]
	random.shuffle(UserAgentList)
	return {'User-Agent': random.choice(UserAgentList)}

def genNC(image=None, listofwords=[], artist=None, song=None):
	Words = {}
	Information = {}
	for i, image in enumerate(image):
		i = i + 1
		Words[i] = pytesseract.image_to_string(Image.open(image))
	Information['GuessedWords'] = Words
	Information["Real_Lyrics"] = listofwords
	with open('{}Transcript.json'.format(Words[1]), 'w') as f:
		json.dump(Information, f)

def findSong(artist, song):
	return genYoutube('{} {} lyrics'.format(artist, song))

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

def ExtractAudio(filename):
	#This receives a .mp4 file but it removes .mp4 because the alternative seemed confusing af
	filename = str(filename).replace('.mp4', '')
	os.system('ffmpeg -i {}.mp4 -y {}.mp3'.format(filename, filename))
	return '{}.mp3'.format(filename)
	#I don't know why this returns anything.  ideally it should just be a boolean depending on if it worked or not

def ReturnAll(folder, extension='mp3'):
	return glob.glob("{}/*.{}".format(folder, extension))

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

def CombineAudioandImage(audio, image=None, output=None):
	if image == None:
		image = GenerateBackground()
	if output == None:
		output = str(audio)
	output = str(output).replace('.wav', '')
	output = str(output).replace('.mp3', '')
	os.system("ffmpeg -loop 1 -i {} -i {} -y -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest -strict -2 {}.mp4".format(image, audio, output))

def GenerateBackground():
	return random.choice(glob.glob("src/backgrounds/*.jpg"))

def DownloadVideo(url, saveas='Vid.mp4'):
	os.system("youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' --output {} {} 2> /dev/null".format(saveas, url))
	return saveas

def ExtractFrames(video, folder=None):
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