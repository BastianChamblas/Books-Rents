import mysql.connector
from django.conf import settings
from django.contrib.auth.hashers import check_password
import tkinter as tk
from tkinter import messagebox

# Configurar Django manualmente
settings.configure(
    PASSWORD_HASHERS=[
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    ]
)

# Función para verificar el hash de la base de datos
def obtener_hash_usuario(email):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbacapstone"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM app_customuser WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result[0]  # Extraer el valor de la tupla
        return None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {err}")
        return None

# Función para verificar la contraseña
def verificar_contraseña(email, contraseña):
    hash_almacenado = obtener_hash_usuario(email)
    if hash_almacenado:
        return check_password(contraseña, hash_almacenado)
    return False

# Función que se ejecuta al hacer clic en el botón "Login"
def login():
    email = email_entry.get()
    contraseña = password_entry.get()

    if verificar_contraseña(email, contraseña):
        messagebox.showinfo("Login exitoso", "¡Contraseña correcta!")
    else:
        messagebox.showerror("Error de autenticación", "Correo o contraseña incorrectos")

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Login de usuario")

# Crear el formulario de login
tk.Label(root, text="Correo electrónico:").grid(row=0, column=0, padx=10, pady=10)
email_entry = tk.Entry(root)
email_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Botón de Login
login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Iniciar el loop principal de Tkinter
root.mainloop()
