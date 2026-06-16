import mysql.connector
from mysql.connector import Error


class ConexionDB_Automat_Edelcosas(): 

    def __init__(self):
        
        self.host = "bc4kybdqpafusnb4s9wt-mysql.services.clever-cloud.com"
        self.user = "uyvygbgu0q0vlpoi"
        self.password = "9oluZ63pIOUuyY32cAwz"
        self.database = "bc4kybdqpafusnb4s9wt"
        self.port = 3306

        self.conexion = None
        self.cursor = None 

    def LinkDb(self): 

        try: 

            self.conexion= mysql.connector.connect(
                host= self.host,
                user= self.user,
                password= self.password,
                database= self.database,
                port= self.port,
            ) 

            self.cursor= self.conexion.cursor(
                dictionary=True, 
                buffered=True
            ) 

            return True 
        
        except Error as vel: 

            print(f"Error mysql{vel}") 

            return False 
        
    def busqueda(self, sql, parametros=None): 

        self.cursor.execute( 
            sql, 
            parametros or ()
        ) 

        return self.cursor.fetchall() 
    
    def busqueda_masiva(self, sql, parametros=None): 

        self.cursor.execute(
            sql, 
            parametros or ()   
        ) 

        return self.cursor.fetchone() 
    
    def Alterar_Db (self, sql, parametros= None): 
        try:
            self.cursor.execute(
                sql,
                parametros or ()
            )
            self.conexion.commit()

            return {
                "filas afectadas": self.cursor.rowcount,
                "Ultimo id": self.cursor.lastrowid,
            }

        except Error as e:
            if self.conexion:
                try:
                    self.conexion.rollback()
                except Exception:
                    pass
            raise


    def closer_enlace(self): 

        if self.cursor: 
            self.cursor.close() 

        if self.conexion: 
            self.conexion.close()

