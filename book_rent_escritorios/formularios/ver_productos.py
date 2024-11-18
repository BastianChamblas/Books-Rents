import tkinter as tk
from tkinter import ttk, messagebox
import threading
import mysql.connector
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import filedialog
import requests
import threading
import time
import re

def animar_boton(boton, cargando_flag, ventana):
    def actualizar_texto():
        if not cargando_flag[0] or not boton.winfo_exists():
            boton.config(text="Modificar")  # Texto final cuando se detiene
            return

        # Contar puntos para simular animación
        puntos = boton.cget("text").count(".") % 3 + 1
        boton.config(text="Cargando" + "." * puntos)
        
        # Llama a la función nuevamente después de 500ms para actualizar la animación
        ventana.after(500, actualizar_texto)

    # Iniciar la animación
    actualizar_texto()

class VerProductos:
    def __init__(self, parent):
        self.parent = parent
        self.pagina_actual = 0
        self.productos_por_pagina = 2  
        self.cache_imagenes = {}
        self.mostrar_productos()

    def obtener_productos(self, limite=10, offset=0, busqueda=None):
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
                SELECT app_libro.id, app_libro.nom_libro, app_libro.precio, app_libro.stock, app_libro.imagen, 
                    app_autor.nombre_autor, app_generolib.nombre 
                FROM app_libro
                JOIN app_autor ON app_libro.id_autor_id = app_autor.id
                JOIN app_generolib ON app_libro.id_genero_id = app_generolib.id
                WHERE LOWER(app_libro.nom_libro) LIKE %s
                LIMIT %s OFFSET %s
                """
                cursor.execute(query, (f'%{busqueda}%', limite, offset))
            else:
                query = """
                SELECT app_libro.id, app_libro.nom_libro, app_libro.precio, app_libro.stock, app_libro.imagen, 
                    app_autor.nombre_autor, app_generolib.nombre 
                FROM app_libro
                JOIN app_autor ON app_libro.id_autor_id = app_autor.id
                JOIN app_generolib ON app_libro.id_genero_id = app_generolib.id
                LIMIT %s OFFSET %s
                """
                cursor.execute(query, (limite, offset))

            productos = cursor.fetchall()
            cursor.close()
            conexion.close()
            return productos
        except Exception as e:
            print(f"Error al obtener los productos: {e}")
            return []

    def obtener_total_productos(self):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='dbacapstone'
            )
            cursor = conexion.cursor()
            query = "SELECT COUNT(*) FROM app_libro"
            cursor.execute(query)
            total_productos = cursor.fetchone()[0]
            cursor.close()
            conexion.close()
            return total_productos
        except Exception as e:
            print(f"Error al obtener el total de productos: {e}")
            return 0

    def convertir_url_google_drive(self, url):
        if "drive.google.com" in url:
            file_id = url.split("/d/")[1].split("/")[0]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        return url

    def crear_carta_producto(self, container_frame, producto_id, nom_libro, precio, stock, imagen_url, nombre_autor, nombre_genero):
        # Disminuir el espacio vertical entre las cards ajustando el valor de pady
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
            self.cargar_imagen_diferida(frame_carta, imagen_url, label_cargando)

        padding_vertical = 1
        bold_font = ("Roboto", 12, "bold")

        # Crear los demás labels
        label_nombre_campo = tk.Label(frame_carta, text="Nombre: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_nombre_campo.grid(row=0, column=1, sticky='w', padx=5, pady=(5, padding_vertical))

        label_nombre_valor = tk.Label(frame_carta, text=nom_libro, bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_nombre_valor.grid(row=0, column=2, sticky='w', padx=5, pady=(5, padding_vertical))

        label_autor_campo = tk.Label(frame_carta, text="Autor: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_autor_campo.grid(row=1, column=1, sticky='w', padx=5, pady=padding_vertical)

        label_autor_valor = tk.Label(frame_carta, text=nombre_autor, bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_autor_valor.grid(row=1, column=2, sticky='w', padx=5, pady=padding_vertical)

        label_genero_campo = tk.Label(frame_carta, text="Género: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_genero_campo.grid(row=2, column=1, sticky='w', padx=5, pady=padding_vertical)

        label_genero_valor = tk.Label(frame_carta, text=nombre_genero, bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_genero_valor.grid(row=2, column=2, sticky='w', padx=5, pady=padding_vertical)

        label_precio_campo = tk.Label(frame_carta, text="Precio: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_precio_campo.grid(row=3, column=1, sticky='w', padx=5, pady=padding_vertical)

        label_precio_valor = tk.Label(frame_carta, text=f"${precio}", bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_precio_valor.grid(row=3, column=2, sticky='w', padx=5, pady=padding_vertical)

        label_stock_campo = tk.Label(frame_carta, text="Stock: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_stock_campo.grid(row=4, column=1, sticky='w', padx=5, pady=(padding_vertical, 5))

        label_stock_valor = tk.Label(frame_carta, text=stock, bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_stock_valor.grid(row=4, column=2, sticky='w', padx=5, pady=(padding_vertical, 5))

        # Bandera de control para la animación del botón
        cargando_flag = [False]

        # Botón Modificar con animación de "Cargando..."
        boton_modificar = ttk.Button(
            frame_carta, 
            text="Modificar", 
            style="Custom.TButton", 
            width=12,  # Define un ancho fijo para evitar cambios de tamaño
            command=lambda: self.iniciar_modificacion_producto(boton_modificar, cargando_flag, nom_libro)
        )
        boton_modificar.grid(row=1, column=3, pady=10, padx=10, sticky="e")


        # Botón Eliminar con el mismo ancho que "Modificar"
        boton_eliminar = ttk.Button(
            frame_carta, 
            text="Eliminar", 
            style="Custom.TButton", 
            width=12,  # Mismo ancho que el botón "Modificar"
            command=lambda: self.confirmar_eliminacion(producto_id, nom_libro)
        )
        boton_eliminar.grid(row=3, column=3, pady=10, padx=10, sticky="e")

        frame_carta.grid_columnconfigure(2, weight=1)
        frame_carta.grid_columnconfigure(3, weight=1)

    def iniciar_modificacion_producto(self, boton, cargando_flag, nom_libro):
        ventana_principal = self.parent

        # Activa la bandera de carga y comienza la animación en el hilo principal
        cargando_flag[0] = True
        animar_boton(boton, cargando_flag, ventana_principal)

        # Abrir el formulario de modificación y pasar el callback
        threading.Thread(target=lambda: ModificarProductoForm(self.parent, nom_libro, self.actualizar_lista_productos)).start()

        # Inicia el proceso de modificación en otro hilo de fondo y detiene la animación al finalizar
        def cerrar_animacion():
            self.proceso_modificacion(cargando_flag)

        threading.Thread(target=cerrar_animacion).start()


    def proceso_modificacion(self, cargando_flag):
        # Simula un proceso que toma tiempo
        time.sleep(3)  # Aquí iría el proceso de modificación real

        # Detiene la animación una vez que el proceso ha terminado
        self.parent.after(0, lambda: cargando_flag.__setitem__(0, False))
        





    def confirmar_eliminacion(self, producto_id, nom_libro):
        respuesta = messagebox.askquestion(
            "Eliminar Producto", 
            f"¿Realmente quiere eliminar el producto '{nom_libro}'?\nEste no podrá ser recuperado.",
            icon='warning'
        )
        if respuesta == 'yes':
            self.eliminar_producto(producto_id)

    def eliminar_producto(self, producto_id):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='dbacapstone'
            )
            cursor = conexion.cursor()

            query = "DELETE FROM app_libro WHERE id = %s"
            cursor.execute(query, (producto_id,))
            conexion.commit()

            cursor.close()
            conexion.close()

            messagebox.showinfo("Producto Eliminado", "El producto ha sido eliminado correctamente.")
            self.mostrar_productos()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")

    def cargar_imagen_diferida(self, frame_carta, imagen_url, label_cargando):
        def cargar():
            try:
                response = requests.get(imagen_url)
                image_data = BytesIO(response.content)
                img = Image.open(image_data)
                img = img.resize((100, 150))
                img_tk = ImageTk.PhotoImage(img)
                self.cache_imagenes[imagen_url] = img_tk
                frame_carta.after(0, lambda: self.mostrar_imagen(frame_carta, img_tk, label_cargando))
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")

        hilo_imagen = threading.Thread(target=cargar)
        hilo_imagen.start()

    def mostrar_imagen(self, frame_carta, img_tk, label_cargando):
        if frame_carta.winfo_exists():
            label_cargando.destroy()
            label_img = tk.Label(frame_carta, image=img_tk, bg="#1f2329")
            label_img.image = img_tk  
            label_img.grid(row=0, column=0, rowspan=5, padx=10, pady=10)

    def mostrar_productos(self):
        if not hasattr(self, 'pagina_actual'):
            self.pagina_actual = 0
        if not hasattr(self, 'productos_por_pagina'):
            self.productos_por_pagina = 2

        if hasattr(self, 'frame_productos') and self.frame_productos.winfo_exists():
            self.frame_productos.destroy()

        if not hasattr(self, 'frame_ver_productos') or not self.frame_ver_productos.winfo_exists():
            self.frame_ver_productos = tk.Frame(self.parent, bg="#1f2329")
            self.frame_ver_productos.pack(fill='both', expand=True)

            if not hasattr(self, 'entry_busqueda') or not self.entry_busqueda.winfo_exists():
                self.frame_busqueda = tk.Frame(self.frame_ver_productos, bg="#1f2329")
                self.frame_busqueda.pack(fill='x', padx=10, pady=10)

                self.entry_busqueda = ttk.Entry(self.frame_busqueda, width=40, style="Custom.TEntry")
                self.entry_busqueda.pack(side=tk.LEFT, padx=10)
                self.entry_busqueda.insert(0, "Búsqueda por nombre")
                self.entry_busqueda.bind("<FocusIn>", self.clear_placeholder)
                self.entry_busqueda.bind("<FocusOut>", self.add_placeholder)
                self.entry_busqueda.bind("<KeyRelease>", self.mostrar_productos_filtrados)

        self.frame_productos = tk.Frame(self.frame_ver_productos, bg="#1f2329")
        self.frame_productos.pack(fill='both', expand=True)

        if not hasattr(self, 'frame_paginacion') or not self.frame_paginacion.winfo_exists():
            self.frame_paginacion = tk.Frame(self.frame_ver_productos, bg="#1f2329")
            self.frame_paginacion.pack(pady=10, side=tk.BOTTOM, fill='x')

            self.boton_anterior = ttk.Button(self.frame_paginacion, text="Anterior", command=self.anterior_pagina, style="Custom.TButton", width=10)
            self.boton_anterior.pack(side=tk.LEFT, padx=10, pady=10)

            # Crear la etiqueta de paginación en el centro entre los botones con una fuente más pequeña y negrita
            self.label_paginacion = tk.Label(self.frame_paginacion, text="Página 1 de 1", bg="#1f2329", fg="#c7d5e0", font=("Roboto", 10, "bold"))
            self.label_paginacion.pack(side=tk.LEFT, padx=10, pady=10, expand=True)  # Expandir para centrar

            self.boton_siguiente = ttk.Button(self.frame_paginacion, text="Siguiente", command=self.siguiente_pagina, style="Custom.TButton", width=10)
            self.boton_siguiente.pack(side=tk.RIGHT, padx=10, pady=10)

        self.mostrar_productos_paginados()


    def mostrar_productos_paginados(self):
        for widget in self.frame_productos.winfo_children():
            widget.destroy()

        productos = self.obtener_productos(limite=self.productos_por_pagina, offset=self.pagina_actual * self.productos_por_pagina)

        if not productos:
            label_no_productos = tk.Label(self.frame_productos, text="No se encontraron productos.", bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
            label_no_productos.pack(pady=20)
            return

        for producto in productos:
            self.crear_carta_producto(self.frame_productos, *producto)

        total_productos = self.obtener_total_productos()
        self.actualizar_botones_paginacion(total_productos)

    def mostrar_productos_filtrados(self, event=None):
        # Obtener el término de búsqueda y almacenarlo
        busqueda = self.entry_busqueda.get().lower().strip()
        self.busqueda_actual = busqueda  # Almacenar el término de búsqueda

        # Reiniciar la paginación al iniciar una búsqueda
        self.pagina_actual = 0

        if not busqueda:  # Si no hay búsqueda, mostrar todos los productos
            self.mostrar_productos_paginados()
        else:
            # Obtener los productos filtrados con paginación
            productos = self.obtener_productos(busqueda=busqueda, limite=self.productos_por_pagina, offset=self.pagina_actual * self.productos_por_pagina)
            
            # Obtener el total de productos filtrados
            total_productos_filtrados = len(self.obtener_productos(busqueda=busqueda))  # Obtener el total de productos filtrados sin límite

            # Limpiar los productos existentes
            for widget in self.frame_productos.winfo_children():
                widget.destroy()

            if not productos:
                # Si no hay productos filtrados, ocultar la etiqueta de paginación y deshabilitar los botones
                self.label_paginacion.pack_forget()
                self.boton_anterior.config(state=tk.DISABLED)
                self.boton_siguiente.config(state=tk.DISABLED)

                # Mostrar mensaje de "No se encontraron productos"
                label_no_productos = tk.Label(self.frame_productos, text="No se encontraron productos.", bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
                label_no_productos.pack(pady=20)
            else:
                # Mostrar las cartas de productos filtrados
                for producto in productos:
                    self.crear_carta_producto(self.frame_productos, *producto)

                # Actualizar los botones de paginación y la etiqueta
                self.actualizar_botones_paginacion(total_productos_filtrados)



    def mostrar_productos_paginados_filtrados(self):
        # Asegurarnos de que estamos utilizando la búsqueda almacenada
        busqueda = self.busqueda_actual

        # Obtener los productos filtrados con paginación
        productos = self.obtener_productos(busqueda=busqueda, limite=self.productos_por_pagina, offset=self.pagina_actual * self.productos_por_pagina)
        
        # Obtener el total de productos filtrados para actualizar los botones de paginación
        total_productos_filtrados = len(self.obtener_productos(busqueda=busqueda))  # Obtener el total de productos filtrados sin límite

        # Limpiar los productos existentes
        for widget in self.frame_productos.winfo_children():
            widget.destroy()

        if not productos:
            label_no_productos = tk.Label(self.frame_productos, text="No se encontraron productos.", bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
            label_no_productos.pack(pady=20)
        else:
            # Crear las cartas de productos filtrados
            for producto in productos:
                self.crear_carta_producto(self.frame_productos, *producto)

            # Actualizar los botones de paginación para productos filtrados
            self.actualizar_botones_paginacion(total_productos_filtrados)

    def actualizar_botones_paginacion(self, total_productos):
        # Calcular el total de páginas
        total_paginas = (total_productos + self.productos_por_pagina - 1) // self.productos_por_pagina

        # Si no hay productos, ocultar la etiqueta de paginación y deshabilitar los botones
        if total_productos == 0:
            self.label_paginacion.pack_forget()  # Ocultar la etiqueta de paginación
            self.boton_anterior.config(state=tk.DISABLED)
            self.boton_siguiente.config(state=tk.DISABLED)
        else:
            # Mostrar la etiqueta si hay productos
            self.label_paginacion.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

            # Actualizar el texto de la etiqueta de paginación
            self.label_paginacion.config(text=f"Página {self.pagina_actual + 1} de {total_paginas}")

            # Actualizar el estado de los botones "Anterior" y "Siguiente"
            if self.pagina_actual == 0:
                self.boton_anterior.config(state=tk.DISABLED)
            else:
                self.boton_anterior.config(state=tk.NORMAL)

            if self.pagina_actual >= total_paginas - 1:
                self.boton_siguiente.config(state=tk.DISABLED)
            else:
                self.boton_siguiente.config(state=tk.NORMAL)


    def siguiente_pagina(self):
        # Avanzar a la siguiente página, considerando si es una búsqueda o no
        self.pagina_actual += 1

        if hasattr(self, 'busqueda_actual') and self.busqueda_actual:
            self.mostrar_productos_paginados_filtrados()  # Llamar a la función para mostrar productos filtrados
        else:
            self.mostrar_productos_paginados()  # Mostrar productos completos

    def anterior_pagina(self):
        # Retroceder a la página anterior, considerando si es una búsqueda o no
        self.pagina_actual -= 1

        if hasattr(self, 'busqueda_actual') and self.busqueda_actual:
            self.mostrar_productos_paginados_filtrados()  # Llamar a la función para mostrar productos filtrados
        else:
            self.mostrar_productos_paginados()  # Mostrar productos completos

    def clear_placeholder(self, event):
        if self.entry_busqueda.get() == "Búsqueda por nombre":
            self.entry_busqueda.delete(0, tk.END)

    def add_placeholder(self, event):
        if not self.entry_busqueda.get():
            self.entry_busqueda.insert(0, "Búsqueda por nombre")

    def actualizar_lista_productos(self):
        self.mostrar_productos()




def centrar_ventana(ventana, width, height):
    """Centrar la ventana en la pantalla"""
    ventana.update_idletasks()  # Asegurarse de que la ventana se ha renderizado correctamente
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla - width) // 2
    y = (alto_pantalla - height) // 2

    # Aplicar las coordenadas calculadas para centrar la ventana
    ventana.geometry(f"{width}x{height}+{x}+{y}")
    ventana.lift()  # Elevar la ventana al frente
    ventana.focus_force()  # Forzar el enfoque en la ventana


class ModificarProductoForm:
    def __init__(self, parent, nom_libro, callback):
        self.parent = parent
        self.nom_libro = nom_libro
        self.callback = callback  # Almacenar el callback
        self.img_tk = None
        self.cargando = [False]
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'dbacapstone'
        }

        # Crear la ventana de modificación de producto
        self.ventana_modificar = tk.Toplevel(self.parent)
        self.ventana_modificar.title(f"Modificar Producto: {self.nom_libro}")
        self.ventana_modificar.configure(bg="#1f2329")

        # Dimensiones de la ventana
        w, h = 700, 500

        # Llamar a la función para crear el formulario
        self.crear_formulario_modificar_producto()

        # Centrar la ventana
        centrar_ventana(self.ventana_modificar, w, h)

    def crear_formulario_modificar_producto(self):
        main_frame = tk.Frame(self.ventana_modificar, bg="#1f2329")
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Obtener los detalles del producto
        producto = self.obtener_datos_producto(self.nom_libro)
        if not producto:
            messagebox.showerror("Error", "No se pudo encontrar el producto.")
            self.cerrar_ventana()  # Cerrar la ventana si no se encuentra el producto
            return

        # Cargar y mostrar la imagen del producto
        label_img = tk.Label(main_frame, bg="#1f2329")
        label_img.grid(row=0, column=0, rowspan=6, padx=10, pady=10)
        imagen_url = self.convertir_url_google_drive(producto[3])
        self.cargar_imagen_desde_url(imagen_url, label_img)

        # Botón para cargar una nueva imagen
        button_cargar_imagen = ttk.Button(main_frame, text="Cargar Imagen", style="Custom.TButton", command=lambda: self.cargar_imagen_modificar_producto(label_img))
        button_cargar_imagen.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        # Crear campos del formulario
        self.entry_nombre = self.crear_campo_formulario(main_frame, "Nombre del Libro:", producto[0], 40, 0)
        self.entry_precio = self.crear_campo_formulario(main_frame, "Precio:", producto[1], 40, 2)
        self.entry_stock = self.crear_campo_formulario(main_frame, "Stock:", producto[2], 40, 4)

        autores = self.obtener_autores()
        self.combo_autor = self.crear_combobox_formulario(main_frame, "Autor:", autores, producto[4], 38, 6)

        generos = self.obtener_generos()
        self.combo_genero = self.crear_combobox_formulario(main_frame, "Género:", generos, producto[5], 38, 8)

        # Botón modificar con texto dinámico
        self.button_modificar = ttk.Button(
            main_frame, 
            text="Modificar", 
            style="Custom.TButton", 
            width=12,  # Ancho fijo para acomodar "Cargando..."
            command=self.iniciar_modificacion
        )
        self.button_modificar.grid(row=10, column=1, padx=10, pady=20, sticky='w')

        button_cancelar = ttk.Button(
            main_frame, 
            text="Cancelar", 
            style="Custom.TButton", 
            width=12,  # Mismo ancho que el botón "Modificar"
            command=self.cerrar_ventana
        )
        button_cancelar.grid(row=10, column=2, padx=10, pady=20, sticky='e')

    def iniciar_modificacion(self):
        # Iniciar la animación de "Cargando..."
        self.cargando[0] = True
        animar_boton(self.button_modificar, self.cargando, self.parent)

        # Ejecuta la modificación en un hilo separado para no bloquear la interfaz
        threading.Thread(target=self.modificar_producto_en_bd).start()

    def cerrar_ventana(self):
        self.ventana_modificar.destroy()

    def obtener_autores(self):
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

    def obtener_generos(self):
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

    def crear_campo_formulario(self, parent, label_text, value, entry_width, row):
        label = ttk.Label(parent, text=label_text, background="#1f2329", foreground="#c7d5e0", font=("Segoe UI", 12))
        label.grid(row=row, column=1, padx=10, pady=(20, 5), sticky='w')
        entry = ttk.Entry(parent, width=entry_width, style="Custom.TEntry")
        entry.grid(row=row + 1, column=1, columnspan=2, padx=10, pady=5, sticky='w')
        entry.insert(0, value)
        return entry

    def crear_combobox_formulario(self, parent, label_text, values, selected_value, combo_width, row):
        label = ttk.Label(parent, text=label_text, background="#1f2329", foreground="#c7d5e0", font=("Segoe UI", 12))
        label.grid(row=row, column=1, padx=10, pady=5, sticky='w')
        combobox = ttk.Combobox(parent, values=values, width=combo_width, style="Custom.TCombobox")
        combobox.grid(row=row + 1, column=1, columnspan=2, padx=10, pady=5, sticky='w')
        combobox.set(selected_value)
        return combobox

    def obtener_datos_producto(self, nom_libro):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            query = """
                SELECT app_libro.nom_libro, app_libro.precio, app_libro.stock, app_libro.imagen, 
                       app_autor.nombre_autor, app_generolib.nombre 
                FROM app_libro
                JOIN app_autor ON app_libro.id_autor_id = app_autor.id
                JOIN app_generolib ON app_libro.id_genero_id = app_generolib.id
                WHERE app_libro.nom_libro = %s
            """
            cursor.execute(query, (nom_libro,))
            producto = cursor.fetchone()
            cursor.close()
            conexion.close()
            return producto
        except Exception as e:
            print(f"Error al obtener los datos del producto: {e}")
            return None

    def convertir_url_google_drive(self, url):
        """Función para convertir URLs de Google Drive a formato descargable"""
        if "drive.google.com" in url:
            file_id = url.split("/d/")[1].split("/")[0]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        return url

    def cargar_imagen_desde_url(self, imagen_url, label_img):
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

    def cargar_imagen_modificar_producto(self, label_img):
        self.ventana_modificar.attributes('-topmost', False)
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg;*.png")])
        self.ventana_modificar.attributes('-topmost', True)
        if file_path:
            img = Image.open(file_path)
            img = img.resize((150, 200))
            self.img_tk = ImageTk.PhotoImage(img)
            label_img.config(image=self.img_tk)
            label_img.image = self.img_tk

    def modificar_producto_en_bd(self):
        time.sleep(3)  # Simula el tiempo de procesamiento

        # Detiene la animación
        self.cargando[0] = False

        # Resto de la lógica de modificación en la base de datos
        id_producto = self.nom_libro
        nombre = self.entry_nombre.get()
        precio = float(self.entry_precio.get())
        stock = int(self.entry_stock.get())
        autor = self.combo_autor.get()
        genero = self.combo_genero.get()

        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            query = """
                UPDATE app_libro 
                SET nom_libro=%s, precio=%s, stock=%s, 
                    id_autor_id=(SELECT id FROM app_autor WHERE nombre_autor=%s), 
                    id_genero_id=(SELECT id FROM app_generolib WHERE nombre=%s)
                WHERE nom_libro=%s
            """
            cursor.execute(query, (nombre, precio, stock, autor, genero, id_producto))
            conexion.commit()
            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
            self.callback()  # Llamar al callback para actualizar la lista de productos
            self.cerrar_ventana()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el producto: {e}")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()