from bs4 import BeautifulSoup
import requests
import html
import pandas as pd
import csv
from datetime import datetime
from datetime import timedelta
import re

## Current version

Searchterm = 'bier'

begin_time = datetime.now()

cols = ['Date', 'Name', 'Party', 'Function', 'Statement', 'Debate Subject', 'Type of debate', 'Particular committee', 'Speaker', 'URL', 'ID']
data = pd.DataFrame(columns = cols)

count = 0

#The function of a minister or secretary is written per name in  different dataset, because it couldn't be easilly retrieved from the webpages. 
Minis = pd.read_excel('Ministers.xlsx')

#The range stands for the number of pages counting from 0 you want to scrape from the search result.
for i in range(0,5): 
    url = "https://debatgemist.tweedekamer.nl/zoeken?search_api_views_fulltext=" + Searchterm + "&page=" + str(i)
    soup = BeautifulSoup(requests.get(url).content, "lxml") #This is initially where the pages are being loaded.
    debates = soup.find_all('div', class_="data")
    
    #Here we grab every piece in the html where a debate is listed wherein the search term is found by the site.    
    for debate in debates:
        debate_sub = debate.div.h2.text
        found_statements = debate.find_all('li')
        count = count + 1
        
        #Here we grab every particilar statement from a politician within the listed debates.
        for s in found_statements:
            s_url = s.a['href']
            
            #Because within the text, the name of the politician its party he/she is part of and the statement is written, we have to divide it up so we can correctly archive.
            to_split = re.split('[\W](?<!\d)[.,](?!\d)', re.sub('\s+', " ", s.text))
            statement = to_split[-3]
            to_split = re.split('\s|(?<!\d)[.](?!\d)', to_split[0])
            party = to_split[-1]
            
            function = 'Unknown'
            if party == '-':
                name_split = to_split[1:-1]
                name = " ".join(name_split)
                
                for m in Minis['Name']:
                    if name_split[-1] in m:
                        function = Minis.Function[Minis.Name == m].to_string(index=False)
                    else:
                        m = ''
            else:
                name = " ".join(to_split[1:-2])
                function = 'Kamerlid'
            
            #Because there is some data that is only written on the site of the actual debate itself, we can load that site and grab info from there.
            #So we start a new instance of loading pages and load the particular debate.
            if 'debatten' in s_url:
                st_soup = BeautifulSoup(requests.get(s_url).content,"lxml")
                date = re.split('\W', st_soup.find('div',class_="meta").time['datetime'])
                part_find = st_soup.find('div',class_="meta")
                date_strf = datetime(int(date[0]), int(date[1]), int(date[2])).strftime("%b %d %Y")
                deb_and_com = part_find.find_all('span')
                typ_deb = deb_and_com[-1].text
                typ_com = deb_and_com[0].text
                speaker = st_soup.find_all('option')[1].text
                time = re.split('\W', st_soup.find_all("label", class_="option")[1].text)
                ident_num = ''.join(date[0:3]) + '-' + ''.join(time[6:8]) + ''.join(time[10:12])
                statement_start = int(re.split('\W', s_url)[-1])
                statement_time = str(timedelta(seconds=start_st) + timedelta(hours=int(time[6]), minutes=int(time[7])))
                if typ_com == typ_deb:
                    typ_com = 'Not a particular committee'
            
                data = data.append({'Date': date_strf, 'Name': name, 'Party': party, 'Function': function, 'Statement': statement, 'Debate Subject': debate_sub, 'Speaker': speaker, 'Type of debate': typ_deb, 'Particular committee': typ_com, 'URL': s_url, 'ID': ident_num},ignore_index=True)
            

end_time = datetime.now()
completion_time = end_time - begin_time
current_time = end_time.strftime("%d%m%Y-%H%M")

#Ultimatly, we want to analyse the data. So to make things easier, we automatically write the data to a .csv file
Name_file = Searchterm + '-' + current_time + '.csv'
Write_csv = data.to_csv(Name_file)

match = soup.title.text
print(match)
print(completion_time)