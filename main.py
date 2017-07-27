#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
from tesserocr import PyTessBaseAPI, RIL
import pyautogui
import json
import os
import bs4
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
counter = {"lev": 500, "item": ""}
lock = threading.Lock()
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
def PrintWarning(warningtext):
	print '\n' + bcolors.WARNING + warningtext + bcolors.ENDC
def PrintFail(failtext):
	print '\n' + bcolors.FAIL + failtext + bcolors.ENDC
def PrintGood(goodtext):
	print '\n' + bcolors.OKGREEN + goodtext + bcolors.ENDC
###############################################################################3
## Utilities

def ReturnFileName(file):
	return str(file).partition('.')[0]

def ReturnFileExtension(file):
	return str(file).partition('.')[2]

def process_item(lent=None, item=None, lenorig=0):
	global counter
	lock.acquire()
	if lent != None:
		print(str(lent), str(item))
		if lent < counter["lev"]:
			counter["lev"] = lent
			counter["item"] = str(item)
		lock.release()
	else:

		f = counter["item"]
		counter = {"lev": 500, "item": ""}
		lock.release()
		return f

def LevList(listone, listtwo):
	#a = len(set(listtwo) - set(listone))
	a = 0
	'''for i, words in enumerate(listone):
		try:
			#print(words)
			a = a + levenshtein(words, listtwo[i])
		except:
			pass'''
	try:
		if list(''.join(listtwo))[0] == list(''.join(listone))[0] or list(''.join(listtwo))[1] == list(''.join(listone))[1]:
			if list(''.join(listtwo))[-1] == list(''.join(listone))[-1] or list(''.join(listtwo))[-2] == list(''.join(listone))[-2]:
				print(list(''.join(listtwo))[0])
				print(list(''.join(listone))[0])
				a = len(set(listtwo) - set(listone))
				process_item(a, str(' '.join(listtwo)), len(listone))
	except:
		pass
def LowestSetOfNumbers(wordslist, lyrics):
	threads = []
	for i in range(len(lyrics)):
		listone = wordslist
		listtwo = lyrics[i:i+len(wordslist)]
		if abs(len(listone) - len(listtwo)) < 5:
			t = threading.Thread(target=LevList, args=(listone,listtwo))
			threads.append(t)
			t.start()
	for t in threads:
		t.join()
	return process_item()
		

def PromptList(text, inputted):
	PrintWarning('Initiated the list function\n')
	if inputted != None:
		return [inputted]
	List = []
	while True:
		New = raw_input(text)
		if New != '':
			List.append(New)
		else:
			if len(List) == 0:
				PrintFail('You need to input something here')
			else:
				if 'Y' in str(raw_input("Are you sure you don't want to input anymore? Y/N ")).upper():
					return List

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

def nextInList(smalist, biglist):
	##Fix this function
	try:
		smalist = [item.encode('utf-8') for item in smalist]
		biglist = [item.encode('utf-8') for item in biglist]
		print(smalist)
		print('Biglist: {}'.format(biglist))
		words = str(smalist).partition("'',")
		try:
			beforeword = words[0].split(',')[-2].replace('"', '').replace("'", "").replace(' ', '')
		except:
			return ''
		print(beforeword)
		afterword = words[2].split(',')[0].replace('"', '').replace("'", "").replace(' ', '')
		print(afterword)
		d = str((re.findall("{}.,(.*){}".format(beforeword, afterword), str(biglist))))
		print(d)
		d = d.split(',')[0]
		guess = ''.join(re.findall('\w', d))
		print(guess)
		#raw_input("Before {}\nMiddle {}\nAfter {}".format(beforeword, guess, afterword))
		return guess
		'''raw_input("cnf")
		for idx, wor in enumerate(biglist):
			wor = ''.join(filter(str.isalpha, str(wor).lower()))
			beforeword = ''.join(filter(str.isalpha, str(beforeword).lower()))
			print(wor)
			print(beforeword)
			if wor == beforeword:
				print('found word')
				if ''.join(filter(str.isalpha, str(wor[(idx + 2) % len(wor)]).lower())) == ''.join(filter(str.isalpha, str(afterword).lower())):
					print('word found: {}'.format(str(wor[(idx + 1) % len(wor)]).lower()))
					raw_input('test')
					return str(wor[(idx + 1) % len(wor)]).lower()'''
	except Exception as exp:
		raw_input(exp)
		return ''

	'''x = x.replace("'", "")
	x = x.replace('\\n', '')
	x = x.replace('\\t', '')
	x = x.replace(' ', '')'''

