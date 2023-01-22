import re
import json
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def cleanText(s):
    return re.sub(r'\s+', ' ', s.strip())


URL = 'https://wellness.mcmaster.ca/crisis-support/'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

if page.status_code == 200:
    data = []
  
    soup = BeautifulSoup(page.content, "html.parser")
    section = soup.find('section', attrs={"class": "thumbnail-cards white my-5"})
    
    titles = section.find_all('h3', attrs={"class": "card-title"})
    descriptions = section.find_all('div', attrs={"class": "card-text mb-0"})
    links = section.find_all('a', href=True)

    store_data = []
    
    fileObject = open("../data/mcmaster.json", "w")
    # fileObject = open ("mcmaster.txt", "w")
    for i in range(len(titles)):
        store_data.append({'source': 'mcmaster',
                            'name': cleanText(titles[i].text.replace("More Info", '')),
                            'description': cleanText(descriptions[i].text),
                            'link': cleanText(links[i]['href'])})
    
fileObject.write(json.dumps(store_data, indent=4))    