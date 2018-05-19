import json
import requests
import random
import os

idList = []
for val in open("listOfClientIDs.txt").read().split("\n"):
	if len(val) > 5:
		idList.append(val)
if len(idList) == 0:
	raise Exception("No Client IDs")
clientID = random.choice(idList)

DATABASE_FILE = "database.json"
DATABASE = json.load(open(DATABASE_FILE))

USERINFO_FILE = "userInfo.json"
USERINFO = json.load(open(USERINFO_FILE))

def resetDB():
	os.system("mv {} {}".format(DATABASE_FILE, "backup.json"))
	os.system("mv {} {}".format("dbTemplate.json", DATABASE_FILE))

def updateDB():
	os.system("mv {} {}".format(DATABASE_FILE, "backup.json"))
	with open(DATABASE_FILE, 'w') as f:
		json.dump(DATABASE, f)
	print("Updated")

def updateJSON(fileName):
	os.system("mv {} {}".format(USERINFO_FILE, "backup.json"))
	with open(USERINFO_FILE, 'w') as f:
		json.dump(USERINFO, f)
	print("Updated")

def updateUser(userInfo):
	for val in DATABASE['users']:
		if val['id'] == userInfo['id']:
			DATABASE['users'].remove(val)
			DATABASE['users'].append(userInfo)
			break
	DATABASE["userIDs"].append(userInfo['id'])

def addFollower(userInfo):
	if userInfo['id'] in DATABASE["userIDs"]:
		updateUser(userInfo)
	else:
		DATABASE["userIDs"].append(userInfo['id'])
		DATABASE["users"].append(userInfo)
	if userInfo['id'] not in DATABASE["followers"]:
		DATABASE["followers"].append(userInfo['id'])
	updateDB()

def updateUserList(userInfo):
	for val in USERINFO:
		if val['id'] == userInfo['id']:
			return
	USERINFO.append(userInfo)
	os.system("mv {} {}".format(USERINFO_FILE, "backupUI.json"))
	with open(USERINFO_FILE, 'w') as f:
		json.dump(USERINFO, f)
	print("Updated")
	return

if __name__ == '__main__':
	url = "https://api-v2.soundcloud.com/users/38122545/followings?&limit=200&client_id={}".format(clientID)
	res = requests.get(url)
	for val in res.json()['collection']:
		#addFollower(val)
		updateUserList(val)
