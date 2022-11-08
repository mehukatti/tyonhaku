from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
import os

def suorita_haku_tyovoimatoimisto(hakusana, hakusijainti, ilmoitettu, kielletyt_tittelit): #lisäsin kielletyt tittelit
    #tyhjät listat yksittäisen haun tuloksille.
    temp_titteli, temp_tyonantaja, temp_sijainti, temp_linkki = [], [], [], []

    #haku suoritetaan niin monta kertaa kuin hakusanoja ja sijaintejakin on
    for s in hakusana.split(", "):
        for p in hakusijainti.split(", "):
            url = "https://paikat.te-palvelut.fi/tpt/?searchPhrase=" + s + "&locations=" + p + "&announced=" + ilmoitettu + "&leasing=0&english=false&sort=8"
            options = Options()
            options.add_argument('--headless') #automatisoitua selainta ei näy.
            browser = webdriver.Firefox(options=options, service_log_path=os.devnull)
            browser.get(url)
            time.sleep(2)

            #Parse beautifoulsoupiksi, koska aloittaessani en osannut käyttää Seleniumin XPATH:ia.
            #En ole muuttanut, koska tämä toimii vielä.

            soup_browser = browser.page_source
            soup = BeautifulSoup(soup_browser, 'html.parser')

            #Kun selain on parsittu bs:ksi, suljetaan selain.
            #Muuten ei sulkeudu, jos sivun html on päivitetty eikä työpaikan tiedot enää löydy samoista paikoista.
            browser.close()

            if soup.find(class_ = "badge adCount"): #badgecountissa on hakutuloksien määrä.
                tulokset = soup.findAll('div', class_ = 'list-group-item')
                for tulos in tulokset:
                    aliluokka = tulos.find('a', attrs={'tabindex': '0'}) #linkki on tämän luokan sisässä, mutta .get('href') ei voi laittaa suoraan sen luokan perään.
                    temp_linkki.append("https://paikat.te-palvelut.fi" + aliluokka.get('href'))
                    titteli = tulos.h4.text
                    if titteli in kielletyt_tittelit:
                        continue

                    #lisätään yhden paikan tiedot listoille
                    temp_titteli.append(titteli)
                    temp_tyonantaja.append(tulos.p.span.text.strip().strip("-"))
                    temp_sijainti.append(tulos.p.findChildren()[2].contents[2])
            
    
    tulokset = temp_titteli, temp_tyonantaja, temp_sijainti, temp_linkki #listat listalle
    tulostaulukko = pd.DataFrame(tulokset).transpose() #transponoi lista taulukon suuntaiseksi
    tulostaulukko.columns = ['Titteli', 'Työnantaja', 'Sijainti', 'Linkki'] #lisää taulukolle otsikot

    #duplikaatit pitää poistaa, koska hakuja suoritetaan niin monta, kuin on hakusanoja. Sama voi tulla useassa haussa.
    tulostaulukko = tulostaulukko.drop_duplicates()

    return tulostaulukko;
