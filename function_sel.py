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
from Modelos.ConexionDb import ConexionDB_Automat_Edelcosas


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

def Scrap_ruler(LinkDri,inpForm):

    freeze= WebDriverWait(LinkDri,timeout=20) 

    Rulacaze=1  

    Time_reset = time.time()

    Interval= 25 * 60

    while True:      

        if time.time() - Time_reset >= Interval: 

            print("Recargando CRM") 

            Reborn_scrap( 
                LinkDri,
                inpForm, 
                Rulacaze
            )

            # Reiniciar el contador para que el evento vuelva a dispararse
            # solo después de otros `Interval` segundos
            Time_reset = time.time()
            print(f"Timer reiniciado tras Reborn_scrap (esperando {Interval}s)")

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


def Invocador_ultima(): 

    Ruta_inv= Path(r"C:\Users\AUXSISTEMAS\Desktop\selenium pruebas\Execel_inventarios") 

    ArchivosInv= list( 
        Ruta_inv.glob("Inventario_Actual_*.xlsx")
    ) 

    if not ArchivosInv: 
        raise FileNotFoundError(
            "sin inventarios de referencia"
        )

    Last_Alejandria= max(
        ArchivosInv, 
        key= lambda x: x.stat().st_mtime
    ) 

    return Maker.read_excel(Last_Alejandria)

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
 
def normalizar_iva(valor):

    return (
        str(valor)
        .replace("%", "")
        .replace(" ", "")
        .replace(".0", "")
        .strip()
    )

