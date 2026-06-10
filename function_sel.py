from selenium import webdriver 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ExCont
from time import sleep   
from selenium.common.exceptions import ElementClickInterceptedException   
from selenium.common.exceptions import StaleElementReferenceException
from Modelos.Master_mod import ProdsSport 
import pandas as Maker 
import openpyxl  
import os 
from datetime import datetime 
from selenium.webdriver.chrome.options import Options
from pathlib import Path 
import shutil
import time 
import unicodedata


InDex_memo_ram={}

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

    Rulacaze=1 

    while True:  

        HandScrolMarts = WebDriverWait( LinkDri, timeout=10).until(

        ExCont.presence_of_element_located((
            By.CSS_SELECTOR,
            'cdk-virtual-scroll-viewport'
        ))
        )

        print(f"Buscando indice -> {Rulacaze}")  

        #ubicar indice de registro en tabla para comparacion/solo de registros visibles 

        Find_code= None 

        while Find_code is None:  

            Content_table= WebDriverWait(LinkDri, timeout=5).until( 
                ExCont.presence_of_all_elements_located((By. CSS_SELECTOR,'tbody tr.ng-star-inserted'))
            )  

            for finderCodes in Content_table: 

                try: 

                    Columna= finderCodes.find_elements(
                        By.CSS_SELECTOR,'td'
                    )

                    Numero_deFila= Columna[0].text.strip()

                    if Numero_deFila == str(Rulacaze):  

                        Find_code= finderCodes 

                        break 

                except StaleElementReferenceException:

                    print("Angular reconstruyó la tabla")
                    break

                except Exception as e:   

                    print(e)

                    continue 

            #scrolls para buscar si no 
         
            if Find_code is None:  

                print(f"sroll en busca de mas informacion")   

                try: 

                    Content_table= WebDriverWait(LinkDri, timeout=5).until( 
                        ExCont.presence_of_all_elements_located((By. CSS_SELECTOR,'tbody tr.ng-star-inserted'))
                    )  

                    First_fallIndex= Content_table[-1].find_element(By.CSS_SELECTOR,'td').text.strip()  

                except StaleElementReferenceException:

                    print("Tabla actualizada por Angular")
                    continue

                LinkDri.execute_script(
                    """
                    arguments[0].scrollTop +=350;
                    """,HandScrolMarts
                )  

                sleep(10)

                New_Content_table=  WebDriverWait(LinkDri, timeout=5).until( 
                ExCont.presence_of_all_elements_located((By. CSS_SELECTOR,'tbody tr.ng-star-inserted'))
                ) 

                Second_fallIndex= New_Content_table[-1].find_element(By.CSS_SELECTOR,'td').text.strip() 

                if First_fallIndex == Second_fallIndex: 

                    print(f"no existen resultados")  

                    descargar_codice(LinkDri)
                    Ruler_xel() 

                    return

        # ingreso a modulo editar  

        print(f"resultado {Rulacaze} encontrado")

        OptionsAcccest= Find_code.find_element(By.CSS_SELECTOR,'a#opcionesV2')
        
        LinkDri.execute_script(
            """
            arguments[0].click();
            """,OptionsAcccest
        ) 


        EditModulo= WebDriverWait(LinkDri, timeout=5).until( 
            ExCont.element_to_be_clickable((By. CSS_SELECTOR,'button#boton-Editar'))
        ) 

        LinkDri.execute_script( 
            """
            arguments[0].click();
            """,EditModulo
        )


        Cordmodulo= WebDriverWait(LinkDri, timeout=5).until( 
            ExCont.presence_of_element_located((By. XPATH,"//span[contains(text(),'Detalle de Producto/Servicio')]"))
        )  

        def selector_Safetext(by, selector, attr=None): 

            try:  

                Elemetor= WebDriverWait(LinkDri, timeout=20).until( 
                    ExCont.presence_of_element_located((by, selector))
                ) 

                if attr: 
                    return Elemetor.get_attribute(attr) 
                
                return Elemetor.text.strip()

            except Exception as e:   

                print(f"error {e} con scrap de codigo N {Rulacaze}")
                return ""


        if Cordmodulo:    

            MaxCraps=2 

            Intend_crap=0

            while Intend_crap < MaxCraps: 

                #Codigo sku
                ProdSku= selector_Safetext(
                    By.CSS_SELECTOR,'div[id^="numero_hcodigo-select_react"] input.ant-input', 
                    "value"
                ) 

                if ProdSku == "": 

                    ProdSku="Null/value"
                
                #Descripcio producto
                ProdDesc= selector_Safetext( 
                    By.CSS_SELECTOR,'div[id^="numero_hdescripcion-select_react"] input.ant-input',
                    "value"
                )  
                if ProdDesc == "": 

                    ProdDesc="Null/value"

                #Unidad de medida Prod 
                ProdUnit= selector_Safetext(
                    By.CSS_SELECTOR,'#unidadMedida nz-select-item'
                ) 
                if ProdUnit == "": 

                    ProdUnit="Null/value"

                #Clasificacion del producto 
                ProdClasifi= selector_Safetext(
                    By.CSS_SELECTOR ,'#inventarioClasificacion nz-select-item'
                )
                if ProdClasifi == "": 

                    ProdClasifi="Null/value"

                #Grupo de inventario 
                ProInvgrup= selector_Safetext( 
                    By.CSS_SELECTOR,'wo-tree-select nz-tree-select .ant-select-selection-item'
                )
                if ProInvgrup == "": 

                    ProInvgrup="Null/value"

                #porcentaje de iva    
                ProdIva= selector_Safetext(
                    By.CSS_SELECTOR,'#porcentajeIva nz-select-item'
                ) 
                if ProdIva == "": 

                    ProdIva="Null/value"

                #Contabilizacion del producto
                ProdCont= selector_Safetext(
                    By.CSS_SELECTOR,'#contabilizacion nz-select-item'
                )
                if ProdCont == "": 

                    ProdCont="Null/value"    

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
                ProdMarca= selector_Safetext( 
                    By.XPATH,'//label[contains(.,"MARCA")]/ancestor::nz-form-item//input', 
                    "value"
                ) 
                if ProdMarca == "": 
                    ProdMarca="Null/value"


                #referencia de producto
                prodReferencia= selector_Safetext(
                    By.XPATH,'//label[contains(.,"REFERENCIA")]/ancestor::nz-form-item//input', 
                    "value"
                )  
                if prodReferencia == "": 
                    prodReferencia="Null/value"


                CompScrap=[ 
                    ProdSku,
                    ProdDesc, 
                    ProdUnit,
                    ProdClasifi, 
                    ProInvgrup,
                    ProdIva, 
                    ProdCont, 
                ] 

                if all(Contenido != "" and Contenido !="Null/value" for Contenido in CompScrap):  

                    print(f"Datos de indice {Rulacaze} cargados correctamente") 
                    break  

                Intend_crap+=1 

                sleep(2)

                print(f"Error en carga reintentando") 

                if Intend_crap >= MaxCraps: 

                    print(f"falla en scrap datos de codigo incompletos") 
                    break 

               

            InDex_memo_ram[Rulacaze]= { 
                "Indice":Rulacaze,
                "sku": ProdSku,
                "Descripcion": ProdDesc,
                "Unit_Med": ProdUnit,
                "Clasificacion": ProdClasifi,
                "Grup_Inv": ProInvgrup,
                "IVA": ProdIva,
                "Contabilizacion": ProdCont,
                "Marca":ProdMarca,
                "Referencia": prodReferencia
            } 

            print(f"Registro {Rulacaze} guardado")  

            

        Lookback= WebDriverWait(LinkDri, timeout=5).until( 
            ExCont.element_to_be_clickable((By.XPATH,'//div[contains(@class,"tab-header") and contains(.,"Gestión de Productos y Servicios")]' ))
        ) 

        LinkDri.execute_script(
            """ 
            arguments[0].click();
            """,Lookback
        ) 

        sleep(2)

        WebDriverWait(LinkDri, timeout=8).until( 
            ExCont.presence_of_element_located((By.CSS_SELECTOR,'tbody tr.ng-star-inserted'))
        ) 

        Rulacaze+=1 

 
