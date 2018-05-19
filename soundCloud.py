import requests

try:
	idList = []
	for val in open("listOfClientIDs.txt").read().split("\n"):
		if len(val) > 5:
			idList.append(val)
	if len(idList) == 0:
		raise Exception("No Client IDs")
	clientID = random.choice(idList)
except:
	clientID = raw_input("Client ID: ")

try:
	authCode = open("authCode.txt").read().split('\n')[0]
	if len(authCode) == 0:
		raise Exception("No Auth IDs")
except:
	authCode = raw_input("Auth Code: ")
