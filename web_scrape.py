'''
    Created by: Hitansh Bhatt
    Program to scrape the UofT Mental Health Resources Website
'''

import requests
import json
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen

#store extracted data into resource.txt file
fileObject = open("resource.txt", "w")

#fileObject.write(data)
store_data = []

for num in range(1,11):
    init_URL = 'https://mentalhealth.utoronto.ca/?sfid=205&sf_action=get_data&sf_data=results&sf_paged='+(str(num))+'&lang=en'

    req = Request(init_URL, headers = {'User-Agent': 'Mozilla/5.0'})
    res = urlopen(req).read()
    webpage = json.loads(res)["results"]
    #print(webpage)

    '''page = requests.get(init_URL)
    print(page.status_code) #print status code for debugging purposes

    if (page.status_code == 200):
    '''
    soup = bs(webpage, "html.parser")
    #data = soup.get_text()


    results = soup.find_all(attrs ={"class":"row service-item"})

    #print(service_titles)

    #print(service_titles)
    for result in results:
        title = result.find('h3').text
        location = result.find('div', class_='service-info').text
        description = result.find('div', class_='service-desc').text
        link = result.find('a').href
        store_data.append([title, location, description, link])

fileObject.write(json.dumps(store_data, indent=4))
# print(store_data)


