from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.support import expected_conditions
import pandas as pd
import time
import os

def suorita_haku_tyovoimatoimisto(hakusana, hakusijainti, ilmoitettu, kielletyt_tittelit): #lisäsin kielletyt tittelit
    temp_titteli, temp_tyonantaja, temp_sijainti, temp_linkki = [], [], [], []
    for s in hakusana.split(", "):
        for p in hakusijainti.split(", "):
            url = "https://paikat.te-palvelut.fi/tpt/?searchPhrase=" + s + "&locations=" + p + "&announced=" + ilmoitettu + "&leasing=0&english=false&sort=8"
            options = Options()
            options.add_argument('--headless')
            browser = webdriver.Firefox(options=options, service_log_path=os.devnull)
            browser.get(url)
            time.sleep(2)
            soup_browser = browser.page_source
            soup = BeautifulSoup(soup_browser, 'html.parser')
            if soup.find(class_ = "badge adCount"):
                #tulosten_maara = int(soup.find(class_ = "badge adCount").text)
                #tulokset = soup.findAll('a', attrs={'tabindex': '0'}) #löytää kaikki
                tulokset = soup.findAll('div', class_ = 'list-group-item')
                for tulos in tulokset:
                    #temp_linkki.append("https://paikat.te-palvelut.fi" + tulos.get('href'))
                    aliluokka = tulos.find('a', attrs={'tabindex': '0'}) #linkki on tämän luokan sisässä, mutta .get('href') ei voi laittaa suoraan sen luokan perään.
                    temp_linkki.append("https://paikat.te-palvelut.fi" + aliluokka.get('href'))
                    titteli = tulos.h4.text
                    if titteli in kielletyt_tittelit:#lisäsin tämän
                        continue #lisäsin tämän
                    temp_titteli.append(titteli)
                    temp_tyonantaja.append(tulos.p.span.text.strip().strip("-"))
                    temp_sijainti.append(tulos.p.findChildren()[2].contents[2])
            browser.close()
    tulokset = temp_titteli, temp_tyonantaja, temp_sijainti, temp_linkki
    tulostaulukko = pd.DataFrame(tulokset).transpose()
    tulostaulukko.columns = ['Titteli', 'Työnantaja', 'Sijainti', 'Linkki']
    tulostaulukko = tulostaulukko.drop_duplicates()
    return tulostaulukko;