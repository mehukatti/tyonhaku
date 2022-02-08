import tkinter as tk
from tkinter import Tk, Checkbutton, Radiobutton, Button, Entry, DISABLED, END
import openpyxl
#import csv
from duunitori_haku import suorita_haku_duunitori
from tyovoimatoimisto_selenium import suorita_haku_tyovoimatoimisto
import sys
import time
import pandas as pd

#suorituksen keston testaus
start_time = None

def conf_widgets(string):
    widgets = hakusana_kentta, sijainti_kentta, tekstista, duunitori, tyokkari, kaikki, vuorokausi, kolme_paivaa, viikko, tallenna_haku, tallennettu_nappi, haku_nappi
    for widget in widgets:
        widget.config(state=string)
    window.update()
    return;

class call_search_to_get_results:
    def hakusivun_valinta(start_time):
        #print("Tuli hakusivun valintaan")
        sana, paikka = hakusana_kentta.get(), sijainti_kentta.get()
        if len(sana) == 0: sana = ""
        if len(paikka) == 0: paikka = ""
        tulostaulukko = pd.DataFrame()
        if (duunitori_luku.get() == 1):
            erotus = option.get()
            tulostaulukko, onko_yli_sata = suorita_haku_duunitori(sana, paikka, duunitori_tekstista.get(), erotus)
        if (tyokkari_luku.get() == 1):
            julkaistu = str(option.get())
            for s in sana.split(" "):
                for p in paikka.split(" "):
                    (lista, onko_yli_sata) = suorita_haku_tyovoimatoimisto(s, p, julkaistu)
                    tulostaulukko = tulostaulukko.append(lista, ignore_index = True)
                    tulostaulukko = tulostaulukko.drop_duplicates()
        if (tulostaulukko.empty):
            ei_hakusanoilla.config(text="Ei hakutuloksia hakusanoilla.")
        else:
            #taulukko.to_csv("Hakutulokset.csv", encoding="utf-8")
            tulostaulukko.to_excel(r'Hakutulokset.xlsx', index = False)
            tiedostojen_sijainti.config(text="Valmis.")
            print(time.time() - start_time)
        conf_widgets("normal")

class start:
    def take_input():
        global start_time
        start_time = time.time()
        ei_hakusanoilla.config(text=" ")
        ei_sivustoa.config(text="")
        global ei
        ei = ""
        if tallenna.get() == 1:
            words, locations, text_also = hakusana_kentta.get(), sijainti_kentta.get(), duunitori_tekstista.get()
            x = str(duunitori_luku.get()) + str(tyokkari_luku.get())+ str(option.get())
            data = words + '\n' + locations + '\n' + x + '\n' + text_also
            saved_parameters = open('tallennettu_haku.txt', 'w+', encoding='utf-8')
            saved_parameters.write(data)
            saved_parameters.close()
        if (duunitori_luku.get() == 0) & (tyokkari_luku.get() == 0):
            ei_sivustoa.config(text="Valitse joku hakusivu.")
            print("hakusivua ei valittu. " + str(time.time()-start_time))
        else:
            print("hakusivun_valinta. " + str(time.time()-start_time))
            conf_widgets('disable')
            call_search_to_get_results.hakusivun_valinta(start_time)

    def load_saved_input():
        hakusana_kentta.delete(0, END)
        sijainti_kentta.delete(0, END)
        global start_time
        start_time = time.time()
        words, locations, x, y = open('tallennettu_haku.txt', encoding='utf-8').read().split('\n')
        duunitori_luku.set(int(x[0]))
        tyokkari_luku.set(int(x[1]))
        option.set(int(x[2]))
        hakusana_kentta.insert(0, words)
        sijainti_kentta.insert(0, locations)
        duunitori_tekstista.set(y)
        conf_widgets("disabled")
        call_search_to_get_results.hakusivun_valinta(start_time)

#luo ikkunan
window= tk.Tk()
window.title('Super työnhaku')
window.geometry('500x500')

