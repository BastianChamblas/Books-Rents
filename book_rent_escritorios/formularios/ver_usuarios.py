import tkinter as tk
from tkinter import ttk, messagebox
import threading
import mysql.connector
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import filedialog
import requests
import time
import re

def animar_boton(boton, cargando_flag, ventana):
    def actualizar_texto():
        # Verifica si el botón sigue existiendo
        if not cargando_flag[0] or not boton.winfo_exists():
            if boton.winfo_exists():  # Verifica si el botón sigue existiendo antes de cambiar el texto
                boton.config(text="Modificar")  # Texto final cuando se detiene
            return

        # Contar puntos para simular animación
        puntos = boton.cget("text").count(".") % 3 + 1
        boton.config(text="Cargando" + "." * puntos)
        
        # Llama a la función nuevamente después de 500ms para actualizar la animación
        ventana.after(500, actualizar_texto)

    # Iniciar la animación
    actualizar_texto()



class VerUsuarios:
    def __init__(self, parent, db_config):
        self.parent = parent
        self.db_config = db_config
        self.pagina_actual = 0
        self.usuarios_por_pagina = 2  # Cambiado a 2 para coincidir con tu solicitud
        self.cache_imagenes = {}
        self.verificar_estructura_ui()
        self.mostrar_usuarios()
        
    def verificar_estructura_ui(self):
        # Configurar el estilo personalizado para Entry
        style = ttk.Style(self.parent)
        style.configure("Custom.TEntry",
                        foreground="#c7d5e0",    # Color del texto
                        background="#1b2838",    # Color del widget
                        fieldbackground="#1b2838")  # Color de fondo del campo


        # Verifica si los elementos de búsqueda ya existen
        if not hasattr(self, 'frame_usuarios'):
            self.frame_usuarios = tk.Frame(self.parent, bg="#1f2329")
            self.frame_usuarios.pack(fill='both', expand=True)

            # Marco de búsqueda
            self.frame_busqueda = tk.Frame(self.frame_usuarios, bg="#1f2329")
            self.frame_busqueda.pack(fill='x', padx=10, pady=10)

            self.entry_busqueda = ttk.Entry(self.frame_busqueda, width=40, style="Custom.TEntry")
            self.entry_busqueda.pack(side=tk.LEFT, padx=10)
            self.entry_busqueda.insert(0, "Búsqueda por RUT, Nombre o Apellido")
            self.entry_busqueda.bind("<FocusIn>", self.clear_placeholder)
            self.entry_busqueda.bind("<FocusOut>", self.add_placeholder)
            self.entry_busqueda.bind("<KeyRelease>", self.mostrar_usuarios_filtrados)

            # Botón de búsqueda
            self.button_buscar = ttk.Button(
                self.frame_busqueda,
                text="Buscar",
                command=self.mostrar_usuarios_filtrados,
                style="Custom.TButton"
            )
            self.button_buscar.pack(side=tk.LEFT, padx=5)

        # Marco de usuarios
        self.frame_listado = tk.Frame(self.frame_usuarios, bg="#1f2329")
        self.frame_listado.pack(fill='both', expand=True)

        # Marco de paginación
        self.frame_paginacion = tk.Frame(self.frame_usuarios, bg="#1f2329")
        self.frame_paginacion.pack(pady=10, side=tk.BOTTOM, fill='x')

        self.boton_anterior = ttk.Button(
            self.frame_paginacion,
            text="Anterior",
            command=self.anterior_pagina,
            style="Custom.TButton",
            width=10
        )
        self.boton_anterior.pack(side=tk.LEFT, padx=10, pady=10)

        self.label_paginacion = tk.Label(
            self.frame_paginacion,
            text="Página 1 de 1",
            bg="#1f2329",
            fg="#c7d5e0",
            font=("Roboto", 10, "bold")
        )
        self.label_paginacion.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        self.boton_siguiente = ttk.Button(
            self.frame_paginacion,
            text="Siguiente",
            command=self.siguiente_pagina,
            style="Custom.TButton",
            width=10
        )
        self.boton_siguiente.pack(side=tk.RIGHT, padx=10, pady=10)

    def obtener_usuarios(self, limite=10, offset=0, busqueda=None):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()

            if busqueda:
                busqueda = f"%{busqueda.lower()}%"
                query = """
                SELECT rut, first_name, last_name, telefono, direccion, id
                FROM app_customuser
                WHERE LOWER(rut) LIKE %s OR LOWER(first_name) LIKE %s OR LOWER(last_name) LIKE %s
                LIMIT %s OFFSET %s
                """
                cursor.execute(query, (busqueda, busqueda, busqueda, limite, offset))
            else:
                query = """
                SELECT rut, first_name, last_name, telefono, direccion, id
                FROM app_customuser
                LIMIT %s OFFSET %s
                """
                cursor.execute(query, (limite, offset))

            usuarios = cursor.fetchall()
            cursor.close()
            conexion.close()
            return usuarios
        except Exception as e:
            print(f"Error al obtener los usuarios: {e}")
            return []

    def obtener_total_usuarios(self, busqueda=None):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            if busqueda:
                busqueda = f"%{busqueda.lower()}%"
                query = """
                SELECT COUNT(*)
                FROM app_customuser
                WHERE LOWER(rut) LIKE %s OR LOWER(first_name) LIKE %s OR LOWER(last_name) LIKE %s
                """
                cursor.execute(query, (busqueda, busqueda, busqueda))
            else:
                query = "SELECT COUNT(*) FROM app_customuser"
                cursor.execute(query)

            total_usuarios = cursor.fetchone()[0]
            cursor.close()
            conexion.close()
            return total_usuarios
        except Exception as e:
            print(f"Error al obtener el total de usuarios: {e}")
            return 0

    def crear_carta_usuario(self, container_frame, rut, first_name, last_name, telefono, direccion, user_id):
        frame_carta = tk.Frame(container_frame, bg="#1f2329", relief="raised", borderwidth=2)
        frame_carta.pack(pady=5, padx=10, fill='x')

        bold_font = ("Roboto", 12, "bold")

        # Etiquetas de los campos
        label_rut_campo = tk.Label(frame_carta, text="RUT: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_rut_campo.grid(row=0, column=0, sticky='w', padx=5, pady=(5, 2))

        label_rut_valor = tk.Label(frame_carta, text=rut, bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_rut_valor.grid(row=0, column=1, sticky='w', padx=5, pady=(5, 2))

        label_nombre_campo = tk.Label(frame_carta, text="Nombre: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_nombre_campo.grid(row=1, column=0, sticky='w', padx=5, pady=2)

        label_nombre_valor = tk.Label(frame_carta, text=first_name, bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_nombre_valor.grid(row=1, column=1, sticky='w', padx=5, pady=2)

        label_apellido_campo = tk.Label(frame_carta, text="Apellido: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_apellido_campo.grid(row=2, column=0, sticky='w', padx=5, pady=2)

        label_apellido_valor = tk.Label(frame_carta, text=last_name, bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_apellido_valor.grid(row=2, column=1, sticky='w', padx=5, pady=2)

        label_telefono_campo = tk.Label(frame_carta, text="Teléfono: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_telefono_campo.grid(row=3, column=0, sticky='w', padx=5, pady=2)

        label_telefono_valor = tk.Label(frame_carta, text=telefono, bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_telefono_valor.grid(row=3, column=1, sticky='w', padx=5, pady=2)

        label_direccion_campo = tk.Label(frame_carta, text="Dirección: ", bg="#1f2329", fg="#c7d5e0", font=bold_font)
        label_direccion_campo.grid(row=4, column=0, sticky='w', padx=5, pady=2)

        label_direccion_valor = tk.Label(frame_carta, text=direccion, bg="#1f2329", fg="#c7d5e0", font=("Roboto", 12))
        label_direccion_valor.grid(row=4, column=1, sticky='w', padx=5, pady=2)

        # Botones Modificar y Eliminar
        boton_modificar = ttk.Button(
            frame_carta,
            text="Modificar",
            style="Custom.TButton",
            width=12,
            command=lambda: self.iniciar_modificacion_usuario(boton_modificar, user_id, rut)
        )
        boton_modificar.grid(row=0, column=2, padx=10, pady=5, sticky='e')

        boton_eliminar = ttk.Button(
            frame_carta,
            text="Eliminar",
            style="Custom.TButton",
            width=12,
            command=lambda: self.confirmar_eliminacion(user_id, first_name)
        )
        boton_eliminar.grid(row=1, column=2, padx=10, pady=5, sticky='e')

        frame_carta.grid_columnconfigure(1, weight=1)

    def iniciar_modificacion_usuario(self, boton, user_id, rut):
        # Iniciar animación en el botón
        cargando_flag = [True]
        animar_boton(boton, cargando_flag, self.parent)

        # Abrir el formulario de modificación en un hilo separado
        threading.Thread(
            target=lambda: ModificarUsuarioForm(
                self.parent,
                user_id,
                rut,
                self.db_config,
                self.actualizar_lista_usuarios
            )
        ).start()

        # Detener la animación después de abrir el formulario
        cargando_flag[0] = False

    def confirmar_eliminacion(self, user_id, first_name):
        respuesta = messagebox.askquestion(
            "Eliminar Usuario",
            f"¿Realmente desea eliminar al usuario '{first_name}'?\nEsta acción no se puede deshacer.",
            icon='warning'
        )
        if respuesta == 'yes':
            self.eliminar_usuario(user_id)

    def eliminar_usuario(self, user_id):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            query = "DELETE FROM app_customuser WHERE id = %s"
            cursor.execute(query, (user_id,))
            conexion.commit()
            cursor.close()
            conexion.close()
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
            self.mostrar_usuarios()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el usuario: {e}")

    def cargar_imagen_diferida(self, frame_carta, imagen_url, label_cargando):
        def cargar():
            try:
                response = requests.get(imagen_url)
                image_data = BytesIO(response.content)
                img = Image.open(image_data)
                img = img.resize((100, 100))
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

    def mostrar_usuarios(self, busqueda=None):
        # Reiniciar la página actual si se realiza una nueva búsqueda
        if busqueda is not None:
            self.pagina_actual = 0
            self.busqueda_actual = busqueda

        # Limpiar el listado de usuarios
        for widget in self.frame_listado.winfo_children():
            widget.destroy()

        # Obtener los usuarios para la página actual
        usuarios = self.obtener_usuarios(
            limite=self.usuarios_por_pagina,
            offset=self.pagina_actual * self.usuarios_por_pagina,
            busqueda=self.busqueda_actual if hasattr(self, 'busqueda_actual') else None
        )

        if not usuarios:
            label_no_usuarios = tk.Label(
                self.frame_listado,
                text="No se encontraron usuarios.",
                bg="#1f2329",
                fg="#c7d5e0",
                font=("Roboto", 12)
            )
            label_no_usuarios.pack(pady=20)
            return

        for usuario in usuarios:
            self.crear_carta_usuario(self.frame_listado, *usuario)

        total_usuarios = self.obtener_total_usuarios(
            self.busqueda_actual if hasattr(self, 'busqueda_actual') else None
        )
        self.actualizar_botones_paginacion(total_usuarios)

    def mostrar_usuarios_filtrados(self, event=None):
        busqueda = self.entry_busqueda.get().lower().strip()
        if busqueda == "búsqueda por rut, nombre o apellido":
            busqueda = ""
        self.mostrar_usuarios(busqueda)

    def actualizar_botones_paginacion(self, total_usuarios):
        total_paginas = (total_usuarios + self.usuarios_por_pagina - 1) // self.usuarios_por_pagina

        # Actualizar la etiqueta de paginación
        self.label_paginacion.config(text=f"Página {self.pagina_actual + 1} de {total_paginas}")

        # Actualizar el estado de los botones
        if self.pagina_actual == 0:
            self.boton_anterior.config(state=tk.DISABLED)
        else:
            self.boton_anterior.config(state=tk.NORMAL)

        if self.pagina_actual >= total_paginas - 1:
            self.boton_siguiente.config(state=tk.DISABLED)
        else:
            self.boton_siguiente.config(state=tk.NORMAL)

    def siguiente_pagina(self):
        self.pagina_actual += 1
        self.mostrar_usuarios()

    def anterior_pagina(self):
        self.pagina_actual -= 1
        self.mostrar_usuarios()

    def clear_placeholder(self, event):
        if self.entry_busqueda.get() == "Búsqueda por RUT, Nombre o Apellido":
            self.entry_busqueda.delete(0, tk.END)
            self.entry_busqueda.config(foreground="#c7d5e0")  # Asegurar el color del texto

    def add_placeholder(self, event):
        if not self.entry_busqueda.get():
            self.entry_busqueda.insert(0, "Búsqueda por RUT, Nombre o Apellido")
            self.entry_busqueda.config(foreground="#a9a9a9")

    def actualizar_lista_usuarios(self):
        # Método para actualizar la lista de usuarios después de una modificación
        self.mostrar_usuarios()


def validar_rut(rut):
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

def validar_nombre(nombre):
    return re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre) is not None

class ModificarUsuarioForm:
    def __init__(self, parent, user_id, rut, db_config, callback):
        self.parent = parent
        self.user_id = user_id
        self.rut = rut
        self.db_config = db_config
        self.callback = callback
        self.cargando = [False]

        # Crear la ventana de modificación de usuario
        self.ventana_modificar = tk.Toplevel(self.parent)
        self.ventana_modificar.title(f"Modificar Usuario: {rut}")
        self.ventana_modificar.configure(bg="#1f2329")
        self.ventana_modificar.geometry("500x400")
        centrar_ventana(self.ventana_modificar, 500, 400)
        self.ventana_modificar.transient(self.parent)  # Mantener la ventana encima
        self.ventana_modificar.grab_set()  # Bloquear la ventana principal

        self.crear_formulario_modificar_usuario()

    def crear_formulario_modificar_usuario(self):
        main_frame = tk.Frame(self.ventana_modificar, bg="#1f2329")
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Obtener los detalles del usuario
        usuario = self.obtener_datos_usuario()
        if not usuario:
            messagebox.showerror("Error", "No se pudo encontrar el usuario.")
            self.cerrar_ventana()
            return

        # Campos del formulario
        label_rut = ttk.Label(
            main_frame,
            text="RUT:",
            background="#1f2329",
            foreground="#c7d5e0",
            font=("Segoe UI", 12)
        )
        label_rut.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.entry_rut = ttk.Entry(main_frame, width=40, style="Custom.TEntry")
        self.entry_rut.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.entry_rut.insert(0, usuario['rut'] or "")

        label_nombre = ttk.Label(
            main_frame,
            text="Nombre:",
            background="#1f2329",
            foreground="#c7d5e0",
            font=("Segoe UI", 12)
        )
        label_nombre.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.entry_nombre = ttk.Entry(main_frame, width=40, style="Custom.TEntry")
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        self.entry_nombre.insert(0, usuario['first_name'] or "")  # Manejar None

        label_apellido = ttk.Label(
            main_frame,
            text="Apellido:",
            background="#1f2329",
            foreground="#c7d5e0",
            font=("Segoe UI", 12)
        )
        label_apellido.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.entry_apellido = ttk.Entry(main_frame, width=40, style="Custom.TEntry")
        self.entry_apellido.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.entry_apellido.insert(0, usuario['last_name'] or "")  # Manejar None

        label_telefono = ttk.Label(
            main_frame,
            text="Teléfono:",
            background="#1f2329",
            foreground="#c7d5e0",
            font=("Segoe UI", 12)
        )
        label_telefono.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.entry_telefono = ttk.Entry(main_frame, width=40, style="Custom.TEntry")
        self.entry_telefono.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        self.entry_telefono.insert(0, usuario['telefono'] or "")  # Manejar None

        label_direccion = ttk.Label(
            main_frame,
            text="Dirección:",
            background="#1f2329",
            foreground="#c7d5e0",
            font=("Segoe UI", 12)
        )
        label_direccion.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.entry_direccion = ttk.Entry(main_frame, width=40, style="Custom.TEntry")
        self.entry_direccion.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        self.entry_direccion.insert(0, usuario['direccion'] or "")  # Manejar None

        # Botones Modificar y Cancelar
        self.button_modificar = ttk.Button(
            main_frame,
            text="Modificar",
            style="Custom.TButton",
            width=12,
            command=self.iniciar_modificacion_usuario
        )
        self.button_modificar.grid(row=5, column=0, padx=10, pady=20, sticky='w')

        self.button_cancelar = ttk.Button(
            main_frame,
            text="Cancelar",
            style="Custom.TButton",
            width=12,
            command=self.cerrar_ventana
        )
        self.button_cancelar.grid(row=5, column=1, padx=10, pady=20, sticky='e')

    def iniciar_modificacion_usuario(self):
        # Iniciar animación en el botón
        self.cargando = [True]
        animar_boton(self.button_modificar, self.cargando, self.parent)

        # Ejecutar la modificación en un hilo separado
        threading.Thread(target=self.modificar_usuario_en_bd).start()

    def modificar_usuario_en_bd(self):
        time.sleep(2)  # Simular tiempo de procesamiento

        # Obtener los datos del formulario
        rut = self.entry_rut.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        telefono = self.entry_telefono.get().strip()
        direccion = self.entry_direccion.get().strip()

        # Validar que todos los campos estén llenos
        if not (rut and nombre and apellido and telefono and direccion):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            self.cargando[0] = False
            return

        # Validar el formato del RUT
        if not validar_rut(rut):
            messagebox.showerror("Error", "El RUT ingresado no es válido.")
            self.cargando[0] = False
            return

        # Validar el nombre y apellido
        if not validar_nombre(nombre):
            messagebox.showerror("Error", "El nombre solo debe contener letras.")
            self.cargando[0] = False
            return

        if not validar_nombre(apellido):
            messagebox.showerror("Error", "El apellido solo debe contener letras.")
            self.cargando[0] = False
            return

        # Validar que el teléfono sea numérico
        if not telefono.isdigit():
            messagebox.showerror("Error", "El teléfono debe contener solo números.")
            self.cargando[0] = False
            return

        # Verificar si el RUT ya existe
        if self.rut_existe(rut):
            messagebox.showerror("Error", "El RUT ingresado ya existe para otro usuario.")
            self.cargando[0] = False
            return

        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            query = """
            UPDATE app_customuser
            SET rut = %s,
                first_name = %s,
                last_name = %s,
                telefono = %s,
                direccion = %s
            WHERE id = %s
            """
            cursor.execute(query, (rut, nombre, apellido, telefono, direccion, self.user_id))
            conexion.commit()
            cursor.close()
            conexion.close()
            messagebox.showinfo("Éxito", "Usuario modificado correctamente.")
            self.callback()  # Actualizar la lista de usuarios
            self.cerrar_ventana()
        except mysql.connector.IntegrityError as e:
            if e.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                messagebox.showerror("Error", "El RUT ingresado ya existe. Por favor, ingresa un RUT único.")
            else:
                messagebox.showerror("Error", f"Error de integridad: {e}")
            self.cargando[0] = False
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el usuario: {e}")
            self.cargando[0] = False

    def rut_existe(self, rut):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor()
            query = "SELECT id FROM app_customuser WHERE rut = %s AND id != %s"
            cursor.execute(query, (rut, self.user_id))
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()
            return resultado is not None
        except Exception as e:
            print(f"Error al verificar el RUT en la base de datos: {e}")
            return False

    def cerrar_ventana(self):
        self.ventana_modificar.destroy()

    def obtener_datos_usuario(self):
        try:
            conexion = mysql.connector.connect(**self.db_config)
            cursor = conexion.cursor(dictionary=True)
            query = """
            SELECT rut, first_name, last_name, telefono, direccion
            FROM app_customuser
            WHERE id = %s
            """
            cursor.execute(query, (self.user_id,))
            usuario = cursor.fetchone()
            cursor.close()
            conexion.close()
            return usuario
        except Exception as e:
            print(f"Error al obtener los datos del usuario: {e}")
            return None

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
