import os
import Image, ImageChops, ImageDraw, ImageFont, ImageFilter
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


'''def WriteToImage(output, txt, size=45, input='background.jpg'):
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
	i2.save('{}.png'.format(output))'''

def addText(image, text, inputs='background.jpg', font='Royal.ttf', fontsize=75, x=300, y=300):
	image = str(image).replace('.png', '').replace('.jpg', '')
	saveas = image + '.png'
	background = inputs
	text = text.upper()
	'''if len(text) > 40:
		a = [text[i:i+40] for i in range(0, len(text), 40)]
		if len(str(a[-1])) < 10:
			a.remove(a[-1])
		text = '\n'.join(a)'''
	if len(text) > 40:
		text = text.split(' ')
		text = [" ".join(text[i:i+8]) for i in range(0, len(text), 8)]
		text = '\n'.join(text)


	with Image.open(inputs) as img:
		width, height = img.size
	y = float(height * .95)
	x = width / 2
	font = os.getcwd() + "/" + font
	font = 'Helvetica-Bold'
	os.system('convert -font {} -pointsize {} -fill black -gravity South -annotate +10+10 "{}" {} {}.png.tmp'.format(font, fontsize, text, background, image))
	os.system('convert -font {} -pointsize {} -fill white -gravity South -annotate +5+5 "{}" {}.png.tmp {}.png'.format(font, fontsize, text, image, image))
	#os.system('convert -font {} -pointsize {} -fill black -draw "text {},{} \'{}\'" -fill white -draw "text {},{} \'{}\'" {} {}.tmp'.format(font, fontsize, x, y, text, x-3, y-3, text, image, image))
	os.system('rm {}.png.tmp'.format(image))
	os.system('rm {}.jpg'.format(image))

