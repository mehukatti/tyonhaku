import tkinter as tk
import openpyxl
import csv
from duunitori_haku import suorita_haku_duunitori
#from tyovoimatoimisto_selenium import suorita_haku_tyovoimatoimisto
import time

#luo ikkunan
window= tk.Tk()
window.title('Super työnhaku')
window.geometry('500x500')

#Jos ei tuloksia hakusanoilla
ei_hakusanoilla = tk.Label(window, text=' ')
ei_hakusanoilla.grid(row=3,columnspan=4, pady=5)

#Ilmoitus tiedostojen sijainnista
tiedostojen_sijainti = tk.Label(window, text=' ')
tiedostojen_sijainti.grid(row=4,columnspan=4, pady=5)

#Jos ei valittu työnhakusivustoa
ei_sivustoa = tk.Label(window, text=' ')
ei_sivustoa.grid(row=6,columnspan=4, pady=5)

#Hakusanat-tekstiruutu
label1 = tk.Label(window, text='Hakusanat', font=('helvetica', 10)).grid(row=1,column=1, padx=5)
hakusana_kentta = tk.Entry(window)
hakusana_kentta.grid(row=2,column=1, padx=5)

#Sijainti-tekstiruutu
label2 = tk.Label(window, text='Sijainti', font=('helvetica', 10)).grid(row=1,column=2, padx=5)
sijainti_kentta = tk.Entry(window)
sijainti_kentta.grid(row=2,column=2, padx=5)

#suorituksen keston testaus
start_time = None

def tuloksien_arviointi(taulukko, luku, yksi, sijainti, aika):
    if (taulukko.empty):
        ei_hakusanoilla.config(text="Ei hakutuloksia hakusanoilla " + yksi + " ja " + sijainti)
    else:
        if luku > 100:
            ei_hakusanoilla.config(text="Koska tuloksia on yli 100 sanoilla" + yksi + " ja " + sijainti + ". Kaikkia ei haettu.")
        taulukko.to_csv("Duunitori" + yksi + "_" + sijainti + ".csv", encoding="utf-8")
        tiedostojen_sijainti.config(text="Tiedostot löytyvät kansiosta blaa blaa.")
        print("--- %s seconds ---" % (time.time() - aika))

def hakusivun_valinta():
    start_time = time.time()
    ei_hakusanoilla.config(text=" ")
    paikka = sijainti_kentta.get()
    sana = hakusana_kentta.get()
    if (duunitori_luku.get() == 1):
        for s in sana.split(" "):
            lista, tuloksia = suorita_haku_duunitori(s, paikka)
            tuloksien_arviointi(lista, tuloksia, s, paikka, start_time)
    if (tyokkari_luku.get() == 1):
        #for s in sana.split(" "):
            #lista, onko_yli_sata = suorita_haku_tyovoimatoimisto(s, paikka)
            #print("Palautettu taulukko")
            #print(lista)
            #print("\n" + "Palautettu boolean")
            #tuloksien_arviointi(lista, onko_yli_sata, s, paikka)
        print("Työkkäri ei juuri nyt ole käytettävissä.")
    elif (tyokkari_luku.get() == 0) & (duunitori_luku.get() == 0): 
        ei_sivustoa.config(text="Valitse joku hakusivu.")

#Hakusivujen valintaruudut
duunitori_luku = tk.IntVar()
tyokkari_luku = tk.IntVar()
duunitori = tk.Checkbutton(window, text="Duunitori.fi", variable=duunitori_luku, onvalue=1, offvalue=0).grid(row=5,column=1, padx=5)
tyokkari = tk.Checkbutton(window, text="Työvoimatoimisto", variable=tyokkari_luku, onvalue=1, offvalue=0).grid(row=5,column=2, padx=5)

#Hae-nappi
tk.Button(window, text='Hae', command=hakusivun_valinta).grid(row=7,column=1, columnspan=2, padx=5)
#Lopetus-nappo
tk.Button(window, text='Lopeta', command=window.quit).grid(row=7,column=3, padx=5)

window.mainloop()
