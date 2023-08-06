import json

def teste():
 print('Hello Word')
 dic = {
    "Entrevistas": [
        {
            "nome": "Chris"
        },
        {
            "nome": "Jose"
        },
        {
            "nome": "Sophia"
        },
        {
            "nome": "Chris"
        },
        {
            "nome": "Chris"
        },
        {
            "nome": "Chris"
        },
        {
            "nome": "Teste"
        },
        {
            "nome": "Teste1"
        },
        {
            "nome": "Jorge"
        },
        {
            "nome": "Marcos"
        },
        {
            "nome": "Para"
        },
        {
            "nome": "Chris"
        }
    ]
}

 cont = 0
 for i in dic['Entrevistas']:
    print(f'Hello {dic["Entrevistas"][cont]["nome"]}')
    cont += 1

def main():
 teste()
