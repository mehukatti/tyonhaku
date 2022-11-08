import json

def avaa_txt(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()

#ja sama withill‰
def avaa_json_sanalla(hakusana, filename):
    with open(filename) as file:
        return json.load(file)[hakusana]

def open_json(filename):
    with open(filename) as file:
        return json.load(file)

#ja sama withill‰
def write_data_to_json_with(data, filename):
    with open(filename, "w",encoding="utf8") as file:
        json.dump(data,file)
    return

def list_to_string(lista, separator):
    string = ""
    for x in lista:
        string = string + separator + x
    return string[2:]

def nolla_tyhjaksi(x): #jos k‰ytt‰j‰ ei anna teksti‰ tekstikentt‰‰n, vaihdetaan nolla-arvo tyhj‰ksi, jotta voidaan tehd‰ hakulinkki
    if len(x) == 0: x = ""
    return x