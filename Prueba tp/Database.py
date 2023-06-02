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
        except sqlite3.Error:
            print("SQL::BAD REQUEST")
            res = -1
        return res