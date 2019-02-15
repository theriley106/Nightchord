import os
import base64
import json
import time
APIKEY = open('apiKey.txt','r').read()

def convertBase(image):
	return base64.b64encode(open(image, "rb").read())

def genCurl(basefile):
	a = 'curl -v -s -H "Content-Type: application/json" https://vision.googleapis.com/v1/images:annotate?key={} --data-binary @{}'.format(APIKEY, basefile)
	return a

class genOCR(object):
	def __init__(self):
		self.Files = []
		self.OCR = {}
		self.command = '''
		{
		  "requests": [
			'''

	def addImage(self, image):
		self.Files.append(image)
		addition = '''
		{
		"image": {
			"content": "BASE"
		  },
		  "features": [
			{
			  "type": "TEXT_DETECTION",
			  "maxResults": 1
			},
		  ]
		},
		'''
		addition = addition.replace("BASE", convertBase(image))
		self.command = self.command + addition

	def returnCommand(self, saveas="Request.tmp"):
		responses= []
		self.command = self.command + '''
		  ]
		}'''
		out = open(saveas, 'w')
		out.write(self.command)
		out.close()
		a = genCurl(saveas)
		os.system("{} > tmp.json".format(a))
		with open('tmp.json') as json_data:
			d = json.load(json_data)
		for i, lines in enumerate(d['responses']):
			try:
				self.OCR[self.Files[i]] = lines['textAnnotations'][0]['description']
			except:
				self.OCR[self.Files[i]] = ''
		return self.OCR
start = time.time()
a = genOCR()
for i in range(1,16):
	a.addImage("the_show/test/thumb{}.jpg".format(str(i).zfill(4)))
for key, value in a.returnCommand().iteritems():
	print key, value
end = time.time()
print(end - start)
