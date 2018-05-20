from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import json

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/viz1', methods=['GET'])
def testPage():
	likeCount = []
	followInfo = []
	tDict = []
	listOfFollowers = json.load(open("static/datasets/database.json"))["followers"]
	for val in json.load(open("static/datasets/userInfo.json")):
		if val['id'] in listOfFollowers:
			followInfo.append(val)
	for val in followInfo:
		ratio = (float(val['likes_count']) / float(val['followings_count']))
		tDict.append({"Ratio": ratio, "ID": val['id']})
	DATABASE = sorted(tDict, key=lambda k: k['Ratio'])
	return render_template("viz1.html", DATABASE=DATABASE)

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000)
