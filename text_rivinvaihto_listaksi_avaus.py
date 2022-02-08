import openpyxl

#aputiedostojen sijainti
asetuksetKansio = 'C:/pythontestit/'

#avaa textitiodoston ja muuttaa rivinvaihdot listan "soluiksi"
def txt_listaksi(tiedosto):
     lista = open(asetuksetKansio + tiedosto, encoding='utf-8').read().split('\n')
     return lista;