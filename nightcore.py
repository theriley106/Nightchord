from main import *
from itertools import islice
import googleinteraction
import threading
import time
import writePic
import os

TMP_DIR = "toClean"
try:
	os.system("mkdir {}".format(TMP_DIR))
except:
	pass

def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

def createYoutube(URL=None, Speed=None, SaveAs=None):
	listOfInputs = []
	if URL == None:
		while True:
			artist = raw_input('Artist: ')
			if len(artist) == 0:
				break
			song = raw_input('Song: ')
			listOfInputs.append({"artist": artist, "song": song})
	for val in listOfInputs:
		URL = findSong(val['artist'], val['song'])
		filename = '{}_{}'.format(val['artist'].replace(' ', '_'), val['song'].replace(' ', '_'))
		val['filename'] = filename
		DownloadVideo(URL, saveas=filename)
		a = ExtractAudio('{}.mp4'.format(filename))
		os.system("mv {} {}/{}.mp3".format(a, TMP_DIR, a))
	os.system("audacity")
	#applyChain('{}.mp3'.format(filename))
	#CombineAudioandImage('{}.mp3'.format(filename))


def removePics(filename):
	deletedFiles = []
	for file in writePic.removeSimilarImages(ReturnAll(filename, 'jpg')):
		deletedFiles.append(file)
		os.system('rm {}'.format(file))
	return deletedFiles

def genFileName(folder, i):
	return '{}/{}.png'.format(str(folder).partition('/')[0], i)

class nightcore(object):
	#sources = []
	sources = [{'url': 'https://www.youtube.com/watch?v=upZ_q9CdXl4', 'song': '22', 'artist': 'taylor swift'}]
	sources = []
	#Soruces should contain a list of dictionaries containing
	# yotuube URLS
	def __init__(self, speed=1.3, ocr=False, archive=False):
		print('Initiated')
		self.ocr = ocr
		self.archive = archive
		self.speed = speed

	def youtubeUrl(self, url):
		information = {'url': str(url)}
		self.sources.append(information)

	def artist(self, artist):
		for song in grabSongs(artist):
			try:
				self.song(artist, song)
			except Exception as exp:
				print(exp)

	def song(self, artist=None, song=None):
		if artist == None:
			artist = raw_input('Artist: ')
			song = raw_input('Song: ')
		URL = findSong(artist, song)
		information = {'artist': artist, 'song': song, 'url': URL}
		self.sources.append(information)

	def youtubeSearch(self, search):
		information = {'url': genYoutube(search)}
		self.sources.append(information)

	def genVideos(self):
		for items in self.sources:
			start = time.time()
			print items['artist']
			print items['song']
			try:
				filename = '{}_{}'.format(items['artist'].replace(' ', '_'), items['song'].replace(' ', '_'))
			except:
				filename = items['url'].replace('https://www.youtube.com/watch?v=', '')

			DownloadVideo(items['url'], saveas=filename)
			if self.ocr == True:
				ExtractFrames(filename, filename)
				totalFiles = len(ReturnAll(filename, 'jpg'))
				audio = ExtractAudio('{}.mp4'.format(filename))
				results = {}
				removePics(filename)
				for filelist in list(chunk(ReturnAll(filename, 'jpg'), 16)):
					a = googleinteraction.genOCR()
					for file in filelist:
						a.addImage(file)
					info = a.returnCommand()
					for key, value in info.iteritems():
						results[key] = value
				print results
				threads = []
				f = 0
				for key, value in results.iteritems():
					t = threading.Thread(target=writePic.addText, args=(key, value))
					threads.append(t)
					t.start()
					f = f + 1
					if f % 10 == 0:
						time.sleep(5)
				for t in threads:
					t.join()

				for i in range(1, totalFiles-1):
					if os.path.exists(genFileName(filename, i+1)) == False:
						os.system('cp {} {}'.format(genFileName(filename, i), genFileName(filename, i+1)))
				os.system('rm {}'.format(genFileName(filename, 1)))
				os.system('rm {}'.format(genFileName(filename, 2)))
				video = genVidFromFolder(filename, "{}.mp4".format(filename))
				filename = "{}.mp4".format(filename)
				l1 = GetDuration(audio)
				print('start gen cil')
				genCIL(audio)
				l2 = GetDuration(audio)
				video = SpeedUpVideo(filename)
				print 'done with speed up'
				return CombineVidandAudio(audio, video)
			else:
				audio = ExtractAudio('{}.mp4'.format(filename))
				genCIL(audio)
				background = 'background.jpg'
				saveas = filename + '.mp4'
				os.system('ffmpeg -i {} -i {} -acodec libvo_aacenc -vcodec libx264 -y {}'.format(background, audio, saveas))
			#genNC(image=e, artist=items['artist'], song=items['song'])
			#CompareOCR(filename, filename)
			#ExtractAudio('{}.mp4'.format(filename))
			#applyChain('{}.mp3'.format(filename))
			#genCIL("{}.mp3".format(filename))
			#CombineAudioandImage('{}.mp3'.format(filename))

		'''for item in ReturnAll('../Main', 'mp4') + ReturnAll('../Main', 'mp3') + ReturnAll('../Main', 'avi'):
			os.remove(item)
		for item in ReturnAll('cleaned/', 'mp4'):
			os.system('mv {} Video/{}'.format(item, item.partition('cleaned/')[2]))
		for item in ReturnAll('cleaned/', 'wav'):
			os.system('mv {} Audio/{}'.format(item, item.partition('cleaned/')[2]))'''
if __name__ == '__main__':
	createYoutube()
