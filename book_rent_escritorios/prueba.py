import mysql.connector
from django.conf import settings
from django.contrib.auth.hashers import check_password

# Configurar Django manualmente
settings.configure(
    PASSWORD_HASHERS=[
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    ]
)

# El resto de tu código...

# Conectar a la base de datos usando las credenciales proporcionadas
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="dbacapstone"
    )

    # Verificar si la conexión fue exitosa
    if conn.is_connected():
        print("Conexión exitosa a la base de datos")
    else:
        print("No se pudo conectar a la base de datos")

    # Obtener el hash de la contraseña almacenada
    def obtener_hash_usuario(email):
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM app_customuser WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]  # Extraer el valor de la tupla
        return None

    # Verificar la contraseña usando Django
    def verificar_contraseña(email, contraseña):
        hash_almacenado = obtener_hash_usuario(email)
        if hash_almacenado:
            print(f"Hash almacenado: {hash_almacenado}")
            return check_password(contraseña, hash_almacenado)  # Verificar con Django
        return False

    # Ejemplo de usos
    email = "admin@admin.cl"
    contraseña = "admin"
    if verificar_contraseña(email, contraseña):
        print("Contraseña correcta")
    else:
        print("Contraseña incorrecta")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if conn.is_connected():
        conn.close()
