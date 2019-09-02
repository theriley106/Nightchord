from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
from datetime import datetime
import csv
import os
import nightcore
import time

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

# @app.route('/downloadFile/<fileName>', methods=["GET"])
def downloadFile(fileName=None):
	if fileName == None:
		return "<h1>Invalid File</h1>"
	return send_file("static/"+fileName, attachment_filename=fileName, as_attachment=True)


@app.route('/download/', methods=["GET"])
def download():
	for i in range(1,4):
		try:
			artist = request.args.get("artist")
			song = request.args.get("song")
			fileName = nightcore.createYoutubeCLI(artist, song)
			fileNameNew = fileName[::-1].partition("/")[0][::-1]
			os.system("mv {} static/{}".format(fileName, fileNameNew))
			return redirect(url_for('index', fileName=fileNameNew))
		except Exception as exp:
			print(exp)
			time.sleep(i*2)
	return "<h1>ERROR PLEASE TRY AGAIN LATER</h1>"

@app.route('/<fileName>', methods=['GET'])
def index(fileName="final8.mp3"):
	if request.args.get("download", False) != False:
		return downloadFile(fileName)
	return render_template("viz.html", fileURL='http://127.0.0.1:5000/static/{}'.format(fileName))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
