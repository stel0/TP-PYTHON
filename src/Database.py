import sqlite3

class Database:
    conn = None
    cur = None
    def __init__(self,filename):
        self._filename = filename #El nombre de la base de datos
    def connect(self):
        self.conn = sqlite3.connect(self._filename) #conecta con la base de datos
        self.cur = self.conn.cursor() # crea un cursor/puntero a la base de datos

    def disconnect(self):
        if self.conn:
            self.conn.close()
    
    """
        tabla: string con la tabla en la cual insertamos los datos
        values: diccionario conteniendo los datos a ser ingresados
    """

    def insertarData(self,table,values):
        columnas=""
        valores=""
        valores_lista=[]        
        for key in values:
            columnas+=key+","
            valores+="?,"
            valores_lista.append(values[key])
        columnas = columnas[0:len(columnas)-1]
        valores = valores[0:len(valores)-1]
        query = f"INSERT INTO {table} ({columnas}) VALUES ({valores});"
        valores_tuple = tuple(valores_lista)
        self.cur.execute(query,valores_tuple)
        self.conn.commit()

    """
        tabla: tabla de la cual buscamos los datos
        condition: condicion para el where, si no se pasa se devuelve todo lo de la tabla
        columns: columnas que queremos de la busqueda, si no se pasa se devuelven todas las columnas
    """

    def buscarData(self, tabla, condition:str =None, columns:list =None):
        # preparacion de la query a ser realizada
        columnas = "*"
        if columns != None:
            columnas = ""
            for i in range(len(columns)-1):
                columnas += columns[i] + ", "
            columnas += columns[len(columns)-1]    
        stmt = f"SELECT {columnas} FROM {tabla}"
        if condition != None:
            stmt += " WHERE " + condition

        print(stmt)
        try:
            self.cur.execute(stmt)
            res = self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"SQL::BAD REQUEST {e}")
            res = -1
        return res
    
    """
    Funcion para hacer un update query simple, no implementa ORDER BY ni LIMIT
    tabla: la tabla a ser modificada
    columns: lista de str con el nombre de las columnas a ser modificadas
    condition: condicion para saber que fila modificar
    """
    def updateData(self, tabla: str, columns: list, values:list, condition: str):
        columnas = ""
        # teniendo en cuenta la naturaleza del update, la longitud de values es la misma que columns
        for i in range(len(columns)-1):
            if type(values[i]) != str:
                columnas += columns[i] + f" = {values[i]}, "
            else:
                columnas += columns[i] + f" = '{values[i]}', "
        if type(values[len(columns)-1]) != str:
            columnas += columns[len(columns)-1] + f" = {values[len(columns)-1]}"
        else:
            columnas += columns[len(columns)-1] + f" = '{values[len(columns)-1]}'"
        
        stmt = f"UPDATE {tabla} SET {columnas} WHERE {condition}"
        print(stmt)

        try:
            self.cur.execute(stmt)
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return
        self.conn.commit()
        
        """
    Funcion para Borrar
    tabla: la tabla a ser modificada
    condition: condicion para saber que fila borrar
    """
    def deleteRecord(self, tabla: str, condition: str):
        stmt = f"DELETE from {tabla} WHERE {condition}"
        try:
            self.cur.execute(stmt)
        except sqlite3.Error as e:
            print(f"Error: {e}")
            return
        self.conn.commit()