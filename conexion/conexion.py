import mysql.connector
from mysql.connector import Error

def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='desarrollo_web'
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None