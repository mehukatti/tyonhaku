import os
import csv
import subprocess
#tasks = csv.DictReader(subprocess.check_output("tasklist /fo csv").splitlines())
#prosessit = os.system('tasklist')
prosessit = str(prosessit).split("\r\n")
prosessit = subprocess.check_output('tasklist')#.split(None)
print(prosessit)
#tallennetut_prosessit = open('C:/pythontestit/' + 'prosessit.txt', 'w+', encoding='utf-8')
#for prosessi in prosessit:
    #tallennetut_prosessit.write(prosessi)
#tallennetut_prosessit.close()
#prosessit = open('C:/pythontestit/' + 'prosessit.txt', 'w+', encoding='utf-8')
#pkill -f tyovoimatoimisto_selenium.py