def descargar_codice(LinkDri):  
    FolderDown = Path.home() / "Downloads"
    Forderfate = Path(r"C:\Users\AUXSISTEMAS\Desktop\selenium pruebas\Execel_inventarios\Plantilla de comparacion")

    # lista de xlsx antes de la exportación
    before = set(FolderDown.glob("*.xlsx"))

    # click export
    WebDriverWait(LinkDri, timeout=10).until(
        ExCont.element_to_be_clickable((By.XPATH,'//*[@id="paneTabs"]/app-lista-inventarios/div/app-boton-exportar/button'))
    ).click()

    print("Download element")

    # esperar a que aparezca un .crdownload (opcional)
    start = time.time()
    timeout = 60
    while time.time() - start < timeout:
        if list(FolderDown.glob("*.crdownload")):
            break
        time.sleep(0.5)

    # esperar un nuevo .xlsx (comparando con la lista previa)
    start = time.time()
    while time.time() - start < timeout:
        XlsCRM = list(FolderDown.glob("*.xlsx"))
        new = [f for f in XlsCRM if f not in before]
        if new:
            Ultima_XlsCRM = max(new, key=lambda x: x.stat().st_mtime)
            break
        time.sleep(1)
    else:
        raise FileNotFoundError("Archivo no econtrado (timeout)")

    FinalFate = Forderfate / Ultima_XlsCRM.name
    limpiarNido()
    shutil.move(str(Ultima_XlsCRM), str(FinalFate))
    print("Archivo transferido")

