from bs4 import BeautifulSoup
import requests

Searchterm = 'zuipen'
url = 'https://debatgemist.tweedekamer.nl/zoeken?search_api_views_fulltext=' + Searchterm
rall = requests.get(url)
r = rall.content
soup = BeautifulSoup(r,"lxml")

match = soup.title
match

debat = soup.find('li', class_='')
#print(debat)

debat2 = debat.article
debat3 = debat2.find('div', class_="data")
onderwerp = debat3.div.h2.text
print(onderwerp)

gesproken = debat3.div.div.ul.li.text
print(gesproken)