from __init__ import *

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
#createYoutube()

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
			print items['artist']
			print items['song']
			try:
				filename = '{}_{}'.format(items['artist'].replace(' ', '_'), items['song'].replace(' ', '_'))
			except:
				filename = items['url'].replace('https://www.youtube.com/watch?v=', '')
			DownloadVideo(items['url'], saveas=filename)
			ExtractFrames(filename, filename)
			e = ReturnAll(filename, 'jpg')
			print(e)
			genNC(image=e, artist=items['artist'], song=items['song'])
			#CompareOCR(filename, filename)
			ExtractAudio('{}.mp4'.format(filename))
			applyChain('{}.mp3'.format(filename))
			CombineAudioandImage('cleaned/{}.wav'.format(filename))

		for item in ReturnAll('../Main', 'mp4') + ReturnAll('../Main', 'mp3') + ReturnAll('../Main', 'avi'):
			os.remove(item)
		for item in ReturnAll('cleaned/', 'mp4'):
			os.system('mv {} Video/{}'.format(item, item.partition('cleaned/')[2]))
		for item in ReturnAll('cleaned/', 'wav'):
			os.system('mv {} Audio/{}'.format(item, item.partition('cleaned/')[2]))
