import requests
import random
import time
import random
LIMIT = 10000
# This is the result limit

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

listOfAccts = ["nightcore-3"]
willFollow = 0
followingMin = 30
likesMin = 100
toFollow = []
listOfFollowings = []
# These are the people that the account is currently following

def getFollowingsCount():
	res = requests.get("https://api-mobi.soundcloud.com/resolve?permalink_url=https%3A//soundcloud.com/user-367430385&client_id=iZIs9mchVcX5lhVRyQGGAYlNPVldzAoX&format=json&app_version=1524734136")
	return res.json()['followings_count']

def updateToFollow(followCount=None):
	offset = None
	url = "https://api-v2.soundcloud.com/users/38122545/followers?&limit=200&client_id={}".format(clientID)
	while len(toFollow) < followCount:
		res = requests.get(url)
		for val in res.json()['collection']:
			#if (float(val['followings_count']) / float(val['followers_count']) * 100)
			if (val['followings_count'] > followingMin) and (val['likes_count'] > likesMin):
				if len(toFollow) <= followCount and (val['id'] not in listOfFollowings):
					toFollow.append(val['id'])
					print("{} - {}".format(val['permalink_url'], val['id']))
		url = res.json()['next_href'] + "&client_id={}".format(clientID)

def updateCurrentFollowing(actID='438591654'):
	followings = getFollowingsCount()
	url = 'https://api-v2.soundcloud.com/users/{}/followings?limit={}&client_id={}'.format(actID, LIMIT, clientID)
	while len(listOfFollowings) < followings:
		try:
			res = requests.get(url)
			for val in res.json()['collection']:
				listOfFollowings.append(val['id'])
			url = res.json()['next_href'] + "&client_id={}".format(clientID)
		except:
			pass
		print("Finished searching page")




def follow(idVal):
	headers = {
		'Pragma': 'no-cache',
		'Origin': 'https://soundcloud.com',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'en-US,es-US;q=0.8,es;q=0.6,ru-BY;q=0.4,ru;q=0.2,en;q=0.2',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.113 Chrome/60.0.3112.113 Safari/537.36',
		'Content-Type': 'application/json',
		'Accept': 'application/json, text/javascript, */*; q=0.1',
		'Cache-Control': 'no-cache',
		'Authorization': authCode,
		'Connection': 'keep-alive',
		'Referer': 'https://soundcloud.com/',
	}
	sleepTime = round(random.uniform(1.0, 20.0), 2)
	print("Following {} in {} Seconds".format(idVal, sleepTime))
	time.sleep(sleepTime)

	params = (
		('client_id', clientID),
		('app_version', '1525260260'),
		('app_locale', 'en'),
	)

	data = 'null'

	requests.post('https://api-v2.soundcloud.com/me/followings/{}'.format(idVal), headers=headers, params=params, data=data)

if __name__ == '__main__':
	updateCurrentFollowing()
	# Updates list of users that are currently being followed
	updateToFollow(int(raw_input("How many users do you want to follow: ")))
	print len(toFollow)
	for val in toFollow:
		follow(val)


