from openpyxl import Workbook
import openpyxl
#pitäskö duunitorin kategorioita käsittelevät työntää samaan luokkaan ja kielletyt hakusanat toiseen luokkaan?
#kielletyt hakusanat tarkistettaisiin myös työkkärin haussa

#avaa kieltolista lukumuodossa
def kieltolista_luku():
     kieltolista = open('C:/pythontestit/' + 'kielletyt_kategoriat_duunitori.txt', encoding='utf-8').read().split('\n')
     print("kieltolista avattu")
     return kieltolista;

def osuvuudet():
    kielletyt = kieltolista_luku()
    wb = openpyxl.load_workbook('C:\pythontestit\Hakutulokset.xlsx', read_only=True) #täältä otetaan kielletyt ja lisätään listalle
    ws = wb.active
    for row in ws.iter_rows(min_col=7, max_col=7):
        for cell in row:
            if cell.value == 0:
                #jos on nollia, onko kategoria jo kiellettyjen joukossa
                #print(ws.cell(row=cell.row, column=6).value)
                if ws.cell(row=cell.row, column=6).value not in kielletyt:
                    kielletyt.append(str(ws.cell(row=cell.row, column=6).value))
    apu = ""
    for item in kielletyt:
        apu += item + '\n' #saisko tän forin kanssa samaan riviin?
    print(3)
    print(kielletyt)
    istunto = open('C:/pythontestit/' + 'kielletyt_kategoriat_duunitori.txt', 'w+', encoding='utf-8')
    print(istunto)
    istunto.write(apu)
    istunto.close()
    print("valmis")
    return;