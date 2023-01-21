import re
import json
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen

URL = 'https://studentlife.ontariotechu.ca/current-students/health-and-wellness/mental-health-services/resources-and-self-help/helpful-links.php'
FILE = '../data/ontariotech.json'

def cleanText(s):
    return re.sub(r'\s+', ' ', s.strip())

store_data = []

res = urlopen(Request(URL))
webpage = res.read()

soup = bs(webpage, "html.parser")

content = soup.find('section', id='page-content')

for accord in content.find_all('ul', type='disc'):
    for element in content.find_all('li'):
        link_element = element.find('a')
        title = cleanText(link_element.text)
        description = cleanText(element.text)
        link = cleanText(link_element['href'])
        store_data.append({'source': 'ontario-tech', 'name': title,
                    'description': description, 'link': link})

with open(FILE, 'w') as f:
    json.dump(store_data, f, indent=4)