#Jos ei tuloksia hakusanoilla
ei_hakusanoilla = tk.Label(window, text=' ')
ei_hakusanoilla.grid(row=3, sticky='w', pady=5, padx=5)

#tuloksia yli sata
ilmoitus_sata = tk.Label(window, text=' ')
ilmoitus_sata.grid(row=5,columnspan=4, pady=5)

#Ilmoitus tiedostojen sijainnista
tiedostojen_sijainti = tk.Label(window, text=' ')
tiedostojen_sijainti.grid(row=6,columnspan=4, pady=5)

#Jos ei valittu työnhakusivustoa
ei_sivustoa = tk.Label(window, text=' ')
ei_sivustoa.grid(row=8,columnspan=4, pady=5)

#Hakusanat-tekstiruutu
label1 = tk.Label(window, text='Hakusanat', font=('helvetica', 10)).grid(row=1, sticky='w', column=0, padx=5)
hakusana_kentta = tk.Entry(window)
hakusana_kentta.grid(row=2, sticky='w', column=0, padx=5)

#Sijainti-tekstiruutu
label2 = tk.Label(window, text='Sijainti', font=('helvetica', 10)).grid(row=1, sticky='w', column=1, padx=5)
sijainti_kentta = tk.Entry(window)
sijainti_kentta.grid(row=2, sticky='w', column=1, padx=5)

#Hakusivujen valintaruudut
duunitori_luku = tk.IntVar()
duunitori_tekstista = tk.StringVar()
tyokkari_luku = tk.IntVar()

duunitori = tk.Checkbutton(window, text="Duunitori.fi", variable=duunitori_luku, onvalue=1, offvalue=0)
tekstista = tk.Checkbutton(window, text="Haku myös tekstistä", variable=duunitori_tekstista, onvalue="&search_also_descr=1", offvalue="")
tyokkari = tk.Checkbutton(window, text="Työvoimatoimisto", variable=tyokkari_luku, onvalue=1, offvalue=0)

duunitori.grid(row=7,column=0, padx=5)
tekstista.grid(row=9,column=0, padx=5)
tyokkari.grid(row=7,column=1, padx=5)

#Hakujen rajoitus ilmoitusajankohdan mukaan
tyokkari_aika = tk.Label(window, text='Julkaistu')
tyokkari_aika.grid(row=9, column=1, sticky='w', pady=5, padx=5)
option = tk.IntVar()

kaikki = Radiobutton(window, text="kaikki", value=0, var=option)
vuorokausi = Radiobutton(window, text="vuorokausi", value=1, var=option)
kolme_paivaa = Radiobutton(window, text="3 päivää", value=2, var=option)
viikko = Radiobutton(window, text="viikko", value=3, var=option)

kaikki.grid(row=10, column=1, sticky='w', pady=5, padx=5)
vuorokausi.grid(row=11, column=1, sticky='w', pady=5, padx=5)
kolme_paivaa.grid(row=12, column=1, sticky='w', pady=5, padx=5)
viikko.grid(row=13, column=1, sticky='w', pady=5, padx=5)

#Tallenna haku
tallenna = tk.IntVar()
tallenna_haku = tk.Checkbutton(window, text="Tallenna", variable=tallenna, onvalue=1, offvalue=0)
tallenna_haku.grid(row=14,column=0, padx=5)

#Tallennettu haku
tallennettu_nappi = Button(window, text='Tallennettu haku', command=start.load_saved_input)
tallennettu_nappi.grid(row=15,column=1, columnspan=2, padx=5, pady=5)

#Hae-nappi
haku_nappi = Button(window, text='Hae', command=start.take_input)
haku_nappi.grid(row=14,column=0, columnspan=2, padx=5)
#Lopetus-nappo
lopeta_nappi = Button(window, text='Lopeta', command=window.quit)
lopeta_nappi.grid(row=14,column=2, padx=5)

window.mainloop()
