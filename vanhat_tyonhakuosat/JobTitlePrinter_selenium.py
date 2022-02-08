#import docx
#from docx import Document
import os
import requests
from requests import get
import re
from selenium import webdriver                    # Import module 
from selenium.webdriver.common.keys import Keys   # For keyboard keys
from selenium.webdriver.common.by import By
import time                                       # Waiting function  

#doc = docx.Document("C:/pythontestit/Duunitorin_tulokset.docx")
browser = webdriver.Chrome('\pythontestit\vanhat_tyonhakuosat\chromedriver') # Create driver object means open the browser

url = 'https://duunitori.fi/tyopaikat/?haku=Bio&alue=Pirkanmaa'

browser.get(url)
all_trails = []
time.sleep(2) #2

tulokset = browser.find_elements_by_class_name('job-box__hover.gtm-search-result')

for tiedot in tulokset:
    print(tiedot.get_attribute("href"))
    #tiedot = browser.find_element_by_class_name('job-box__hover.gtm-search-result')
    #for linkki in tiedot:
        #print(linkki.get_attribute("href"))
    #tiedot = browser.find_element_by_class_name('job-box__title')
    #print(tiedot.text)
    #for titteli in tiedot:
        #doc.add_paragraph(tiedot.get_attribute("href")+ titteli.text)
        #print(titteli.text)
        #doc.save("C:/pythontestit/Duunitorin_tulokset.docx")

browser.close()
#tämä toimii ja tulostaa kaikki tekstit kaikkien job-box-titlejen sisällä.
#tiedot = browser.find_elements_by_class_name('job-box__title') #toimii
#for titteli in tiedot:
    #print(titteli.text)

#Haluan välttää div containereita, joissa on data-tag-level="Nosto"


