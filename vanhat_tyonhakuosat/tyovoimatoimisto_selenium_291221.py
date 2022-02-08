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

def suorita_haku_tyovoimatoimisto(hakusana, hakusijainti, ilmoitettu):
    temp_titteli, temp_tyonantaja, temp_sijainti, temp_linkki = [], [], [], []
    for s in hakusana.split(" "):
        for p in hakusijainti.split(" "):
            url = "https://paikat.te-palvelut.fi/tpt/?searchPhrase=" + s + "&locations=" + p + "&announced=" + ilmoitettu + "&leasing=0&english=false&sort=8"
            options = Options()
            options.add_argument('--headless')
            browser = webdriver.Firefox(options=options)
            browser.get(url)
            time.sleep(2)
            soup_browser = browser.page_source
            soup = BeautifulSoup(soup_browser, 'html.parser')
            if soup.find(class_ = "badge adCount"):
                print(soup.find('div', class_ = 'list-group-item'))
                #tulosten_maara = int(soup.find(class_ = "badge adCount").text)
                tulokset = soup.findAll('a', attrs={'tabindex': '0'}) #löytää kaikki
                for tulos in tulokset:
                    if not tulos.get('href'): #työkkärin sivuilla on myös muuta kuin työnhakutuloksia saman nimisen luokan alla, joten, jos lapsissa ei ole linkkiä, se ei ole hakutulos.
                        continue
                    temp_linkki.append("https://paikat.te-palvelut.fi" + tulos.get('href'))
                    temp_titteli.append(tulos.h4.text)
                    temp_tyonantaja.append(tulos.p.span.text.strip().strip("-"))
                    temp_sijainti.append(tulos.p.findChildren()[2].contents[2])
            browser.close()
    tulokset = temp_titteli, temp_tyonantaja, temp_sijainti, temp_linkki
    tulostaulukko = pd.DataFrame(tulokset).transpose()
    tulostaulukko.columns = ['Titteli', 'Työnantaja', 'Sijainti', 'Linkki']
    tulostaulukko = tulostaulukko.drop_duplicates()
    return tulostaulukko;