import math
import os
import shutil
import threading
import requests
import tkinter as tk
from tkinter import font, messagebox, ttk, filedialog
from io import BytesIO
from PIL import Image, ImageTk
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from mysql.connector import Error
import mysql.connector
import pyodbc
from django.conf import settings
from django.contrib.auth.hashers import check_password
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA, conectar_db
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
from formularios.ver_productos import VerProductos
from styles import apply_styles
from formularios.agregar_productos import AgregarProductosForm
from formularios.animacion import mostrar_animacion_hexagono
from formularios.ver_arriendos import VerArriendos
from formularios.agregar_arriendos import AgregarArriendosForm
from formularios.ver_usuarios import VerUsuarios
from formularios.agregar_usuarios import AgregarUsuariosForm
from formularios.dashboard_1 import cargar_contenido_dashboard_1
from formularios.dashboard_2 import cargar_contenido_dashboard_2
from formularios.dashboard_3 import cargar_contenido_dashboard_3
import mysql.connector
from mysql.connector import Error
from datetime import date, datetime




if not settings.configured:
    settings.configure(
        PASSWORD_HASHERS=[
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
        ]
    )

def conectar_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='dbacapstone'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return None

def obtener_hash_usuario(email):
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM app_customuser WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return result[0]  # Extraer el primer valor de la tupla (el hash de la contraseña)
    return None

def verificar_contraseña(email, contraseña):
    hash_almacenado = obtener_hash_usuario(email)
    if hash_almacenado:
        return check_password(contraseña, hash_almacenado)  # Verificar con Django
    return False