def limpiarNido(): 

    Folder= Path(r'C:\Users\AUXSISTEMAS\Desktop\selenium pruebas\Execel_inventarios\Plantilla de comparacion')

    for info in Folder.iterdir(): 
        try: 

            if info.is_file():  

                info.unlink() 
            
            elif info.is_dir():
                os.rmdir(info)


        except Exception as e: 

            print(f"falla en limpieza {e}") 
    print("carpeta limpia") 

def invocador(): 

    Fold2= Path(r"C:\Users\AUXSISTEMAS\Desktop\selenium pruebas\Execel_inventarios\Plantilla de comparacion")

    CompXls= list(Fold2.glob("*.xlsx")) 

    if not CompXls: 

        raise FileNotFoundError("carpeta vacia") 
    
    AcrhivoComp= max(
        CompXls, 
        key=lambda x: x.stat().st_mtime
    ) 

    return AcrhivoComp




def Ruler_xel():    

    Crm_excel= Maker.read_excel(invocador())  
   
    Crm_excel.columns = [
    unicodedata.normalize("NFKC", str(c)).strip()
    for c in Crm_excel.columns
]

    for item in InDex_memo_ram.values(): 

        PrimarCode= item["sku"]

        FilaCRMXLS= Crm_excel[Crm_excel["Código"]==PrimarCode] 

        if FilaCRMXLS.empty: 
            continue
        
        FilaCRMXLS= FilaCRMXLS.iloc[0]

        Alejandria={ 
            "Descripcion": "Descripción",
                "Unit_Med": "Unidad Medida",
                "Clasificacion": "Clasificacion",
                "Grup_Inv": "Grupo Inventario",
                "IVA": "Valor IVA",
                "Contabilizacion": "Contabilizacion",
                "Marca": "Encab: Personalizado 1",
                "Referencia": "Encab: Personalizado 2"
        } 

        for DatoDic, DatoCrm in Alejandria.items(): 

            Valor_iterDicc= item[DatoDic] 

            if Valor_iterDicc in["",None,"Null/value"]: 

                Valor_IterCMR=FilaCRMXLS[DatoCrm] 

                if Maker.notna(Valor_IterCMR):
                    
                    item[DatoDic]= str(Valor_IterCMR)
            
 # convertir diccionario a dataframe
    Stix = Maker.DataFrame(InDex_memo_ram.values())

    # ordenar por el indice del CRM
    Stix = Stix.sort_values(by="Indice")

    # generar fecha
    Fecha = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")

    # ruta final
    Rute = rf'C:\Users\AUXSISTEMAS\Desktop\selenium pruebas\Execel_inventarios\Inventario_Actual_{Fecha}.xlsx'

    # generar excel
    Stix.to_excel(
        Rute,
        index=False,
        engine="openpyxl"
    )








        
    