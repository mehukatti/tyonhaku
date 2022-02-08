import os
import requests
from requests import get
import re
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import csv

#luo taulukko
tulostaulukko = pd.DataFrame(columns = ['Titteli', 'Työnantaja', 'Sijainti', 'Linkki'])

def sijainnin_putsaus(x):
    x = x.text.strip().strip('–').strip()
    return x;

#def tulostaulukon_muodostus(x):

def suorita_haku(url):
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser') #jäi kesken. Jokaisella hakusanalla haluan uuden välilehden.
    #Entä, jos hakusanalla ei ole tuloksia?
    if soup.find('span', class_= 'text--nowrap'):
        print("Ei tuloksia hakusanoilla")
    else:
        #tulostaulukon_muodostus(tulokset)
        tulokset = soup.find_all('div', class_ = 'grid grid--middle job-box job-box--lg')
        #lopussa ei aina ole kahta nostoa, voi olla myös yksi
        for tulos in tulokset:
            global tulostaulukko
            titteli = tulos.findChild('div', class_ = 'job-box__content').findChild('h3').text
            tyonantaja = tulos.findChild().get('data-company')
            sijainti = sijainnin_putsaus(tulos.findChild('div', class_ = 'job-box__content').findChild(class_ = 'job-box__job-location'))
            linkki ="duunitori.fi" + tulos.findChild().get('href')
            tulostaulukko = tulostaulukko.append({'Titteli' : titteli, 'Työnantaja' : tyonantaja, 'Sijainti' : sijainti, 'Linkki' : linkki}, ignore_index = True)
            #onko useita sivuja?
        return tulostaulukko; #taulukko ei nollaannu, vaan rivejä lisätään eri hakujen välissä
