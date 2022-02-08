import tkinter as tk
from tkinter import Tk, Checkbutton, Radiobutton, Entry, DISABLED, END, Frame, Text, Label, BOTH, Canvas
import openpyxl
import csv
from duunitori_haku import suorita_haku_duunitori
from tyovoimatoimisto_selenium import suorita_haku_tyovoimatoimisto
#import numpy as np
import sys
import time

#suorituksen keston testaus
start_time = None

#Hakusanojen yhteenkeräämistä varten
ei = ""

class call_search_to_get_results(object):
    def __init__(variable):
        pass
    
    def tuloksien_arviointi(variable, self, taulukko, boolean, yksi, sijainti, hakukone):
        if (taulukko.empty):
            global ei
            #ei = ei + " " + yksi + " ja " + sijainti + ", "
            ei = ei + " " + yksi
            ei_hakusanoilla.config(text="Ei hakutuloksia hakusanoilla:")
            hakusanoilla.config(text=ei)
        else:
            if boolean == True:
                self.ilmoitus_sata.config(text="Koska tuloksia on yli 100 sanoilla" + yksi + " ja " + sijainti + ". Kaikkia ei haettu.")
            if hakukone == 1:
                taulukko.to_csv("Duunitori_" + yksi + "_" + sijainti + ".csv", encoding="utf-8")
            elif hakukone == 2:
                taulukko.to_csv("Tyovoimatoimisto_" + yksi + "_" + sijainti + ".csv", encoding="utf-8")
            self.tiedostojen_sijainti.config(text="Tiedostot löytyvät kansiosta blaa blaa.")
            #print("haku loppui. " + str(time.time()-start_time))

    def hakusivun_valinta(variable, self):
        #print("Tuli hakusivun valintaan")
        sana, paikka = self.hakusana_kentta.get(), self.sijainti_kentta.get()
        if len(sana) == 0:
            sana = " "
        if len(paikka) == 0:
            paikka = " "
        if (self.duunitori_luku.get() == 1):
            teksti = self.duunitori_tekstista.get()
            if teksti == " ":
                teksti = ""
            erotus = self.option.get()
            kone = 1
            for s in sana.split(" "):
                for p in paikka.split(" "):
                    #print("menee duunitori_hakuun. " + str(time.time()-start_time))
                    (lista, onko_yli_sata) = suorita_haku_duunitori(s, p, teksti, erotus)
                    #print("menee tulosten arviointiin duunitorin jälkeen. " + str(time.time()-start_time))
                    call_search_to_get_results.tuloksien_arviointi(variable, self, lista, onko_yli_sata, s, p, kone)
            #conf_widgets(True)
        if (self.tyokkari_luku.get() == 1):
            julkaistu = str(self.option.get())
            kone = 2
            for s in sana.split(" "):
                for p in paikka.split(" "):
                    #print("menee työkkärin hakuun. " + str(time.time()-start_time))
                    (lista, onko_yli_sata, liikaa) = suorita_haku_tyovoimatoimisto(s, p, julkaistu)
                    if liikaa == True:
                        self.rajaa.config(text="Rajaa työvoimatoimiston hakua.")
                        #print("Rajaa työvoimatoimiston hakua." + "Aikaa kului: " + str(time.time()-start_time))
                        continue
                    #print("menee tulosten arviointiin työkkärin jälkeen.. " + str(time.time()-start_time))
                    call_search_to_get_results.tuloksien_arviointi(variable, self, lista, onko_yli_sata, s, p, kone)
            #conf_widgets(True)

class start(object):
    def __init__(variable):
        pass
    
    def take_input(variable, self):
        global start_time
        start_time = time.time()
        self.ei_hakusanoilla.config(text=" ")
        self.rajaa.config(text=" ")
        self.ei_sivustoa.config(text="")
        global ei
        ei = ""
        if self.tallenna.get() == 1:
            words = self.hakusana_kentta.get()
            #words, locations, locations = hakusana_kentta.get(), sijainti_kentta.get(), duunitori_tekstista.get()
            locations = self.sijainti_kentta.get()
            text_also = self.duunitori_tekstista.get()
            x = str(self.duunitori_luku.get()) + str(self.tyokkari_luku.get())+ str(self.option.get())
            data = words + '\n' + locations + '\n' + x + '\n' + text_also
            saved_parameters = open('tallennettu_haku.txt', 'w+', encoding='utf-8')
            saved_parameters.write(data)
            saved_parameters.close()
        if (self.duunitori_luku.get() == 0) & (self.tyokkari_luku.get() == 0):
            self.ei_sivustoa.config(text="Valitse joku hakusivu.")
            print("hakusivua ei valittu. " + str(time.time()-start_time))
        else:
            print("hakusivun_valinta. " + str(time.time()-start_time))
            #conf_widgets('disable')
            #call_search_to_get_results.hakusivun_valinta()

    def load_saved_input(variable, self):
        #hakusana_kentta.delete(0, END)
        #sijainti_kentta.delete(0, END)
        global start_time
        start_time = time.time()
        words, locations, x, y = open('tallennettu_haku.txt', encoding='utf-8').read().split('\n')
        self.duunitori_luku.set(int(x[0]))
        self.tyokkari_luku.set(int(x[1]))
        self.option.set(int(x[2]))
        self.hakusana_kentta.insert(0, words)
        self.sijainti_kentta.insert(0, locations)
        self.duunitori_tekstista.set(y)
        #hakusana_kentta.config(state='disabled') # OR entry['state'] = 'disabled'
        #change.conf_widgets(False) #Miksei tää nyt toimi?
        call_search_to_get_results.hakusivun_valinta(variable, self)

