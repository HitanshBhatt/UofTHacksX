'''
    Created by: Hitansh Bhatt
    Program to scrape the UofT Mental Health Resources Website
'''

import requests
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen

init_URL = 'https://mentalhealth.utoronto.ca/find-support-and-services/'

req = Request(init_URL, headers = {'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

'''page = requests.get(init_URL)
print(page.status_code) #print status code for debugging purposes

if (page.status_code == 200):
'''
soup = bs(webpage, "html.parser")
data = soup.get_text()

#store extracted data into resource.txt file
fileObject = open("resource.txt", "w")
fileObject.write(data)