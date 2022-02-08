import tkinter as tk
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

#muodostaa linkit valituille sivuille
def kysy_hakusanat (sivu):
    sana = hakusana_kentta.get()
    paikka = sijainti_kentta.get()
    if sivu == 1:
        #tässä voisi mennä toiseen metodiin eri tiedostossa
        Duunitori = "https://duunitori.fi/tyopaikat/?haku=" + sana + "&alue=" + paikka
        print(suorita_haku(Duunitori))
    else:
        print('Valitse hakusivu') #tää pitäis tulla siihen ikkunaan eikä komentoriville

class hakusivun_valinta: #tää koskee nyt pelkästään duunitoria
    def __init__(self, master):
        self.check = tk.IntVar()
        #voiko osan nappuloista luoda tän classin ulkopuolella? Ei, koska self ei ole määritelty
        self.e = tk.Checkbutton(root, text="Duunitori.fi", variable=self.check)
        laatikko.create_window(100, 70, window=self.e)

        self.macro_button = tk.Button(master, text="Hae", command=self.test)
        laatikko.create_window(100, 90, window=self.macro_button)

    def test(self):
        if self.check.get():
            print('Duunitori valittu')
            Duunitori_tarkistus = 1
            kysy_hakusanat(Duunitori_tarkistus)

        else:
            print('Duunitori pois päältä')
            Duunitori_tarkistus = 0
            kysy_hakusanat(Duunitori_tarkistus)
        
my_gui = hakusivun_valinta(root)

root.mainloop()
