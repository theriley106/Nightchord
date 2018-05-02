import requests
import bs4

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
res = requests.get('https://soundcloud.com/user-367430385/tracks', headers=headers)
page = bs4.BeautifulSoup(res.text, 'lxml')
print page.title.string
