import os
import requests
from requests import get
import re
import bs4
from bs4 import BeautifulSoup

url = 'https://duunitori.fi/tyopaikat/?haku=Bio&alue=Pirkanmaa'
response = get(url)
soup = BeautifulSoup(response.text, 'html.parser')

#https://www.dataquest.io/blog/web-scraping-beautifulsoup/
linkit = soup.find_all('a', class_ = 'job-box__hover gtm-search-result')
print(len(linkit))

for linkki in linkit:
    print(linkki.get('href'))

