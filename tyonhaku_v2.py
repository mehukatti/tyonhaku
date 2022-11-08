import tkinter as tk
from tkinter import *
from duunitori_haku import suorita_haku_duunitori
from tyovoimatoimisto_selenium import suorita_haku_tyovoimatoimisto
import access_files
from osuvuuden_tarkistus import osuvuudet
import time
import pandas as pd
import os

#Fingelskaa. Muutan kaiken suomeksi myöhemmin.
class tyonhaku_sovellus(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.luo_widgetit()
    def luo_widgetit(self):
        canvas = Canvas(self)

        #Ilmoitus tiedostojen sijainnista ja tuloksista
        self.tuloskohta = tk.Label(self.master, text=' ')
        self.tuloskohta.grid(row=5,columnspan=4, pady=5)

        #Tarkistus-nappi haun tarkistuksen jälkeen
        """
        Haluan eroon tästä napista. Tämä tarkistaa, onko tulosexcelissä 1 vai 0 kullakin rivillä.
        Jos se on 0, lisätään kiellettyjen kategorioiden listalle.
        Tämän valinta ei ole hakukohtainen, vaan koskee jokaista hakua.
        Tällä hetkellä kategorioita ei voi valita kuin excelin tai suoraan jsonin kautta.
        """
        self.tarkistus_nappi = Button(self.master, text='Tarkista', command=osuvuudet) 
        self.tarkistus_nappi.grid(row=6,column=3, columnspan=2, padx=5, pady=5)

        #Hakusanat-tekstiruutu
        label1 = tk.Label(self.master, text='Hakusanat', font=('helvetica', 10)).grid(row=1, sticky='w', column=0, padx=5)
        self.hakusana_kentta = tk.Entry(self.master)
        self.hakusana_kentta.grid(row=2, sticky='w', column=0, padx=5)
        
        #Sijainti-tekstiruutu
        label2 = tk.Label(self.master, text='Sijainti', font=('helvetica', 10)).grid(row=1, sticky='w', column=1, padx=5)
        self.sijainti_kentta = tk.Entry(self.master)
        self.sijainti_kentta.grid(row=2, sticky='w', column=1, padx=5)

        #Mutta ei näillä-tekstiruutu
        label3 = tk.Label(self.master, text='Mutta ei näillä titteleillä', font=('helvetica', 10)).grid(row=1, sticky='w', column=3, padx=5)
        self.ei_nailla_titteleilla = tk.Entry(self.master)
        self.ei_nailla_titteleilla.grid(row=2, sticky='w', column=3, padx=5)
        
        #Hakusivujen valintaruudut
        self.duunitori_luku = tk.IntVar()
        self.duunitori_tekstista = tk.StringVar()
        self.tyokkari_luku = tk.IntVar()
        
        self.duunitori = tk.Checkbutton(self.master, text="Duunitori.fi", variable=self.duunitori_luku, onvalue=1, offvalue=0)
        self.tekstista = tk.Checkbutton(self.master, text="Haku myös tekstistä", variable=self.duunitori_tekstista, onvalue="&search_also_descr=1", offvalue="")
        self.tyokkari = tk.Checkbutton(self.master, text="Työvoimatoimisto", variable=self.tyokkari_luku, onvalue=1, offvalue=0)
        
        self.duunitori.grid(row=6,column=0, padx=5)
        self.tekstista.grid(row=7,column=0, padx=5)
        self.tyokkari.grid(row=6,column=1, padx=5)

        #duunitorin kategorioiden valinta
        """
        duunitorin kategorioiden valinta parantaa hakutuloksia, kun hakee esim. bioalalta.
        Tällä hetkellä niiden valinta tehdään lisäämällä tulosexceliin 1 tai 0.
        Ei ole kovin näppärää ja haluaisin lisätä myös sen valinnan.
        Kategorioita on kuitenkin useita ja haluaisin löytää jonkin järkevän monivalinta-vaihtoehdon.
        """
        #tk.Label(self.master, text='Duunitorin kategoriat', font=('helvetica', 10)).grid(row=8, sticky='w', column=0, padx=5)
        #kaikissa on oletuksena 1 eli oletuksena valittu
        self.duunitorin_kategoriat = {
            "asennus, huolto ja puhtaanapito (ala)": 1,
            "asiakaspalvelu (ala)": 1,
            "asiantuntijatyöt ja konsultointi (ala)": 1,
            "hallinto ja yleiset toimistotyöt (ala)": 1,
            "henkilöstöala (ala)": 1,
            "hyvinvointi ja henkilöpalvelut (ala)": 1,
            "johtotehtävät (ala)": 1,
            "julkinen sektori ja järjestöt (ala)": 1,
            "kiinteistöala (ala)": 1,
            "kuljetus, logistiikka ja liikenne (ala)": 1,
            "kulttuuri-, viihde- ja taidealat (ala)": 1,
            "lakiala (ala)": 1,
            "markkinointi (ala)": 1,
            "myynti ja kaupan ala (ala)": 1,
            "opetusala (ala)": 1,
            "opiskelijoiden työpaikat (ala)": 1,
            "rakennusala (ala)": 1,
            "ravintola- ja matkailuala (ala)": 1,
            "sosiaali- ja hoiva-ala (ala)": 1,
            "taloushallinto ja pankkiala (ala)": 1,
            "teollisuus ja teknologia (ala)": 1,
            "terveydenhuoltoala (ala)": 1,
            "tieto- ja tietoliikennetekniikka (ala)": 1,
            "turvallisuusala (ala)": 1,
        }
        
        #Hakujen rajoitus ilmoitusajankohdan mukaan
        self.tyokkari_aika = tk.Label(self.master, text='Julkaistu')
        self.tyokkari_aika.grid(row=8, column=1, sticky='w', pady=5, padx=5)
        self.ilmoitusajan_valinta = tk.IntVar()
        
        self.kaikki = Radiobutton(self.master, text="kaikki", value=0, variable=self.ilmoitusajan_valinta)
        self.vuorokausi = Radiobutton(self.master, text="vuorokausi", value=1, variable=self.ilmoitusajan_valinta)
        self.kolme_paivaa = Radiobutton(self.master, text="3 päivää", value=2, variable=self.ilmoitusajan_valinta)
        self.viikko = Radiobutton(self.master, text="viikko", value=3, variable=self.ilmoitusajan_valinta)
        
        self.kaikki.grid(row=9, column=1, sticky='w', pady=5, padx=5)
        self.vuorokausi.grid(row=10, column=1, sticky='w', pady=5, padx=5)
        self.kolme_paivaa.grid(row=11, column=1, sticky='w', pady=5, padx=5)
        self.viikko.grid(row=12, column=1, sticky='w', pady=5, padx=5)
        
        #Tallenna haku
        self.tallenna = tk.IntVar()
        self.tallenna_haku = tk.Checkbutton(self.master, text="Tallenna, nimellä:", variable=self.tallenna, onvalue=1, offvalue=0)
        self.tallenna_haku.grid(row=13,column=0, padx=5)
        self.nimella_kentta = tk.Entry(self.master)
        self.nimella_kentta.grid(row=14, sticky='w', column=0, padx=5)
        
        #Tallennettu haku
        self.tallennettu_nappi = Button(self.master, text='Tallennettu haku', command=self.select_saved_search)
        self.tallennettu_nappi.grid(row=16,column=1, columnspan=2, padx=5, pady=5)
        
        #Hae-nappi
        self.haku_nappi = Button(self.master, text='Hae', command=self.take_input)
        self.haku_nappi.grid(row=15,column=0, columnspan=2, padx=5)
        #Lopetus-nappi
        self.lopeta_nappi = Button(self.master, text='Lopeta', command=self.master.destroy)
        self.lopeta_nappi.grid(row=15,column=2, padx=5)

        #jos haluat muuttaa tulosexcelin tai tietojen tallennustiedoston nimeä, muuta tästä.
        self.tallennettujen_hakujen_polut = "names_of_saved_param.json" #tänne tallennetaan tallennettujen hakujen nimet 
        self.tulosexcelin_polku = 'Hakutulokset.xlsx' #tänne tallennetaan suoritetun haun tulokset (titteli, paikka, linkki, ilmoituspäivä)

        #jotta voi laskea, kauanko haku kestää
        self.aloitus_aika = None

    def tallenna_GUI_input(self, nimi):
        tallennetut_parametrit = {
            #koska laitoin vain yhden kentän per hakusana ja sijainti, pitää useat hakusanat ja sijainnit erottaa jollakin merkillä.
            "search_words": self.hakusana_kentta.get().split(", "), 
            "locations": self.sijainti_kentta.get().split(", "),
            "duunitori": self.duunitori_luku.get(),
            "tetoimisto": self.tyokkari_luku.get(),
            "published":self.ilmoitusajan_valinta.get(),
            "duunitori_from_text_also": self.duunitori_tekstista.get(),
            "not_with_these_words": self.ei_nailla_titteleilla.get().split(", ")
        }
        #tallennetaan hakutekijät omalla nimellä yhteen tiedostoon
        access_files.write_data_to_json_with(tallennetut_parametrit, nimi + '.json')

    
    def take_input(self): #kerää käyttäjän antamat inputit
        self.tyhjenna_tulosteksti_GUIssa()
        self.aloitus_aika = time.time() #jotta saadaan laskettua haun kesto
        if (self.duunitori_luku.get() == 0) & (self.tyokkari_luku.get() == 0):
            self.tuloskohta.config(text="Valitse joku hakusivu.") #jos mitään työnhakusivua ei valittu, käskee valitsemaan
        else:
            if self.tallenna.get() == 1:
                tallennetun_nimi = self.nimella_kentta.get()
                if len(tallennetun_nimi)==0:
                    self.tuloskohta.config(text="Lisää tallennetulle haulle nimi.")
                else:
                    #check if the given name already exists.
                    tallennettujen_hakujen_nimet = access_files.open_json(self.tallennettujen_hakujen_polut)
                    if tallennetun_nimi in tallennettujen_hakujen_nimet:
                        self.tuloskohta.config(text="Tällä nimellä on jo tallennettu hakuparametrit. Anna toinen nimi.")
                    else:
                        tallennettujen_hakujen_nimet.append(tallennetun_nimi)
                        access_files.write_data_to_json_with(tallennettujen_hakujen_nimet, self.tallennettujen_hakujen_polut)
                        self.tallenna_GUI_input(tallennetun_nimi)
        print("hakusivun_valinta. " + str(time.time()-self.aloitus_aika))
        self.en_disable_widgets('disable')
        self.hakusivun_valinta(self.aloitus_aika)

    def select_saved_search(self):
        #avataan tiedosto ja luodaan sen perusteella dropdown menu
        saved_searches_options = access_files.open_json(self.tallennettujen_hakujen_polut)
        if len(saved_searches_options) == 0:
            self.tuloskohta.config(text="Ei tallennettuja hakusanoja. Anna hakusanat ja paina Hae-nappia.")
        else:
            #dropdown menun luonti
            self.named_searches = StringVar(self.master)
            self.named_searches.set(saved_searches_options[0]) # default value
            w = OptionMenu(self.master, self.named_searches, *saved_searches_options)
            w.grid(row=17, column=0)

            self.show_chosen_parameters_button = Button(self.master, text='Näytä parametrit', command=self.load_saved_input)
            self.show_chosen_parameters_button.grid(row=17,column=1, columnspan=2, padx=5, pady=5)

            #tarkastelu-vaihtoehdon luonti (poistaminen ja muokkaaminen)

    def load_saved_input(self):
        tallennetut_tiedot = access_files.open_json(self.named_searches.get() + ".json")
        self.tyhjenna_GUI_input()
        self.tyhjenna_tulosteksti_GUIssa()
        self.aloitus_aika = time.time()

        self.hakusana_kentta.insert(0, access_files.list_to_string(tallennetut_tiedot["search_words"], ", "))
        self.sijainti_kentta.insert(0, access_files.list_to_string(tallennetut_tiedot["locations"], ", "))
        self.duunitori_luku.set(int(tallennetut_tiedot["duunitori"]))
        self.tyokkari_luku.set(int(tallennetut_tiedot["tetoimisto"]))
        self.ilmoitusajan_valinta.set(int(tallennetut_tiedot["published"]))
        self.duunitori_tekstista.set(tallennetut_tiedot["duunitori_from_text_also"])
        self.ei_nailla_titteleilla.insert(0, access_files.list_to_string(tallennetut_tiedot["not_with_these_words"], ", "))
        self.saved_search_info = tk.Label(self.master, text='Voit muokata ennen kuin painat Jatko-nappia ja tiedot tallentuvat automaattisesti.')
        self.saved_search_info.grid(row=20,columnspan=4, pady=5)

        #lopuksi luo jatkonapin ja poisto-napin
        self.continue_saved_search_button = Button(self.master, text='Jatka tallennettua hakua', command=self.hae_tallennetuilla_parametreilla)
        self.continue_saved_search_button.grid(row=18,column=2, columnspan=2, padx=5, pady=5)
        self.remove_saved_search_button = Button(self.master, text='Poista tallennettu haku', command=self.remove_selected_search_parameters)
        self.remove_saved_search_button.grid(row=18,column=0, columnspan=2, padx=5, pady=5)

    def remove_selected_search_parameters(self):
        #poistaa ne tallennetut hakuparametrit, jotka on valittuna.
        remove_this = self.named_searches.get()
        #tahan viela vahvistuslaatikko voisi olla ok, mutta en nyt jaksa tehda.
        names_of_saved_params = access_files.open_json(self.tallennettujen_hakujen_polut)
        if remove_this in names_of_saved_params:
            names_of_saved_params.remove(remove_this)
            access_files.write_data_to_json_with(names_of_saved_params, self.tallennettujen_hakujen_polut)
            os.remove(remove_this + ".json")
            self.saved_search_info.config(text="poistettu tallennetut hakutiedot nimellä: " + remove_this)
            self.select_saved_search #this does not update optionmenu
        else:
            self.saved_search_info.config(text="virhe yrittäessä poistaa hakutietoja nimellä: " + remove_this)

    def hae_tallennetuilla_parametreilla(self):
        self.en_disable_widgets("disabled") #estää GUI:n käytön haun aikana
        self.tallenna_GUI_input(self.named_searches.get()) #tallenna sillä nimellä, mikä valittiin
        self.hakusivun_valinta(time.time())

    def hakusivun_valinta(self, aloitus_aika):
        print("hakusivun valinta")
        sana, paikka, ei_tittelit = access_files.nolla_tyhjaksi(self.hakusana_kentta.get()), access_files.nolla_tyhjaksi(self.sijainti_kentta.get()), access_files.nolla_tyhjaksi(self.ei_nailla_titteleilla.get())
        sanalista = sana.split(", ")
        paikkalista = paikka.split(", ")
        ei_tittelit_lista = ei_tittelit.split(", ")
        tulostaulukko = pd.DataFrame()
        if (self.duunitori_luku.get() == 1):
            tulostaulukko = suorita_haku_duunitori(sanalista, paikkalista, ei_tittelit_lista, self.duunitori_tekstista.get(), self.ilmoitusajan_valinta.get()) #option on julkaisupäivän valinta
        if (self.tyokkari_luku.get() == 1):
            #lisäsin kielletyt tittelit työkkärin hakuun mukaan
            tulostaulukko = tulostaulukko.append(suorita_haku_tyovoimatoimisto(sana, paikka, str(self.ilmoitusajan_valinta.get()), ei_tittelit_lista), ignore_index = True) #Tässä haluan poistaa samat rivit vaan toisesta taulukosta
            tulostaulukko = tulostaulukko.drop_duplicates(subset=['Titteli', 'Työnantaja', 'Sijainti']) #tämä ei ihan toimi
        if (tulostaulukko.empty):
            self.tuloskohta.config(text="Ei hakutuloksia hakusanoilla.")
        else:
            #taulukko.to_csv("Hakutulokset.csv", encoding="utf-8")
            tulostaulukko.to_excel('Hakutulokset.xlsx', index = False)
            self.tuloskohta.config(text="Valmis. Tarkista tulokset ja merkitse huonot ('0') ja hyvät ('1'). Paina 'Tarkista'.")
            self.change_tarkistus("normal")
            print(time.time() - self.aloitus_aika)
        self.en_disable_widgets("normal") #sallii GUI:n käytön haun jälkeen
    
    #tkinterin widgetien värit ja klikkauksien estot
    def en_disable_widgets(self,string): #string voi olla joko "disabled" tai "normal". Jos on "disabled", ei voi klikkailla tai kirjoittaa ja jos on "normal", voi muokata.
        widgets = self.hakusana_kentta, self.sijainti_kentta, self.tekstista, self.duunitori, self.tyokkari, self.kaikki, self.vuorokausi, self.kolme_paivaa, self.viikko, self.tallenna_haku, self.tallennettu_nappi, self.haku_nappi, self.ei_nailla_titteleilla
        for widget in widgets:
            widget.config(state=string)
        self.update()
        return;

    def tyhjenna_GUI_input(self):
        #Kun syötetään tallennettuja tietoja, pitää varmistaa, että käyttäjä ei ollut jo antanut joitain tietoja.
        self.hakusana_kentta.delete(0, END)
        self.sijainti_kentta.delete(0, END)
        self.ei_nailla_titteleilla.delete(0, END)
        return;

    def tyhjenna_tulosteksti_GUIssa(self):
        #tyhjentää hakukenttien alle tulevan kohdan, jonne tulee viestejä ja ohjeita
        self.tuloskohta.config(text=" ")
        return;

    def change_tarkistus(self,string):
        #Kun syötetään tallennettuja tietoja, pitää varmistaa, että käyttäjä ei ollut jo antanut joitain tietoja.
        #ei ole mitään syytä laittaa tämä nappi erikseen disabloitavaksi ja hyväksyttäväksi. Toisaalta haluan poistaa tämän napin, mutta se edellyttää vähän enemmän työtä.
        self.tarkistus_nappi.config(state=string)

#luo ikkunan
ikkuna = tk.Tk()
ikkuna.title('Super työnhaku')
ikkuna.geometry('700x900')
ikkuna = tyonhaku_sovellus(ikkuna)
ikkuna.mainloop()
