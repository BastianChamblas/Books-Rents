import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import mysql.connector
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import threading
import time
import os

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

class AgregarProductosForm:
    def __init__(self, master, db_config):
        """
        Inicializa el formulario de agregar productos.

        :param master: El widget padre donde se colocará el formulario.
        :param db_config: Diccionario con la configuración de la base de datos.
        """
        self.master = master
        self.host = db_config.get('host')
        self.user = db_config.get('user')
        self.password = db_config.get('password')
        self.database = db_config.get('database')
        self.ruta_imagen = None  # Inicializar ruta de imagen
        self.cargando_flag = [False]  # Bandera para la animación
        self.crear_formulario_agregar_productos()

    def iniciar_envio(self):
        # Realizar validaciones antes de iniciar la animación
        if not self.validar_formulario():
            return  # Detener si la validación falla

        # Activar la bandera y comenzar la animación del botón
        self.cargando_flag[0] = True
        animar_boton(self.button_enviar, self.cargando_flag, self.master)

        # Iniciar el proceso de envío en un hilo separado
        threading.Thread(target=self.enviar_formulario_agregar_productos).start()

    def validar_formulario(self):
        # Capturar los valores de los campos del formulario
        nombre_libro = self.entry_nombre.get()
        precio = self.entry_precio.get()
        stock = self.entry_stock.get()
        nombre_autor = self.combo_autor.get()
        nombre_genero = self.combo_genero.get()

        # Verificar si los campos no están vacíos
        if not (nombre_libro and precio and stock and nombre_autor and nombre_genero):
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return False

        # Verificar que el autor y el género seleccionados están en las listas disponibles
        if nombre_autor not in self.combo_autor['values']:
            messagebox.showerror("Error", "Seleccione un autor válido de la lista.")
            return False

        if nombre_genero not in self.combo_genero['values']:
            messagebox.showerror("Error", "Seleccione un género válido de la lista.")
            return False

        # Verificar si precio y stock son valores numéricos
        if not precio.isdigit() or not stock.isdigit():
            messagebox.showerror("Error", "El precio y el stock deben ser valores numéricos.")
            return False

        # Verificar si se ha cargado una imagen
        if not hasattr(self, 'ruta_imagen_local'):
            messagebox.showerror("Error", "Por favor, cargue una imagen para el producto.")
            return False

        return True

    def crear_formulario_agregar_productos(self):
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
        style.configure("Custom.TCombobox",
                        fieldbackground="#1b2838",
                        background="#1b2838",
                        foreground="#c7d5e0",
                        bordercolor="#c7d5e0",
                        lightcolor="#c7d5e0",
                        darkcolor="#c7d5e0",
                        borderwidth=2,
                        relief="flat")
        style.configure("Custom.TEntry",
                        fieldbackground="#1b2838",
                        background="#1b2838",
                        foreground="#c7d5e0",
                        bordercolor="#c7d5e0",
                        lightcolor="#c7d5e0",
                        darkcolor="#c7d5e0",
                        borderwidth=2,
                        relief="flat")

        # Crear un frame para los campos en la misma fila
        fields_frame = tk.Frame(main_frame, bg="#1f2329")
        fields_frame.pack(pady=20)

        # Etiquetas y entradas para Nombre del Libro, Precio y Stock
        label_nombre = ttk.Label(fields_frame, text="Nombre del Libro:", style="TLabel")
        label_nombre.grid(row=0, column=0, padx=5, pady=(40, 5), sticky='w')
        self.entry_nombre = ttk.Entry(fields_frame, width=30, style="Custom.TEntry")
        self.entry_nombre.grid(row=1, column=0, padx=5, pady=10, sticky='w')

        label_precio = ttk.Label(fields_frame, text="Precio:", style="TLabel")
        label_precio.grid(row=0, column=1, padx=5, pady=(40, 5), sticky='w')
        self.entry_precio = ttk.Entry(fields_frame, width=30, style="Custom.TEntry")
        self.entry_precio.grid(row=1, column=1, padx=5, pady=10, sticky='w')

        label_stock = ttk.Label(fields_frame, text="Stock:", style="TLabel")
        label_stock.grid(row=0, column=2, padx=5, pady=(40, 5), sticky='w')
        self.entry_stock = ttk.Entry(fields_frame, width=30, style="Custom.TEntry")
        self.entry_stock.grid(row=1, column=2, padx=5, pady=10, sticky='w')

        # Obtener autores y géneros de la base de datos
        autores = self.obtener_autores()
        generos = self.obtener_generos()

        # Etiquetas y entradas para Autor y Género
        label_autor = ttk.Label(fields_frame, text="Autor:", style="TLabel")
        label_autor.grid(row=2, column=0, padx=5, pady=10, sticky='w')
        self.combo_autor = ttk.Combobox(fields_frame, values=autores, width=30, style="Custom.TCombobox")
        self.combo_autor.grid(row=3, column=0, padx=5, pady=10, sticky='w')

        label_genero = ttk.Label(fields_frame, text="Género:", style="TLabel")
        label_genero.grid(row=2, column=1, padx=5, pady=10, sticky='w')
        self.combo_genero = ttk.Combobox(fields_frame, values=generos, width=30, style="Custom.TCombobox")
        self.combo_genero.grid(row=3, column=1, padx=5, pady=10, sticky='w')

        # Campo Imagen
        label_imagen = ttk.Label(fields_frame, text="Imagen:", style="TLabel")
        label_imagen.grid(row=4, column=0, padx=5, pady=10, sticky='w')
        button_imagen = ttk.Button(fields_frame, text="Cargar Imagen", command=self.cargar_imagen_agregar_productos, style="Custom.TButton")
        button_imagen.grid(row=5, column=0, padx=5, pady=10, sticky='w')

        # Botones Enviar y Limpiar
        button_frame = tk.Frame(main_frame, bg="#1f2329")
        button_frame.pack(pady=20)

        # Botón Enviar con animación
        self.button_enviar = ttk.Button(button_frame, text="Enviar", command=self.iniciar_envio, style="Custom.TButton")
        self.button_enviar.pack(side=tk.LEFT, padx=10)

        button_limpiar = ttk.Button(button_frame, text="Limpiar", command=self.limpiar_formulario_agregar_productos, style="Custom.TButton")
        button_limpiar.pack(side=tk.LEFT, padx=10)



    def obtener_generos(self):
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre FROM app_generolib")
            generos = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conexion.close()
            return generos
        except Exception as e:
            print(f"Error al obtener los géneros: {e}")
            return []

    def obtener_autores(self):
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre_autor FROM app_autor")
            autores = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conexion.close()
            return autores
        except Exception as e:
            print(f"Error al obtener los autores: {e}")
            return []

    def limpiar_formulario_agregar_productos(self):
        # Limpiar las entradas de texto
        self.entry_nombre.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)

        # Limpiar los ComboBoxes
        self.combo_autor.set('')
        self.combo_genero.set('')

        # Limpiar la ruta de la imagen
        self.ruta_imagen = None

        print("Formulario limpiado")

    def cargar_imagen_agregar_productos(self):
        # Seleccionar el archivo de imagen desde el sistema
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.png")])
        if file_path:
            self.ruta_imagen_local = file_path
            print(f"Imagen seleccionada: {file_path}")

    def autenticar_google_drive(self):
        gauth = GoogleAuth()
        gauth.LoadClientConfigFile('client_secrets.json')
        gauth.LoadCredentialsFile("mycreds.txt")

        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile("mycreds.txt")
        return GoogleDrive(gauth)

    def enviar_formulario_agregar_productos(self):
        nombre_libro = self.entry_nombre.get()
        precio = self.entry_precio.get()
        stock = self.entry_stock.get()
        nombre_autor = self.combo_autor.get()
        nombre_genero = self.combo_genero.get()

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

            # Obtener el ID del autor a partir del nombre
            cursor.execute("SELECT id FROM app_autor WHERE nombre_autor = %s", (nombre_autor,))
            autor_id = cursor.fetchone()[0]

            # Obtener el ID del género a partir del nombre
            cursor.execute("SELECT id FROM app_generolib WHERE nombre = %s", (nombre_genero,))
            genero_id = cursor.fetchone()[0]

            # Subir la imagen a Google Drive
            drive = self.autenticar_google_drive()
            archivo_drive = drive.CreateFile({
                'parents': [{'id': '1nHP5tyVyjDPpXE7N5Tm4nAK63PhzUIEP'}],
                'title': nombre_libro
            })
            archivo_drive.SetContentFile(self.ruta_imagen_local)
            archivo_drive.Upload()

            # Guardar el link de la imagen en Google Drive para la base de datos
            self.ruta_imagen = archivo_drive['alternateLink']
            print(f"Imagen subida correctamente: {self.ruta_imagen}")

            # Realizar la inserción en la tabla app_libro
            insert_query = """
                INSERT INTO app_libro (nom_libro, precio, stock, imagen, id_autor_id, id_genero_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (nombre_libro, precio, stock, self.ruta_imagen, autor_id, genero_id))
            conexion.commit()

            self.cargando_flag[0] = False
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.limpiar_formulario_agregar_productos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar el producto: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
