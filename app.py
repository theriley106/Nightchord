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
	fileNameNew = fileName[::-1].partition("/")[0][::-1]
	os.system("mv {} static/{}".format(fileName, fileNameNew))
	return redirect(url_for('index', fileName=fileNameNew))
	return send_from_directory(directory="", filename=fileName)

@app.route('/<fileName>', methods=['GET'])
def index(fileName="final8.mp3"):
	return render_template("viz.html", fileURL='http://127.0.0.1:5000/static/{}'.format(fileName))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
