from function_sel import * 
from prueba1selenium import Scrap_init


print("GESTOR INVENTARIOS WORLD CLOUD \n") 


otrOp=[1,2,3,4]

while True:   

    print('''

    1/Extraccion 
    2/Archivo Historico
    3/Edicion de Marcas y referencias 
    4/Salida

    ''')   

    try:
        OpMenu= int(input("Ingrese opcion: "))

        if OpMenu not in otrOp:  
            print(f"Opcion {OpMenu} invalida ")  
            continue

       

    except ValueError:  
        print("solo opciones numerica valida") 
        continue

    if OpMenu == 1: 
        Scrap_init()

    elif OpMenu== 2:  
        sincronicle_DataBase()

    elif OpMenu == 3:  
        print("edicion")

    elif OpMenu == 4: 
        break

print("---------------------------------------------| END SCRIPT |-----------------------------------------------")

