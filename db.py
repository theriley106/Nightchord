import json

DATABASE = json.load(open("database.json"))

def addFollower(userInfo):
	if userInfo['id'] not in DATABASE["followers"]:
		DATABASE["followers"].append(userInfo['id'])
		DATABASE["users"].append(userInfo)

print DATABASE