class FormularioPrincipalDesign(tk.Tk):

    def __init__(self):
        super().__init__()
        apply_styles()
        print("Estilos disponibles:", ttk.Style().theme_names())
        
        # Configuración general
        self.perfil = util_img.leer_imagen("./imagenes/logo.png", (100, 100))
        self.config_window()
        self.crear_notebook()
        self.paneles()  # Asegura que `cuerpo_principal` esté creado
        
        # Configuración de la base de datos (inicializar `db_config` antes de usarlo)
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'dbacapstone'
        }
        
        # Llama a `mostrar_formulario_productos` para aplicar el estilo y luego oculta
        self.mostrar_formulario_productos()  
        self.cuerpo_principal.pack_forget()

        # Carga el login o la interfaz principal
        self.mostrar_login()

        # Configuración adicional de atributos
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "dbacapstone"
        self.pagina_actual = 0
        self.productos_por_pagina = 2
        self.ver_productos = None
        
    def config_window(self):
        # Configuración inicial de la ventana
        self.title('Python GUI')
        w, h = 1280, 720  # Aumentar el tamaño de la ventana
        # Centrar la ventana en la pantalla
        self.geometry(f"{w}x{h}+{(self.winfo_screenwidth() - w) // 2}+{(self.winfo_screenheight() - h) // 2}")


    def crear_notebook(self):
        # Crear el estilo para el notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=COLOR_MENU_LATERAL, borderwidth=0)
        style.configure('TNotebook.Tab', background=COLOR_MENU_LATERAL, foreground='#fff', font=("Roboto", 10), padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', COLOR_MENU_LATERAL), ('!selected', '#555555')], foreground=[('selected', '#fff'), ('!selected', '#ccc')])
        style.configure('TNotebook.Tab', borderwidth=0, relief='flat', padding=[10, 5], tabmargins=[0, 0, 0, 0])

        # Crear el notebook (pestañas)
        self.notebook = ttk.Notebook(self, style='TNotebook')
        self.notebook.pack(fill='both', expand=True)

        # Crear las pestañas
        self.tab_login = ttk.Frame(self.notebook, style='TFrame')
        self.tab_principal = ttk.Frame(self.notebook, style='TFrame')

        self.notebook.add(self.tab_login, text="Login")
        self.notebook.add(self.tab_principal, text="Principal")

        # Deshabilitar la pestaña principal hasta que se inicie sesión
        self.notebook.tab(1, state='disabled')

    def mostrar_login(self):
        # Crear el marco principal con el nuevo color
        main_frame = tk.Frame(self.tab_login, bg=COLOR_BARRA_SUPERIOR)
        main_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Crear un sub-marco para centrar el contenido
        center_frame = tk.Frame(main_frame, bg=COLOR_BARRA_SUPERIOR)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Crear el marco del rectángulo con un color de fondo diferente
        rect_frame = tk.Frame(center_frame, bg="#2e3b4e", bd=0, relief="flat")
        rect_frame.pack(padx=40, pady=40)  # Aumentar el tamaño del marco

        # Margen arriba del título
        tk.Label(rect_frame, bg="#2e3b4e").pack(pady=(20, 0))

        # Título del login
        labelTitulo = tk.Label(rect_frame, text="Bienvenido", font=("Roboto", 30), bg="#2e3b4e", fg="#c7d5e0")
        labelTitulo.pack(pady=(20, 10))

        # Crear el formulario de login dentro del marco del rectángulo
        form_frame = tk.Frame(rect_frame, bg="#2e3b4e")
        form_frame.pack(padx=20, pady=20, fill='both', expand=True)  # Aumentar el tamaño del formulario

        # Definir estilos específicos para los widgets de login
        style = ttk.Style()
        style.configure("CustomLogin.TLabel", font=('Segoe UI', 12), background="#2e3b4e", foreground="#c7d5e0")
        style.configure("CustomLogin.TEntry", fieldbackground="#1b2838", background="#1b2838", foreground="#c7d5e0", bordercolor="#c7d5e0", lightcolor="#c7d5e0", darkcolor="#c7d5e0", borderwidth=2, relief="flat")
        style.configure("CustomLogin.TButton", fieldbackground="#1b2838", background="#1b2838", foreground="#c7d5e0", bordercolor="#c7d5e0", lightcolor="#c7d5e0", darkcolor="#c7d5e0", borderwidth=2, relief="raised")
        style.map("CustomLogin.TButton", background=[("active", "#1b2838")])

        # Etiquetas y entradas para Usuario y Contraseña
        label_usuario = ttk.Label(form_frame, text="Usuario:", style="CustomLogin.TLabel")
        label_usuario.grid(row=0, column=0, padx=10, pady=(20, 5), sticky='w')
        self.entry_usuario = ttk.Entry(form_frame, width=80, style="CustomLogin.TEntry")
        self.entry_usuario.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        label_contrasena = ttk.Label(form_frame, text="Contraseña:", style="CustomLogin.TLabel")
        label_contrasena.grid(row=2, column=0, padx=10, pady=(20, 5), sticky='w')
        self.entry_contrasena = ttk.Entry(form_frame, width=80, style="CustomLogin.TEntry", show="*")
        self.entry_contrasena.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # Botones Ingresar y Olvidaste tu contraseña
        button_frame = tk.Frame(form_frame, bg="#2e3b4e")
        button_frame.grid(row=4, column=0, pady=20)

        button_ingresar = ttk.Button(button_frame, text="Ingresar", command=self.ingresar, style="CustomLogin.TButton")
        button_ingresar.pack(side=tk.LEFT, padx=5)


        # Margen abajo de los botones
        tk.Label(rect_frame, bg="#2e3b4e").pack(pady=(0, 20))

    # Dentro de la clase FormularioPrincipalDesign o similar
    def ingresar(self):
        email = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='dbacapstone'
            )
            if connection.is_connected():
                print("Conexión a la base de datos exitosa")
                if verificar_contraseña(email, contrasena):
                    print("Ingreso exitoso")
                    self.notebook.tab(1, state='normal')
                    self.notebook.tab(0, state='disabled')
                    self.notebook.select(1)
                    self.mostrar_interfaz_principal()
                    mostrar_animacion_hexagono(self)
                else:
                    messagebox.showerror("Error de autenticación", "Usuario o contraseña incorrectos. Por favor, inténtelo de nuevo.")
            else:
                messagebox.showerror("Error de conexión", "No es posible establecer conexión entre el software y la base de datos. Contacte a su administrador.")
        except Error as e:
            if e.errno == 2003:
                messagebox.showerror("Error de conexión", "No es posible establecer conexión entre el software y la base de datos. Contacte a su administrador.")
            elif e.errno == 1045:
                messagebox.showerror("Error de autenticación", "Usuario o contraseña incorrectos. Por favor, inténtelo de nuevo.")
            else:
                messagebox.showerror("Error", str(e))

    def olvidaste_contrasena(self, event):
        # Función para manejar el evento de olvidar contraseña
        print("Redirigir a la página de recuperación de contraseña")

    def mostrar_interfaz_principal(self):
        # Crear los paneles antes de mostrarlos
        self.paneles()
        self.barra_superior.pack(side=tk.TOP, fill='both')
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.mostrar_dashboard()

    def paneles(self):        
        # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(self.tab_principal, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.menu_lateral = tk.Frame(self.tab_principal, bg=COLOR_MENU_LATERAL, width=150)
        self.cuerpo_principal = tk.Frame(self.tab_principal, bg=COLOR_CUERPO_PRINCIPAL)

    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=20)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Book&Rent")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT, padx=(0, 116))  # Agrega un margen de 10 píxeles a la izquierda

        # Botón del menú lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\u2630", font=font_awesome, command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)
    
    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 30
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)
        
        # Etiqueta de perfil
        self.labelPerfil = tk.Label(self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        # Declarar todos los botones como atributos de la clase
        self.buttonDashBoard = tk.Button(self.menu_lateral)
        self.buttonProductos = tk.Button(self.menu_lateral)
        self.buttonUsuarios = tk.Button(self.menu_lateral)
        self.buttonArriendos = tk.Button(self.menu_lateral)  # Declarado correctamente aquí
        self.buttonMantenedorArriendos = tk.Button(self.menu_lateral)

        # Lista de botones con sus respectivas configuraciones
        buttons_info = [
            ("Dashboard", "📊", self.buttonDashBoard, self.mostrar_dashboard),
            ("Mantenedor Productos", "📚", self.buttonProductos, self.mostrar_formulario_productos),
            ("Mantenedor Usuarios", "👥", self.buttonUsuarios, self.mostrar_formulario_usuarios),
            ("Seguimiento Arriendos", "📅", self.buttonArriendos, self.mostrar_seguimiento_arriendos),  # Comando correcto
            ("Mantenedor Arriendos", "🏠", self.buttonMantenedorArriendos, self.mostrar_formulario_arriendos)
        ]

        # Configurar y empaquetar los botones
        for text, icon, button, command in buttons_info:
            button.config(
                text=f"  {icon}    {text}",
                anchor="w",
                font=font_awesome,
                bd=0,
                bg=COLOR_MENU_LATERAL,
                fg="white",
                width=ancho_menu,
                height=alto_menu,
                command=command
            )
            button.pack(side=tk.TOP)
            self.bind_hover_events(button)


    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
            # Re-empaquetar cuerpo_principal para ocupar todo el espacio
            self.cuerpo_principal.pack_forget()
            self.cuerpo_principal.pack(side=tk.LEFT, fill='both', expand=True)
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)
            # Re-empaquetar cuerpo_principal para estar al lado derecho
            self.cuerpo_principal.pack_forget()
            self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def mostrar_dashboard(self):
        # Minimizar el menú lateral
        self.toggle_panel()

        # Limpiar el cuerpo principal
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Crear un marco para agregar márgenes
        frame_notebook = tk.Frame(self.cuerpo_principal, bg="#1f2329")
        frame_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Título del dashboard
        labelTitulo = tk.Label(frame_notebook, text="📊 Dashboard", font=("Roboto", 20), bg="#2a3138", fg="white", anchor='w')
        labelTitulo.pack(fill='x', pady=(0, 0))

        # Crear el notebook para las pestañas
        notebook = ttk.Notebook(frame_notebook, style='TNotebook')
        notebook.pack(fill='both', expand=True, padx=0, pady=0)

        # Crear los frames para cada pestaña
        frame_dashboard_1 = tk.Frame(notebook, bg="#1f2329")
        frame_dashboard_2 = tk.Frame(notebook, bg="#1f2329")
        frame_dashboard_3 = tk.Frame(notebook, bg="#1f2329")

        # Agregar los frames al notebook
        notebook.add(frame_dashboard_1, text="Dashboard 1")
        notebook.add(frame_dashboard_2, text="Dashboard 2")
        notebook.add(frame_dashboard_3, text="Dashboard 3")

        # Cargar contenido en cada frame desde los archivos
        cargar_contenido_dashboard_1(frame_dashboard_1)
        cargar_contenido_dashboard_2(frame_dashboard_2)
        cargar_contenido_dashboard_3(frame_dashboard_3)

        # Enlazar el evento para manejar cambios de pestaña
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected_dashboard)

    def on_tab_selected_dashboard(self, event):
        # Aquí puedes agregar la lógica para cuando se cambia de pestaña
        selected_tab = event.widget.index("current")
        print("Pestaña seleccionada en Dashboard:", selected_tab)


    def mostrar_formulario_productos(self):
        # Limpiar el cuerpo principal antes de agregar nuevo contenido
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Crear un contenedor sin márgenes adicionales para el notebook
        frame_notebook = tk.Frame(self.cuerpo_principal, bg=COLOR_MENU_LATERAL)
        frame_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Título del formulario
        labelTitulo = tk.Label(frame_notebook, text="📚 Mantenedor Productos", font=("Roboto", 20), bg=COLOR_MENU_LATERAL, fg="white")
        labelTitulo.pack(anchor='nw', padx=0, pady=(0, 0))

        # Crear el notebook (pestañas) sin márgenes adicionales
        notebook = ttk.Notebook(frame_notebook, style='TNotebook')
        notebook.pack(fill='both', expand=True, padx=0, pady=0)

        # Crear las pestañas
        frame_ver_productos = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)
        frame_agregar_productos = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)

        notebook.add(frame_ver_productos, text="Ver Productos")
        notebook.add(frame_agregar_productos, text="Agregar Productos")

        # Asignar el frame para ver productos
        self.frame_ver_productos = frame_ver_productos

        # Inicializa self.ver_productos solo si VerProductos está disponible
        if VerProductos:
            self.ver_productos = VerProductos(self.frame_ver_productos)

        # Mostrar productos cuando se selecciona la pestaña "Ver Productos"
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected_usuarios)

        # **Integración del Formulario de Agregar Productos**
        # Instanciar la clase AgregarProductosForm sin usar pack
        agregar_productos_form = AgregarProductosForm(frame_agregar_productos, self.db_config)

    def on_tab_selected_usuarios(self, event):
        notebook = event.widget
        selected_tab = notebook.index("current")
        if notebook.tab(selected_tab, "text") == "Ver Usuarios":
            # Verifica que self.ver_usuarios esté inicializado
            if self.ver_usuarios is not None:
                self.ver_usuarios.mostrar_usuarios()
            else:
                print("Error: self.ver_usuarios no está inicializado.")


    def mostrar_formulario_arriendos(self):
        # Limpiar el cuerpo principal antes de agregar nuevo contenido
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Crear un marco para agregar márgenes
        frame_notebook = tk.Frame(self.cuerpo_principal, bg=COLOR_MENU_LATERAL)
        frame_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Título del formulario
        labelTitulo = tk.Label(frame_notebook, text="🏠 Mantenedor Arriendos", font=("Roboto", 20), bg=COLOR_MENU_LATERAL, fg="white")
        labelTitulo.pack(anchor='nw', padx=0, pady=(0, 0))

        # Crear el notebook usando el estilo global TNotebook
        notebook = ttk.Notebook(frame_notebook, style='TNotebook')
        notebook.pack(fill='both', expand=True)

        # Crear las pestañas
        frame_ver_arriendos = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)
        frame_agregar_arriendos = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)

        notebook.add(frame_ver_arriendos, text="Ver Arriendos")
        notebook.add(frame_agregar_arriendos, text="Agregar Arriendos")

        # Asignar el frame para ver arriendos
        self.frame_ver_arriendos = frame_ver_arriendos

        # Crear una instancia de VerArriendos y pasarle el frame de "Ver Arriendos"
        self.ver_arriendos = VerArriendos(self.frame_ver_arriendos)

        # Enlazar el evento con el método definido
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected_arriendos)

        # **Integración del Formulario de Agregar Arriendos**
        # Instanciar la clase AgregarArriendosForm y pasarle el frame correspondiente
        AgregarArriendosForm(frame_agregar_arriendos, self.db_config)
        self.update_idletasks()  # Asegura que el estilo se aplique correctamente

    def on_tab_selected_arriendos(self, event):
        # Aquí puedes agregar la lógica para cuando se cambia de pestaña en el notebook de arriendos
        selected_tab = event.widget.index("current")
        print("Pestaña seleccionada en Mantenedor de Arriendos:", selected_tab)   

    def mostrar_formulario_usuarios(self):
        # Limpiar el cuerpo principal antes de agregar nuevo contenido
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Crear un contenedor sin márgenes adicionales para el notebook
        frame_notebook = tk.Frame(self.cuerpo_principal, bg=COLOR_MENU_LATERAL)
        frame_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Título del formulario
        labelTitulo = tk.Label(frame_notebook, text="👥 Mantenedor Usuarios", font=("Roboto", 20), bg=COLOR_MENU_LATERAL, fg="white")
        labelTitulo.pack(anchor='nw', padx=0, pady=(0, 0))

        # Crear el notebook (pestañas) sin márgenes adicionales
        notebook = ttk.Notebook(frame_notebook, style='TNotebook')
        notebook.pack(fill='both', expand=True, padx=0, pady=0)

        # Crear las pestañas
        frame_ver_usuarios = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)
        frame_agregar_usuarios = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)

        notebook.add(frame_ver_usuarios, text="Ver Usuarios")
        notebook.add(frame_agregar_usuarios, text="Agregar Usuarios")

        # Asignar el frame para ver usuarios
        self.frame_ver_usuarios = frame_ver_usuarios

        # Inicializa self.ver_usuarios solo si VerUsuarios está disponible y asegurarte de pasar db_config
        if VerUsuarios:
            self.ver_usuarios = VerUsuarios(self.frame_ver_usuarios, self.db_config)

        # Mostrar usuarios cuando se selecciona la pestaña "Ver Usuarios"
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected_usuarios)

        # **Integración del Formulario de Agregar Usuarios**
        # Instanciar la clase AgregarUsuariosForm sin usar pack
        agregar_usuarios_form = AgregarUsuariosForm(frame_agregar_usuarios, self.db_config)





























    def mostrar_seguimiento_arriendos(self):
        # Limpiar el cuerpo principal antes de agregar nuevo contenido
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Utilizar el toggle_panel para ocultar el menú lateral si es necesario
        if hasattr(self, 'menu_lateral') and self.menu_lateral.winfo_ismapped():
            self.toggle_panel()

        # Crear un marco para agregar márgenes
        frame_notebook = tk.Frame(self.cuerpo_principal, bg="#2a3138")
        frame_notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Título del formulario
        labelTitulo = tk.Label(frame_notebook, text="\ud83d\udcc5 Seguimiento de Arriendos", font=("Roboto", 20),
                               bg="#2a3138", fg="white")
        labelTitulo.pack(anchor='nw', padx=0, pady=(0, 20))

        # Crear el notebook usando el estilo global TNotebook
        notebook = ttk.Notebook(frame_notebook, style='TNotebook')
        notebook.pack(fill="both", expand=True)

        # Crear las pestañas
        frame_arriendos_pendientes = tk.Frame(notebook, bg="#2a3138")
        frame_arriendos_entregados = tk.Frame(notebook, bg="#2a3138")

        notebook.add(frame_arriendos_pendientes, text="Arriendos Pendientes")
        notebook.add(frame_arriendos_entregados, text="Arriendos Entregados")

        # Llenar las pestañas con tablas
        self.crear_tabla_seguimiento(frame_arriendos_pendientes, "Pendiente", "pendientes")
        self.crear_tabla_seguimiento(frame_arriendos_entregados, "Entregado", "entregados")

        # Evento para manejar cambios de pestaña
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected_seguimiento_arriendos)

        self.cuerpo_principal.update_idletasks()  # Asegura que el estilo se aplique correctamente

    def crear_tabla_seguimiento(self, frame, estado, tab_name):
        # Crear el contenedor principal para la tabla
        table_frame = tk.Frame(frame, bg="#2a3138")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Crear un contenedor para los filtros en la misma línea
        top_frame = tk.Frame(table_frame, bg="#2a3138")
        top_frame.pack(pady=10, anchor="w", fill="x")

        # Crear un contenedor para los filtros
        filters_frame = tk.Frame(top_frame, bg="#2a3138")
        filters_frame.pack(side="left")

        # Obtener lista de meses y años disponibles en la base de datos
        meses_lista, años_lista = self.obtener_meses_años_disponibles()

        # Combobox para seleccionar mes
        meses_filter = ["Todos"] + meses_lista
        mes_combobox = ttk.Combobox(filters_frame, values=meses_filter, state="readonly", font=("Roboto", 10),
                                    style='Custom.TCombobox')  # Usa el estilo definido
        mes_combobox.set("Todos")  # Establecer "Todos" como valor por defecto
        mes_combobox.pack(side="left", padx=5)

        # Combobox para seleccionar año
        año_combobox = ttk.Combobox(filters_frame, values=["Todos"] + años_lista, state="readonly", font=("Roboto", 10),
                                    style='Custom.TCombobox')  # Usa el estilo definido
        año_combobox.set("Todos")  # Seleccionar "Todos" por defecto
        año_combobox.pack(side="left", padx=5)

        # Guardar referencias a los Comboboxes y árboles por pestaña
        if tab_name == "pendientes":
            self.mes_combobox_pendientes = mes_combobox
            self.año_combobox_pendientes = año_combobox
        elif tab_name == "entregados":
            self.mes_combobox_entregados = mes_combobox
            self.año_combobox_entregados = año_combobox

        # Botón para aplicar filtros
        aplicar_button = ttk.Button(filters_frame, text="Aplicar Filtros",
                                   command=lambda: self.actualizar_tabla(tree, estado, mes_combobox.get(),
                                                                     año_combobox.get()),
                                   style="Custom.TButton")
        aplicar_button.pack(side="left", padx=5)

        # Definir las columnas de la tabla
        columns = ("nombre", "rut", "telefono", "estado_libro", "nom_libro", "inicio_arriendo", "fin_arriendo",
                   "dias_atraso", "valor_multa", "accion")

        tree = ttk.Treeview(table_frame, columns=columns, show='headings', selectmode='browse')

        # Definir encabezados de columnas
        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())

        # Definir anchos de columnas
        tree.column("nombre", width=150, anchor="center")
        tree.column("rut", width=100, anchor="center")
        tree.column("telefono", width=100, anchor="center")
        tree.column("estado_libro", width=100, anchor="center")
        tree.column("nom_libro", width=150, anchor="center")
        tree.column("inicio_arriendo", width=100, anchor="center")
        tree.column("fin_arriendo", width=100, anchor="center")
        tree.column("dias_atraso", width=80, anchor="center")
        tree.column("valor_multa", width=80, anchor="center")
        tree.column("accion", width=150, anchor="center")

        # Configurar estilos de la tabla
        style_tree = ttk.Style()
        style_tree.configure("Treeview",
                             background="#1f2329",
                             foreground="white",
                             fieldbackground="#1f2329",
                             rowheight=25,
                             font=("Roboto", 10))
        style_tree.map('Treeview', background=[('selected', '#2a3138')])

        style_tree.configure("Treeview.Heading",
                             background="#2a3138",
                             foreground="white",
                             font=("Roboto", 10, "bold"))

        # Configurar colores alternos para filas
        tree.tag_configure('oddrow', background="#1f2329")
        tree.tag_configure('evenrow', background="#39424e")

        # Agregar barra de desplazamiento
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar eventos de clic en la columna "Acción"
        def on_tree_click(event):
            region = tree.identify("region", event.x, event.y)
            if region != "cell":
                return
            column = tree.identify_column(event.x)
            if column == "#10":  # Columna "Acción" es la décima columna
                row_id = tree.identify_row(event.y)
                if not row_id:
                    return  # No se seleccionó ninguna fila
                valores = tree.item(row_id, 'values')
                arriendo_id = row_id  # El iid es el ID del arriendo
                if estado == "Pendiente":
                    self.recibir_libro(arriendo_id)
                else:
                    self.marcar_pendiente(arriendo_id)

        tree.bind("<Button-1>", on_tree_click)

        tree.pack(fill="both", expand=True)

        # Guardar referencias al árbol por pestaña
        if tab_name == "pendientes":
            self.tree_pendientes = tree
        elif tab_name == "entregados":
            self.tree_entregados = tree

        # Cargar datos iniciales sin filtros
        self.actualizar_tabla(tree, estado, mes_combobox.get(), año_combobox.get())

    def obtener_meses_años_disponibles(self):
        try:
            # Conectar a la base de datos dbacapstone
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="dbacapstone"
            )
            cursor = conn.cursor()

            # Obtener lista de meses y años basados en fecha_inicio
            cursor.execute("SELECT DISTINCT MONTH(fecha_inicio) FROM app_arriendo")
            meses = [int(row[0]) for row in cursor.fetchall()]

            cursor.execute("SELECT DISTINCT YEAR(fecha_inicio) FROM app_arriendo")
            años = [str(row[0]) for row in cursor.fetchall()]

            cursor.close()
            conn.close()

            # Mapeo de meses en español
            meses_es = {
                1: "Enero",
                2: "Febrero",
                3: "Marzo",
                4: "Abril",
                5: "Mayo",
                6: "Junio",
                7: "Julio",
                8: "Agosto",
                9: "Septiembre",
                10: "Octubre",
                11: "Noviembre",
                12: "Diciembre"
            }

            # Eliminar duplicados y ordenar los meses
            meses = sorted(set(meses))
            meses_lista = [meses_es[mes] for mes in meses]

            return meses_lista, años

        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return [], []

    def actualizar_tabla(self, tree, estado, mes, anio):
        # Limpiar la tabla
        for item in tree.get_children():
            tree.delete(item)

        # Obtener datos filtrados
        datos = self.obtener_datos_seguimiento(estado, mes, anio)

        # Insertar datos en la tabla
        for index, fila in enumerate(datos):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            arriendo_id = fila[-1]
            tree.insert("", tk.END, iid=arriendo_id, values=fila[:-1], tags=(tag,))

    def obtener_datos_seguimiento(self, estado, mes, anio):
        # Mapear el estado a 0 o 1
        estado_num = 0 if estado == "Pendiente" else 1

        try:
            # Conectar a la base de datos dbacapstone
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="dbacapstone"
            )
            cursor = conn.cursor()

            # Construir la consulta SQL con filtros
            query = """
            SELECT
                CONCAT(app_customuser.first_name, ' ', app_customuser.last_name) AS nombre,
                app_customuser.rut,
                app_customuser.telefono,
                app_arriendo.libro_entregado AS estado_libro,
                app_libroarr.nom_libro AS nom_libro,
                app_arriendo.fecha_inicio AS inicio_arriendo,
                app_arriendo.fecha_fin AS fin_arriendo,
                app_arriendo.id AS arriendo_id
            FROM
                app_arriendo
            JOIN app_customuser ON app_arriendo.cliente_id = app_customuser.id
            JOIN app_libroarr ON app_arriendo.producto_id = app_libroarr.id
            WHERE
                app_arriendo.libro_entregado = %s
            """

            # Lista de parámetros para la consulta
            params = [estado_num]

            # Agregar filtros de mes y año basados en fecha_inicio
            if mes != "Todos":
                # Mapeo de meses en español a números
                meses_es = {
                    "Enero": 1,
                    "Febrero": 2,
                    "Marzo": 3,
                    "Abril": 4,
                    "Mayo": 5,
                    "Junio": 6,
                    "Julio": 7,
                    "Agosto": 8,
                    "Septiembre": 9,
                    "Octubre": 10,
                    "Noviembre": 11,
                    "Diciembre": 12
                }
                mes_num = meses_es.get(mes)
                if mes_num:
                    query += " AND MONTH(app_arriendo.fecha_inicio) = %s"
                    params.append(mes_num)

            if anio != "Todos":
                query += " AND YEAR(app_arriendo.fecha_inicio) = %s"
                params.append(anio)

            cursor.execute(query, params)
            result = cursor.fetchall()

            data = []
            for row in result:
                nombre = row[0]
                rut = row[1]
                telefono = row[2]
                estado_libro_db = row[3]
                nom_libro = row[4]
                inicio_arriendo = row[5]
                fin_arriendo = row[6]
                arriendo_id = row[7]

                # Formatear fechas en formato día-mes-año
                inicio_arriendo_str = inicio_arriendo.strftime("%d-%m-%Y")
                fin_arriendo_str = fin_arriendo.strftime("%d-%m-%Y")

                # Calcular días de atraso y valor multa
                # Verificar si fin_arriendo es datetime o date
                if isinstance(fin_arriendo, datetime):
                    fin_arriendo_date = fin_arriendo.date()
                elif isinstance(fin_arriendo, date):
                    fin_arriendo_date = fin_arriendo
                else:
                    # Manejar otros tipos o establecer a hoy si es None
                    fin_arriendo_date = date.today()

                today = date.today()
                dias_atraso = (today - fin_arriendo_date).days
                if dias_atraso < 0:
                    dias_atraso = 0
                # Supongamos que el valor de la multa es 1000 por día de atraso
                valor_multa = dias_atraso * 1000

                # Actualizar estado visualmente
                if estado_libro_db == 0:
                    if dias_atraso > 0:
                        estado_libro = "Atrasado"
                    else:
                        estado_libro = "Pendiente"
                else:
                    estado_libro = "Entregado"

                # Determinar acción
                if estado == "Pendiente":
                    accion = "Recibir Libro"
                else:
                    accion = "Marcar como Pendiente"

                # Agregar datos a la lista
                data.append((
                    nombre,
                    rut,
                    telefono,
                    estado_libro,
                    nom_libro,
                    inicio_arriendo_str,
                    fin_arriendo_str,
                    str(dias_atraso),
                    f"${valor_multa}",
                    accion,
                    arriendo_id  # Agregar ID para identificar el registro
                ))

            cursor.close()
            conn.close()

            return data

        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return []

    def recibir_libro(self, arriendo_id):
        # Confirmar la acción con el usuario
        respuesta = messagebox.askyesno("Confirmación", "¿Desea marcar este libro como recibido?")
        if respuesta:
            try:
                # Conectar a la base de datos dbacapstone
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="dbacapstone"
                )
                cursor = conn.cursor()

                # Actualizar el estado a '1' (Entregado) para el arriendo seleccionado
                cursor.execute("""
                    UPDATE app_arriendo SET libro_entregado = 1 WHERE id = %s
                """, (arriendo_id,))

                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Éxito", "El libro ha sido marcado como recibido.")

                # Actualizar las tablas después de cambiar el estado
                self.actualizar_tabla_pendientes()
                self.actualizar_tabla_entregados()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"No se pudo actualizar el estado: {e}")

    def marcar_pendiente(self, arriendo_id):
        # Confirmar la acción con el usuario
        respuesta = messagebox.askyesno("Confirmación", "¿Desea marcar este libro como pendiente nuevamente?")
        if respuesta:
            try:
                # Conectar a la base de datos dbacapstone
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="dbacapstone"
                )
                cursor = conn.cursor()

                # Actualizar el estado a '0' (Pendiente) para el arriendo seleccionado
                cursor.execute("""
                    UPDATE app_arriendo SET libro_entregado = 0 WHERE id = %s
                """, (arriendo_id,))

                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Éxito", "El libro ha sido marcado como pendiente nuevamente.")

                # Actualizar las tablas después de cambiar el estado
                self.actualizar_tabla_pendientes()
                self.actualizar_tabla_entregados()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"No se pudo actualizar el estado: {e}")

    def actualizar_tabla_pendientes(self):
        # Obtener el estado actual de los filtros
        mes = self.mes_combobox_pendientes.get()
        anio = self.año_combobox_pendientes.get()

        # Actualizar la tabla de pendientes
        self.actualizar_tabla(self.tree_pendientes, "Pendiente", mes, anio)

    def actualizar_tabla_entregados(self):
        # Obtener el estado actual de los filtros
        mes = self.mes_combobox_entregados.get()
        anio = self.año_combobox_entregados.get()

        # Actualizar la tabla de entregados
        self.actualizar_tabla(self.tree_entregados, "Entregado", mes, anio)

    def on_tab_selected_seguimiento_arriendos(self, event):
        selected_tab = event.widget.index("current")
        print(f"Pestaña seleccionada en Seguimiento de Arriendos: {selected_tab}")