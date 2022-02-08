#import docx
#from docx import Document
import os
import requests
from requests import get
import re
from selenium import webdriver                    # Import module 
from selenium.webdriver.common.keys import Keys   # For keyboard keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
import time                                       # Waiting function  

#doc = docx.Document("C:/pythontestit/Duunitorin_tulokset.docx")
#browser = webdriver.Chrome('\pythontestit\chromedriver') # Create driver object means open the browser
browser = webdriver.Firefox() #'\pythontestit\geckodriver'

url = 'https://duunitori.fi/tyopaikat/?haku=Bio&alue=Pirkanmaa'

browser.get(url)
all_trails = []
time.sleep(2) #2

#def findLink(laatikko):
    #laatikko = browser.find_element_by_class_name('job-box__hover.gtm-search-result').get_attribute("href")
    #print("Tämä on funktion tulos:" + laatikko)
    #return laatikko;

#tulokset = browser.find_elements_by_class_name('grid.grid--middle.job-box.job-box--lg')

tulokset = browser.find_elements_by_css_selector('div.grid.grid--middle.job-box.job-box--lg')
print(len(tulokset))

for tiedot in tulokset:
    #tiedot.find_element_by_class_name('job-box__hover.gtm-search-result')
    #tiedot.find_element_by_css_selector('a.job-box__hover.gtm-search-result')
    #https://stackoverflow.com/questions/14049983/selenium-webdriver-finding-an-element-in-a-sub-element
    print(tiedot.text) #tulostaa job-box contentin tiedot
    print(tiedot.get_attribute("href"))

browser.close()

#Haluan välttää div containereita, joissa on data-tag-level="Nosto"


