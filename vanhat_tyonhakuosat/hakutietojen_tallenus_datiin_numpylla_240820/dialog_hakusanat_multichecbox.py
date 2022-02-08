import tkinter as tk
from tkinter import *
import openpyxl
import csv
from duunitori_haku import suorita_haku_duunitori
from tyovoimatoimisto_selenium import suorita_haku_tyovoimatoimisto
import numpy as np
import time

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

#suorituksen keston testaus
start_time = None

#Hakusanojen yhteenkeräämistä varten
ei = ""

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

def hakusivun_valinta(sana, paikka, start_time):
    print("Tuli hakusivun valintaan")
    if (duunitori_luku.get() == 1):
        teksti = duunitori_tekstista.get()
        if teksti == " ":
            teksti = ""
        erotus = option.get()
        kone = 1
        for s in sana.split(" "):
            for p in paikka.split(" "):
                print("menee duunitori_hakuun. " + str(time.time()-start_time))
                (lista, onko_yli_sata) = suorita_haku_duunitori(s, p, teksti, erotus)
                print("menee tulosten arviointiin duunitorin jälkeen. " + str(time.time()-start_time))
                tuloksien_arviointi(lista, onko_yli_sata, s, p, kone, start_time)
    if (tyokkari_luku.get() == 1):
        julkaistu = str(option.get())
        kone = 2
        for s in sana.split(" "):
            print(s)
            for p in paikka.split(" "):
                print("paikka: " + p)
                print("menee työkkärin hakuun. " + str(time.time()-start_time))
                (lista, onko_yli_sata, liikaa) = suorita_haku_tyovoimatoimisto(s, p, julkaistu)
                if liikaa == True:
                    rajaa.config(text="Rajaa työvoimatoimiston hakua.")
                    print("Rajaa työvoimatoimiston hakua." + "Aikaa kului: " + str(time.time()-start_time))
                    continue
                print("menee tulosten arviointiin työkkärin jälkeen.. " + str(time.time()-start_time))
                tuloksien_arviointi(lista, onko_yli_sata, s, p, kone, start_time)

def take_input():
    global start_time
    start_time = time.time()
    ei_hakusanoilla.config(text=" ")
    rajaa.config(text=" ")
    ei_sivustoa.config(text="")
    global ei
    ei = ""
    sana, paikka = hakusana_kentta.get(), sijainti_kentta.get()
    if len(sana) == 0:
        sana = " "
    if len(paikka) == 0:
        paikka = " "
    window.update()
    if tallenna.get() == 1:
        teksti = duunitori_tekstista.get()
        if len(teksti) == 0:
            teksti = "_"
        paikka, sana = paikka.replace(' ', '_'), sana.replace(' ', '_')
        words = np.array(sana)
        locations = np.array(paikka)
        x = np.array(str(duunitori_luku.get()) + str(tyokkari_luku.get())+ str(option.get()) + teksti)
        data = np.row_stack((words, locations, x))
        print(data)
        np.savetxt('tallennettu_haku.dat', data, fmt = '%s', encoding='utf-8')
    if (duunitori_luku.get() == 0) & (tyokkari_luku.get() == 0):
        ei_sivustoa.config(text="Valitse joku hakusivu.")
        print("hakusivua ei valittu. " + str(time.time()-start_time))
    else:
        print("hakusivun_valinta. " + str(time.time()-start_time))
        hakusivun_valinta(sana, paikka, start_time)

def load_saved_input():
    hakusana_kentta.delete(0, END)
    sijainti_kentta.delete(0, END)
    global start_time
    start_time = time.time()
    words, locations, x = np.loadtxt('tallennettu_haku.dat', dtype='str', encoding='utf-8')
    duunitori_luku.set(int(x[0]))
    tyokkari_luku.set(int(x[1]))
    option.set(int(x[2]))
    hakusana_kentta.insert(0, words.replace('_', ' '))
    sijainti_kentta.insert(0, locations.replace('_', ' '))
    if x[3:] == "_":
        duunitori_tekstista.set("")
    else:
        duunitori_tekstista.set(x[3:])
    window.update()
    hakusivun_valinta(words.replace('_', ' '), locations.replace('_', ' '), start_time)

#Hakusivujen valintaruudut
duunitori_luku = tk.IntVar()
duunitori_tekstista = tk.StringVar()
tyokkari_luku = tk.IntVar()
duunitori = tk.Checkbutton(window, text="Duunitori.fi", variable=duunitori_luku, onvalue=1, offvalue=0).grid(row=7,column=0, padx=5)
tekstista = tk.Checkbutton(window, text="Haku myös tekstistä", variable=duunitori_tekstista, onvalue="&search_also_descr=1", offvalue="").grid(row=9,column=0, padx=5)
tyokkari = tk.Checkbutton(window, text="Työvoimatoimisto", variable=tyokkari_luku, onvalue=1, offvalue=0).grid(row=7,column=1, padx=5)
tyokkari_aika = tk.Label(window, text='Julkaistu')
tyokkari_aika.grid(row=9, column=1, sticky='w', pady=5, padx=5)

#Hakujen rajoitus ilmoitusajankohdan mukaan
option = tk.IntVar()
kaikki = Radiobutton(window, text="kaikki", value=0, var=option).grid(row=10, column=1, sticky='w', pady=5, padx=5)
vuorokausi = Radiobutton(window, text="vuorokausi", value=1, var=option).grid(row=11, column=1, sticky='w', pady=5, padx=5)
kolme_paivaa = Radiobutton(window, text="3 päivää", value=2, var=option).grid(row=12, column=1, sticky='w', pady=5, padx=5)
viikko = Radiobutton(window, text="viikko", value=3, var=option).grid(row=13, column=1, sticky='w', pady=5, padx=5)

#Tallenna haku
tallenna = tk.IntVar()
tallenna_haku = tk.Checkbutton(window, text="Tallenna", variable=tallenna, onvalue=1, offvalue=0).grid(row=14,column=0, padx=5)

#Tallennettu haku
tk.Button(window, text='Tallennettu haku', command=load_saved_input).grid(row=15,column=1, columnspan=2, padx=5, pady=5)

#Hae-nappi
tk.Button(window, text='Hae', command=take_input).grid(row=14,column=0, columnspan=2, padx=5)
#Lopetus-nappo
tk.Button(window, text='Lopeta', command=window.quit).grid(row=14,column=2, padx=5)

window.mainloop()
