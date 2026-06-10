from selenium import webdriver 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ExCont
from time import sleep  
from function_sel import * 

def Scrap_init():

    #establcer servicio y crear objeto de driver de navegador seleccionado
    ValarDo= Service(ChromeDriverManager().install()) 
    linkDri= webdriver.Chrome(service=ValarDo) 

    #establecer conexion con pagina web mediante metodo get de werbdriver
    linkDri.get('https://www.worldoffice.cloud/#/index') 

    #busqueda de elemento mediande metodo find element de driver/ metodo click para interactuar|
    sesionGen= linkDri.find_element(By.CLASS_NAME,value='boton').click()  
    
    UserInput=WebDriverWait(linkDri, timeout=10).until(
        ExCont.element_to_be_clickable((By.CSS_SELECTOR, 'input#usuario'))
    ).send_keys("asesor6@loelectrico.co") 

    UserCont=WebDriverWait(linkDri, timeout=8).until( 
        ExCont.element_to_be_clickable((By.CSS_SELECTOR, 'input.ant-input[type="password"]'))
    ).send_keys("GAov+0716")
    
    init_session= WebDriverWait(linkDri, timeout=12).until(
        ExCont.element_to_be_clickable((By. CSS_SELECTOR, 'div[style= "width: 100%; display: flex; justify-content: center; align-items: center;"]  button.boton[type="submit"]'
        ))
    ).click() 

    linkDri.maximize_window()
    
    Busqueda= WebDriverWait(linkDri, timeout=10).until(
        ExCont.visibility_of_element_located((By. CSS_SELECTOR,'input#inputBuscar[type="text"]' ))
    ).send_keys("Gestion de productos y servicios")

    enterModProd= WebDriverWait(linkDri, timeout=20).until(
        ExCont.element_to_be_clickable((By. CSS_SELECTOR, 'mat-option#mat-option-2'))
    ).click()

    findlocker="SI" 
    regulus=0

    while findlocker == "SI":

        inpForm= str(input("ingrerese el grupo a almacenar: ")) 

        if regulus>0: 

            Brujula= By.CSS_SELECTOR,'div.contTheme.panel_colapsar > a'
            CardexDom= By.CSS_SELECTOR,'div.ng-star-inserted input#pruebaTextField-'
            CordsDom= By.CSS_SELECTOR,'div.colGrid6.flex.contenedorBotonesListadoConsulta button.botonesListadoConsulta.botonBackgroundColor.flex'

            desplegar(linkDri, Brujula)
            Cleaner_input(linkDri, CardexDom, inpForm,) 

            for x in range (0,2,1): 
                Malphite_Click(linkDri, CordsDom)

        else: 

            ingresoGrup= WebDriverWait(linkDri, timeout=10).until( 
                ExCont.element_to_be_clickable((By.CSS_SELECTOR, 'div.ng-star-inserted input#pruebaTextField-'))
            ).send_keys(inpForm) 

            for i in range(0,2,1):
                actionIng= WebDriverWait(linkDri, timeout=10).until(
                    ExCont.element_to_be_clickable((By. CSS_SELECTOR, 'div.colGrid6.flex.contenedorBotonesListadoConsulta button.botonesListadoConsulta.botonBackgroundColor.flex'))
                ).click()

        try:
            content_querry= WebDriverWait(linkDri, timeout=12).until(
                ExCont.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.ng-star-inserted td.textCenter')) 
            ) 
        except: 
            content_querry=[]

        if len(content_querry)>0:   
            #---------funcion scrap--------
            Scrap_ruler(linkDri) 
            break
        else:  
            regulus+=1 
            print(f"no exiten resultados para {inpForm}")
            findlocker= str(input("Reintentar Si - NO ")).upper() 

            while findlocker!= "SI" and findlocker!= "NO": 
                print(f"OPCION INVALIDA") 
                findlocker= str(input("Reintentar Si - NO ")).upper()  
    
    sleep(20) 

    try:
        linkDri.quit()
    except Exception:
        pass
    return

    