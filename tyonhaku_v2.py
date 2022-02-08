import tkinter as tk
from tkinter import *
import openpyxl
from duunitori_haku import suorita_haku_duunitori
from tyovoimatoimisto_selenium import suorita_haku_tyovoimatoimisto
from text_rivinvaihto_listaksi_avaus import txt_listaksi #miksi tämä on täällä?
from osuvuuden_tarkistus import osuvuudet
import time
import pandas as pd

#suorituksen keston testaus
start_time = None

class conf_widgets():
    global window
    def en_disable(string):
        widgets = window.hakusana_kentta, window.sijainti_kentta, window.tekstista, window.duunitori, window.tyokkari, window.kaikki, window.vuorokausi, window.kolme_paivaa, window.viikko, window.tallenna_haku, window.tallennettu_nappi, window.haku_nappi, window.ei_nailla
        for widget in widgets:
            widget.config(state=string)
        window.update()
        return;
    def clear_data_for_saved_input():
        window.hakusana_kentta.delete(0, END)
        window.sijainti_kentta.delete(0, END)
        window.ei_nailla.delete(0, END)
        return;
    def clear_other_data():
        window.tuloskohta.config(text=" ")
        return;
    def change_tarkistus(string):
        window.tarkistus_nappi.config(state=string)

class call_search_to_get_results:
    def nolla_tyhjaksi(x): #jos käyttäjä ei anna tekstiä tekstikenttään, vaihdetaan nolla-arvo tyhjäksi, jotta voidaan tehdä hakulinkki
        if len(x) == 0: x = ""
        return x;
    def hakusivun_valinta(start_time):
        print("hakusivun valinta")
        global window
        sana, paikka, negaatio = call_search_to_get_results.nolla_tyhjaksi(window.hakusana_kentta.get()), call_search_to_get_results.nolla_tyhjaksi(window.sijainti_kentta.get()), call_search_to_get_results.nolla_tyhjaksi(window.ei_nailla.get())
        tulostaulukko = pd.DataFrame()
        if (window.duunitori_luku.get() == 1):
            tulostaulukko = suorita_haku_duunitori(sana, paikka, negaatio, window.duunitori_tekstista.get(), window.option.get()) #option on julkaisupäivän valinta
        if (window.tyokkari_luku.get() == 1):
            tulostaulukko = tulostaulukko.append(suorita_haku_tyovoimatoimisto(sana, paikka, str(window.option.get())), ignore_index = True) #Tässä haluan poistaa samat rivit vaan toisesta taulukosta
            tulostaulukko = tulostaulukko.drop_duplicates(subset=['Titteli', 'Työnantaja', 'Sijainti']) #tämä ei ihan toimi
        if (tulostaulukko.empty):
            window.tuloskohta.config(text="Ei hakutuloksia hakusanoilla.")
        else:
            #taulukko.to_csv("Hakutulokset.csv", encoding="utf-8")
            tulostaulukko.to_excel(r'C:\pythontestit\Hakutulokset.xlsx', index = False)
            window.tuloskohta.config(text="Valmis. Tarkista tulokset ja merkitse huonot ('0') ja hyvät ('1'). Paina 'Tarkista'.")
            conf_widgets.change_tarkistus("normal")
            print(time.time() - start_time)
        conf_widgets.en_disable("normal")

class start:
    global window
    global start_time
    def take_input(): #kerää käyttäjän antamat inputit
        conf_widgets.clear_other_data()
        start_time = time.time()
        if (window.duunitori_luku.get() == 0) & (window.tyokkari_luku.get() == 0):
            window.tuloskohta.config(text="Valitse joku hakusivu.") #jos mitään työnhakusivua ei valittu, käskee valitsemaan
        else:
            if window.tallenna.get() == 1:
                words, locations, text_also, negaatiot = window.hakusana_kentta.get(), window.sijainti_kentta.get(), window.duunitori_tekstista.get(), window.ei_nailla.get() #nämä muuttujat ovat näitä kenttiä
                x = str(window.duunitori_luku.get()) + str(window.tyokkari_luku.get())+ str(window.option.get())
                data = words + '\n' + locations + '\n' + x + '\n' + text_also + '\n' + negaatiot
                saved_parameters = open('C:/pythontestit/' + 'tallennettu_haku.txt', 'w+', encoding='utf-8')
                saved_parameters.write(data)
                saved_parameters.close()
            print("hakusivun_valinta. " + str(time.time()-start_time))
            conf_widgets.en_disable('disable')
            call_search_to_get_results.hakusivun_valinta(start_time)
    def load_saved_input():
        conf_widgets.clear_data_for_saved_input()
        conf_widgets.clear_other_data()
        start_time = time.time()
        words, locations, x, y, negaatiot = open('C:/pythontestit/' + 'tallennettu_haku.txt', encoding='utf-8').read().split('\n')
        window.duunitori_luku.set(int(x[0]))
        window.tyokkari_luku.set(int(x[1]))
        window.option.set(int(x[2]))
        window.hakusana_kentta.insert(0, words)
        window.sijainti_kentta.insert(0, locations)
        window.ei_nailla.insert(0, negaatiot)
        window.duunitori_tekstista.set(y)
        conf_widgets.en_disable("disabled")
        call_search_to_get_results.hakusivun_valinta(start_time)

class job_search_app(Frame):
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
        label3 = tk.Label(self.master, text='Mutta ei näillä', font=('helvetica', 10)).grid(row=1, sticky='w', column=3, padx=5)
        self.ei_nailla = tk.Entry(self.master)
        self.ei_nailla.grid(row=2, sticky='w', column=3, padx=5)
        
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
        
        self.kaikki = Radiobutton(self.master, text="kaikki", value=0, var=self.option)
        self.vuorokausi = Radiobutton(self.master, text="vuorokausi", value=1, var=self.option)
        self.kolme_paivaa = Radiobutton(self.master, text="3 päivää", value=2, var=self.option)
        self.viikko = Radiobutton(self.master, text="viikko", value=3, var=self.option)
        
        self.kaikki.grid(row=9, column=1, sticky='w', pady=5, padx=5)
        self.vuorokausi.grid(row=10, column=1, sticky='w', pady=5, padx=5)
        self.kolme_paivaa.grid(row=11, column=1, sticky='w', pady=5, padx=5)
        self.viikko.grid(row=12, column=1, sticky='w', pady=5, padx=5)
        
        #Tallenna haku
        self.tallenna = tk.IntVar()
        self.tallenna_haku = tk.Checkbutton(self.master, text="Tallenna", variable=self.tallenna, onvalue=1, offvalue=0)
        self.tallenna_haku.grid(row=13,column=0, padx=5)
        
        #Tallennettu haku
        self.tallennettu_nappi = Button(self.master, text='Tallennettu haku', command=start.load_saved_input)
        self.tallennettu_nappi.grid(row=14,column=1, columnspan=2, padx=5, pady=5)
        
        #Hae-nappi
        self.haku_nappi = Button(self.master, text='Hae', command=start.take_input)
        self.haku_nappi.grid(row=15,column=0, columnspan=2, padx=5)
        #Lopetus-nappi
        self.lopeta_nappi = Button(self.master, text='Lopeta', command=self.master.destroy)
        self.lopeta_nappi.grid(row=15,column=2, padx=5)

#luo ikkunan
window = tk.Tk()
window.title('Super työnhaku')
window.geometry('700x900')
window = job_search_app(window)
window.mainloop()