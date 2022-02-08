import os
import requests
from requests import get
import re
import bs4 as bs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions
import pandas as pd
import time

url = "https://paikat.te-palvelut.fi/tpt/"
options = Options()
#options.add_argument('--headless')
browser = webdriver.Firefox(options=options)
browser.get(url)
#hae ammattinappi
browser.find_element(By.ID, 'ammattialaDialogLink').click()
time.sleep(2)
ylätasot = browser.find_elements(By.CLASS_NAME, 'col-xs-8')
ylä_maara = len(ylätasot)
for taso in ylätasot:
    print(taso.text)
    print(taso)
    taso.click() #kun tämä on avattuna, ei pysty iteroimaan muita tuloksia läpi. pitäisi tehdä metodi, jossa käy läpi kaikki sisimmätkin valinnat
    time.sleep(2)
    print(taso)
    taso.find_element(By.XPATH, '//*[@id="ammattialaDialog"]/div/tpt-ammattiala-breadcrumb/div/div/div[2]/div/ul/li[1]/div/div[2]/div[1]')
    for a in taso:
        print(a.text)
        time.sleep(2)
    time.sleep(10)
    break
#soup_browser = browser.page_source
#soup = BeautifulSoup(soup_browser, 'html.parser')
#browser.close()