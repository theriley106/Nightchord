#!/bin/sh
# $0 is the script name, $1 id the first ARG, $2 is second...
FILTER="$1"
INPUT="$2"
OUTPUT="$3"
if [ $FILTER = "avectorscope" ]; then
	echo "Applying $FILTER"
	ffmpeg -i $INPUT -filter_complex avectorscope=s=320x240 -y -acodec copy $OUTPUT
elif [ $FILTER = "spectogram" ]; then
	echo "Applying $FILTER"
	ffmpeg -i $INPUT -filter_complex showspectrum=mode=separate:color=intensity:slide=1:scale=cbrt -y -acodec copy $OUTPUT
elif [ $FILTER = "mandelbrot" ]; then
	echo "Applying $FILTER"
	ffmpeg -i $INPUT -f lavfi -i mandelbrot=s=320x240 -y -acodec copy $OUTPUT
elif [ $FILTER = "epic" ]; then
	echo "Applying $FILTER"
	ffmpeg -i $INPUT -filter_complex \
	"[0:a]avectorscope=s=640x518,pad=1280:720[vs]; \
	 [0:a]showspectrum=mode=separate:color=intensity:scale=cbrt:s=640x518[ss]; \
	 [0:a]showwaves=s=1280x202:mode=line[sw]; \
	 [vs][ss]overlay=w[bg]; \
	 [bg][sw]overlay=0:H-h,drawtext=fontfile=/usr/share/fonts/TTF/Vera.ttf:fontcolor=white:x=10:y=10:text='\"Song Title\" by Artist'[out]" \
	-map "[out]" -map 0:a -c:v libx264 -preset fast -crf 18 -c:a copy $OUTPUT
else
	echo "No Known Filter..."
fi