from selenium import webdriver 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ExCont
from time import sleep   
from selenium.common.exceptions import ElementClickInterceptedException  
from Master_mod import ProdsSport 
import pandas as Maker 
import openpyxl 
from datetime import datetime

InDex_memo_ram=[]

def Malphite_Click(LinkDri, CordsDom): 
    
    actionfilt= WebDriverWait(LinkDri, timeout=7).until(
        ExCont.element_to_be_clickable(CordsDom)
    ) 

    try: 
        actionfilt.click() 
    except ElementClickInterceptedException: 

        sleep(4) 

        LinkDri.execute_script( 
            "arguments[0].click();", 
            actionfilt
        )

def Cleaner_input(LinkDri, CardexDom, busqPut): 
    
    Filterput= WebDriverWait(LinkDri, timeout=7).until( 
        ExCont.element_to_be_clickable(CardexDom)
    ) 

    try: 

        Filterput.clear() 
        Filterput.send_keys(busqPut)  

    except ElementClickInterceptedException: 

        sleep(4) 

        LinkDri.execute_script( 
            
        """
        arguments[0].value=''; 

        arguments[0].dispatchEvent(
            new Event('input')
        ); 

        arguments[0].value= arguments[1]; 

        arguments[0].dispatchEvent(
            new Event('change')
        );    

        """, Filterput, busqPut
        )  

def desplegar (linkDri, Brujula): 

    Rollo= WebDriverWait(linkDri,  timeout=7).until( 
        ExCont.element_to_be_clickable(Brujula)
    ) 

    try:  
        Rollo.click()
    except ElementClickInterceptedException: 

        sleep(3) 

        linkDri.execute_script( 
            """
              arguments[0].click  
            """
        )

