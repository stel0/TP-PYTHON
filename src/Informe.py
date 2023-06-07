import sqlite3
import csv

# Conexión a la base de datos
conn = sqlite3.connect('base.db')
cursor = conn.cursor()

# Ejecutar una consulta SQL
cursor.execute("SELECT * FROM Persona")

# Obtener los resultados de la consulta
resultados = cursor.fetchall()

# Cerrar la conexión a la base de datos
conn.close()

# Especificar el nombre del archivo de texto
nombre_archivo = 'informe.txt'

# Escribir los resultados en el archivo de texto
with open(nombre_archivo, 'w') as archivo:
    escritor = csv.writer(archivo, delimiter='\t')
    escritor.writerows(resultados)

print("Informe generado y guardado en", nombre_archivo)