class Application(Frame):
    print("Tultiin luo")
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.configureWidgets()
    def configureWidgets(self):
        #self.parent.title("Board")
        #self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)
        print("Tultiin configureWidgets")
        #Jos ei tuloksia hakusanoilla
        self.ei_hakusanoilla = tk.Label(self.parent, text=' ')
        self.ei_hakusanoilla.grid(row=3, sticky='w', pady=5, padx=5)
        self.hakusanoilla = tk.Label(self.parent, text=' ')#, width=60)
        self.hakusanoilla.grid(row=4, columnspan=4, sticky='w', pady=5, padx=5)
        
        #Rajaa työkkärin hakua
        self.rajaa = tk.Label(self.parent, text=' ')
        self.rajaa.grid(row=7, column=2, sticky='w', pady=5, padx=5)
        
        #tuloksia yli sata
        self.ilmoitus_sata = tk.Label(self.parent, text=' ')
        self.ilmoitus_sata.grid(row=5,columnspan=4, pady=5)
        
        #Ilmoitus tiedostojen sijainnista
        self.tiedostojen_sijainti = tk.Label(self.parent, text=' ')
        self.tiedostojen_sijainti.grid(row=6,columnspan=4, pady=5)
        
        #Jos ei valittu työnhakusivustoa
        self.ei_sivustoa = tk.Label(self.parent, text=' ')
        self.ei_sivustoa.grid(row=8,columnspan=4, pady=5)
        
        #Hakusanat-tekstiruutu
        self.label1 = tk.Label(self.parent, text='Hakusanat', font=('helvetica', 10)).grid(row=1, sticky='w', column=0, padx=5)
        self.hakusana_kentta = tk.Entry(self.parent)
        self.hakusana_kentta.grid(row=2, sticky='w', column=0, padx=5)
        
        #Sijainti-tekstiruutu
        self.label2 = tk.Label(self, text='Sijainti', font=('helvetica', 10)).grid(row=1, sticky='w', column=1, padx=5)
        self.sijainti_kentta = tk.Entry(self.parent)
        self.sijainti_kentta.grid(row=2, sticky='w', column=1, padx=5)
        
        #Hakusivujen valintaruudut
        self.duunitori_luku = tk.IntVar()
        self.duunitori_tekstista = tk.StringVar()
        self.tyokkari_luku = tk.IntVar()
        self.duunitori = tk.Checkbutton(self.parent, text="Duunitori.fi", variable=self.duunitori_luku, onvalue=1, offvalue=0).grid(row=7,column=0, padx=5)
        self.tekstista = tk.Checkbutton(self.parent, text="Haku myös tekstistä", variable=self.duunitori_tekstista, onvalue="&search_also_descr=1", offvalue="").grid(row=9,column=0, padx=5)
        self.tyokkari = tk.Checkbutton(self.parent, text="Työvoimatoimisto", variable=self.tyokkari_luku, onvalue=1, offvalue=0).grid(row=7,column=1, padx=5)
        
        #Hakujen rajoitus ilmoitusajankohdan mukaan
        self.tyokkari_aika = tk.Label(self.parent, text='Julkaistu')
        self.tyokkari_aika.grid(row=9, column=1, sticky='w', pady=5, padx=5)
        self.option = tk.IntVar()
        self.kaikki = Radiobutton(self.parent, text="kaikki", value=0, var=self.option).grid(row=10, column=1, sticky='w', pady=5, padx=5)
        self.vuorokausi = Radiobutton(self.parent, text="vuorokausi", value=1, var=self.option).grid(row=11, column=1, sticky='w', pady=5, padx=5)
        self.kolme_paivaa = Radiobutton(self.parent, text="3 päivää", value=2, var=self.option).grid(row=12, column=1, sticky='w', pady=5, padx=5)
        self.viikko = Radiobutton(self.parent, text="viikko", value=3, var=self.option).grid(row=13, column=1, sticky='w', pady=5, padx=5)
        
        #Tallenna haku
        self.tallenna = tk.IntVar()
        self.tallenna_haku = tk.Checkbutton(self.parent, text="Tallenna", variable=self.tallenna, onvalue=1, offvalue=0).grid(row=14,column=0, padx=5)
        
        #Tallennettu haku
        tk.Button(self.parent, text='Tallennettu haku', command=start().load_saved_input(self)).grid(row=15,column=1, columnspan=2, padx=5, pady=5)
        
        #Hae-nappi
        tk.Button(self.parent, text='Hae', command=start().take_input(self)).grid(row=14,column=0, columnspan=2, padx=5)
        #Lopetus-nappo
        tk.Button(self.parent, text='Lopeta', command=quit).grid(row=14,column=2, padx=5)

class change:
    def change_text(label, string):
        self.label()
    def conf_Widgets(string):
        boolean = string
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

def main():
    root = tk.Tk()
    root.title('Super työnhaku')
    root.geometry('500x500')
    gui = Application(root)
    root.mainloop()

if __name__ == '__main__':
    main()

