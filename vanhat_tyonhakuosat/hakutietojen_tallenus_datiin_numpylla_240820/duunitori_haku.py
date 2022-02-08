import os
import requests
from requests import get
import re
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import math
import datetime
from datetime import date
from datetime import datetime
import time

def julkpaiva_laskuri(x):
    if x == 1:
        return 1;
    elif x == 2:
        return 3;
    elif x == 3:
        return 7;

def yhden_sivun_tulokset(url, y):
    osatulokset = pd.DataFrame(columns = ['Titteli', 'Työnantaja', 'Sijainti', 'Linkki', 'Julkaistu'])
    soup = BeautifulSoup(get(url).text, 'html.parser')
    tulokset = soup.find_all('div', class_ = 'grid grid--middle job-box job-box--lg')
    paivaraja = julkpaiva_laskuri(y)
    if y == 0:
        paivaraja = len(tulokset)
    else:
        paivaraja = julkpaiva_laskuri(y)
    for tulos in tulokset:
        if tulos.findChild(class_ = 'tag tag--secondary'):
            continue
        ilmoitus_paiva = tulos.findChild(class_= 'job-box__job-posted').text
        koko_julkpaiva = date(*(time.strptime(ilmoitus_paiva.split(None, 1)[1] + str(date.today().year), '%d.%m.%Y')[0:3]))
        erotus = int((date.today() - koko_julkpaiva).days)
        if erotus < (paivaraja+1):
            titteli = tulos.findChild('div', class_ = 'job-box__content').findChild('h3').text
            tyonantaja = tulos.findChild().get('data-company')
            sijainti = tulos.findChild(class_ = 'job-box__job-location').text.strip().strip('–').strip().replace('\n',' ')
            linkki ="duunitori.fi" + tulos.findChild().get('href') 
            osatulokset = osatulokset.append({'Titteli' : titteli, 'Työnantaja' : tyonantaja, 'Sijainti' : sijainti, 'Linkki' : linkki, 'Julkaistu' : ilmoitus_paiva}, ignore_index = True)
        else:
            break
    return osatulokset;

def suorita_haku_duunitori(hakusana, hakusijainti, haku_tekstista, x):
    soup = BeautifulSoup(get("https://duunitori.fi/tyopaikat/?haku=" + hakusana + "&alue=" + hakusijainti).text, 'html.parser')
    tuloksien_maara = int(soup.find(class_ = "heading__small").b.text)
    tulostaulukko = pd.DataFrame()
    Onko_yli_sata = False
    if tuloksien_maara == 0:
        return tulostaulukko, Onko_yli_sata;
    else:
        sivumaara = math.ceil(tuloksien_maara/20)
        if sivumaara > 5:
            sivumaara = 5
            Onko_yli_sata = True 
        for n in range(1, sivumaara + 1):
            tulostaulukko = tulostaulukko.append(yhden_sivun_tulokset(("https://duunitori.fi/tyopaikat/?haku=" + hakusana + "&alue=" + hakusijainti + haku_tekstista + "&order_by=date_posted" + "&sivu=" + str(n)), x), ignore_index = True)
    return tulostaulukko, Onko_yli_sata;