def ReturnAll(folder, fileextension='mp3'):
	return glob.glob("{}/*.{}".format(folder, fileextension))

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

def CombineVidandAudio(audio, video):
	audio = str(audio).replace('.mp3', '')
	video = str(video).replace('.mp4', '')
	video = str(video).replace('.avi', '')
	filename = str(video).replace('.mp4', '')
	os.system('ffmpeg -i {}.mp3 -i {}.avi -y -strict -2 {}z.mp4'.format(audio, video, filename))
	#os.system('ffmpeg -i {} -i {} -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 {}z.mp4'.format(video, audio, filename))
	os.remove('{}.mp4'.format(filename))
	os.system('mv {}z.mp4 -y {}.mp4'.format(filename, filename))
	#those weird lines above need to be done because FFMPEG doesn't correctly overwrite files
	return '{}.mp4'.format(filename)

def CombineAudioandImage(audio, image=None, output=None):
	if image == None:
		image = GenerateBackground()
	if output == None:
		output = str(audio)
	output = str(output).replace('.wav', '')
	output = str(output).replace('.mp3', '')
	os.system("ffmpeg -loop 1 -i {} -i {} -y -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest -strict -2 {}.mp4".format(image, audio, output))

##############################################################################################
## Generate

def GenerateNewMusic():
	return billboard.ChartData('hot-100')

def GenerateBackground():
	return random.choice(glob.glob("src/backgrounds/*.jpg"))

def ReturnAll(folder, extension='mp3'):
	return glob.glob("{}/*.{}".format(folder, extension))

def GetDuration(clip):
	if '.mp4' in str(clip): return VideoFileClip(clip).duration
	elif '.mp3' in str(clip): return eyed3.load('{}'.format(clip)).info.time_secs

def GrabSongLyrics(artist, song):
	return str(PyLyrics.getLyrics(artist, song)).replace('\n', ' ').replace('\t', '').split(' ')

##########################################################################
## Video
def ExtractFrames(video, folder=None):
	if folder == None:
		folder = str(random.randint(1, 10000))
	os.system('mkdir {}'.format(folder))
	videourl = video.replace('.mp4', '')
	for i in range(1, int(GetDuration('{}.mp4'.format(videourl)))):
		os.system("ffmpeg -loglevel panic -ss {} -i {}.mp4 -y {}/{}.jpg".format(i, videourl, folder, i))

def CompareOCR(video, folder=None):
	ExtractFrames(video, folder)
	findLyrics(ReturnAll(folder, 'jpg'), listofwords=[''])

def DownloadVideo(url, saveas='Vid.mp4'):
	os.system("youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' --output {} {} 2> /dev/null".format(saveas, url))
	return saveas

def YoutubeToFrames(url=None):
	PrintGood('This function convert youtube video into frames in a randomly created folder')
	PrintWarning("This fails a bunch of times, but it still runs - IDK why")
	if isinstance(url, list) == False:
		url = PromptList('Which image/images to convert from frames: ', url)
	for url in url:
		video = DownloadVideo(url, saveas='Vid.mp4')
		ExtractFrames(video)

def SpeedUpVideo(vidfile, percent=1.31):
	if 'avi' in str(vidfile):
		os.system('ffmpeg -i {} -c:a aac -b:a 128k -c:v libx264 -crf 23 {}.mp4'.format(vidfile, vidfile.replace('.avi', '')))
		vidfile = vidfile.replace('.avi', '')
	vidfile = vidfile.replace('.mp4', '')
	os.system('ffmpeg -i {}.mp4 -y -vcodec copy -acodec copy {}.avi'.format(vidfile, vidfile))
	os.system('mencoder -nosound -speed {} -o {}z.avi -ovc lavc {}.avi'.format(str(percent), vidfile, vidfile))
	os.remove('{}.mp4'.format(vidfile))
	os.system('ffmpeg -i {}z.avi -c:a aac -b:a 128k -c:v libx264 -crf 23 {}.mp4'.format(vidfile, vidfile))
	os.remove('{}z.avi'.format(vidfile))
	#os.remove('{}.mp4'.format(vidfile))
	#os.system('mv {}z.mp4 {}.mp4'.format(vidfile, vidfile))
	return '{}.mp4'.format(vidfile)

######################################################################################
## OCR

