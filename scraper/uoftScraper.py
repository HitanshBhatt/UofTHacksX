'''
    Created by: Hitansh Bhatt
    Program to scrape the UofT Mental Health Resources Website
'''

import re
import json
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen


def getUrl(i):
    return 'https://mentalhealth.utoronto.ca/?sfid=205&sf_action=get_data&sf_data=results&sf_paged={}&lang=en'.format(i)


def cleanText(s):
    return re.sub(r'\s+', ' ', s.strip())


fileObject = open("../data/uoft.json", "w")

# fileObject.write(data)
store_data = []

for num in range(1, 11):
    init_URL = getUrl(num)
    req = Request(init_URL, headers={'User-Agent': 'Mozilla/5.0'})
    res = urlopen(req).read()
    webpage = json.loads(res)["results"]

    '''page = requests.get(init_URL)
    print(page.status_code) #print status code for debugging purposes

    if (page.status_code == 200):
    '''
    soup = bs(webpage, "html.parser")
    # data = soup.get_text()

    results = soup.find_all(attrs={"class": "row service-item"})

    # print(service_titles)

    # print(service_titles)
    for result in results:
        title = cleanText(result.find('h3').text)
        location = cleanText(result.find('div', class_='service-info').text)
        description = cleanText(result.find('div', class_='service-desc').text)
        link = cleanText(result.find('a')['href'])
        store_data.append({'source': 'uoft', 'name': title, 'location': location,
                          'description': description, 'link': link})

fileObject.write(json.dumps(store_data, indent=4))
