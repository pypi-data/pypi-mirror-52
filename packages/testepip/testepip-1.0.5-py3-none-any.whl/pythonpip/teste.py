import json

def teste():
 print('Hello Word')
 ler = open('pythonpip//dados.json','r')
 dic = json.load(ler)
 cont = 0
 for i in dic['Entrevistas']:
    print(f'Hello {dic["Entrevistas"][cont]["nome"]}')
    cont += 1

def main():
 teste()
