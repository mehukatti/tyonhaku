import docx2txt
import docx
import os
import pandas as pd
import openpyxl #tallentamista varten

Duunitori = "anus"

hakusanat = docx2txt.process("hakusanat.docx").split(" ")
#wordCount = len(hakusanat)

#Luo otsikkorivi
df = pd.DataFrame(columns = ['Hakusanat', 'Linkit']) 


for sanat in hakusanat:
    Duunitori = "https://duunitori.fi/tyopaikat/?haku=" + sanat + "&alue=Pirkanmaa"
    df = df.append(pd.DataFrame({'Hakusanat':sanat,'Linkit': Duunitori}, index=[0]), ignore_index = True)
df.to_csv('searchLinks_Duunitori.csv')

