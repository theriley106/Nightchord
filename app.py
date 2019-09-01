from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
from datetime import datetime
import csv
import os
import nightcore

app = Flask(__name__)

@app.route('/nightcore/', methods=['POST'])
def song():
	a = nightcore.nightcore()
	content = request.get_json()
	a.song(content['artist'], content['song'])
	file = a.genVideos()
	os.system("rm -r {}".format(file.replace('.mp4', '')))
	os.system("rm  {}".format(file.replace('.mp4', '.mp3')))
	return send_from_directory(directory="", filename=file)

@app.route('/download/', methods=["GET"])
def download():
	artist = request.args.get("artist")
	song = request.args.get("song")
	fileName = nightcore.createYoutubeCLI(artist, song)
	return send_from_directory(directory="", filename=fileName)

@app.route('/', methods=['GET'])
def index():
	return render_template("viz.html")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
