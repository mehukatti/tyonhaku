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
    if len(hakusana) > 1: hakusana.replace(" ", "%3B")
    if len(hakusijainti)> 1: hakusijainti.replace(" ", "%3B")
    soup = BeautifulSoup(get("https://duunitori.fi/tyopaikat/?haku=" + hakusana + "&alue=" + hakusijainti + haku_tekstista + "&order_by=date_posted").text, 'html.parser')
    tuloksien_maara = int(soup.find(class_ = "heading__small").b.text)
    tulostaulukko = pd.DataFrame()
    if tuloksien_maara == 0:
        return tulostaulukko, False;
    else:
        sivumaara = math.ceil(tuloksien_maara/20)
        if sivumaara > 5 and (x == 0 or (x == 3 and (hakusana == "" or hakusijainti == ""))): #Jos valittu kaikki tulokset tai viikon tulokset ilman hakusanaa tai sijaintia
            sivumaara, Onko_yli_sata = 5, True
            if len(hakusana.split("%3B")) > 1 or len(hakusijainti.split("%3B")) > 1:
                print("on yli 1")
                hakusana.replace("%3B", " ")
                hakusijainti.replace("%3B", " ")
                #search_separately_without_duplicates()
        for s in hakusana.split(" "):
            for p in hakusijainti.split(" "):
                for n in range(1, sivumaara + 1):
                    osataulukko = yhden_sivun_tulokset(("https://duunitori.fi/tyopaikat/?haku=" + hakusana + "&alue=" + hakusijainti + haku_tekstista + "&order_by=date_posted" + "&sivu=" + str(n)), x)
                    tulostaulukko = tulostaulukko.append(osataulukko, ignore_index = True)
                    tulostaulukko = tulostaulukko.drop_duplicates()
        return tulostaulukko, Onko_yli_sata;