def RetrOCR(image=None, listofwords=[]):
	if len(listofwords) == 0:
		PrintFail('You need to input a list of words')
		if 'y' in str(raw_input("Do you want to search for lyrics now? ")).lower():
			artist = raw_input("Artist: ")
			song = raw_input("Song: ")
			listofwords = GrabSongLyrics(artist, song)
			print(listofwords)
		else:
			return
	if isinstance(image, list) == False:
		image = PromptList('Which image/images to Scan: ', image)
	for image in image:
		WordsInImage = []
		#spaces = Spaces(image)
		lines = genLines(image)
		print(lines)
		for e in range(len(lines)):
			for wordlyric in lines[e]:
				try:
					a = difflib.get_close_matches(wordlyric, listofwords)[0]
					wordlyric = a
					WordsInImage.append(wordlyric)
				except Exception as exp:
					print exp
				
		WordsToSet = ' '.join(WordsInImage)
		imagelocation = image[:image.rfind('/') + 1]
		WriteToImage(image, WordsToSet, size=45, input=image)
	os.system("mkdir OCR &> /dev/null/")
	for result in glob.glob("{}/*.png".format(imagelocation)):
		resultz = result.partition('/')[2]
		os.system("mv {} OCR/{}".format(result, resultz))

def genLines(image=None):
	PrintGood('This is going to return OCR on either a list of images or full images')
	if isinstance(image, list) == False:
		image = PromptList('Which image/images to OCR: ', image)
	Found = []
	for image in image:
		image = Image.open(image)
		with PyTessBaseAPI() as api:
			api.SetImage(image)
			boxes = api.GetComponentImages(RIL.TEXTLINE, True)
			print 'Found {} textline image components.'.format(len(boxes))
			for i, (im, box, _, _) in enumerate(boxes):
				# im is a PIL image object
				# box is a dict with x, y, w and h keys
				api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
				ocrResult = api.GetUTF8Text().split(' ')
				conf = api.MeanTextConf()
				ocrResult = [word.strip() for word in ocrResult]
				Found.append(ocrResult)
				print (u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, "
					   "confidence: {1}, text: {2}").format(i, conf, ocrResult, **box)
	return Found

def genCords(image=None, listofwords=[]):
	AllWords = []
	PrintGood('This is going to return individual images for every undefined word found')
	if len(listofwords) == 0:
		PrintWarning("This is going to save all words, to define words to look for input a list containing words for tesseract to find.\n")
		if 'y' in str(raw_input("Do you want to search for lyrics now? ")).lower():
			artist = raw_input("Artist: ")
			song = raw_input("Song: ")
			listofwords = GrabSongLyrics(artist, song)
			listofwords = [x.upper() for x in listofwords]
			listofwords = [i.replace('\n','') for i in listofwords]
			listofwords = [i.replace('\t','') for i in listofwords]
			print(listofwords)
		else:
			return
	if isinstance(image, list) == False:
		image = PromptList('Which image/images to OCR: ', image)
	for image in image:
		im = Image.open(image)
		os.system("tesseract {} stdout -c tessedit_create_hocr=1 -c tessedit_pageseg_mode=1 -l eng -psm 3 > index.html".format(image))
		page = bs4.BeautifulSoup(open("index.html")).select('#page_1')
		for x in page[0].select('.ocrx_word'):
			text = x.getText().encode('ascii', 'ignore').decode('ascii')
			coordinates = str(re.findall("bbox\s(.*);", str(x))[0]).split(' ')
			coordinates = tuple([float(i) for i in coordinates])

			if str(text).upper() not in listofwords:
				try:
					f = im.crop(coordinates)
					with PyTessBaseAPI() as api:
						api.SetImage(f)
						ocrResult = api.GetUTF8Text()
						conf = api.MeanTextConf()
						print("confidence: {}".format(conf))
					f.save('{}.jpg'.format(text))
				except Exception as exp:
					print(exp)
					PrintWarning("Error, the following text was ignored: \"{}\"\nThe program will continue running\n".format(text))
			else:
				AllWords.append(text)	
	return AllWords

def Spaces(image=None):
	PrintGood('This returns the number of spaces in a specific image or images')
	if isinstance(image, list) == False:
		image = PromptList('Which image/images to Scan: ', image)
	for image in image:
		image = Image.open(image)
		with PyTessBaseAPI() as api:
			api.SetImage(image)
			boxes = api.GetComponentImages(RIL.TEXTLINE, True)
			Spaces = 0
			for i, (im, box, _, _) in enumerate(boxes):
				im.save('saving{}.jpg'.format(i))
				api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
				ocrResult = api.GetUTF8Text()
				conf = api.MeanTextConf()
				text = str(ocrResult).replace('\n', '').split(' ')
				Spaces = len(text) + Spaces
	return int(Spaces)


