import os
#import requests
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

def suorita_haku_tyovoimatoimisto(hakusana, hakusijainti, ilmoitettu):
    url = "https://paikat.te-palvelut.fi/tpt/?searchPhrase=" + hakusana + "&locations=" + hakusijainti + "&announced=" + ilmoitettu + "&leasing=0&english=false&sort=8"
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Firefox(options=options)
    browser.get(url)
    time.sleep(2)
    soup_browser = browser.page_source
    soup = BeautifulSoup(soup_browser, 'html.parser')
    tulostaulukko = pd.DataFrame(columns = ['Titteli', 'Työnantaja', 'Sijainti', 'Linkki', 'Julkaistu'])
    Onko_yli_sata = False
    Liikaa_tuloksia = False
    if soup.find('div', class_ = "col-xs-12 noresults"):
        Liikaa_tuloksia = True
    if soup.find(class_ = "badge adCount"):
        tulosten_maara = int(soup.find(class_ = "badge adCount").text)
        if tulosten_maara > 100:
            Onko_yli_sata = True
        tulokset = soup.findAll('a', attrs={'tabindex': '0'})
        for tulos in tulokset:
            if not tulos.get('href'):
                continue
            linkki ="https://paikat.te-palvelut.fi" + tulos.get('href')
            titteli = tulos.h5.text
            tyonantaja = tulos.p.span.text.strip().strip("-")
            sijainti = tulos.p.findChildren()[2].contents[2]
            tulostaulukko = tulostaulukko.append({'Titteli' : titteli, 'Työnantaja' : tyonantaja, 'Sijainti' : sijainti, 'Linkki' : linkki}, ignore_index = True)
    browser.close()
    return tulostaulukko, Onko_yli_sata, Liikaa_tuloksia;

