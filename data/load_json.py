import json

def data_loader(caminho:str):
    with open(caminho,"r") as file:
        data = json.load(file)
    return data