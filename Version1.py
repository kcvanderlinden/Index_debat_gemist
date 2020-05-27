from bs4 import BeautifulSoup
import requests
import html
import pandas as pd
import csv
from datetime import datetime
import re

Searchterm = 'bier'

now = datetime.now()
current_time = now.strftime("%d%m%Y-%H%M")

cols = ['Date', 'Debate Subject', 'Statement', 'URL']
data = pd.DataFrame(columns = cols)

count = 0

for i in range(0,2): #Hoe veel pagina's je wilt doorzoeken. Per pagina worden er op debatgemist.tweedekamer.nl 10 debatten laten zien.
    url = "https://debatgemist.tweedekamer.nl/zoeken?search_api_views_fulltext=" + Searchterm + "&page=" + str(i)
    rall = requests.get(url)
    r = rall.content
    soup = BeautifulSoup(r,"lxml") #Open de pagina's in BeautifulSoup voor webscraping.
    debates = soup.find_all('div', class_="data")
    for debate in debates:
        debate_sub = debate.div.h2.text
        found_statements = debate.find_all('li')
        count = count + 1
        #list_url = []
        for s in found_statements:
            s_url = s.a
            s_url = s_url['href']
            unformatted_statement = s.text
            statement = re.sub('\s+', " ", unformatted_statement)
            
            statement_url = requests.get(s_url)
            st_url = statement_url.content
            st_soup = BeautifulSoup(st_url,"lxml")
            date = st_soup.find('div',class_="meta")
            date = date.time.text
            
            data = data.append({'Date': date, 'Debate Subject': debate_sub, 'Statement': statement, 'URL': s_url},ignore_index=True)
            
Name_file = Searchterm + '-' +current_time + '.csv'
Write_csv = data.to_csv(Name_file) #Schrijf de rijen naar een .csv bestand om daarna te kunnen analyseren.

match = soup.title.text
print(match)
