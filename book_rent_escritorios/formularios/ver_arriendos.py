import tkinter as tk
from tkinter import ttk, messagebox
import threading
import mysql.connector
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import filedialog
import requests
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def animar_boton_arriendo(boton, cargando_flag, ventana):
    def actualizar_texto():
        # Verificar si el botón aún existe antes de intentar actualizar su texto
        if not boton.winfo_exists():
            return
        
        # Detener la animación si cargando_flag es False
        if not cargando_flag[0]:
            boton.config(text="Modificar")  # Texto final cuando se detiene
            return
        
        # Animación de puntos suspensivos
        puntos = boton.cget("text").count(".") % 3 + 1
        boton.config(text="Cargando" + "." * puntos)
        
        # Llama a actualizar_texto después de 500 ms para continuar la animación
        ventana.after(500, actualizar_texto)
    
    actualizar_texto()

class VerArriendos:
    def __init__(self, parent):
        self.parent = parent
        self.pagina_actual = 0
        self.arriendos_por_pagina = 2  
        self.cache_imagenes = {}
        self.mostrar_arriendos() 

    def obtener_arriendos(self, limite=10, offset=0, busqueda=None):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='dbacapstone'
            )
            cursor = conexion.cursor()

            if busqueda:
                query = """
                SELECT app_libroarr.id, app_libroarr.nom_libro, app_libroarr.stock, app_libroarr.imagen, 
                       app_autor.nombre_autor, app_generolib.nombre, app_libroarr.id_genero_id
                FROM app_libroarr
                JOIN app_autor ON app_libroarr.id_autor_id = app_autor.id
                JOIN app_generolib ON app_libroarr.id_genero_id = app_generolib.id
                WHERE LOWER(app_libroarr.nom_libro) LIKE %s
                LIMIT %s OFFSET %s
                """
                cursor.execute(query, (f'%{busqueda}%', limite, offset))
            else:
                query = """
                SELECT app_libroarr.id, app_libroarr.nom_libro, app_libroarr.stock, app_libroarr.imagen, 
                       app_autor.nombre_autor, app_generolib.nombre, app_libroarr.id_genero_id
                FROM app_libroarr
                JOIN app_autor ON app_libroarr.id_autor_id = app_autor.id
                JOIN app_generolib ON app_libroarr.id_genero_id = app_generolib.id
                LIMIT %s OFFSET %s
                """
                cursor.execute(query, (limite, offset))

            arriendos = cursor.fetchall()
            cursor.close()
            conexion.close()
            return arriendos
        except Exception as e:
            print(f"Error al obtener los arriendos: {e}")
            return []

    def obtener_total_arriendos(self):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='dbacapstone'
            )
            cursor = conexion.cursor()
            query = "SELECT COUNT(*) FROM app_libroarr"
            cursor.execute(query)
            total_arriendos = cursor.fetchone()[0]
            cursor.close()
            conexion.close()
            return total_arriendos
        except Exception as e:
            print(f"Error al obtener el total de arriendos: {e}")
            return 0

    @staticmethod
    def convertir_url_google_drive(url):
        if "drive.google.com" in url:
            file_id = url.split("/d/")[1].split("/")[0]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        return url


    def crear_carta_arriendo(self, container_frame, arriendo_id, nom_libro, stock, imagen_url, nombre_autor, nombre_genero, id_genero_id):
        frame_carta = tk.Frame(container_frame, bg="#1f2329", relief="raised", borderwidth=2)
        frame_carta.pack(pady=10, padx=10, fill='x')

        imagen_url = self.convertir_url_google_drive(imagen_url)

        if imagen_url in self.cache_imagenes:
            img_tk = self.cache_imagenes[imagen_url]
            label_img = tk.Label(frame_carta, image=img_tk, bg="#1f2329")
            label_img.image = img_tk  
            label_img.grid(row=0, column=0, rowspan=6, padx=10, pady=10)
        else:
            label_cargando = tk.Label(frame_carta, text="Cargando...", bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
            label_cargando.grid(row=0, column=0, rowspan=6, padx=10, pady=10)
            self.cargar_imagen_diferida_arriendo(frame_carta, imagen_url, label_cargando)

        padding_vertical = 5
        bold_font = ("Roboto", 12, "bold")

        # Crear los demás labels con espaciado uniforme
        label_nombre_campo = tk.Label(frame_carta, text="Nombre: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_nombre_campo.grid(row=0, column=1, sticky='w', padx=5, pady=padding_vertical)

        label_nombre_valor = tk.Label(frame_carta, text=nom_libro, bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_nombre_valor.grid(row=0, column=2, sticky='w', padx=5, pady=padding_vertical)

        label_autor_campo = tk.Label(frame_carta, text="Autor: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_autor_campo.grid(row=1, column=1, sticky='w', padx=5, pady=padding_vertical)

        label_autor_valor = tk.Label(frame_carta, text=nombre_autor, bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_autor_valor.grid(row=1, column=2, sticky='w', padx=5, pady=padding_vertical)

        label_genero_campo = tk.Label(frame_carta, text="Género: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_genero_campo.grid(row=2, column=1, sticky='w', padx=5, pady=padding_vertical)

        label_genero_valor = tk.Label(frame_carta, text=nombre_genero, bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_genero_valor.grid(row=2, column=2, sticky='w', padx=5, pady=padding_vertical)

        label_stock_campo = tk.Label(frame_carta, text="Stock: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_stock_campo.grid(row=3, column=1, sticky='w', padx=5, pady=padding_vertical)

        label_stock_valor = tk.Label(frame_carta, text=stock, bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_stock_valor.grid(row=3, column=2, sticky='w', padx=5, pady=padding_vertical)

        cargando_flag = [False]

        # Botón Modificar, alineado a la derecha
        boton_modificar = ttk.Button(
            frame_carta, 
            text="Modificar", 
            style="Custom.TButton", 
            width=12,
            command=lambda: self.iniciar_modificacion_arriendo(boton_modificar, cargando_flag, arriendo_id, nom_libro, id_genero_id)
        )
        boton_modificar.grid(row=1, column=3, pady=padding_vertical, padx=5, sticky="e")

        # Botón Eliminar, alineado a la derecha
        boton_eliminar = ttk.Button(
            frame_carta, 
            text="Eliminar", 
            style="Custom.TButton", 
            width=12,
            command=lambda: self.confirmar_eliminacion_arriendo(arriendo_id, nom_libro)
        )
        boton_eliminar.grid(row=2, column=3, pady=padding_vertical, padx=5, sticky="e")

        frame_carta.grid_columnconfigure(2, weight=1)
        frame_carta.grid_columnconfigure(3, weight=1)


    def iniciar_modificacion_arriendo(self, boton, cargando_flag, arriendo_id, nom_libro, id_genero_id):
        ventana_principal = self.parent
        cargando_flag[0] = True
        animar_boton_arriendo(boton, cargando_flag, ventana_principal)
        threading.Thread(target=lambda: ModificarArriendoForm(self, self.parent, arriendo_id, nom_libro, id_genero_id, cargando_flag)).start()





    def proceso_modificacion_arriendo(self, cargando_flag):
        time.sleep(3)
        self.parent.after(0, lambda: cargando_flag.__setitem__(0, False))

    def confirmar_eliminacion_arriendo(self, arriendo_id, nom_libro):
        respuesta = messagebox.askquestion(
            "Eliminar Arriendo", 
            f"¿Realmente quiere eliminar el arriendo '{nom_libro}'?\nEste no podrá ser recuperado.",
            icon='warning'
        )
        if respuesta == 'yes':
            self.eliminar_arriendo(arriendo_id)

    def eliminar_arriendo(self, arriendo_id):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='dbacapstone'
            )
            cursor = conexion.cursor()
            query = "DELETE FROM app_libro WHERE id = %s"
            cursor.execute(query, (arriendo_id,))
            conexion.commit()
            cursor.close()
            conexion.close()
            messagebox.showinfo("Arriendo Eliminado", "El arriendo ha sido eliminado correctamente.")
            self.mostrar_arriendos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el arriendo: {e}")

    def cargar_imagen_diferida_arriendo(self, frame_carta, imagen_url, label_cargando):
        def cargar():
            try:
                response = requests.get(imagen_url)
                image_data = BytesIO(response.content)
                img = Image.open(image_data)
                img = img.resize((100, 150))
                img_tk = ImageTk.PhotoImage(img)
                self.cache_imagenes[imagen_url] = img_tk
                frame_carta.after(0, lambda: self.mostrar_imagen_arriendo(frame_carta, img_tk, label_cargando))
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")
        hilo_imagen = threading.Thread(target=cargar)
        hilo_imagen.start()

    def mostrar_imagen_arriendo(self, frame_carta, img_tk, label_cargando):
        if frame_carta.winfo_exists():
            label_cargando.destroy()
            label_img = tk.Label(frame_carta, image=img_tk, bg="#1f2329")
            label_img.image = img_tk  
            label_img.grid(row=0, column=0, rowspan=5, padx=10, pady=10)

    def mostrar_arriendos(self):
        if not hasattr(self, 'pagina_actual'):
            self.pagina_actual = 0
        if not hasattr(self, 'arriendos_por_pagina'):
            self.arriendos_por_pagina = 2

        if hasattr(self, 'frame_arriendos') and self.frame_arriendos.winfo_exists():
            self.frame_arriendos.destroy()

        if not hasattr(self, 'frame_ver_arriendos') or not self.frame_ver_arriendos.winfo_exists():
            self.frame_ver_arriendos = tk.Frame(self.parent, bg="#1f2329")
            self.frame_ver_arriendos.pack(fill='both', expand=True)
            self.frame_ver_arriendos.focus_set()
            self.frame_ver_arriendos.update_idletasks()

            if not hasattr(self, 'entry_busqueda') or not self.entry_busqueda.winfo_exists():
                self.frame_busqueda = tk.Frame(self.frame_ver_arriendos, bg="#1f2329")
                self.frame_busqueda.pack(fill='x', padx=10, pady=10)

                self.entry_busqueda = ttk.Entry(self.frame_busqueda, width=40, style="Custom.TEntry")
                self.entry_busqueda.pack(side=tk.LEFT, padx=10)
                self.entry_busqueda.insert(0, "Búsqueda por nombre")
                self.entry_busqueda.bind("<FocusIn>", self.clear_placeholder_arriendo)
                self.entry_busqueda.bind("<FocusOut>", self.add_placeholder_arriendo)
                self.entry_busqueda.bind("<KeyRelease>", self.mostrar_arriendos_filtrados)
                self.entry_busqueda.update_idletasks()

        self.frame_arriendos = tk.Frame(self.frame_ver_arriendos, bg="#1f2329")
        self.frame_arriendos.pack(fill='both', expand=True)
        self.frame_arriendos.update_idletasks()

        if not hasattr(self, 'frame_paginacion') or not self.frame_paginacion.winfo_exists():
            self.frame_paginacion = tk.Frame(self.frame_ver_arriendos, bg="#1f2329")
            self.frame_paginacion.pack(pady=10, side=tk.BOTTOM, fill='x')

            self.boton_anterior = ttk.Button(self.frame_paginacion, text="Anterior", command=self.anterior_pagina_arriendo, style="Custom.TButton", width=10)
            self.boton_anterior.pack(side=tk.LEFT, padx=10, pady=10)
            self.boton_anterior.update_idletasks()

            self.label_paginacion = tk.Label(self.frame_paginacion, text="Página 1 de 1", bg="#1f2329", fg="#c7d5e0", font=("Roboto", 10, "bold"))
            self.label_paginacion.pack(side=tk.LEFT, padx=10, pady=10, expand=True)
            self.label_paginacion.update_idletasks()

            self.boton_siguiente = ttk.Button(self.frame_paginacion, text="Siguiente", command=self.siguiente_pagina_arriendo, style="Custom.TButton", width=10)
            self.boton_siguiente.pack(side=tk.RIGHT, padx=10, pady=10)
            self.boton_siguiente.update_idletasks()

        self.mostrar_arriendos_paginados()

    def mostrar_arriendos_paginados(self):
        for widget in self.frame_arriendos.winfo_children():
            widget.destroy()

        arriendos = self.obtener_arriendos(limite=self.arriendos_por_pagina, offset=self.pagina_actual * self.arriendos_por_pagina)

        if not arriendos:
            label_no_arriendos = tk.Label(self.frame_arriendos, text="No se encontraron arriendos.", bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
            label_no_arriendos.pack(pady=20)
            return

        for arriendo in arriendos:
            self.crear_carta_arriendo(self.frame_arriendos, *arriendo)

        total_arriendos = self.obtener_total_arriendos()
        self.actualizar_botones_paginacion_arriendo(total_arriendos)

    def mostrar_arriendos_filtrados(self, event=None):
        busqueda = self.entry_busqueda.get().lower().strip()
        self.busqueda_actual = busqueda
        self.pagina_actual = 0

        if not busqueda:
            self.mostrar_arriendos_paginados()
        else:
            arriendos = self.obtener_arriendos(busqueda=busqueda, limite=self.arriendos_por_pagina, offset=self.pagina_actual * self.arriendos_por_pagina)
            total_arriendos_filtrados = len(self.obtener_arriendos(busqueda=busqueda))

            for widget in self.frame_arriendos.winfo_children():
                widget.destroy()

            if not arriendos:
                self.label_paginacion.pack_forget()
                self.boton_anterior.config(state=tk.DISABLED)
                self.boton_siguiente.config(state=tk.DISABLED)
                label_no_arriendos = tk.Label(self.frame_arriendos, text="No se encontraron arriendos.", bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
                label_no_arriendos.pack(pady=20)
            else:
                for arriendo in arriendos:
                    self.crear_carta_arriendo(self.frame_arriendos, *arriendo)
                self.actualizar_botones_paginacion_arriendo(total_arriendos_filtrados)

    def mostrar_arriendos_paginados_filtrados(self):
        busqueda = self.busqueda_actual
        arriendos = self.obtener_arriendos(busqueda=busqueda, limite=self.arriendos_por_pagina, offset=self.pagina_actual * self.arriendos_por_pagina)
        total_arriendos_filtrados = len(self.obtener_arriendos(busqueda=busqueda))

        for widget in self.frame_arriendos.winfo_children():
            widget.destroy()

        if not arriendos:
            label_no_arriendos = tk.Label(self.frame_arriendos, text="No se encontraron arriendos.", bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
            label_no_arriendos.pack(pady=20)
        else:
            for arriendo in arriendos:
                self.crear_carta_arriendo(self.frame_arriendos, *arriendo)
            self.actualizar_botones_paginacion_arriendo(total_arriendos_filtrados)

    def actualizar_botones_paginacion_arriendo(self, total_arriendos):
        total_paginas = (total_arriendos + self.arriendos_por_pagina - 1) // self.arriendos_por_pagina

        if total_arriendos == 0:
            self.label_paginacion.pack_forget()
            self.boton_anterior.config(state=tk.DISABLED)
            self.boton_siguiente.config(state=tk.DISABLED)
        else:
            self.label_paginacion.pack(side=tk.LEFT, padx=10, pady=10, expand=True)
            self.label_paginacion.config(text=f"Página {self.pagina_actual + 1} de {total_paginas}")

            if self.pagina_actual == 0:
                self.boton_anterior.config(state=tk.DISABLED)
            else:
                self.boton_anterior.config(state=tk.NORMAL)

            if self.pagina_actual >= total_paginas - 1:
                self.boton_siguiente.config(state=tk.DISABLED)
            else:
                self.boton_siguiente.config(state=tk.NORMAL)

    def siguiente_pagina_arriendo(self):
        self.pagina_actual += 1

        if hasattr(self, 'busqueda_actual') and self.busqueda_actual:
            self.mostrar_arriendos_paginados_filtrados()
        else:
            self.mostrar_arriendos_paginados()

    def anterior_pagina_arriendo(self):
        self.pagina_actual -= 1

        if hasattr(self, 'busqueda_actual') and self.busqueda_actual:
            self.mostrar_arriendos_paginados_filtrados()
        else:
            self.mostrar_arriendos_paginados()

    def clear_placeholder_arriendo(self, event):
        if self.entry_busqueda.get() == "Búsqueda por nombre":
            self.entry_busqueda.delete(0, tk.END)

    def add_placeholder_arriendo(self, event):
        if not self.entry_busqueda.get():
            self.entry_busqueda.insert(0, "Búsqueda por nombre")

def centrar_ventana_arriendo(ventana, width, height):
    ventana.update_idletasks()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla - width) // 2
    y = (alto_pantalla - height) // 2
    ventana.geometry(f"{width}x{height}+{x}+{y}")
    ventana.lift()
    ventana.focus_force()


class ModificarArriendoForm:
    def __init__(self, ver_arriendos_instance, parent, arriendo_id, nom_libro, id_genero_id, cargando_flag):
        self.ver_arriendos_instance = ver_arriendos_instance
        self.parent = parent
        self.arriendo_id = arriendo_id
        self.nom_libro = nom_libro
        self.id_genero_id = id_genero_id
        self.img_tk = None
        self.cargando = [False]
        self.cargando_flag = cargando_flag
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'dbacapstone'
        }

        # Crear la ventana de modificación
        self.ventana_modificar = tk.Toplevel(self.parent)
        self.ventana_modificar.title(f"Modificar Arriendo: {self.nom_libro}")
        self.ventana_modificar.configure(bg="#1f2329")
        w, h = 700, 500
        self.crear_formulario_modificar_arriendo()
        centrar_ventana_arriendo(self.ventana_modificar, w, h)
        self.cargando_flag[0] = False 
            
    def crear_formulario_modificar_arriendo(self):
        main_frame = tk.Frame(self.ventana_modificar, bg="#1f2329")
        main_frame.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="nsew")

        # Padding consistente
        padding_vertical = 10
        padding_horizontal = 20
        extra_padding_top_buttons = 80  # Espacio adicional en la parte superior de los botones

        arriendo = self.obtener_datos_arriendo(self.nom_libro)

        if not arriendo:
            messagebox.showerror("Error", "No se encontraron datos para el arriendo.")
            self.ventana_modificar.destroy()
            return

        # Imagen y botón "Cargar Imagen" con padding uniforme
        label_img = tk.Label(main_frame, bg="#1f2329")
        label_img.grid(row=0, column=0, rowspan=6, padx=padding_horizontal, pady=(padding_vertical * 3, padding_vertical))
        imagen_url = VerArriendos.convertir_url_google_drive(arriendo[2])
        self.cargar_imagen_desde_url_arriendo(imagen_url, label_img)

        # Estimación del ancho del botón en función del ancho del label de la imagen
        main_frame.update_idletasks()  # Asegura que label_img tenga su tamaño final
        ancho_imagen = label_img.winfo_width()
        ancho_boton = max(10, int(ancho_imagen / 10 * 1.5))  # Ajuste a tres cuartos del doble en caracteres

        # Crear el botón "Cargar Imagen" con el ancho calculado
        button_cargar_imagen = ttk.Button(main_frame, text="Cargar Imagen", style="Custom.TButton", command=lambda: self.cargar_imagen_modificar_arriendo(label_img))
        button_cargar_imagen.grid(row=6, column=0, padx=padding_horizontal, pady=padding_vertical, sticky='w')
        button_cargar_imagen.config(width=ancho_boton)  # Ajusta el ancho del botón

        # Campos de formulario con padding uniforme
        self.entry_nombre = self.crear_campo_formulario_arriendo(main_frame, "Nombre del Libro:", arriendo[0], 30, 0, 1, padding_vertical, padding_horizontal)
        self.entry_stock = self.crear_campo_formulario_arriendo(main_frame, "Stock:", arriendo[1], 30, 2, 1, padding_vertical, padding_horizontal)

        autores = self.obtener_autores_arriendo()
        self.combo_autor = self.crear_combobox_formulario_arriendo(main_frame, "Autor:", autores, arriendo[3], 30, 4, 1, padding_vertical, padding_horizontal)

        generos = self.obtener_generos_arriendo()
        self.combo_genero = self.crear_combobox_formulario_arriendo(main_frame, "Género:", generos, arriendo[4], 30, 6, 1, padding_vertical, padding_horizontal)

        # Botones con espacio adicional en la parte superior
        self.button_modificar = ttk.Button(main_frame, text="Modificar", style="Custom.TButton", width=12, command=self.iniciar_modificacion_arriendo)
        self.button_modificar.grid(row=8, column=1, padx=padding_horizontal, pady=(extra_padding_top_buttons, padding_vertical), sticky='e')

        button_cancelar = ttk.Button(main_frame, text="Cancelar", style="Custom.TButton", width=12, command=self.cerrar_ventana_arriendo)
        button_cancelar.grid(row=8, column=2, padx=padding_horizontal, pady=(extra_padding_top_buttons, padding_vertical), sticky='w')

        # Ajuste de columnas
        main_frame.grid_columnconfigure(1, weight=1)






    def iniciar_modificacion_arriendo(self):
        # Iniciar la bandera de animación antes de llamar a la animación
        self.cargando[0] = True
        # Iniciar la animación en el botón
        animar_boton_arriendo(self.button_modificar, self.cargando, self.parent)
        # Ejecutar el proceso de modificación en un hilo separado
        threading.Thread(target=self.modificar_arriendo_en_bd).start()

    def cerrar_ventana_arriendo(self):
        self.cargando[0] = False  # Detener la animación
        self.ventana_modificar.destroy()

    def obtener_autores_arriendo(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre_autor FROM app_autor")
            autores = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conexion.close()
            return autores
        except Exception as e:
            print(f"Error al obtener los autores: {e}")
            return []

    def obtener_generos_arriendo(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre FROM app_generolib")
            generos = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conexion.close()
            return generos
        except Exception as e:
            print(f"Error al obtener los géneros: {e}")
            return []

    def crear_campo_formulario_arriendo(self, parent, label_text, value, entry_width, row, column, pady=5, padx=5):
        label = ttk.Label(parent, text=label_text, background="#1f2329", foreground="#c7d5e0", font=("Segoe UI", 12))
        label.grid(row=row, column=column, padx=padx, pady=(pady, 0), sticky='w')
        entry = ttk.Entry(parent, width=entry_width, style="Custom.TEntry")
        entry.grid(row=row, column=column + 1, padx=padx, pady=pady, sticky='w')
        entry.insert(0, value)
        return entry

    def crear_combobox_formulario_arriendo(self, parent, label_text, values, selected_value, combo_width, row, column, pady=5, padx=5):
        label = ttk.Label(parent, text=label_text, background="#1f2329", foreground="#c7d5e0", font=("Segoe UI", 12))
        label.grid(row=row, column=column, padx=padx, pady=(pady, 0), sticky='w')
        combobox = ttk.Combobox(parent, values=values, width=combo_width, style="Custom.TCombobox")
        combobox.grid(row=row, column=column + 1, padx=padx, pady=pady, sticky='w')
        combobox.set(selected_value)
        return combobox


    def obtener_datos_arriendo(self, nom_libro):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            query = """
                SELECT app_libroarr.nom_libro, app_libroarr.stock, app_libroarr.imagen, 
                    app_autor.nombre_autor, app_generolib.nombre 
                FROM app_libroarr
                JOIN app_autor ON app_libroarr.id_autor_id = app_autor.id
                JOIN app_generolib ON app_libroarr.id_genero_id = app_generolib.id
                WHERE app_libroarr.nom_libro = %s
            """
            cursor.execute(query, (nom_libro,))
            arriendo = cursor.fetchone()
            cursor.close()
            conexion.close()
            return arriendo
        except Exception as e:
            print(f"Error al obtener los datos del arriendo: {e}")
            return None

    def cargar_imagen_desde_url_arriendo(self, imagen_url, label_img):
        if imagen_url:
            try:
                response = requests.get(imagen_url)
                if response.status_code == 200:
                    image_data = BytesIO(response.content)
                    img = Image.open(image_data)
                    img = img.resize((150, 200))
                    self.img_tk = ImageTk.PhotoImage(img)
                    label_img.config(image=self.img_tk)
                    label_img.image = self.img_tk
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")

    def cargar_imagen_modificar_arriendo(self, label_img):
        self.ventana_modificar.attributes('-topmost', False)
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.png")])
        self.ventana_modificar.attributes('-topmost', True)
        if file_path:
            img = Image.open(file_path)
            img = img.resize((150, 200))
            self.img_tk = ImageTk.PhotoImage(img)
            label_img.config(image=self.img_tk)
            label_img.image = self.img_tk

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

    def modificar_arriendo_en_bd(self):
        # Variables de entrada para la base de datos
        id_arriendo = self.nom_libro
        nombre = self.entry_nombre.get()
        stock = int(self.entry_stock.get())
        autor = self.combo_autor.get()
        genero = self.combo_genero.get()
        imagen_url = None

        try:
            # Si se ha seleccionado una nueva imagen, subirla a Google Drive
            if hasattr(self, 'ruta_imagen_local'):
                drive = self.autenticar_google_drive()
                archivo_drive = drive.CreateFile({
                    'parents': [{'id': '1nHP5tyVyjDPpXE7N5Tm4nAK63PhzUIEP'}],
                    'title': nombre
                })
                archivo_drive.SetContentFile(self.ruta_imagen_local)
                archivo_drive.Upload()
                imagen_url = archivo_drive['alternateLink']
                print(f"Imagen actualizada correctamente: {imagen_url}")

            # Conectar a la base de datos y actualizar los datos, incluyendo la imagen si se cambió
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            
            # Construir la consulta de actualización
            query = """
                UPDATE app_libroarr 
                SET nom_libro=%s, stock=%s, 
                    id_autor_id=(SELECT id FROM app_autor WHERE nombre_autor=%s), 
                    id_genero_id=(SELECT id FROM app_generolib WHERE nombre=%s)
            """
            params = [nombre, stock, autor, genero]
            
            # Solo incluir la URL de la imagen si fue cambiada
            if imagen_url:
                query += ", imagen=%s"
                params.append(imagen_url)
            
            query += " WHERE nom_libro=%s"
            params.append(id_arriendo)

            # Ejecutar la consulta de actualización
            cursor.execute(query, params)
            conexion.commit()

            # Hacer que la ventana esté en modo topmost antes de mostrar el mensaje
            self.ventana_modificar.attributes('-topmost', True)
            messagebox.showinfo("Éxito", "Arriendo modificado correctamente.", parent=self.ventana_modificar)
            self.ventana_modificar.attributes('-topmost', False)

            # Detener la animación una vez que todo el proceso se haya completado
            self.cargando[0] = False

            # Cerrar la ventana de modificación
            self.cerrar_ventana_arriendo()
            
            # Actualizar la ventana de arriendos después de modificar
            self.ver_arriendos_instance.mostrar_arriendos()

        except Exception as e:
            # Mostrar el mensaje de error en caso de falla
            self.cargando[0] = False  # Asegurarse de detener la animación
            messagebox.showerror("Error", f"No se pudo modificar el arriendo: {e}")

        finally:
            # Cerrar los recursos de la base de datos
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def cargar_imagen_modificar_arriendo(self, label_img):
        self.ventana_modificar.attributes('-topmost', False)
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.png")])
        self.ventana_modificar.attributes('-topmost', True)
        if file_path:
            self.ruta_imagen_local = file_path  # Guardar la ruta de la imagen seleccionada
            img = Image.open(file_path)
            img = img.resize((150, 200))
            self.img_tk = ImageTk.PhotoImage(img)
            label_img.config(image=self.img_tk)
            label_img.image = self.img_tk