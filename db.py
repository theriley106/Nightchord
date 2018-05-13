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

def resetDB():
	os.system("mv {} {}".format(DATABASE_FILE, "backup.json"))
	os.system("mv {} {}".format("dbTemplate.json", DATABASE_FILE))

def updateDB():
	os.system("mv {} {}".format(DATABASE_FILE, "backup.json"))
	with open(DATABASE_FILE, 'w') as f:
		json.dump(DATABASE, f)
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



if __name__ == '__main__':
	url = "https://api-v2.soundcloud.com/users/38122545/followers?&limit=200&client_id={}".format(clientID)
	res = requests.get(url)
	for val in res.json()['collection']:
		addFollower(val)