def findLyrics(image=None, listofwords=[]):
	PrintGood('This is going to successfully OCR lyric screenshots')

	if len(listofwords) == 0:
		PrintFail('You need to input a list of words')
		if 'y' in str(raw_input("Do you want to search for lyrics now? ")).lower():
			artist = raw_input("Artist: ")
			song = raw_input("Song: ")
			listofwords = GrabSongLyrics(artist, song)
			print(listofwords)
		else:
			return
	if isinstance(image, list) == False:
		image = PromptList('Which image/images to Scan: ', image)
	for image in image:
		WordsInImage = []
		spaces = Spaces(image)
		lines = genLines(image)
		print(lines)
		for e in range(len(lines)):
			for wordlyric in lines[e]:
				if wordlyric not in listofwords:
					print('not in list of words: {}'.format(wordlyric))
					for words in listofwords:
						A = False
						if levenshtein(wordlyric, words) < 1:
							A = True
							WordsInImage.append(words)
							break
					if A == False:
						WordsInImage.append(["", wordlyric])
				else:
					print('appended: {}'.format(wordlyric))
					WordsInImage.append(wordlyric)

		for w in WordsInImage:
			if len(w[1]) > 1:
				w = nextInList(WordsInImage, listofwords)
			print(w)

def writeLyrics(image=None, listofwords=[]):
	imagez = GenerateBackground()
	if len(listofwords) == 0:
		PrintFail('You need to input a list of words')
		if 'y' in str(raw_input("Do you want to search for lyrics now? ")).lower():
			artist = raw_input("Artist: ")
			song = raw_input("Song: ")
			listofwords = GrabSongLyrics(artist, song)
			print(listofwords)
		else:
			return
	if isinstance(image, list) == False:
		image = PromptList('Which image/images to Scan: ', image)
	for image in image:
		WordsInImage = []
		#spaces = Spaces(image)
		lines = genLines(image)
		print(lines)
		for e in range(len(lines)):
			for wordlyric in lines[e]:
				if wordlyric not in listofwords:
					print('not in list of words: {}'.format(wordlyric))
					for words in listofwords:
						A = False
						if levenshtein(wordlyric, words) < 1:
							A = True
							WordsInImage.append(words)
							break
					if A == False:
						WordsInImage.append("")
				else:
					print('appended: {}'.format(wordlyric))
					WordsInImage.append(wordlyric)
		e = []
		WordsToSet = LowestSetOfNumbers(WordsInImage, listofwords)
		if len(WordsToSet) == 0:
			WordsToSet = ' '.join(WordsInImage)
		imagelocation = image[:image.rfind('/') + 1]
		WriteToImage(image, WordsToSet, size=45, input=imagez)
	os.system("mkdir OCR &> /dev/null/")
	for result in glob.glob("{}/*.png".format(imagelocation)):
		resultz = result.partition('/')[2]
		os.system("mv {} OCR/{}".format(result, resultz))

def imageToOCR(image, listofwords):
	WordsInImage = []
	lines = genLines(image)
	for e in range(len(lines)):
		for wordlyric in lines[e]:
			if wordlyric not in listofwords:
				print('not in list of words: {}'.format(wordlyric))
				for words in listofwords:
					A = False
					if levenshtein(wordlyric, words) < 1:
						A = True
						WordsInImage.append(words)
						break
				if A == False:
					WordsInImage.append("")
			else:
				print('appended: {}'.format(wordlyric))
				WordsInImage.append(wordlyric)
	e = []
	WordsToSet = LowestSetOfNumbers(WordsInImage, listofwords)
	if len(WordsToSet) == 0:
		WordsToSet = ' '.join(WordsInImage)
	return WordsToSet

def ocrToDict(image=None, listofwords=[]):
	#image can be a list of files
	Words = {}
	if len(listofwords) == 0:
		PrintFail('You need to input a list of words')
		if 'y' in str(raw_input("Do you want to search for lyrics now? ")).lower():
			artist = raw_input("Artist: ")
			song = raw_input("Song: ")
			listofwords = GrabSongLyrics(artist, song)
			print(listofwords)
		else:
			return
	if isinstance(image, list) == False:
		image = PromptList('Which image/images to Scan: ', image)
	for i, image in enumerate(image):
		Words['Clean'][i] = imageToOCR(image, listofwords)
	with open('{}Transcript.json'.format(Words[1]), 'w') as f:
		json.dump(Words, f)

