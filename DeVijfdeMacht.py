from bs4 import BeautifulSoup
import requests
import html
import pandas as pd
import csv
from datetime import datetime
from datetime import timedelta
import re

#Version 5.2

print("What is the word you want to search?")
Searchterm = input() #Searchterm
print("How many pages do you want to scrape?")
c_pages = int(input()) #How many pages you want to search through

begin_time = datetime.now()

cols = ['Date', 'Name', 'Party', 'Function', 'Statement', 'Debate_Subject', 'Type_of_debate', 'Particular_committee', 'Speaker', 'URL', 'ID']
data = pd.DataFrame(columns = cols)

count, prev_name, prev_url, statement_start_prev = 0, "", "", 0

#The function of a minister or secretary is written per name in  different dataset, because it couldn't be easilly retrieved from the webpages. 
Minis = pd.read_excel('Ministers.xlsx').fillna(begin_time)

#The range stands for the number of pages counting from 0 you want to scrape from the search result.
for i in range(0, c_pages): 
    url = "https://debatgemist.tweedekamer.nl/zoeken?search_api_views_fulltext=" + Searchterm + "&page=" + str(i)
    soup = BeautifulSoup(requests.get(url).content, "lxml") #This is initially where the pages are being loaded.
    debates = soup.find_all('div', class_="data")
    
    print("Reading page", i + 1, "of", c_pages)
    
    #Here we grab every piece in the html where a debate is listed wherein the search term is found by the site.    
    for debate in debates:
        debate_sub = debate.div.h2.text
        found_statements = debate.find_all('li')
        count = count + 1
        
        #Here we grab every particilar statement from a politician within the listed debates.
        for s in found_statements:
            s_url = s.a['href']
            statement_start = int(re.split('\W', s_url)[-1])
            
            #Because within the text, the name of the politician its party he/she is part of and the statement is written, we have to divide it up so we can correctly archive.
            spl_statement = re.split('[\W](?<!\d)[.,](?!\d)', re.sub('\s+', " ", s.text))
            spl_party = re.split('\s|(?<!\d)[.](?!\d)', spl_statement[0])
            party = spl_party[-1]
            
            if party == '-':
                name = " ".join(spl_party[1:-1])
            else:
                name = " ".join(spl_party[1:-2])
                function = 'Kamerlid'
            
            #Because spoken text is split, we want to re-unite it when it belongs together. This also saves time by not having to open a webpage to search for info already found.
            time_difference = statement_start - statement_start_prev
            
            if 10 >= time_difference > 0 and name == prev_name and 'debatten' in s_url:
                statement = statement + spl_statement[-3]
                data.iloc[-1,4] = statement
                statement_start_prev = statement_start
                prev_name, prev_url = name, url
            
            elif 'debatten' in s_url:
                statement = spl_statement[-3]
                prev_name, prev_url, statement_start_prev = name, url, statement_start    
                    
                #Because there is some data that is only written on the site of the actual debate itself, we can load that site and grab info from there.
                #So we start a new instance of loading pages and load the particular debate.
                st_soup = BeautifulSoup(requests.get(s_url).content,"lxml")
                date = re.split('\W', st_soup.find('div',class_="meta").time['datetime'])
                part_find = st_soup.find('div',class_="meta")
                date_f = datetime(int(date[0]), int(date[1]), int(date[2]))
                date_strf = date_f.strftime("%b %d %Y")
                deb_and_com = part_find.find_all('span')
                typ_deb = deb_and_com[-1].text
                typ_com = deb_and_com[0].text
                speaker = st_soup.find_all('option')[1].text
                time = re.split('\W', st_soup.find_all("label", class_="option")[1].text)
                ident_num = ''.join(date[0:3]) + '-' + ''.join(time[6:8]) + ''.join(time[10:12])
                statement_time = str(timedelta(seconds=statement_start) + timedelta(hours=int(time[6]), minutes=int(time[7])))
                if typ_com == typ_deb:
                    typ_com = 'Not a particular committee'
                function = Minis.loc[(Minis['Name'] == name) & (Minis['start_date'] < date_f) & (Minis.end_date > date_f)].Function.to_string(index=False)
                if function == 'Series([], )':
                    function = 'Kamerlid'

                data = data.append({'Date': date_strf, 'Name': name, 'Party': party, 'Function': function, 'Statement': statement, 'Debate_Subject': debate_sub, 'Speaker': speaker, 'Type_of_debate': typ_deb, 'Particular_committee': typ_com, 'URL': s_url, 'ID': ident_num},ignore_index=True)

end_time = datetime.now()
completion_time = end_time - begin_time
current_time = end_time.strftime("%d%m%Y-%H%M")

#Ultimatly, we want to analyse the data. So to make things easier, we automatically write the data to a .csv file
#Write_xlsx = data.to_excel(Searchterm + '-' + current_time + '.xlsx')
Write_csv = data.to_csv(Searchterm + '-' + current_time + '.csv')

print("It took me", completion_time, "to search for", Searchterm, "on", c_pages, "page(s).")