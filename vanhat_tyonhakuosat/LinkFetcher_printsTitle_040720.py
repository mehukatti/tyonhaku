import os
import requests
from requests import get
import re
from bs4 import BeautifulSoup
import csv
import pandas as pd
import duunitori_haku

hakusanat = pd.read_csv("searchLinks_Duunitori.csv").Hakusanat
tulostaulukko = pd.DataFrame(columns = ['Titteli', 'Työnantaja', 'Sijainti', 'Linkki'])

for hakusana in hakusanat:
    #jotain.to_excel(r'Duunitori_hakutulokset.xlsx', index = False)
    #jokaisella hakusanalla, pitäisi suorittaa vastaava haku.
    #mitä jos vain rakentaisin linkit tässä ja syöttäisin ne sitten metodiin?

fetchedLinks = pd.read_csv("searchLinks_Duunitori.csv").Linkit #hakee "Linkit" nimisestä sarakkeesta

#Lisätäänkö taulukkoon hakusana välilehden nimeksi?

for links in fetchedLinks:
    #r = requests.get(links.strip())
    #soup = BeautifulSoup(r.text, 'html.parser')
    suorita_haku(soup) # tämä palauttaa tulostaulukon
    #print(soup.head.title)
    tulostaulukko.to_excel(r'Duunitori_hakutulokset.xlsx', index = False)
    #Haluan joka hakusanan tulokset eri välilehdelle
