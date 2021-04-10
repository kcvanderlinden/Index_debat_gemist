# Indexing Debates
>Indexing information from search results from https://debatgemist.tweedekamer.nl to a csv or Excel dataset.

---

### Table of Contents

- [The project](#The-project)
- [How To Use](#How-can-I-use-this-project?)
- [References](#references)
- [Author Info](#author-info)

---

## The project

### What is this project about?
This project is about scraping data from debates in ‘de Tweede Kamer’ (the Dutch Parliament/ House of Representatives). This is done by utilising the search option from the website [‘Debat Gemist – Tweede Kamer’]( https://debatgemist.tweedekamer.nl/zoeken?search_api_views_fulltext=). By inserting a search term in the python script, the code scrapes the data (only of which is asked for in the code) from the debates which are found through the search query of website itself. The results are exported to a .csv file by which the data can be analysed by a data scientist. 
The scraping of data is achieved by utilising a Python library named BeautifulSoup.

### Why did I start this project?
I did my Bachelor Thesis on the quantitative relation of transparency and accountability in the European Parliament. For my research I made use of a somewhat recent [database](https://linkedpolitics.project.cwi.nl/web/html/home.html) of all the debates linked to the information of the members of parliament. This database was accessible through SPARQL, which is, if I am not mistaken, a relational database language. While I, a gamma student of Public Administration, had some knowhow on programming, my tutor didn’t. When I told him about the database, he was very enthusiastic about the scope of data hidden in the database, but was turned-off by the required programming experience. 
This, and my spare time through the Coronavirus, motivated me to start this project. I wanted to make the available data of the House of Representatives (Tweede Kamer) easily accessible for data scientist. Most students I know, sociologists and of Public Administration, do have experience with tools like SPSS, but do not have any experience with programming languages as Python. So, through my desire to make more data accessible for research, I set out on this journey.

### For who is this project meant?
Any data enthusiast who speaks/reads Dutch can thinker with the data retrieved by running the code. A dataset as .csv is retrieved, which then can be imported to well-known applications like SPSS. However, the main focus for this project is on data research (quantitative or qualitative) about the House of Representatives (Tweede Kamer). So, anyone who wants easy access to the debates in the Dutch House of Representatives, can utilise this code. Moreover, this project is also about showing the possibility of creating such a tool for any parliament with open access to its debates.

### How can I use this project?
At this stage, you can run the code by inserting a search term within the Python file and running it with the program Python. The variable ‘Searchterm’ is already defined, so you only have to change the word between quotation marks. 
In the future, I am planning to write a more sophisticated guide on how to setup Python and the necessary libraries. 

```python
    Searchterm = "bier" #I like to use "bier" as my test search term
```

---

## References
- [LinkedEP](https://linkedpolitics.project.cwi.nl/web/html/home.html), for the usage in my Bachelor Thesis and thus prompting the idea of this project.
- [Phil Gorman](https://towardsdatascience.com/scraping-hansard-with-python-and-beautifulsoup-f2887f0bc937) on [towards data science](https://towardsdatascience.com/) for his tutorial on how he did a similar project only with data from the Parliament in the United Kingdom.
- [They Work For Us](https://www.theyworkforyou.com/) for inspiration.


---


## Author Info

- Twitter 	- [@linden_karel](https://twitter.com/linden_karel)
- LinkedIn 	- [Karel van der Linden](https://www.linkedin.com/in/karel-van-der-linden-aa313514b/)


[Back To The Top](#read-me-template)
