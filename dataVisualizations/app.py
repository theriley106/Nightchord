from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import json

app = Flask(__name__, static_url_path='/static')

listOfFollowers = json.load(open("static/datasets/database.json"))["followers"]
print listOfFollowers
@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/viz1', methods=['GET'])
def testPage():
	followInfo = []
	listOfFollowers = json.load(open("static/datasets/database.json"))["followers"]
	for val in json.load(open("static/datasets/userInfo.json")):
		if val['id'] in listOfFollowers:
			followInfo.append(val)
	return jsonify(followInfo)
	return render_template("viz1.html")

'''@app.route('/Jan19/', methods=['GET'])
def Jan19():
	import Jan17
	DATABASE=Jan17.getDatabase()
	for data in DATABASE:
		if data['Nootropics']["Sentiment"] == 0 or data['StackAdvice']["Sentiment"] == 0:
			DATABASE.remove(data)
	DATABASE = sorted(DATABASE, key=lambda k: k['StackAdvice']['Occurances'])
	date = sys._getframe().f_code.co_name
	if xUtilities.checkForScreenshot(date) == False:
		threading.Thread(target=xUtilities.saveScreenshot, args=(date,)).start()
		return "Getting Screenshot"
	return render_template("Jan19.html", DATABASE=DATABASE[::-1][:10])'''

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000)
