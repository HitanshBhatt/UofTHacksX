import re
import json
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen

URL = 'https://studentlife.ontariotechu.ca/current-students/health-and-wellness/mental-health-services/resources-and-self-help/helpful-links.php'
FILE_LENGTH = 30
file_idx = 1

def get_file_name():
    return '../data/ontariotech-{}.json'.format(file_idx)

def cleanText(s):
    return re.sub(r'\s+', ' ', s.strip())

store_data = []

res = urlopen(Request(URL))
webpage = res.read()
urls = set()

soup = bs(webpage, "html.parser")

content = soup.find('section', id='page-content')

for accord in content.find_all('ul', type='disc'):
    for element in content.find_all('li'):
        link_element = element.find('a')
        title = cleanText(link_element.text)
        description = cleanText(element.text)
        link = cleanText(link_element['href'])
        if 'https://' in link and link not in urls:
            urls.add(link)
            store_data.append({'source': 'ontario-tech', 'name': title,
                        'description': description, 'link': link})
            if len(store_data) > FILE_LENGTH:
                with open(get_file_name(), 'w') as f:
                     json.dump(store_data, f, indent=4)
                     store_data = []
                file_idx+=1
if len(store_data) > 0:
    with open(get_file_name(), 'w') as f:
            json.dump(store_data, f, indent=4)
