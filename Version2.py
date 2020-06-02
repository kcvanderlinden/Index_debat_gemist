Searchterm = 'bier'

begin_time = datetime.now()

cols = ['Date', 'Name', 'Party', 'Statement', 'Debate Subject', 'Type of debate', 'Particular committee', 'URL']
data = pd.DataFrame(columns = cols)

count = 0

#The range stands for the number of pages counting from 0 you want to scrape from the search result.
for i in range(0,100): 
    url = "https://debatgemist.tweedekamer.nl/zoeken?search_api_views_fulltext=" + Searchterm + "&page=" + str(i)
    rall = requests.get(url)
    r = rall.content
    soup = BeautifulSoup(r,"lxml") #This is initially where the pages are being loaded.
    debates = soup.find_all('div', class_="data")
    
    #Here we grab every piece in the html where a debate is listed wherein the search term is found by the site.    
    for debate in debates:
        debate_sub = debate.div.h2.text
        found_statements = debate.find_all('li')
        count = count + 1
        
        #Here we grab every particilar statement from a politician within the listed debates.
        for s in found_statements:
            s_url = s.a
            s_url = s_url['href']
            
            #Because within the text, the name of the politician its party he/she is part of and the statement is written, we have to divide it up so we can correctly archive.
            unformatted_statement = s.text
            statement = re.sub('\s+', " ", unformatted_statement)
            to_split = re.split('[\W](?<!\d)[.,](?!\d)', statement)
            statement = to_split[-3]
            to_split = re.split('\s|(?<!\d)[.](?!\d)', to_split[0])
            party = to_split[-1]
            if party == '-':
                name = to_split[1:-1]
                name = " ".join(name)
            else:
                name = to_split[1:-2]
                name = " ".join(name)
            
            #Because there is some data that is only written on the site of the actual debate itself, we can load that site and grab info from there.
            #So we start a new instance of loading pages and load the particular debate.
            if 'debatten' in s_url:
                statement_url = requests.get(s_url)
                st_url = statement_url.content
                st_soup = BeautifulSoup(st_url,"lxml")
                part_find = st_soup.find('div',class_="meta")
                date = part_find.time.text   
                deb_and_com = part_find.find_all('span')
                typ_deb = deb_and_com[-1].text
                typ_com = deb_and_com[0].text
                if typ_com == typ_deb:
                    typ_com = 'Not a particular committee'
            
                data = data.append({'Date': date, 'Name': name, 'Party': party, 'Statement': statement, 'Debate Subject': debate_sub, 'Type of debate': typ_deb, 'Particular committee': typ_com, 'URL': s_url},ignore_index=True)
            

end_time = datetime.now()
completion_time = end_time - begin_time
current_time = end_time.strftime("%d%m%Y-%H%M")

#Ultimatly, we want to analyse the data. So to make things easier, we automatically write the data to a .csv file
Name_file = Searchterm + '-' + current_time + '.csv'
Write_csv = data.to_csv(Name_file)

match = soup.title.text
print(match)
print(completion_time)