import json
import requests
import random
import os
import growAccount
import time
LIMIT = 200

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
	if userInfo['id'] not in DATABASE["followers"]:
		DATABASE["followers"].append(userInfo['id'])
		updateDB()

def addFollowing(userInfo):
	if userInfo['id'] not in DATABASE["followings"]:
		DATABASE["followings"].append(userInfo['id'])
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


def grabAllFollowings(actID='438591654'):
	listOfFollowings = []
	url = 'https://api-v2.soundcloud.com/users/{}/followings?limit={}&client_id={}'.format(actID, LIMIT, clientID)
	while True:
		try:
			res = requests.get(url)
			for val in res.json()['collection']:
				listOfFollowings.append(val)
				updateUserList(val)
				addFollowing(val)
			if res.json()['next_href'] == None:
				print("{} Followings Checked".format(len(listOfFollowings)))
				return listOfFollowings
			else:
				url = str(res.json()['next_href'] + "&client_id={}".format(clientID))
		except Exception as exp:
			print exp
			pass
		print("Finished searching page")
	print("{} Followings Checked".format(len(listOfFollowings)))

	return listOfFollowings

def grabAllFollowers(actID='438591654'):
	listOfFollowers = []
	url = 'https://api-v2.soundcloud.com/users/{}/followers?limit={}&client_id={}'.format(actID, LIMIT, clientID)
	while True:
		try:
			res = requests.get(url)
			for val in res.json()['collection']:
				listOfFollowers.append(val)
				updateUserList(val)
				addFollower(val)
			if res.json()['next_href'] == None:
				print("{} Followers Checked".format(len(listOfFollowers)))
				return listOfFollowers
			else:
				url = str(res.json()['next_href'] + "&client_id={}".format(clientID))
		except Exception as exp:
			print exp
			pass
		print("Finished searching page")
	print("{} Followers Checked".format(len(listOfFollowers)))
	return listOfFollowers

def getUserInfo(userID):
	for val in USERINFO:
		if str(val['id']) == str(userID):
			return val

def unfollowUser(userID):
	url = 'https://api-v2.soundcloud.com/me/followings/{}?&client_id={}'.format(userID, clientID)
	print url
	sleepTime = round(random.uniform(1.0, 20.0), 2)
	print("Unfollowing {} in {} Seconds".format(userID, sleepTime))
	time.sleep(sleepTime)
	response = requests.delete(url)
	print("Unfollowed: {}".format(userID))

def update():
	grabAllFollowings()
	grabAllFollowers()

if __name__ == '__main__':
	unfollowUser("17778617")
	update()
