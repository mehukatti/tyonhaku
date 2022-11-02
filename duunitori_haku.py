from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import math
from datetime import date
import time
from osuvuuden_tarkistus import kieltolista_luku

def duunitoriParse(sana, paikka, a, sivunro):
    url = "https://duunitori.fi/tyopaikat/?haku=" + sana + "&alue=" + paikka + a + "&order_by=date_posted" #a on se, haetaanko myös ilmoituksen tekstistä
    if sivunro > 0:
        url = url + "&sivu=" + str(sivunro)
    #print(url)
    return BeautifulSoup(get(url).text, 'html.parser')

def yhdista_lista_stringiksi(lista, erotin):
    if len(lista)> 1:
        return erotin.join(lista)
    else:
        return ""

def paiva_muoto(y): #jos päivämäärä sisältää vuoden, ei lisätä vuotta. Jos ei sisällä vuotta, lisätään tämä vuosi.
    if len(y) > 6:
        y = y
        #print(y)
    else:
            #jos päivä ei ole vielä mennyt esim. joulukuu, joka pitäisi olla viime vuodelta, pitäisi tämä ottaa huomioon. Nyt ei ota.
        y = y + str(date.today().year)
    y = date(*(time.strptime(y, '%d.%m.%Y')[0:3]))
    return y;

def julkpaiva_laskuri(x): #Tarkistaa, kuinka monen päivän tulokset hakija haluaa nähdä ja muuttaa ne päiviksi. (Työkkärin arvot duunitoriin sopivaksi)
    if x == 0:
        return 150; #Käytännössä ei vanhempia tuloksia
    elif x == 1:
        return 1;
    elif x == 2:
        return 3;
    elif x == 3:
        return 7;

def yhden_sivun_tulokset(sivu, y, kielletyt_tittelit, kielletyt_kategoriat):
    time.sleep(0.01)
    temp_titteli, temp_tyonantaja, temp_sijainti, temp_linkki, temp_julkaistu, temp_kategoria = [], [], [], [], [], []
    if sivu.find('h3', class_= 'm-t-25-on-all m-b-25-on-all text--secondary'):
        pass
    else:
        tulosalue = sivu.find('div', class_ = 'grid-sandbox grid-sandbox--tight-bottom grid-sandbox--tight-top') #uusi
        #tulokset = sivu.find_all('div', class_ = 'grid grid--middle job-box job-box--lg') #vanha
        tulokset = tulosalue.findChildren('div', class_ = 'grid grid--middle job-box job-box--lg')
        paivaraja = julkpaiva_laskuri(y)
        for tulos in tulokset:
            if tulos.findChild(class_ = 'tag tag--secondary'):
                continue
            ilmoitus_paiva = tulos.findChild(class_= 'job-box__job-posted').text
            ilmoitus_paiva = ilmoitus_paiva.split(None, 1)[1]
            koko_julkpaiva = paiva_muoto(ilmoitus_paiva)
            erotus = int((date.today() - koko_julkpaiva).days)
            if erotus < (paivaraja+1):
                #print("julkaisupäivä: " + str(koko_julkpaiva) + " ja päiväraja: " + str(paivaraja+1))
                kategoria = tulos.findChild().get('data-category') #Jos tuloksia, avaa kategorioiden kieltolistan
                #print("kategoria: " + kategoria)
                if kategoria in kielletyt_kategoriat:
                    continue
                titteli = tulos.findChild('div', class_ = 'job-box__content').findChild('h3').text
                #print("titteli: " + titteli)
                if titteli == None: #johtuuko ylimääräiset päivät ilman muita tietoja tästä?
                    print("tittelin pituus on nolla")
                    continue
                #if any(a[i:len(titteli)+i] for a in kielletyt_tittelit for i in range(len(a)-len(titteli)+1) if titteli[i:len(titteli)+i].lower() == a.lower()):
                if any(titteli[i:len(a)+i] for a in kielletyt_tittelit for i in range(len(titteli)-len(a)+1) if titteli[i:len(a)+i].lower() == a.lower()):
                    continue
                temp_julkaistu.append(koko_julkpaiva)
                temp_titteli.append(titteli)
                temp_tyonantaja.append(tulos.findChild().get('data-company'))
                temp_sijainti.append(tulos.findChild(class_ = 'job-box__job-location').text.strip().strip('–').strip().replace('\n',' '))
                temp_linkki.append("duunitori.fi" + tulos.findChild().get('href'))
                temp_kategoria.append(kategoria)
            else:
                break
        #print(pd.DataFrame(temp_titteli))#.transpose())
    return temp_titteli, temp_tyonantaja, temp_sijainti, temp_linkki, temp_julkaistu, temp_kategoria;

def suorita_haku_duunitori(hakusanat, hakusijainti, negaatiot, haku_tekstista, julkpvm):
    temp_titteli, temp_tyonantaja, temp_sijainti, temp_linkki, temp_julkaistu, temp_kategoria, osuvuus = [], [], [], [], [], [], []
    sanatyhteen = yhdista_lista_stringiksi(hakusanat, "%3B")
    paikatyhteen = yhdista_lista_stringiksi(hakusijainti, "%3B")
    soup = duunitoriParse(sanatyhteen, paikatyhteen, haku_tekstista, 0) #tää nyt käy läpi myös niitä sivuja, joissa ei oikeasti ole niin monetta sivua
    tuloksien_maara = int(soup.find(class_ = "m-b-10-on-all text--body text--left text--center-desk").b.text)
    #duuniutori.fi on päivittänyt sivujaan
    #tuloksien_maara = int(soup.find(class_ = "heading__small").b.text)
    if tuloksien_maara > 0:
        kielletyt_kategoriat = kieltolista_luku()
        sivumaara = math.ceil(tuloksien_maara/20)
        if sivumaara > 5: #Jos valittu kaikki tulokset tai viikon tulokset ilman hakusanaa tai sijaintia
            sivumaara = 5 # Jos tuloksia on näin paljon, niin voi olla, että jollakin hakusanalla löydettyjä ei ollenkaan käydä läpi, koska max 100.
        for s in hakusanat:
            for p in hakusijainti:
                for n in range(1, sivumaara + 1):
                    sivu_titteli, sivu_tyonantaja, sivu_sijainti, sivu_linkki, sivu_julkaistu, sivu_kategoria = yhden_sivun_tulokset(duunitoriParse(s, p, haku_tekstista, n), julkpvm, negaatiot, kielletyt_kategoriat) #negaatiot on siihen kenttään syötetyt sanat, kieltolistassa on kielletyt kategoriat
                    temp_titteli, temp_tyonantaja = temp_titteli + sivu_titteli, temp_tyonantaja + sivu_tyonantaja
                    temp_sijainti = temp_sijainti + sivu_sijainti
                    temp_linkki = temp_linkki + sivu_linkki
                    temp_julkaistu = temp_julkaistu + sivu_julkaistu
                    temp_kategoria = temp_kategoria + sivu_kategoria
        tulokset = temp_titteli, temp_tyonantaja, temp_sijainti, temp_linkki, temp_julkaistu, temp_kategoria, osuvuus
        tulostaulukko = pd.DataFrame(tulokset).transpose()
        tulostaulukko.columns = ['Titteli', 'Työnantaja', 'Sijainti', 'Linkki', 'Julkaistu', 'Kategoria', 'Osuvuus']
        tulostaulukko = tulostaulukko.drop_duplicates()
        return tulostaulukko;
    else:
        return pd.DataFrame();