def sincronicle_DataBase(): 

    Referencia_INV= Invocador_ultima() 

    AutoDB= ConexionDB_Automat_Edelcosas() 

    if not AutoDB.LinkDb(): 
        return
    
    Db_Marca= Maker.DataFrame (AutoDB.busqueda( 
        "SELECT IdMarc, NombreMarc FROM marca WHERE EstadoMarc = '1'; "
    ))

    DB_grupoInv= Maker.DataFrame (AutoDB.busqueda( 
        "SELECT IdGrupoinv, NombGrup  FROM  grupo_inventario WHERE Estado= '1'; "
    ))

    DB_Contabilizacion= Maker.DataFrame (AutoDB.busqueda( 
        "SELECT IdCont, Grupo_cont FROM  contabilizacion WHERE Estado_Gcont= '1'"
    ))

    DB_Clasificacion= Maker.DataFrame (AutoDB.busqueda( 
        "SELECT IdClasifi, NombClasificacion FROM clasificacio_item WHERE Estado_Clasific= '1'"
    ))  

    #Marcas comparacion ----------------------------------------------------------------|

    Marcas_Actu= set(Db_Marca["NombreMarc"].astype(str).str.upper()) 

    MarcasInv=(  
        Referencia_INV["Marca"].dropna().astype(str).str.upper().unique()
    ) 

    for MrcActu in MarcasInv: 
        
        if MrcActu not in  Marcas_Actu: 

            AutoDB.Alterar_Db( 
                """
                    INSERT INTO marca(NombreMarc) values(%s)
                """, 
                (MrcActu,)
            )  

            print(f"Nueva marca {MrcActu}") 

    Db_Marca= Maker.DataFrame (AutoDB.busqueda( 
     "SELECT IdMarc, NombreMarc FROM marca WHERE EstadoMarc = '1'; "
    ))
    #-------------------------------------------------------------------------------------|
        
    #Grupo de inventario comparacion ----------------------------------------------------------------|

    GrupoInventario_actu= set(DB_grupoInv["NombGrup"].astype(str).str.upper()) 

    GrupoInv=( 
        Referencia_INV["Grup_Inv"].dropna().astype(str).str.upper().unique()
    ) 

    for GrupInvActu in GrupoInv: 

        if GrupInvActu not in GrupoInventario_actu: 

            AutoDB.Alterar_Db(

                """
                INSERT INTO grupo_inventario(NombGrup) VALUES (%s)
                """, 
                (GrupInvActu,)
            ) 

            print(f"nuevo grupo inventario {GrupInvActu}")

    DB_grupoInv= Maker.DataFrame (AutoDB.busqueda( 
        "SELECT IdGrupoinv, NombGrup FROM  grupo_inventario WHERE Estado= '1'; "
    ))
    #------------------------------------------------------------------------------------------------|

    #Grupo de contabilizacion comparacion -----------------------------------------------------------| 

    Contabilizacion_Actu= set(DB_Contabilizacion["Grupo_cont"].astype(str).str.upper()) 

    ContabilizacionINV= (Referencia_INV["Contabilizacion"].dropna().astype(str).str.upper().unique() ) 

    for ContaInvActu in ContabilizacionINV: 

        if ContaInvActu not in Contabilizacion_Actu: 
             
             AutoDB.Alterar_Db(
                 """
                    INSERT INTO contabilizacion(Grupo_cont) VALUES (%s)
                 """, 
                 (ContaInvActu,)
             ) 

             print(f"nuevo grupo contable {ContaInvActu}") 

    DB_Contabilizacion= Maker.DataFrame (AutoDB.busqueda( 
        "SELECT IdCont, Grupo_cont FROM  contabilizacion WHERE Estado_Gcont= '1'"
    ))
    #------------------------------------------------------------------------------------------------|

    #Clasificacion-----------------------------------------------------------------------------------|  

    Clasificacion_Actu= set(DB_Clasificacion["NombClasificacion"].astype(str).str.upper()) 

    ClasificacionINV=( 
        Referencia_INV["Clasificacion"].dropna().astype(str).str.upper().unique()
    ) 

    for RefeINVActu in ClasificacionINV: 

        if RefeINVActu not in Clasificacion_Actu: 

            AutoDB.Alterar_Db( 
                """
                    INSERT INTO clasificacio_item(NombClasificacion) VALUES (%s) 
                """,
                (RefeINVActu,)
            ) 

            print(f"nueva clasificacion {RefeINVActu}") 

    DB_Clasificacion= Maker.DataFrame (AutoDB.busqueda( 
        "SELECT IdClasifi, NombClasificacion FROM clasificacio_item WHERE Estado_Clasific= '1'"
    ))

    #------------------------------------------------------------------------------------------------|  



    # Igualar foraneas marcas -----------------------------------------------------------------------| 

    Referencia_INV["Marca_Auxiliar"]=(
        Referencia_INV["Marca"].astype(str).str.upper())
    

    Db_Marca["NombreMarc"]=( 
        Db_Marca["NombreMarc"].astype(str).str.upper()
    ) 


    Referencia_INV= Referencia_INV.merge( 
        Db_Marca, 
        left_on= "Marca_Auxiliar",
        right_on= "NombreMarc", 
        how="left"
    )  

    Referencia_INV.rename( 
        columns={"IdMarc":"Marca_ID"}, 
        inplace=True
    )

    #------------------------------------------------------------------------------------------------|   

    # Igualar foraneas Grupo inventario -------------------------------------------------------------|
    
    Referencia_INV["AuxGrup_Inv"]=(
        Referencia_INV["Grup_Inv"].astype(str).str.upper())
    

    DB_grupoInv["NombGrup"]=( 
        DB_grupoInv["NombGrup"].astype(str).str.upper()
    ) 


    Referencia_INV= Referencia_INV.merge( 
        DB_grupoInv, 
        left_on= "AuxGrup_Inv",
        right_on= "NombGrup", 
        how="left"
    )  

    Referencia_INV.rename( 
        columns={"IdGrupoinv":"ID_GrupInv"}, 
        inplace=True
    )

    #------------------------------------------------------------------------------------------------|

    # Igualar foraneas contabilizacion --------------------------------------------------------------|

    Referencia_INV["AuxContabilizacion"]=(
        Referencia_INV["Contabilizacion"].astype(str).str.upper())
    

    DB_Contabilizacion["Grupo_cont"]=( 
        DB_Contabilizacion["Grupo_cont"].astype(str).str.upper()
    ) 


    Referencia_INV= Referencia_INV.merge( 
        DB_Contabilizacion, 
        left_on= "AuxContabilizacion",
        right_on= "Grupo_cont", 
        how="left"
    )  

    Referencia_INV.rename( 
        columns={"IdCont":"Contabilizacion_ID"}, 
        inplace=True
    )

    #------------------------------------------------------------------------------------------------|


    # Igualar foraneas clasificacion ----------------------------------------------------------------| 

    Referencia_INV["AuxClasificacion"]=(
        Referencia_INV["Clasificacion"].astype(str).str.upper())
    

    DB_Clasificacion["NombClasificacion"]=( 
        DB_Clasificacion["NombClasificacion"].astype(str).str.upper()
    ) 


    Referencia_INV= Referencia_INV.merge( 
        DB_Clasificacion, 
        left_on= "AuxClasificacion",
        right_on= "NombClasificacion", 
        how="left"
    )  

    Referencia_INV.rename( 
        columns={"IdClasifi":"Clasificacion_ID"}, 
        inplace=True
    )

    #------------------------------------------------------------------------------------------------| 

    Referencia_INV.drop(
        columns=[
            "Marca_Auxiliar",
            "NombreMarc",
            "AuxGrup_Inv",
            "NombGrup",
            "AuxContabilizacion",
            "Grupo_cont",
            "AuxClasificacion"
        ],
        inplace=True,
        errors="ignore"
    )

    ItemsDB= Maker.DataFrame (AutoDB.busqueda( 
       'SELECT * FROM itemlog where EstadoItem = "1" '
    ))  

    if ItemsDB.empty: 

        SkuItemDb= {}

    else: 
        
        SkuItemDb= (ItemsDB
        .set_index("Sku_item")
        .to_dict("index")
        ) 


    for _, Item_Fila_reigisto in Referencia_INV.iterrows(): 
         
        codigo_SKu= str(Item_Fila_reigisto["sku"]) 

        if codigo_SKu not in SkuItemDb: 

            AutoDB.Alterar_Db( 
                """
                INSERT INTO itemlog(
                Sku_item,
                DescItem,
                Unidad_medida,
                Iva,
                Referencia,
                IDmarcaIt,
                IDgrupoIt,
                IDcontabilizacion,
                IDclasificacionIt
                )
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, 
                (codigo_SKu, 
                Item_Fila_reigisto["Descripcion"], 
                Item_Fila_reigisto["Unit_Med"], 
                Item_Fila_reigisto["IVA"], 
                Item_Fila_reigisto["Referencia"], 
                Item_Fila_reigisto["Marca_ID"],
                Item_Fila_reigisto["ID_GrupInv"],
                Item_Fila_reigisto["Contabilizacion_ID"],
                Item_Fila_reigisto["Clasificacion_ID"]
                )
            ) 

            print(f"Trasladando item {codigo_SKu} a DB")

        else: 

            AlterItemDB= SkuItemDb[codigo_SKu] 

            Alters=( 

                str(AlterItemDB["DescItem"]) != str(Item_Fila_reigisto["Descripcion"])
                or str(AlterItemDB["Unidad_medida"]) != str(Item_Fila_reigisto["Unit_Med"])  
                or str(AlterItemDB["Iva"]) != normalizar_iva(Item_Fila_reigisto["IVA"])
                or str(AlterItemDB["Referencia"]) != str(Item_Fila_reigisto["Referencia"])
                or str(AlterItemDB["IDmarcaIt"]) != str(Item_Fila_reigisto["Marca_ID"]) 
                or str(AlterItemDB["IDgrupoIt"]) != str(Item_Fila_reigisto["ID_GrupInv"])
                or str(AlterItemDB["IDcontabilizacion"]) != str(Item_Fila_reigisto["Contabilizacion_ID"]) 
                or str(AlterItemDB["IDclasificacionIt"]) != str(Item_Fila_reigisto["Clasificacion_ID"])
            ) 

            if Alters: 

                AutoDB.Alterar_Db( 
                    """"
                    UPDATE itemlog SET  
                    DescItem=%s,
                    Unidad_medida=%s,
                    Iva=%s,
                    Referencia=%s,
                    IDmarcaIt=%s,
                    IDgrupoIt=%s,
                    IDcontabilizacion=%s,
                    IDclasificacionIt=%s

                    WHERE Sku_item=%s
                    """, 
                    ( 
                        Item_Fila_reigisto["Descripcion"], 
                        Item_Fila_reigisto["Unit_Med"], 
                        Item_Fila_reigisto["IVA"], 
                        Item_Fila_reigisto["Referencia"], 
                        Item_Fila_reigisto["Marca_ID"],
                        Item_Fila_reigisto["ID_GrupInv"],
                        Item_Fila_reigisto["Contabilizacion_ID"],
                        Item_Fila_reigisto["Clasificacion_ID"], 
                        codigo_SKu
                    )
                ) 
            else: 
                print(f"item {codigo_SKu} sin cambios aparentes")

def Reborn_scrap (LinkDri, inpForm, Rulacaze): 

    LinkDri.refresh() 

    sleep(10) 

    Volver_resultados(LinkDri)

    Re_busqueda(LinkDri,inpForm) 

    Cardinal_indice(LinkDri,Rulacaze) 

    print(f"Estado recuperado. Indice{Rulacaze}")

    
def Volver_resultados (LinkDri): 

    Modulo = WebDriverWait(LinkDri, timeout=12).until(
        ExCont.element_to_be_clickable((By.XPATH, '//div[contains(@class,"tab-header") and contains(.,"Gestión de Productos y Servicios")]'))
    )

    LinkDri.execute_script(
        """
            arguments[0].click();
        """,
        Modulo,
    ) 

    sleep(3)

def Re_busqueda(LinkDri,inpForm): 

    print("buscando nuevamente") 
    Busqueda = WebDriverWait(LinkDri, timeout=12).until(
        ExCont.presence_of_element_located((By.CSS_SELECTOR, "div.ng-star-inserted input#pruebaTextField-"))
    )

    Busqueda.clear()
    Busqueda.send_keys(inpForm)

    Action = WebDriverWait(LinkDri, timeout=12).until(
        ExCont.element_to_be_clickable((By.CSS_SELECTOR, 'div.colGrid6.flex.contenedorBotonesListadoConsulta button.botonesListadoConsulta.botonBackgroundColor.flex'))
    )

    for i in range(0, 2, 1):
        LinkDri.execute_script(
            """
            arguments[0].click();
            """,
            Action,
        )

        WebDriverWait( LinkDri, timeout=20).until(
            ExCont.presence_of_element_located(
            (By.CSS_SELECTOR,'tbody tr.ng-star-inserted'))) 
        
        print(f"Resultados restaurados")


def Cardinal_indice(LinkDri,Rulacaze): 

    HandScrolMarts = WebDriverWait( LinkDri, timeout=10).until(
        ExCont.presence_of_element_located((
            By.CSS_SELECTOR,
            'cdk-virtual-scroll-viewport'
        )))
    
    while True: 

        filas = LinkDri.find_elements(
            By.CSS_SELECTOR,
            'tbody tr.ng-star-inserted'
        )

        for fila in filas:

            try:

                numero = fila.find_elements(
                    By.CSS_SELECTOR,
                    'td'
                )[0].text.strip()

                if numero == str(Rulacaze):

                    print(
                        f"Índice {Rulacaze} localizado"
                    )

                    return

            except:

                continue

        LinkDri.execute_script(
            """
            arguments[0].scrollTop += 350;
            """,
            HandScrolMarts
        )

        sleep(1)
        
