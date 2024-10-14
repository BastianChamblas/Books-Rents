import mysql.connector

COLOR_BARRA_SUPERIOR = "#1f2329"
COLOR_MENU_LATERAL = "#2a3138"
COLOR_CUERPO_PRINCIPAL = "#f1faff"
COLOR_MENU_CURSOR_ENCIMA = "#2f88c5"

def conectar_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbacapstone"
        )

        if conn.is_connected():
            print("Conexión exitosa a la base de datos")
            return conn
        else:
            print("No se pudo conectar a la base de datos")
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

