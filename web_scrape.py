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

for num in range(1,11):
    init_URL = 'https://mentalhealth.utoronto.ca/?sfid=205&sf_action=get_data&sf_data=results&sf_paged='+(str(num))+'&lang=en'

    req = Request(init_URL, headers = {'User-Agent': 'Mozilla/5.0'})
    res = urlopen(req).read()
    webpage = json.loads(res)["results"]
    print(webpage)

    '''page = requests.get(init_URL)
    print(page.status_code) #print status code for debugging purposes

    if (page.status_code == 200):
    '''
    soup = bs(webpage, "html.parser")
    #data = soup.get_text()

    
    #fileObject.write(data)
    store_data = []

    service_titles = soup.find_all('h3')

    #print(service_titles)
    for title in service_titles:
        store_data.append((title.text))
        #print(title.text, title.next_sibling)

    for item in store_data:
        fileObject.write(item + "\n")


