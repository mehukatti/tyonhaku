import tkinter as tk
from tkinter import *
from duunitori_haku import suorita_haku_duunitori
from tyovoimatoimisto_selenium import suorita_haku_tyovoimatoimisto
import access_files
from osuvuuden_tarkistus import osuvuudet
import time
import pandas as pd
import os

class job_search_app(Frame):
    start_time = None
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.create_widgets()
    def create_widgets(self):
        canvas = Canvas(self) #Tarvitaanko tätä?

        #Ilmoitus tiedostojen sijainnista ja tuloksista
        self.tuloskohta = tk.Label(self.master, text=' ')
        self.tuloskohta.grid(row=5,columnspan=4, pady=5)

        #Tarkistus-nappi haun tarkistuksen jälkeen
        self.tarkistus_nappi = Button(self.master, text='Tarkista', command=osuvuudet)#state=DISABLED, 
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
        self.tekstista.grid(row=8,column=0, padx=5)
        self.tyokkari.grid(row=6,column=1, padx=5)
        
        #Hakujen rajoitus ilmoitusajankohdan mukaan
        self.tyokkari_aika = tk.Label(self.master, text='Julkaistu')
        self.tyokkari_aika.grid(row=8, column=1, sticky='w', pady=5, padx=5)
        self.option = tk.IntVar()#option on julkaisuajankohdan valinta
        
        self.kaikki = Radiobutton(self.master, text="kaikki", value=0, variable=self.option)
        self.vuorokausi = Radiobutton(self.master, text="vuorokausi", value=1, variable=self.option)
        self.kolme_paivaa = Radiobutton(self.master, text="3 päivää", value=2, variable=self.option)
        self.viikko = Radiobutton(self.master, text="viikko", value=3, variable=self.option)
        
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
        #self.tallennettu_nappi = Button(self.master, text='Tallennettu haku', command=start.load_saved_input)
        self.tallennettu_nappi = Button(self.master, text='Tallennettu haku', command=self.select_saved_search)
        self.tallennettu_nappi.grid(row=16,column=1, columnspan=2, padx=5, pady=5)
        
        #Hae-nappi
        #self.haku_nappi = Button(self.master, text='Hae', command=start.take_input)
        self.haku_nappi = Button(self.master, text='Hae', command=self.take_input)
        self.haku_nappi.grid(row=15,column=0, columnspan=2, padx=5)
        #Lopetus-nappi
        self.lopeta_nappi = Button(self.master, text='Lopeta', command=self.master.destroy)
        self.lopeta_nappi.grid(row=15,column=2, padx=5)


    def create_paths(self):
        self.path_to_saved_named_searches = "names_of_saved_param.json"
        self.path_to_results_xlsx = 'Hakutulokset.xlsx'

    def save_input(self, nimi):
        saved_parameters = {
            "search_words": self.hakusana_kentta.get().split(", "),
            "locations": self.sijainti_kentta.get().split(", "),
            "duunitori": self.duunitori_luku.get(),
            "tetoimisto": self.tyokkari_luku.get(),
            "published":self.option.get(),
            "duunitori_from_text_also": self.duunitori_tekstista.get(),
            "not_with_these_words": self.ei_nailla_titteleilla.get().split(", ")
        }
        access_files.write_data_to_json_with(saved_parameters, nimi + '.json')

    
    def take_input(self): #kerää käyttäjän antamat inputit
        self.clear_other_data()
        start_time = time.time()
        if (self.duunitori_luku.get() == 0) & (self.tyokkari_luku.get() == 0):
            self.tuloskohta.config(text="Valitse joku hakusivu.") #jos mitään työnhakusivua ei valittu, käskee valitsemaan
        else:
            if self.tallenna.get() == 1:
                tallennetun_nimi = self.nimella_kentta.get()
                if len(tallennetun_nimi)==0:
                    self.tuloskohta.config(text="Lisää tallennetulle haulle nimi.")
                else:
                    #check if the given name already exists.
                    names_of_saved_parameters = access_files.open_json(self.path_to_saved_named_searches)
                    if tallennetun_nimi in names_of_saved_parameters:
                        self.tuloskohta.config(text="Name already exists. Give a new one.")
                    else:
                        names_of_saved_parameters.append(tallennetun_nimi)
                        access_files.write_data_to_json_with(names_of_saved_parameters, self.path_to_saved_named_searches)
                        self.save_input(tallennetun_nimi)
        print("hakusivun_valinta. " + str(time.time()-start_time))
        self.en_disable('disable')
        self.hakusivun_valinta(start_time)

    def select_saved_search(self):
        #avataan tiedosto ja luodaan sen perusteella dropdown menu
        saved_searches_options = access_files.open_json(self.path_to_saved_named_searches)
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
        self.clear_data_for_saved_input()
        self.clear_other_data()
        start_time = time.time()

        #self.nimella_kentta.insert(0, self.named_searches.get())
        self.hakusana_kentta.insert(0, access_files.list_to_string(tallennetut_tiedot["search_words"], ", "))
        self.sijainti_kentta.insert(0, access_files.list_to_string(tallennetut_tiedot["locations"], ", "))
        self.duunitori_luku.set(int(tallennetut_tiedot["duunitori"]))
        self.tyokkari_luku.set(int(tallennetut_tiedot["tetoimisto"]))
        self.option.set(int(tallennetut_tiedot["published"]))
        self.duunitori_tekstista.set(tallennetut_tiedot["duunitori_from_text_also"])
        self.ei_nailla_titteleilla.insert(0, access_files.list_to_string(tallennetut_tiedot["not_with_these_words"], ", "))
        self.saved_search_info = tk.Label(self.master, text='Voit muokata ennen kuin painat Jatko-nappia ja tiedot tallentuvat automaattisesti.')
        self.saved_search_info.grid(row=20,columnspan=4, pady=5)

        #lopuksi luo jatkonapin ja poisto-napin
        self.continue_saved_search_button = Button(self.master, text='Jatka tallennettua hakua', command=self.continue_search)
        self.continue_saved_search_button.grid(row=18,column=1, columnspan=2, padx=5, pady=5)
        self.remove_saved_search_button = Button(self.master, text='Poista tallennettu haku', command=self.remove_selected_search_parameters)
        self.remove_saved_search_button.grid(row=18,column=0, columnspan=2, padx=5, pady=5)

    def remove_selected_search_parameters(self):
        remove_this = self.named_searches.get()
        #tahan viela vahvistuslaatikko voisi olla ok, mutta en nyt jaksa tehda.
        names_of_saved_params = access_files.open_json(self.path_to_saved_named_searches)
        if remove_this in names_of_saved_params:
            names_of_saved_params.remove(remove_this)
            access_files.write_data_to_json_with(names_of_saved_params, self.path_to_saved_named_searches)
            os.remove(remove_this + ".json")
            self.saved_search_info.config(text="poistettu tallennetut hakutiedot nimellä: " + remove_this)
            self.select_saved_search #this does not update optionmenu
        else:
            self.saved_search_info.config(text="virhe yrittäessä poistaa hakutietoja nimellä: " + remove_this)

    def continue_search(self):
        self.en_disable("disabled")
        self.save_input(self.named_searches.get()) #tallenna sillä nimellä, mikä valittiin
        self.hakusivun_valinta(time.time())

    def hakusivun_valinta(self,start_time):
        print("hakusivun valinta")
        sana, paikka, ei_tittelit = access_files.nolla_tyhjaksi(self.hakusana_kentta.get()), access_files.nolla_tyhjaksi(self.sijainti_kentta.get()), access_files.nolla_tyhjaksi(self.ei_nailla_titteleilla.get())
        sanalista = sana.split(", ")
        paikkalista = paikka.split(", ")
        ei_tittelit_lista = ei_tittelit.split(", ")
        tulostaulukko = pd.DataFrame()
        if (self.duunitori_luku.get() == 1):
            tulostaulukko = suorita_haku_duunitori(sanalista, paikkalista, ei_tittelit_lista, self.duunitori_tekstista.get(), self.option.get()) #option on julkaisupäivän valinta
        if (self.tyokkari_luku.get() == 1):
            #lisäsin kielletyt tittelit työkkärin hakuun mukaan
            tulostaulukko = tulostaulukko.append(suorita_haku_tyovoimatoimisto(sana, paikka, str(self.option.get()), ei_tittelit_lista), ignore_index = True) #Tässä haluan poistaa samat rivit vaan toisesta taulukosta
            tulostaulukko = tulostaulukko.drop_duplicates(subset=['Titteli', 'Työnantaja', 'Sijainti']) #tämä ei ihan toimi
        if (tulostaulukko.empty):
            self.tuloskohta.config(text="Ei hakutuloksia hakusanoilla.")
        else:
            #taulukko.to_csv("Hakutulokset.csv", encoding="utf-8")
            tulostaulukko.to_excel('Hakutulokset.xlsx', index = False)
            self.tuloskohta.config(text="Valmis. Tarkista tulokset ja merkitse huonot ('0') ja hyvät ('1'). Paina 'Tarkista'.")
            self.change_tarkistus("normal")
            print(time.time() - start_time)
        self.en_disable("normal")
    
    #tkinterin widgetien värit ja klikkauksien estot
    def en_disable(self,string):
        widgets = self.hakusana_kentta, self.sijainti_kentta, self.tekstista, self.duunitori, self.tyokkari, self.kaikki, self.vuorokausi, self.kolme_paivaa, self.viikko, self.tallenna_haku, self.tallennettu_nappi, self.haku_nappi, self.ei_nailla_titteleilla
        for widget in widgets:
            widget.config(state=string)
        self.update()
        return;
    def clear_data_for_saved_input(self):
        self.hakusana_kentta.delete(0, END)
        self.sijainti_kentta.delete(0, END)
        self.ei_nailla_titteleilla.delete(0, END)
        return;
    def clear_other_data(self):
        self.tuloskohta.config(text=" ")
        return;
    def change_tarkistus(self,string):
        self.tarkistus_nappi.config(state=string)

#luo ikkunan
window = tk.Tk()
window.title('Super työnhaku')
window.geometry('700x900')
window = job_search_app(window)
window.mainloop()