def Scrap_ruler(LinkDri):

    freeze= WebDriverWait(LinkDri,timeout=20) 

    HandScrolMarts= WebDriverWait(LinkDri, timeout=3).until(
        ExCont.presence_of_all_elements_located((By.CSS_SELECTOR,'nz-table-inner-scroll')))

    Rulacaze=1 

    while True: 

        print(f"Buscando indice -> {Rulacaze}")  

        #ubicar indice de registro en tabla para comparacion/solo de registros visibles 

        Find_code= None 

        while Find_code is None:  

            Content_table= WebDriverWait(LinkDri, timeout=5).until( 
                ExCont.presence_of_all_elements_located((By. CSS_SELECTOR,'tbody tr.ng-star-inserted'))
            )  

            for finderCodes in Content_table: 

                try: 

                    Numero_deFila= Content_table.find_element(By.CSS_SELECTOR,'td.textCenter:nth-child(1)').text.strip()

                    if Numero_deFila == str(Rulacaze):  

                        Find_code= Numero_deFila 

                        break

                except:  

                    continue 

            #scrolls para buscar si no 
         
            if Find_code is None:  

                print(f"sroll en busca de mas informacion")  

                First_fallIndex= Content_table[-1].find_element(By.CSS_SELECTOR,'td.textCenter:nth-child(1)').text.strip() 

                LinkDri.execute_script(
                    """
                    arguments[0].scrollTop +=1500;
                    """,HandScrolMarts
                ) 

                sleep(13) 

                New_Content_table=  WebDriverWait(LinkDri, timeout=5).until( 
                ExCont.presence_of_all_elements_located((By. CSS_SELECTOR,'tbody tr.ng-star-inserted'))
                ) 

                Second_fallIndex= New_Content_table[-1].find_element(By.CSS_SELECTOR,'td.textCenter:nth-child(1)').text.strip() 

                if First_fallIndex == Second_fallIndex: 

                    print(f"no existen resultados") 

                    exit()

        # ingreso a modulo editar  

        print(f"resultado {Find_code} encontrado")

        OptionsAcccest= WebDriverWait(Find_code, timeout=7).until(
            ExCont.element_to_be_clickable((By.CSS_SELECTOR,'a#opcionesV2'))
        ) 

        LinkDri.execute_script(
            """
            arguments[0].click();
            """,OptionsAcccest
        ) 


        EditModulo= WebDriverWait(LinkDri, timeout=5).until( 
            ExCont.element_to_be_clickable((By. CSS_SELECTOR,'button#boton-Editar'))
        ) 

        LinkDri.execute_srcipt( 
            """
            arguments[0].click();
            """,EditModulo
        )


        Cordmodulo= WebDriverWait(LinkDri, timeout=5).until( 
            ExCont.presence_of_element_located((By. XPATH,"//span[contains(text(),'Detalle de Producto/Servicio')]"))
        ) 

        if Cordmodulo:  

            #Codigo sku
            ProdSku= WebDriverWait(LinkDri,timeout=5).until(
                ExCont.presence_of_element_located((By.CSS_SELECTOR,'#numero_hcodigo-select_react-cc0ept2er input.ant-input'))
            ).get_attribute("value")
             
            #Descripcio producto
            ProdDesc= WebDriverWait(LinkDri, timeout=5).until( 
                ExCont.presence_of_element_located((By.CSS_SELECTOR,'#numero_hdescripcion-select_react-iizi9jkeh input.ant-input'))
            ).get_attribute("value") 

            #Unidad de medida Prod 
            ProdUnit= WebDriverWait(LinkDri, timeout=5).until(
                ExCont.presence_of_element_located((By.CSS_SELECTOR,'#unidadMedida .ant-select-selection-item')) 
            ).text

            #Clasificacion del producto 
            ProdClasifi= WebDriverWait(LinkDri,timeout=5).until( 
                ExCont.presence_of_element_located((By.CSS_SELECTOR ,'#inventarioClasificacion .ant-select-selection-item'))
            ).text


            #Grupo de inventario 
            ProInvgrup= WebDriverWait(LinkDri, timeout=5).until(
                ExCont.presence_of_element_located((By.CSS_SELECTOR,'#tree_tree_-rc1yzbmh4 nz-tree-select .ant-select-selection-item'))
            ).text

            #porcentaje de iva    
            ProdIva= WebDriverWait(LinkDri, timeout=5).until( 
                ExCont.presence_of_element_located((By.CSS_SELECTOR,'#porcentajeIva .ant-select-selection-item'))
            ).text

            #Contabilizacion del producto
            ProdCont= WebDriverWait(LinkDri, timeout=5).until(
                ExCont.presence_of_element_located((By.CSS_SELECTOR,'#contabilizacion .ant-select-selection-item'))
            ).text
            
            #abrir menu para mas datos 

            MenuDatosxt= WebDriverWait(LinkDri, timeout=5).until( 
                ExCont.element_to_be_clickable((By.XPATH,"//nz-collapse-panel[.//span[contains(@class,'titulo__encabezado') and normalize-space(.)='Datos Personalizados']]//div[@role='button' and contains(@class,'ant-collapse-header')]"))
            ) 

            LinkDri.execute_script(
                """
                arguments[0].click();
                """,MenuDatosxt
            )  

            #marca de producto
            ProdMarca= WebDriverWait(LinkDri, timeout=5).until( 
                ExCont.presence_of_element_located((By.CSS_SELECTOR,'div#numero_htextoPrueba-select_react-sjuomz4q5 input.ant-input'))
            ).get_attribute("value") 

            #referencia de producto
            prodReferencia= WebDriverWait(LinkDri, timeout=5).until(
                ExCont.presence_of_element_located((By.CSS_SELECTOR,'div#numero_htextoPrueba-select_react-sjuomz4q5 input.ant-input'))
            ).get_attribute("value") 

            Item= ProdsSport(
            sku= ProdSku,
            Descripcion= ProdDesc,
            Unit_Med= ProdUnit,
            Clasificacion= ProdClasifi,
            Grup_Inv= ProInvgrup,
            IVA= ProdIva,
            Contabilizacion= ProdCont,
            Marca= ProdMarca,
            Referencia= prodReferencia) 

            InDex_memo_ram.append(Item)  

            Ruler_xel()

        Lookback= WebDriverWait(LinkDri, timeout=5).until( 
            ExCont.element_to_be_clickable((By.CSS_SELECTOR,'div[role="tab"][aria-controls="nz-tabs-0-tab-2"]'))
        ) 

        LinkDri.execute_script(
            """ 
            arguments[0].click;
            """,Lookback
        ) 

        WebDriverWait(LinkDri, timeout=8).until( 
            ExCont.presence_of_element_located((By.CSS_SELECTOR,'tbody tr.ng-star-inserted'))
        ) 

        sleep(1) 

        Rulacaze+=1 

def Ruler_xel(): 

    Stix= Maker.DataFrame( 

        InDex_memo_ram, 

        columns=[ 
            "Codigo", 
            "Descripcion",
            "unidad de medida",
            "Clasificacion",
            "Grupo Inventario", 
            "%Iva",
            "Contabilizacion",
            "Marca",
            "Referencia",
        ] 
    )  


    Fecha=datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    # Evitar escapes en string de Windows: usar raw string + format o pathlib/os
    Rute = r'C:\Users\AUXSISTEMAS\Desktop\selenium pruebas\Execel_inventarios\Inventario_Actual_{}'.format(Fecha) + '.xlsx'

    Stix.to_excel(
        Rute, 
        index=False, 
        engine="openpyxl"
    )            








        
    