def genNC(image=None, listofwords=[], artist=None, song=None):
	Words = {}

	if len(listofwords) == 0:
		PrintFail('You need to input a list of words')
		if 'y' in str(raw_input("Do you want to search for lyrics now? ")).lower():
			if artist == None:
				artist = raw_input("Artist: ")
			if song == None:
				song = raw_input("Song: ")
			listofwords = GrabSongLyrics(artist, song)
		else:
			return


	if isinstance(image, list) == False:
		image = PromptList('Which image/images to Scan: ', image)



	for i, image in enumerate(image):
		i = i + 1
		Words[i] = genLines(image)

	with open('{}Transcript.json'.format(Words[1]), 'w') as f:
		json.dump(Words, f)

def readOCR(jsonfile):
	with open(jsonfile) as data_file:    
		data = json.load(data_file)
	for i in range(1, len(data)):
		print('{}-{}'.format(i, data[str(i)]))



############################################################################################3
## Audio

def ExtractAudio(filename):
	#This receives a .mp4 file but it removes .mp4 because the alternative seemed confusing af
	filename = str(filename).replace('.mp4', '')
	os.system('ffmpeg -i {}.mp4 -y {}.mp3'.format(filename, filename))
	return '{}.mp3'.format(filename)
	#I don't know why this returns anything.  ideally it should just be a boolean depending on if it worked or not

def clickFile():
	pyautogui.click(pyautogui.locateCenterOnScreen('src/images/audacity_fileButton.png'))

def clickApplyChain():
	pyautogui.click(pyautogui.locateCenterOnScreen('src/images/audacity_applyChain.png'))

def clickApplyToFile():
	pyautogui.click(pyautogui.locateCenterOnScreen('src/images/audacity_applyToCurrentFile.png'))

def maxWindow():
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

def applyChain(file):
	p = subprocess.Popen(["audacity", "./{}".format(file)])
	time.sleep(7)
	maxWindow()
	time.sleep(1)
	clickFile()
	time.sleep(2)
	clickApplyChain()
	time.sleep(2)
	clickApplyToFile()
	time.sleep(10)
	p.terminate()
	print('Done')

######################################################################################################
## Image

def draw_text_with_halo(img, position, text, font, col, halo_col):
	halo = Image.new('RGBA', img.size, (0, 0, 0, 0))
	ImageDraw.Draw(halo).text(position, text, font = font, fill = halo_col)
	blurred_halo = halo.filter(ImageFilter.BLUR)
	ImageDraw.Draw(blurred_halo).text(position, text, font = font, fill = col)
	return Image.composite(img, blurred_halo, ImageChops.invert(blurred_halo))

def WriteToImage(output, txt, size=45, input='background.jpg'):
	output = str(output).replace('.png', '').replace('.jpg', '')
	i = Image.open(input)
	font = ImageFont.load_default()
	txt = txt.split(' ')
	r = []
	for part in txt:
		r.append(str(part).replace(' ', ''))
	txt = r
	a = ''
	while len(txt) > 0:
		try:
			for e in range(7):
				item = txt[0]
				txt.remove(item)
				a = a + ' ' + str(item)
			a = a + '\n'
		except:
			break
	text_col = (255, 255, 255) # bright green
	halo_col = (0, 0, 0)   # black
	i2 = draw_text_with_halo(i, (20, 40), a, font, text_col, halo_col)
	i2.save('{}.png'.format(output))


if __name__ == "__main__":
	#print(Spaces())
	'''import subprocess
	import time
	cwd=os.path.dirname(os.path.realpath(__file__))
	p = subprocess.Popen(["audacity", "r.mp3"])
	time.sleep(7)
	try:
		if len(list(pyautogui.locateAllOnScreen('src/images/audacity_fileButton.png'))) > 1:
			a = pyautogui.click(pyautogui.locateCenterOnScreen('audacity_fileButton.png'))
	except Exception as exp:
		print('close files that have the file extension thing in background')
	time.sleep(1)
	pyautogui.click(pyautogui.locateCenterOnScreen('audacity_applyChain.png'))
	time.sleep(1)
	pyautogui.click(pyautogui.locateCenterOnScreen('audacity_applyToCurrentFile.png'))
	time.sleep(10)
	p.terminate()'''
	print('started')



#main.findLyrics(image=main.ReturnAll('beware_of_darkness_all_who_remain', 'jpg'), listofwords=[])
#main.RetrOCR(image=main.ReturnAll('beware_of_darkness_all_who_remain', 'jpg'), listofwords=[])
#main.writeLyrics(image=main.ReturnAll('beware_of_darkness_all_who_remain', 'jpg'), listofwords=[])