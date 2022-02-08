import os
import requests
from requests import get
import re
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import math
import tkinter as tk
import time

start_time = time.time()

def sijainnin_putsaus(x):
    return x.text.strip().strip('–').strip();

def yhden_sivun_tulokset(url):
    osatulokset = pd.DataFrame(columns = ['Titteli', 'Työnantaja', 'Sijainti', 'Linkki'])
    soup = BeautifulSoup(get(url).text, 'html.parser')
    tulokset = soup.find_all('div', class_ = 'grid grid--middle job-box job-box--lg')
    for tulos in tulokset:
        if tulos.findChild('div', class_ = 'job-box__content').findChild(class_ = 'tag tag--secondary'):
            continue
        titteli = tulos.findChild('div', class_ = 'job-box__content').findChild('h3').text
        tyonantaja = tulos.findChild().get('data-company')
        sijainti = sijainnin_putsaus(tulos.findChild('div', class_ = 'job-box__content').findChild(class_ = 'job-box__job-location'))
        linkki ="duunitori.fi" + tulos.findChild().get('href')
        osatulokset = osatulokset.append({'Titteli' : titteli, 'Työnantaja' : tyonantaja, 'Sijainti' : sijainti, 'Linkki' : linkki}, ignore_index = True)
    return osatulokset;

def suorita_haku_duunitori(hakusana, hakusijainti):
    soup = BeautifulSoup(get("https://duunitori.fi/tyopaikat/?haku=" + hakusana + "&alue=" + hakusijainti).text, 'html.parser')
    tuloksien_maara = int(soup.find(class_ = "heading__small").b.text)
    tulostaulukko = pd.DataFrame()
    if tuloksien_maara == 0:
        return tulostaulukko, tuloksien_maara; #miksi tää ei palauta tyhjää taulukkoa ja falsee?
    else:
        sivumaara = math.ceil(tuloksien_maara/20)
        for n in range(1, sivumaara + 1):
            tulostaulukko = tulostaulukko.append(yhden_sivun_tulokset("https://duunitori.fi/tyopaikat/?haku=" + hakusana + "&alue=" + hakusijainti + "&order_by=date_posted" + "&sivu=" + str(n)), ignore_index = True)
            if tuloksien_maara<100:
                break

        
    return tulostaulukko, tuloksien_maara;
