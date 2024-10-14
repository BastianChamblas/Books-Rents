import tkinter as tk
from tkinter import font, ttk, filedialog
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_ventana as util_ventana
import util.util_imagenes as util_img

class FormularioPrincipalDesign(tk.Tk):

    def __init__(self):
        super().__init__()
        self.perfil = util_img.leer_imagen("./imagenes/logo.png", (100, 100))
        self.config_window()
        self.crear_notebook()
        self.mostrar_login()

    def config_window(self):
        # Configuración inicial de la ventana
        self.title('Python GUI')
        w, h = 1024, 600        
        self.geometry(f"{w}x{h}+{(self.winfo_screenwidth() - w) // 2}+{(self.winfo_screenheight() - h) // 2}")

    def crear_notebook(self):
        # Crear el notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        # Crear las pestañas
        self.tab_login = tk.Frame(self.notebook, bg="#1f2329")
        self.tab_principal = tk.Frame(self.notebook, bg="white")

        self.notebook.add(self.tab_login, text="Login")
        self.notebook.add(self.tab_principal, text="Principal")

        # Deshabilitar la pestaña principal hasta que se inicie sesión
        self.notebook.tab(1, state='disabled')

    def mostrar_login(self):
        # Crear el marco principal con el nuevo color
        main_frame = tk.Frame(self.tab_login, bg="#1f2329")
        main_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Título del login
        labelTitulo = tk.Label(main_frame, text="Book&Rent", font=("Roboto", 30), bg="#1f2329", fg="#c7d5e0")
        labelTitulo.pack(pady=(20, 10))

        # Crear el formulario de login dentro del marco principal
        form_frame = tk.Frame(main_frame, bg="#1f2329")
        form_frame.pack(padx=10, pady=10, fill='both', expand=True)

        style = ttk.Style()
        style.configure("TLabel", font=('Segoe UI', 12), background="#1f2329", foreground="#c7d5e0")
        style.configure("Custom.TButton", fieldbackground="#1b2838", background="#1b2838", foreground="#c7d5e0", bordercolor="#c7d5e0", lightcolor="#c7d5e0", darkcolor="#c7d5e0", borderwidth=2, relief="raised")
        style.map("Custom.TButton", background=[("active", "#1b2838")])  # Quitar el brillo al pasar el mouse
        style.configure("Custom.TEntry", fieldbackground="#1b2838", background="#1b2838", foreground="#c7d5e0", bordercolor="#c7d5e0", lightcolor="#c7d5e0", darkcolor="#c7d5e0", borderwidth=2, relief="flat")

        # Etiquetas y entradas para Usuario y Contraseña
        label_usuario = ttk.Label(form_frame, text="Usuario:")
        label_usuario.grid(row=0, column=0, padx=10, pady=(20, 5), sticky='w')
        self.entry_usuario = ttk.Entry(form_frame, width=30, style="Custom.TEntry")
        self.entry_usuario.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        label_contrasena = ttk.Label(form_frame, text="Contraseña:")
        label_contrasena.grid(row=2, column=0, padx=10, pady=(20, 5), sticky='w')
        self.entry_contrasena = ttk.Entry(form_frame, width=30, style="Custom.TEntry", show="*")
        self.entry_contrasena.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # Botones Ingresar y Olvidaste tu contraseña
        button_frame = tk.Frame(form_frame, bg="#1f2329")
        button_frame.grid(row=4, column=0, pady=20)

        button_ingresar = ttk.Button(button_frame, text="Ingresar", command=self.ingresar, style="Custom.TButton")
        button_ingresar.pack(side=tk.LEFT, padx=5)

        label_olvidaste_contrasena = tk.Label(button_frame, text="¿Olvidaste tu contraseña?", fg="#c7d5e0", bg="#1f2329", cursor="hand2", font=('Segoe UI', 10, 'underline'))
        label_olvidaste_contrasena.pack(side=tk.LEFT, padx=5)
        label_olvidaste_contrasena.bind("<Button-1>", self.olvidaste_contrasena)

    def ingresar(self):
        # Función para manejar el ingreso
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()
        if usuario == "admin" and contrasena == "admin":
            self.notebook.tab(1, state='normal')
            self.notebook.tab(0, state='disabled')
            self.notebook.select(1)
            self.mostrar_interfaz_principal()
        else:
            print("Usuario o contraseña incorrectos")

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

        # Botones del menú lateral
        self.buttonDashBoard = tk.Button(self.menu_lateral, command=self.mostrar_dashboard)        
        self.buttonProductos = tk.Button(self.menu_lateral, command=self.mostrar_formulario_productos)        
        self.buttonUsuarios = tk.Button(self.menu_lateral, command=self.mostrar_formulario_usuarios)
        self.buttonArriendos = tk.Button(self.menu_lateral, command=self.mostrar_formulario_arriendos)        
        self.buttonMantenedorArriendos = tk.Button(self.menu_lateral, command=self.mostrar_formulario_mantenedor_arriendos)  # Nuevo botón

        buttons_info = [
            ("Dashboard", "📊", self.buttonDashBoard),
            ("Mantenedor Productos", "📚", self.buttonProductos),
            ("Mantenedor Usuarios", "👥", self.buttonUsuarios),
            ("Seguimiento Arriendos", "📅", self.buttonArriendos),
            ("Mantenedor Arriendos", "🏠", self.buttonMantenedorArriendos)  # Nuevo botón
        ]

        for text, icon, button in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)                    

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
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    def mostrar_dashboard(self):
        # Minimizar el menú lateral
        self.toggle_panel()

        # Limpiar el cuerpo principal
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Título del dashboard
        labelTitulo = tk.Label(self.cuerpo_principal, text="📊 Dashboard", font=("Roboto", 20), bg=COLOR_MENU_LATERAL, fg="white")
        labelTitulo.pack(anchor='nw', padx=10, pady=(10, 0))

    def mostrar_formulario_productos(self):
        # Minimizar el menú lateral
        self.toggle_panel()

        # Limpiar el cuerpo principal
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Crear un marco para agregar márgenes
        frame_notebook = tk.Frame(self.cuerpo_principal, bg=COLOR_MENU_LATERAL)
        frame_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Título del formulario
        labelTitulo = tk.Label(frame_notebook, text="📚 Mantenedor Productos", font=("Roboto", 20), bg=COLOR_MENU_LATERAL, fg="white")
        labelTitulo.pack(anchor='nw', padx=0, pady=(0, 0))

        # Crear el estilo para el notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=COLOR_MENU_LATERAL, borderwidth=0)
        style.configure('TNotebook.Tab', background=COLOR_MENU_LATERAL, foreground='#fff', font=("Roboto", 10), padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', COLOR_MENU_LATERAL), ('!selected', '#555555')], foreground=[('selected', '#fff'), ('!selected', '#ccc')])
        style.configure('TNotebook.Tab', borderwidth=0, relief='flat', padding=[10, 5], tabmargins=[0, 0, 0, 0])

        # Crear el notebook (pestañas)
        notebook = ttk.Notebook(frame_notebook, style='TNotebook')
        notebook.pack(fill='both', expand=True)

        # Crear las pestañas
        frame_ver_productos = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)
        frame_agregar_productos = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)
        frame_modificar_productos = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)
        frame_eliminar_productos = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)

        notebook.add(frame_ver_productos, text="Ver Productos")
        notebook.add(frame_agregar_productos, text="Agregar Productos")
        notebook.add(frame_modificar_productos, text="Modificar Productos")
        notebook.add(frame_eliminar_productos, text="Eliminar Productos")

        # Contenido de las pestañas (puedes personalizar esto según tus necesidades)
        tk.Label(frame_ver_productos, text="Contenido de Ver Productos", bg=COLOR_MENU_LATERAL, fg="#fff").pack(pady=10)
        tk.Label(frame_modificar_productos, text="Contenido de Modificar Productos", bg=COLOR_MENU_LATERAL, fg="#fff").pack(pady=10)
        tk.Label(frame_eliminar_productos, text="Contenido de Eliminar Productos", bg=COLOR_MENU_LATERAL, fg="#fff").pack(pady=10)

        # Formulario para agregar productos
        self.crear_formulario_agregar_productos(frame_agregar_productos)

        # Vincular el evento de cambio de pestaña para actualizar los estilos
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def configurar_estilo_entry(self, entry):
        entry.configure(bg="#1b2838", fg="#c7d5e0", insertbackground="#c7d5e0", highlightthickness=2, highlightbackground="#c7d5e0", highlightcolor="#c7d5e0", relief="flat")

    def crear_formulario_agregar_productos(self, frame):
        # Crear el marco principal con el nuevo color
        main_frame = tk.Frame(frame, bg="#1f2329")
        main_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Crear el formulario para agregar productos dentro del marco principal
        form_frame = tk.Frame(main_frame, bg="#1f2329")
        form_frame.pack(padx=10, pady=10, fill='both', expand=True)

        style = ttk.Style()
        style.configure("TLabel", font=('Segoe UI', 12), background="#1f2329", foreground="#c7d5e0")
        style.configure("Custom.TButton", fieldbackground="#1b2838", background="#1b2838", foreground="#c7d5e0", bordercolor="#c7d5e0", lightcolor="#c7d5e0", darkcolor="#c7d5e0", borderwidth=2, relief="raised")
        style.map("Custom.TButton", background=[("active", "#1b2838")])  # Quitar el brillo al pasar el mouse
        style.configure("Custom.TCombobox", fieldbackground="#1b2838", background="#1b2838", foreground="#c7d5e0", bordercolor="#c7d5e0", lightcolor="#c7d5e0", darkcolor="#c7d5e0", borderwidth=2, relief="flat")
        style.configure("Custom.TEntry", fieldbackground="#1b2838", background="#1b2838", foreground="#c7d5e0", bordercolor="#c7d5e0", lightcolor="#c7d5e0", darkcolor="#c7d5e0", borderwidth=2, relief="flat")

        # Crear un frame para los campos en la misma fila
        fields_frame = tk.Frame(form_frame, bg="#1f2329")
        fields_frame.pack(pady=10)

        # Etiquetas y entradas para Nombre del Libro, Precio y Stock
        label_nombre = ttk.Label(fields_frame, text="Nombre del Libro:")
        label_nombre.grid(row=0, column=0, padx=10, pady=(40, 5), sticky='w')  # Margen considerable arriba (duplicado)
        entry_nombre = ttk.Entry(fields_frame, width=30, style="Custom.TEntry")
        entry_nombre.grid(row=1, column=0, padx=10, pady=10, sticky='w')  # Margen a cada columna y fila

        label_precio = ttk.Label(fields_frame, text="Precio:")
        label_precio.grid(row=0, column=1, padx=10, pady=(40, 5), sticky='w')  # Margen considerable arriba (duplicado)
        entry_precio = ttk.Entry(fields_frame, width=30, style="Custom.TEntry")
        entry_precio.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        label_stock = ttk.Label(fields_frame, text="Stock:")
        label_stock.grid(row=0, column=2, padx=10, pady=(40, 5), sticky='w')  # Margen considerable arriba (duplicado)
        entry_stock = ttk.Entry(fields_frame, width=30, style="Custom.TEntry")
        entry_stock.grid(row=1, column=2, padx=10, pady=10, sticky='w')

        # Etiquetas y entradas para Autor y Género
        label_autor = ttk.Label(fields_frame, text="Autor:")
        label_autor.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        combo_autor = ttk.Combobox(fields_frame, values=["Autor 1", "Autor 2"], width=30, style="Custom.TCombobox")
        combo_autor.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        label_genero = ttk.Label(fields_frame, text="Género:")
        label_genero.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        combo_genero = ttk.Combobox(fields_frame, values=["Ciencia Ficción", "Thriller"], width=30, style="Custom.TCombobox")
        combo_genero.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Campo Imagen
        label_imagen = ttk.Label(fields_frame, text="Imagen:")
        label_imagen.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        button_imagen = ttk.Button(fields_frame, text="Cargar Imagen", command=self.cargar_imagen, style="Custom.TButton")
        button_imagen.grid(row=5, column=0, padx=10, pady=10, sticky='w')

        # Botones Enviar y Limpiar
        button_frame = tk.Frame(form_frame, bg="#1f2329")
        button_frame.pack(pady=10)

        button_enviar = ttk.Button(button_frame, text="Enviar", command=self.enviar_formulario, style="Custom.TButton")
        button_enviar.pack(side=tk.LEFT, padx=5)

        button_limpiar = ttk.Button(button_frame, text="Limpiar", command=self.limpiar_formulario, style="Custom.TButton")
        button_limpiar.pack(side=tk.LEFT, padx=5)

    def cargar_imagen(self):
        # Función para cargar una imagen desde el computador
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])
        if file_path:
            print(f"Imagen cargada: {file_path}")

    def enviar_formulario(self):
        # Función para manejar el envío del formulario
        print("Formulario enviado")

    def limpiar_formulario(self):
        # Función para manejar la limpieza del formulario
        print("Formulario limpiado")

    def mostrar_formulario_usuarios(self):
        # Minimizar el menú lateral
        self.toggle_panel()

        # Limpiar el cuerpo principal
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Crear un marco para agregar márgenes
        frame_notebook = tk.Frame(self.cuerpo_principal, bg=COLOR_MENU_LATERAL)
        frame_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Título del formulario
        labelTitulo = tk.Label(frame_notebook, text="👥 Mantenedor Usuarios", font=("Roboto", 20), bg=COLOR_MENU_LATERAL, fg="white")
        labelTitulo.pack(anchor='nw', padx=0, pady=(0, 0))

        # Crear el estilo para el notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=COLOR_MENU_LATERAL, borderwidth=0)
        style.configure('TNotebook.Tab', background=COLOR_MENU_LATERAL, foreground='#fff', font=("Roboto", 10), padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', COLOR_MENU_LATERAL), ('!selected', '#555555')], foreground=[('selected', '#fff'), ('!selected', '#ccc')])
        style.configure('TNotebook.Tab', borderwidth=0, relief='flat', padding=[10, 5], tabmargins=[0, 0, 0, 0])

        # Crear el notebook (pestañas)
        notebook = ttk.Notebook(frame_notebook, style='TNotebook')
        notebook.pack(fill='both', expand=True)

        # Crear las pestañas
        frame_ver_usuarios = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)
        frame_agregar_usuarios = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)
        frame_modificar_usuarios = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)
        frame_eliminar_usuarios = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)

        notebook.add(frame_ver_usuarios, text="Ver Usuarios")
        notebook.add(frame_agregar_usuarios, text="Agregar Usuarios")
        notebook.add(frame_modificar_usuarios, text="Modificar Usuarios")
        notebook.add(frame_eliminar_usuarios, text="Eliminar Usuarios")

        # Contenido de las pestañas (puedes personalizar esto según tus necesidades)
        tk.Label(frame_ver_usuarios, text="Contenido de Ver Usuarios", bg=COLOR_MENU_LATERAL, fg="#fff").pack(pady=10)
        tk.Label(frame_agregar_usuarios, text="Contenido de Agregar Usuarios", bg=COLOR_MENU_LATERAL, fg="#fff").pack(pady=10)
        tk.Label(frame_modificar_usuarios, text="Contenido de Modificar Usuarios", bg=COLOR_MENU_LATERAL, fg="#fff").pack(pady=10)
        tk.Label(frame_eliminar_usuarios, text="Contenido de Eliminar Usuarios", bg=COLOR_MENU_LATERAL, fg="#fff").pack(pady=10)

        # Vincular el evento de cambio de pestaña para actualizar los estilos
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def mostrar_formulario_mantenedor_arriendos(self):
        # Minimizar el menú lateral
        self.toggle_panel()

        # Limpiar el cuerpo principal
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Crear un marco para agregar márgenes
        frame_notebook = tk.Frame(self.cuerpo_principal, bg=COLOR_MENU_LATERAL)
        frame_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Título del formulario
        labelTitulo = tk.Label(frame_notebook, text="🏠 Mantenedor Arriendos", font=("Roboto", 20), bg=COLOR_MENU_LATERAL, fg="white")
        labelTitulo.pack(anchor='nw', padx=0, pady=(0, 0))

        # Crear el estilo para el notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=COLOR_MENU_LATERAL, borderwidth=0)
        style.configure('TNotebook.Tab', background=COLOR_MENU_LATERAL, foreground='#fff', font=("Roboto", 10), padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', COLOR_MENU_LATERAL), ('!selected', '#555555')], foreground=[('selected', '#fff'), ('!selected', '#ccc')])
        style.configure('TNotebook.Tab', borderwidth=0, relief='flat', padding=[10, 5], tabmargins=[0, 0, 0, 0])

        # Crear el notebook (pestañas)
        notebook = ttk.Notebook(frame_notebook, style='TNotebook')
        notebook.pack(fill='both', expand=True)

        # Crear las pestañas
        frame_ver_arriendos = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)
        frame_agregar_arriendos = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)
        frame_modificar_arriendos = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)
        frame_eliminar_arriendos = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)

        notebook.add(frame_ver_arriendos, text="Ver Arriendos")
        notebook.add(frame_agregar_arriendos, text="Agregar Arriendos")
        notebook.add(frame_modificar_arriendos, text="Modificar Arriendos")
        notebook.add(frame_eliminar_arriendos, text="Eliminar Arriendos")

        # Contenido de las pestañas (puedes personalizar esto según tus necesidades)
        tk.Label(frame_ver_arriendos, text="Contenido de Ver Arriendos", bg=COLOR_MENU_LATERAL, fg="#fff").pack(pady=10)
        tk.Label(frame_agregar_arriendos, text="Contenido de Agregar Arriendos", bg=COLOR_MENU_LATERAL, fg="#fff").pack(pady=10)
        tk.Label(frame_modificar_arriendos, text="Contenido de Modificar Arriendos", bg=COLOR_MENU_LATERAL, fg="#fff").pack(pady=10)
        tk.Label(frame_eliminar_arriendos, text="Contenido de Eliminar Arriendos", bg=COLOR_MENU_LATERAL, fg="#fff").pack(pady=10)

        # Vincular el evento de cambio de pestaña para actualizar los estilos
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def mostrar_formulario_arriendos(self):
        # Minimizar el menú lateral
        self.toggle_panel()

        # Limpiar el cuerpo principal
        for widget in self.cuerpo_principal.winfo_children():
            widget.destroy()

        # Crear un marco para agregar márgenes
        frame_notebook = tk.Frame(self.cuerpo_principal, bg=COLOR_MENU_LATERAL)
        frame_notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Título del formulario
        labelTitulo = tk.Label(frame_notebook, text="📅 Seguimiento Arriendos", font=("Roboto", 20), bg=COLOR_MENU_LATERAL, fg="white")
        labelTitulo.pack(anchor='nw', padx=0, pady=(0, 0))

        # Crear el estilo para el notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=COLOR_MENU_LATERAL, borderwidth=0)
        style.configure('TNotebook.Tab', background=COLOR_MENU_LATERAL, foreground='#fff', font=("Roboto", 10), padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', COLOR_MENU_LATERAL), ('!selected', '#555555')], foreground=[('selected', '#fff'), ('!selected', '#ccc')])
        style.configure('TNotebook.Tab', borderwidth=0, relief='flat', padding=[10, 5], tabmargins=[0, 0, 0, 0])

        # Crear el notebook (pestañas)
        notebook = ttk.Notebook(frame_notebook, style='TNotebook')
        notebook.pack(fill='both', expand=True)

        # Crear las pestañas
        frame_pendiente = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)
        frame_entregado = tk.Frame(notebook, bg=COLOR_MENU_LATERAL)

        notebook.add(frame_pendiente, text="Pendiente")
        notebook.add(frame_entregado, text="Entregado")

        # Contenido de las pestañas (puedes personalizar esto según tus necesidades)
        tk.Label(frame_pendiente, text="Contenido de Pendiente", bg=COLOR_MENU_LATERAL, fg="#fff").pack(pady=10)
        tk.Label(frame_entregado, text="Contenido de Entregado", bg=COLOR_MENU_LATERAL, fg="#fff").pack(pady=10)

        # Vincular el evento de cambio de pestaña para actualizar los estilos
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event):
        notebook = event.widget
        selected_tab = notebook.select()
        for tab_id in notebook.tabs():
            if tab_id == selected_tab:
                notebook.tab(tab_id, state='normal')
            else:
                notebook.tab(tab_id, state='normal')