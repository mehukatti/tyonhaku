import tkinter as tk
import openpyxl
import csv
from duunitori_haku import suorita_haku

#luo ikkunan
root= tk.Tk()
laatikko = tk.Canvas(root, width = 400, height = 300)
laatikko.pack()

#Hakusanat-tekstiruutu
label1 = tk.Label(root, text='Hakusanat')
label1.config(font=('helvetica', 10))
laatikko.create_window(100, 20, window=label1)
hakusana_kentta = tk.Entry (root)
laatikko.create_window(100, 40, window=hakusana_kentta)

#Sijainti-tekstiruutu
label2 = tk.Label(root, text='Sijainti')
label2.config(font=('helvetica', 10))
laatikko.create_window(300, 20, window=label2)
sijainti_kentta = tk.Entry (root)
laatikko.create_window(300, 40, window=sijainti_kentta)

class hakusivun_valinta: #tää koskee nyt pelkästään duunitoria
    def __init__(self, master):
        self.check = tk.IntVar()
        self.e = tk.Checkbutton(root, text="Duunitori.fi", variable=self.check)
        laatikko.create_window(100, 70, window=self.e)
        self.macro_button = tk.Button(master, text="Hae", command=self.test)
        laatikko.create_window(100, 90, window=self.macro_button)
    def test(self):
        if self.check.get():
            paikka = sijainti_kentta.get()#tee sanat muualla, jotta voit tarkistaa kaikki valitut hakusivut
            sana = hakusana_kentta.get()
            for s in sana.split(" "):
                lista = suorita_haku(s, paikka)
                if lista.empty:
                    print("Ei hakutuloksia hakusanoilla: " + s + " ja " + paikka)
                else:
                    name = "Duunitori" + s + "_" + paikka + ".csv"
                    lista.to_csv(name, encoding="utf-8")
                    print("valmis")
        else:
            print('Duunitori pois päältä. Valitse hakusivu.')
my_gui = hakusivun_valinta(root)

root.mainloop()
