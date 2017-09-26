import os
import Image, ImageChops, ImageDraw, ImageFont, ImageFilter
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


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

def addText(image, text, fontsize=36, x=300, y=300):
	os.system('convert -font Helvetica -pointsize {} -fill black -draw \'text {},{} "{}" \' {} {}.tmp'.format(fontsize, x, y, text, image, image))
	os.system('rm {}'.format(image))
	os.system('mv {}.tmp {}'.format(image, image))