import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import threading
import re
from django.contrib.auth.hashers import make_password
# Importar y configurar Django
import django
from django.conf import settings

# Configurar Django manualmente
settings.configure(
    PASSWORD_HASHERS=[
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    ]
)

# Inicializar Django
django.setup()



# Función de animación del botón
def animar_boton(boton, cargando_flag, ventana, texto_final="Enviar"):
    def actualizar_texto():
        if not cargando_flag[0]:  # Si cargando_flag es False, detiene la animación
            boton.config(text=texto_final)
            return

        # Animación de puntos suspensivos
        puntos = boton.cget("text").count(".") % 3 + 1
        boton.config(text="Enviando" + "." * puntos)

        # Llama a actualizar_texto después de 500 ms para animar
        ventana.after(500, actualizar_texto)

    # Iniciar la animación
    actualizar_texto()

class AgregarUsuariosForm:
    def __init__(self, master, db_config):
        """
        Inicializa el formulario de agregar usuarios.

        :param master: El widget padre donde se colocará el formulario.
        :param db_config: Diccionario con la configuración de la base de datos.
        """
        self.master = master
        self.host = db_config.get('host')
        self.user = db_config.get('user')
        self.password = db_config.get('password')
        self.database = db_config.get('database')
        self.cargando_flag = [False]  # Bandera para la animación
        self.crear_formulario_agregar_usuarios()

    def iniciar_envio(self):
        # Realizar validaciones antes de iniciar la animación
        if not self.validar_formulario():
            return  # Detener si la validación falla

        # Activar la bandera y comenzar la animación del botón
        self.cargando_flag[0] = True
        animar_boton(self.button_enviar, self.cargando_flag, self.master)

        # Iniciar el proceso de envío en un hilo separado
        threading.Thread(target=self.enviar_formulario_agregar_usuarios).start()

    def validar_formulario(self):
        # Capturar los valores de los campos del formulario
        rut = self.entry_rut.get()
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        telefono = self.entry_telefono.get()
        direccion = self.entry_direccion.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        # Verificar si los campos no están vacíos
        if not (rut and nombre and apellido and telefono and direccion and email and password):
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return False

        # Validar el RUT
        if not self.validar_rut(rut):
            messagebox.showerror("Error", "El RUT ingresado no es válido.")
            return False

        # Validar el formato del email
        if not self.validar_email(email):
            messagebox.showerror("Error", "El email ingresado no es válido.")
            return False

        # Validar que el teléfono sea numérico y de una longitud razonable
        if not telefono.isdigit() or len(telefono) < 7 or len(telefono) > 12:
            messagebox.showerror("Error", "El número de teléfono ingresado no es válido.")
            return False

        # Validar la contraseña (puedes agregar más validaciones si lo deseas)
        if len(password) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres.")
            return False

        return True

    def crear_formulario_agregar_usuarios(self):
        # Crear el contenedor que ocupe toda la ventana
        container = tk.Frame(self.master, bg="#1f2329")
        container.pack(fill='both', expand=True)

        # Crear el marco principal sin márgenes adicionales y centrado
        main_frame = tk.Frame(container, bg="#1f2329")
        main_frame.place(relx=0.5, rely=0.5, anchor='center')  # Centrado en la ventana

        # Configurar estilos
        style = ttk.Style()
        style.configure("TLabel", font=('Segoe UI', 12), background="#1f2329", foreground="#c7d5e0")
        style.configure("Custom.TButton",
                        fieldbackground="#1b2838",
                        background="#1b2838",
                        foreground="#c7d5e0",
                        bordercolor="#c7d5e0",
                        lightcolor="#c7d5e0",
                        darkcolor="#c7d5e0",
                        borderwidth=2,
                        relief="raised")
        style.map("Custom.TButton", background=[("active", "#1b2838")])
        style.configure("Custom.TEntry",
                        fieldbackground="#1b2838",
                        background="#1b2838",
                        foreground="#c7d5e0",
                        bordercolor="#c7d5e0",
                        lightcolor="#c7d5e0",
                        darkcolor="#c7d5e0",
                        borderwidth=2,
                        relief="flat")

        # Crear un frame para los campos
        fields_frame = tk.Frame(main_frame, bg="#1f2329")
        fields_frame.pack(pady=20)

        # Etiquetas y entradas para RUT, Nombre y Apellido
        label_rut = ttk.Label(fields_frame, text="RUT:", style="TLabel")
        label_rut.grid(row=0, column=0, padx=5, pady=(20, 5), sticky='w')
        self.entry_rut = ttk.Entry(fields_frame, width=30, style="Custom.TEntry")
        self.entry_rut.grid(row=1, column=0, padx=5, pady=10, sticky='w')

        label_nombre = ttk.Label(fields_frame, text="Nombre:", style="TLabel")
        label_nombre.grid(row=0, column=1, padx=5, pady=(20, 5), sticky='w')
        self.entry_nombre = ttk.Entry(fields_frame, width=30, style="Custom.TEntry")
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=10, sticky='w')

        label_apellido = ttk.Label(fields_frame, text="Apellido:", style="TLabel")
        label_apellido.grid(row=0, column=2, padx=5, pady=(20, 5), sticky='w')
        self.entry_apellido = ttk.Entry(fields_frame, width=30, style="Custom.TEntry")
        self.entry_apellido.grid(row=1, column=2, padx=5, pady=10, sticky='w')

        # Etiquetas y entradas para Teléfono, Dirección y Email
        label_telefono = ttk.Label(fields_frame, text="Teléfono:", style="TLabel")
        label_telefono.grid(row=2, column=0, padx=5, pady=(20, 5), sticky='w')
        self.entry_telefono = ttk.Entry(fields_frame, width=30, style="Custom.TEntry")
        self.entry_telefono.grid(row=3, column=0, padx=5, pady=10, sticky='w')

        label_direccion = ttk.Label(fields_frame, text="Dirección:", style="TLabel")
        label_direccion.grid(row=2, column=1, padx=5, pady=(20, 5), sticky='w')
        self.entry_direccion = ttk.Entry(fields_frame, width=30, style="Custom.TEntry")
        self.entry_direccion.grid(row=3, column=1, padx=5, pady=10, sticky='w')

        label_email = ttk.Label(fields_frame, text="Email:", style="TLabel")
        label_email.grid(row=2, column=2, padx=5, pady=(20, 5), sticky='w')
        self.entry_email = ttk.Entry(fields_frame, width=30, style="Custom.TEntry")
        self.entry_email.grid(row=3, column=2, padx=5, pady=10, sticky='w')

        # Etiqueta y entrada para Contraseña
        label_password = ttk.Label(fields_frame, text="Contraseña:", style="TLabel")
        label_password.grid(row=4, column=0, padx=5, pady=(20, 5), sticky='w')
        self.entry_password = ttk.Entry(fields_frame, width=30, style="Custom.TEntry", show="*")
        self.entry_password.grid(row=5, column=0, padx=5, pady=10, sticky='w')

        # Botones Enviar y Limpiar
        button_frame = tk.Frame(main_frame, bg="#1f2329")
        button_frame.pack(pady=20)

        # Botón Enviar con animación
        self.button_enviar = ttk.Button(button_frame, text="Enviar", command=self.iniciar_envio, style="Custom.TButton")
        self.button_enviar.pack(side=tk.LEFT, padx=10)

        button_limpiar = ttk.Button(button_frame, text="Limpiar", command=self.limpiar_formulario_agregar_usuarios, style="Custom.TButton")
        button_limpiar.pack(side=tk.LEFT, padx=10)

    def limpiar_formulario_agregar_usuarios(self):
        # Limpiar las entradas de texto
        self.entry_rut.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

        print("Formulario limpiado")

    def validar_rut(self, rut):
        # Implementación de validación de RUT chileno
        rut = rut.replace(".", "").replace("-", "").upper()
        if not re.match(r"^\d{7,8}[0-9K]$", rut):
            return False

        cuerpo = rut[:-1]
        dv = rut[-1]

        suma = 0
        multiplo = 2

        for c in reversed(cuerpo):
            suma += int(c) * multiplo
            multiplo += 1
            if multiplo > 7:
                multiplo = 2

        resto = suma % 11
        dv_calculado = ''
        if resto == 1:
            dv_calculado = 'K'
        elif resto == 0:
            dv_calculado = '0'
        else:
            dv_calculado = str(11 - resto)

        return dv_calculado == dv

    def validar_email(self, email):
        # Expresión regular básica para validar email
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def enviar_formulario_agregar_usuarios(self):
        rut = self.entry_rut.get()
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        telefono = self.entry_telefono.get()
        direccion = self.entry_direccion.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        # Encriptar la contraseña usando el método de Django
        password_encriptada = make_password(password)

        # Si todas las validaciones son exitosas, proceder con la conexión a la base de datos
        cursor = None
        conexion = None

        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = conexion.cursor()

            # Verificar si el RUT ya existe
            cursor.execute("SELECT id FROM app_customuser WHERE rut = %s", (rut,))
            if cursor.fetchone():
                self.cargando_flag[0] = False
                messagebox.showerror("Error", "El RUT ingresado ya existe en la base de datos.")
                return

            # Verificar si el email ya existe
            cursor.execute("SELECT id FROM app_customuser WHERE email = %s", (email,))
            if cursor.fetchone():
                self.cargando_flag[0] = False
                messagebox.showerror("Error", "El email ingresado ya existe en la base de datos.")
                return

            # Realizar la inserción en la tabla app_customuser
            insert_query = """
                INSERT INTO app_customuser (rut, first_name, last_name, telefono, direccion, email, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (rut, nombre, apellido, telefono, direccion, email, password_encriptada))
            conexion.commit()

            self.cargando_flag[0] = False
            messagebox.showinfo("Éxito", "Usuario agregado correctamente")
            self.limpiar_formulario_agregar_usuarios()

        except mysql.connector.Error as e:
            self.cargando_flag[0] = False
            messagebox.showerror("Error", f"Error al agregar el usuario: {e}")
        except Exception as ex:
            self.cargando_flag[0] = False
            messagebox.showerror("Error", f"Se produjo un error inesperado: {ex}")
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
