from bs4 import BeautifulSoup
import requests
import html
import urllib
import pandas as pd

cols = ['onderwerp', 'uitspraak']
data = pd.DataFrame(columns = cols)

Searchterm = 'voetbal'

for i in range(1,25):
    url = "https://debatgemist.tweedekamer.nl/zoeken?search_api_views_fulltext=voetbal&page=" + str(i)
    rall = requests.get(url)
    r = rall.content
    soup = BeautifulSoup(r,"lxml")
    debatten = soup.find_all('div', class_="data")
    for debat in debatten:
        onderwerp = debat.div.h2.text
        gesproken = debat.find_all('li') #('div', class_='list-overview atblock__panel')
        for g in gesproken:
            uitspraak = g.text
            data = data.append({'onderwerp': onderwerp, 'uitspraak': uitspraak},ignore_index=True)
            
match = soup.title.text
print(match)

data[::]