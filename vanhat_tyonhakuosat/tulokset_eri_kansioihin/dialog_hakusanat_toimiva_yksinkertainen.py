import tkinter as tk
from tkinter import Tk, Checkbutton, Radiobutton, Entry, DISABLED, END
import openpyxl
import csv
from duunitori_haku import suorita_haku_duunitori
from tyovoimatoimisto_selenium import suorita_haku_tyovoimatoimisto
#import numpy as np
import sys
import time

#https://stackoverflow.com/questions/51902451/how-to-enable-and-disable-frame-instead-of-individual-widgets-in-python-tkinter/52152773

#suorituksen keston testaus
start_time = None

#Hakusanojen yhteenkeräämistä varten
ei = ""

def conf_widgets(boolean):
    tila = ""
    if boolean == False:
        #string = "disabled"
        #Checkbutton(state='disabled')
        Checkbutton(state=DISABLED)
        Radiobutton(state='disabled')
        #tk.Button(window, text='Hae', command=take_input)
        #tk.Button(window, text='Tallennettu haku', command=load_saved_input)
        Entry(state='disabled')
        #hakusana_kentta.config(state='disabled')
    else:
        #string = 'normal'
        Checkbutton(state='normal')
        Radiobutton(state='normal')
        Entry(state='normal')
    window.update()
    return;

class call_search_to_get_results:
    def tuloksien_arviointi(taulukko, boolean, yksi, sijainti, hakukone, start_time):
        if (taulukko.empty):
            global ei
            #ei = ei + " " + yksi + " ja " + sijainti + ", "
            ei = ei + " " + yksi
            ei_hakusanoilla.config(text="Ei hakutuloksia hakusanoilla:")
            hakusanoilla.config(text=ei)
        else:
            if boolean == True:
                ilmoitus_sata.config(text="Koska tuloksia on yli 100 sanoilla" + yksi + " ja " + sijainti + ". Kaikkia ei haettu.")
            if hakukone == 1:
                taulukko.to_csv("Duunitori_" + yksi + "_" + sijainti + ".csv", encoding="utf-8")
            elif hakukone == 2:
                taulukko.to_csv("Tyovoimatoimisto_" + yksi + "_" + sijainti + ".csv", encoding="utf-8")
            tiedostojen_sijainti.config(text="Tiedostot löytyvät kansiosta blaa blaa.")
            print("haku loppui. " + str(time.time()-start_time))

    def hakusivun_valinta(start_time):
        #print("Tuli hakusivun valintaan")
        sana, paikka = hakusana_kentta.get(), sijainti_kentta.get()
        if len(sana) == 0:
            sana = " "
        if len(paikka) == 0:
            paikka = " "
        if (duunitori_luku.get() == 1):
            teksti = duunitori_tekstista.get()
            if teksti == " ":
                teksti = ""
            erotus = option.get()
            kone = 1
            for s in sana.split(" "):
                for p in paikka.split(" "):
                    #print("menee duunitori_hakuun. " + str(time.time()-start_time))
                    (lista, onko_yli_sata) = suorita_haku_duunitori(s, p, teksti, erotus)
                    #print("menee tulosten arviointiin duunitorin jälkeen. " + str(time.time()-start_time))
                    call_search_to_get_results.tuloksien_arviointi(lista, onko_yli_sata, s, p, kone, start_time)
            conf_widgets(True)
        if (tyokkari_luku.get() == 1):
            julkaistu = str(option.get())
            kone = 2
            for s in sana.split(" "):
                for p in paikka.split(" "):
                    #print("menee työkkärin hakuun. " + str(time.time()-start_time))
                    (lista, onko_yli_sata, liikaa) = suorita_haku_tyovoimatoimisto(s, p, julkaistu)
                    if liikaa == True:
                        rajaa.config(text="Rajaa työvoimatoimiston hakua.")
                        #print("Rajaa työvoimatoimiston hakua." + "Aikaa kului: " + str(time.time()-start_time))
                        continue
                    #print("menee tulosten arviointiin työkkärin jälkeen.. " + str(time.time()-start_time))
                    call_search_to_get_results.tuloksien_arviointi(lista, onko_yli_sata, s, p, kone, start_time)
            #conf_widgets(True)

class start:
    def take_input():
        global start_time
        start_time = time.time()
        ei_hakusanoilla.config(text=" ")
        rajaa.config(text=" ")
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
        #hakusana_kentta.config(state='disabled') # OR entry['state'] = 'disabled'
        conf_widgets(False) #Miksei tää nyt toimi?
        call_search_to_get_results.hakusivun_valinta(start_time)

#luo ikkunan
window= tk.Tk()
window.title('Super työnhaku')
window.geometry('500x500')

#Jos ei tuloksia hakusanoilla
ei_hakusanoilla = tk.Label(window, text=' ')
ei_hakusanoilla.grid(row=3, sticky='w', pady=5, padx=5)
hakusanoilla = tk.Label(window, text=' ')#, width=60)
hakusanoilla.grid(row=4, columnspan=4, sticky='w', pady=5, padx=5)

#Rajaa työkkärin hakua
rajaa = tk.Label(window, text=' ')
rajaa.grid(row=7, column=2, sticky='w', pady=5, padx=5)

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
duunitori = tk.Checkbutton(window, text="Duunitori.fi", variable=duunitori_luku, onvalue=1, offvalue=0).grid(row=7,column=0, padx=5)
tekstista = tk.Checkbutton(window, text="Haku myös tekstistä", variable=duunitori_tekstista, onvalue="&search_also_descr=1", offvalue="").grid(row=9,column=0, padx=5)
tyokkari = tk.Checkbutton(window, text="Työvoimatoimisto", variable=tyokkari_luku, onvalue=1, offvalue=0).grid(row=7,column=1, padx=5)

#Hakujen rajoitus ilmoitusajankohdan mukaan
tyokkari_aika = tk.Label(window, text='Julkaistu')
tyokkari_aika.grid(row=9, column=1, sticky='w', pady=5, padx=5)
option = tk.IntVar()
kaikki = Radiobutton(window, text="kaikki", value=0, var=option).grid(row=10, column=1, sticky='w', pady=5, padx=5)
vuorokausi = Radiobutton(window, text="vuorokausi", value=1, var=option).grid(row=11, column=1, sticky='w', pady=5, padx=5)
kolme_paivaa = Radiobutton(window, text="3 päivää", value=2, var=option).grid(row=12, column=1, sticky='w', pady=5, padx=5)
viikko = Radiobutton(window, text="viikko", value=3, var=option).grid(row=13, column=1, sticky='w', pady=5, padx=5)

#Tallenna haku
tallenna = tk.IntVar()
tallenna_haku = tk.Checkbutton(window, text="Tallenna", variable=tallenna, onvalue=1, offvalue=0).grid(row=14,column=0, padx=5)

#Tallennettu haku
tk.Button(window, text='Tallennettu haku', command=start.load_saved_input).grid(row=15,column=1, columnspan=2, padx=5, pady=5)

#Hae-nappi
tk.Button(window, text='Hae', command=start.take_input).grid(row=14,column=0, columnspan=2, padx=5)
#Lopetus-nappo
tk.Button(window, text='Lopeta', command=window.quit).grid(row=14,column=2, padx=5)

window.mainloop()
