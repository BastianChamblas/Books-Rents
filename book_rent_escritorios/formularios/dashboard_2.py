import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector

selected_months = []

def cargar_contenido_dashboard_2(frame):
    global mes_combobox, año_combobox, selected_months, meses_lista, mes_a_numero
    global autor_combobox, genero_combobox, checkbox_vars

    # Limpiar el contenido actual del frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Definir lista de meses y su mapeo a números
    meses_lista = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                   "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_a_numero = {
        "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
        "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
    }

    selected_months.clear()

    # Conectar a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="etl"
    )
    cursor = conn.cursor()

    # Obtener autores únicos de DimArriendos
    cursor.execute("SELECT DISTINCT nombre_autor FROM DimArriendos")
    autores_data = cursor.fetchall()
    autores = [row[0] for row in autores_data]

    # Obtener géneros únicos de DimArriendos
    cursor.execute("SELECT DISTINCT nombre_genero FROM DimArriendos")
    generos_data = cursor.fetchall()
    generos = [row[0] for row in generos_data]

    # Obtener años únicos de DimTiempoArriendos
    cursor.execute("SELECT DISTINCT anio FROM DimTiempoArriendos")
    años_data = cursor.fetchall()
    años = [str(row[0]) for row in años_data]

    cursor.close()
    conn.close()

    # Crear un contenedor para el título y los filtros en la misma línea
    top_frame = tk.Frame(frame, bg="#1f2329")
    top_frame.pack(pady=10, anchor="w", fill="x")

    # Título
    titulo = tk.Label(top_frame, text="", font=("Roboto", 16), bg="#1f2329", fg="white")
    titulo.pack(side="left", padx=(10, 20))

    # Crear un contenedor para los filtros
    filters_frame = tk.Frame(top_frame, bg="#1f2329")
    filters_frame.pack(side="left")

    # Estilo para los Comboboxes
    style = ttk.Style()
    style.theme_use('default')
    style.configure('Custom.TCombobox',
                    fieldbackground="#2a3138",
                    background="#2a3138",
                    foreground='white',
                    bordercolor="#2a3138",
                    arrowcolor='white')
    style.map('Custom.TCombobox',
              fieldbackground=[('readonly', "#2a3138")],
              foreground=[('readonly', 'white')])

    # Combobox para seleccionar autor
    autor_combobox = ttk.Combobox(filters_frame, values=["Seleccionar autor"] + autores, state="readonly",
                                  font=("Roboto", 10), style='Custom.TCombobox')
    autor_combobox.set("Seleccionar autor")
    autor_combobox.pack(side="left", padx=5)

    # Combobox para seleccionar género
    genero_combobox = ttk.Combobox(filters_frame, values=["Seleccionar género"] + generos, state="readonly",
                                   font=("Roboto", 10), style='Custom.TCombobox')
    genero_combobox.set("Seleccionar género")
    genero_combobox.pack(side="left", padx=5)

    # Combobox para seleccionar mes
    meses_filter = ["Todos"] + meses_lista
    mes_combobox = ttk.Combobox(filters_frame, values=meses_filter, state="readonly", font=("Roboto", 10),
                                style='Custom.TCombobox')
    mes_combobox.set("Todos")  # Establecer "Todos" como valor por defecto
    mes_combobox.pack(side="left", padx=5)

    # Combobox para seleccionar año
    año_combobox = ttk.Combobox(filters_frame, values=años, state="readonly", font=("Roboto", 10),
                                style='Custom.TCombobox')
    año_combobox.set(años[-1])  # Seleccionar el último año por defecto
    año_combobox.pack(side="left", padx=5)

    # Botón para limpiar filtros
    def limpiar_filtros():
        autor_combobox.set("Seleccionar autor")
        genero_combobox.set("Seleccionar género")
        mes_combobox.set("Todos")
        año_combobox.set(años[-1])

        # Seleccionar todos los checkboxes
        selected_months.clear()
        for mes in meses_lista:
            checkbox_vars[mes].set(True)
            selected_months.append(mes)
        actualizar_titulo()
        actualizar_datos()
        actualizar_grafico()

    limpiar_button = tk.Button(filters_frame, text="Limpiar filtros", font=("Roboto", 10), bg="#2a3138", fg="white",
                               command=limpiar_filtros, relief="flat", padx=10, pady=5)
    limpiar_button.pack(side="left", padx=10)

    # Crear el contenedor principal para cuadrados y gráfico
    main_container = tk.Frame(frame, bg="#1f2329")
    main_container.pack(fill="both", expand=True, padx=0, pady=0)

    # Configurar grid para main_container
    for row in range(5):
        main_container.grid_rowconfigure(row, weight=1, minsize=100)
    for col in range(4):
        main_container.grid_columnconfigure(col, weight=1, minsize=150)

    # Configurar colores alternos
    colores = ["#2a3138", "#39424e"]

    # Crear los cuadrados relacionados con libros y porcentaje de devolución
    def crear_cuadrado(parent, row, col, text, value, bg_color):
        cuadrado = tk.Frame(parent, bg=bg_color, relief="ridge", borderwidth=2)
        cuadrado.grid(row=row, column=col, sticky="nsew", padx=0, pady=0)

        titulo_label = tk.Label(cuadrado, text=text, font=("Roboto", 10, "bold"), bg=bg_color, fg="white",
                                anchor="center", wraplength=130, justify="center")
        titulo_label.pack(expand=True, pady=(10, 5))

        valor_label = tk.Label(cuadrado, text=value, font=("Roboto", 12), bg=bg_color, fg="white",
                               anchor="center", justify="center")
        valor_label.pack(expand=True, pady=(5, 10))

        return valor_label

    # Crear los cuatro cuadrados en la fila 0, columnas 0-3
    porcentaje_devolucion_label = crear_cuadrado(main_container, 0, 0, "Porcentaje de\nDevolución", "", colores[0])
    libros_esperados_label = crear_cuadrado(main_container, 0, 1, "Libros Esperados", "", colores[1])
    libros_devueltos_label = crear_cuadrado(main_container, 0, 2, "Libros Devueltos", "", colores[0])
    libros_pendientes_label = crear_cuadrado(main_container, 0, 3, "Libros Pendientes", "", colores[1])

    # Columna de Checkboxes de meses
    check_frame = tk.Frame(main_container, bg="#1f2329")
    check_frame.grid(row=1, column=0, rowspan=4, sticky="nsew", padx=0, pady=0)

    check_title = tk.Label(check_frame, text="Meses", font=("Roboto", 10, "bold"), bg="#1f2329", fg="white")
    check_title.pack(anchor="w", pady=(0, 5), padx=5)

    checkbox_vars = {}
    for mes in meses_lista:
        var = tk.BooleanVar(value=True)
        checkbox_vars[mes] = var
        selected_months.append(mes)
        check = tk.Checkbutton(check_frame, text=mes, font=("Roboto", 9), bg="#1f2329", fg="white",
                               selectcolor=colores[1], variable=var,
                               command=lambda m=mes: toggle_mes(m))
        check.pack(anchor="w", pady=2, padx=5)

    # Gráfico de barras
    figure = plt.Figure(figsize=(6, 6), dpi=100)
    ax = figure.add_subplot(111)

    canvas = FigureCanvasTkAgg(figure, master=main_container)
    canvas.get_tk_widget().grid(row=1, column=1, columnspan=2, rowspan=4, sticky="nsew", padx=0, pady=0)

    # Función para actualizar el título
    def actualizar_titulo():
        selected_mes = mes_combobox.get()
        selected_año = año_combobox.get()
        if selected_mes == "Todos":
            titulo.config(text=f"Año {selected_año}")
        else:
            titulo.config(text=f"Mes de {selected_mes} {selected_año}")
        check_title.config(text=f"Meses {selected_año}")

    # Función para actualizar los datos en los cuadrados
    def actualizar_datos():
        selected_autor = autor_combobox.get()
        selected_genero = genero_combobox.get()
        selected_año = año_combobox.get()

        # Construir cláusulas WHERE y parámetros
        where_clauses = []
        params = []

        if selected_autor != "Seleccionar autor":
            where_clauses.append("da.nombre_autor = %s")
            params.append(selected_autor)
        if selected_genero != "Seleccionar género":
            where_clauses.append("da.nombre_genero = %s")
            params.append(selected_genero)
        if selected_año != "":
            where_clauses.append("dta.anio = %s")
            params.append(int(selected_año))
        if selected_months:
            meses_numeros = [mes_a_numero[mes] for mes in selected_months]
            where_clauses.append("dta.mes IN (" + ",".join(["%s"] * len(meses_numeros)) + ")")
            params.extend(meses_numeros)

        where_clause = " AND ".join(where_clauses)
        if where_clause:
            where_clause = "WHERE " + where_clause

        # Conectar a la base de datos
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="etl"
        )
        cursor = conn.cursor()

        # Obtener datos para los cuadrados
        # Libros Esperados
        query_esperados = f"""
        SELECT COUNT(DISTINCT da.id_arriendo)
        FROM DimArriendos da
        JOIN DimTiempoArriendos dta ON da.id_tiempo_arriendo = dta.id_tiempo_arriendo
        JOIN hechosventaslibros hvl ON da.id_arriendo = hvl.id_arriendo
        JOIN DimEstadoDevolucion ded ON hvl.id_estado_devolucion = ded.id_estado_devolucion
        {where_clause}
        """
        cursor.execute(query_esperados, params)
        libros_esperados = cursor.fetchone()[0] or 0
        libros_esperados_label.config(text=str(libros_esperados))

        # Libros Devueltos (estado = 1)
        query_devueltos = f"""
        SELECT COUNT(DISTINCT da.id_arriendo)
        FROM DimArriendos da
        JOIN DimTiempoArriendos dta ON da.id_tiempo_arriendo = dta.id_tiempo_arriendo
        JOIN hechosventaslibros hvl ON da.id_arriendo = hvl.id_arriendo
        JOIN DimEstadoDevolucion ded ON hvl.id_estado_devolucion = ded.id_estado_devolucion
        {where_clause} AND ded.estado = 1
        """
        cursor.execute(query_devueltos, params)
        libros_devueltos = cursor.fetchone()[0] or 0
        libros_devueltos_label.config(text=str(libros_devueltos))

        # Libros Pendientes
        libros_pendientes = libros_esperados - libros_devueltos
        libros_pendientes_label.config(text=str(libros_pendientes))

        # Porcentaje de Devolución
        if libros_esperados > 0:
            porcentaje_devolucion = (libros_devueltos / libros_esperados) * 100
        else:
            porcentaje_devolucion = 0
        porcentaje_devolucion_label.config(text=f"{porcentaje_devolucion:.2f}%")

        cursor.close()
        conn.close()

    # Función para actualizar el gráfico
    def actualizar_grafico():
        ax.clear()
        ax.set_title("Libros Devueltos vs Pendientes", fontsize=14, pad=5)
        ax.set_xlabel("Meses", fontsize=12)
        ax.set_ylabel("Cantidad de Libros", fontsize=12)

        selected_autor = autor_combobox.get()
        selected_genero = genero_combobox.get()
        selected_año = año_combobox.get()

        # Construir cláusulas WHERE y parámetros comunes
        where_clauses_common = []
        params_common = []

        if selected_autor != "Seleccionar autor":
            where_clauses_common.append("da.nombre_autor = %s")
            params_common.append(selected_autor)
        if selected_genero != "Seleccionar género":
            where_clauses_common.append("da.nombre_genero = %s")
            params_common.append(selected_genero)
        if selected_año != "":
            where_clauses_common.append("dta.anio = %s")
            params_common.append(int(selected_año))

        where_clause_common = " AND ".join(where_clauses_common)
        if where_clause_common:
            where_clause_common = " AND " + where_clause_common

        # Si no hay meses seleccionados, usar todos
        if not selected_months:
            meses = meses_lista
        else:
            meses = sorted(selected_months, key=lambda mes: mes_a_numero[mes])

        libros_devueltos = []
        libros_pendientes = []
        data_exists = False

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="etl"
        )
        cursor = conn.cursor()

        for mes_nombre in meses:
            mes_numero = mes_a_numero[mes_nombre]

            # Agregar condición del mes
            where_clause_mes = where_clause_common + " AND dta.mes = %s"
            params_mes = params_common + [mes_numero]

            # Total de arriendos esperados en el mes
            query_esperados = f"""
            SELECT COUNT(DISTINCT da.id_arriendo)
            FROM DimArriendos da
            JOIN DimTiempoArriendos dta ON da.id_tiempo_arriendo = dta.id_tiempo_arriendo
            JOIN hechosventaslibros hvl ON da.id_arriendo = hvl.id_arriendo
            JOIN DimEstadoDevolucion ded ON hvl.id_estado_devolucion = ded.id_estado_devolucion
            WHERE 1=1 {where_clause_mes}
            """
            cursor.execute(query_esperados, params_mes)
            total_esperados = cursor.fetchone()[0] or 0

            # Total de arriendos devueltos en el mes (estado = 1)
            query_devueltos = f"""
            SELECT COUNT(DISTINCT da.id_arriendo)
            FROM DimArriendos da
            JOIN DimTiempoArriendos dta ON da.id_tiempo_arriendo = dta.id_tiempo_arriendo
            JOIN hechosventaslibros hvl ON da.id_arriendo = hvl.id_arriendo
            JOIN DimEstadoDevolucion ded ON hvl.id_estado_devolucion = ded.id_estado_devolucion
            WHERE ded.estado = 1 {where_clause_mes}
            """
            cursor.execute(query_devueltos, params_mes)
            total_devueltos = cursor.fetchone()[0] or 0

            # Calcular pendientes
            total_pendientes = total_esperados - total_devueltos

            libros_devueltos.append(total_devueltos)
            libros_pendientes.append(total_pendientes)

            if total_devueltos > 0 or total_pendientes > 0:
                data_exists = True

        cursor.close()
        conn.close()

        if data_exists:
            x = range(len(meses))
            ax.bar([i - 0.2 for i in x], libros_devueltos, width=0.4, label='Devueltos', color="#2a3138")
            ax.bar([i + 0.2 for i in x], libros_pendientes, width=0.4, label='Pendientes', color="#39424e")
            ax.set_xticks(x)
            ax.set_xticklabels(meses, rotation=30, ha="right", fontsize=10)
            ax.legend(fontsize=10)
        else:
            # Mostrar mensaje de no hay datos
            ax.text(0.5, 0.5, 'No hay coincidencias para los filtros seleccionados',
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, fontsize=12, color='red')
            ax.set_xticks([])
            ax.set_yticks([])

        figure.subplots_adjust(bottom=0.22, top=0.9, left=0.15, right=0.95)
        canvas.draw()

    # Función para manejar los checkboxes de meses
    def toggle_mes(mes):
        if checkbox_vars[mes].get():
            if mes not in selected_months:
                selected_months.append(mes)
        else:
            if mes in selected_months:
                selected_months.remove(mes)
        actualizar_datos()
        actualizar_grafico()

    # Funciones para manejar las selecciones en los Comboboxes
    def seleccionar_mes(event):
        selected_mes = mes_combobox.get()
        actualizar_titulo()
        actualizar_datos()

        if selected_mes == "Todos":
            selected_months.clear()
            for mes in meses_lista:
                if mes not in selected_months:
                    selected_months.append(mes)
                checkbox_vars[mes].set(True)
        else:
            selected_months.clear()
            for mes in meses_lista:
                checkbox_vars[mes].set(False)
            selected_months.append(selected_mes)
            checkbox_vars[selected_mes].set(True)
        actualizar_grafico()

    mes_combobox.bind("<<ComboboxSelected>>", seleccionar_mes)

    def seleccionar_año(event):
        actualizar_titulo()
        actualizar_datos()
        actualizar_grafico()

    año_combobox.bind("<<ComboboxSelected>>", seleccionar_año)

    def seleccionar_autor(event):
        actualizar_datos()
        actualizar_grafico()

    autor_combobox.bind("<<ComboboxSelected>>", seleccionar_autor)

    def seleccionar_genero(event):
        actualizar_datos()
        actualizar_grafico()

    genero_combobox.bind("<<ComboboxSelected>>", seleccionar_genero)

    # Inicializar datos y gráfico
    actualizar_titulo()
    actualizar_datos()
    actualizar_grafico()

    # Agregar nueva sección en columna 4, fila 3
    info_frame = tk.Frame(main_container, bg="#1f2329")
    info_frame.grid(row=2, column=3, rowspan=2, sticky="nsew", padx=0, pady=0)

    # Título de la nueva sección
    info_title = tk.Label(info_frame, text="Información de Libros", font=("Roboto", 12, "bold"), bg="#1f2329", fg="white")
    info_title.pack(pady=(0, 10), padx=10, anchor="center")

    def generar_informacion():
        # Función que se ejecutará al presionar el botón
        # Crear una nueva ventana
        ventana_tabla = tk.Toplevel()
        ventana_tabla.title("Detalle de Libros")
        ventana_tabla.configure(bg="#1f2329")

        # Establecer tamaño de la ventana y centrarla
        ancho_ventana = 1200
        alto_ventana = 800

        # Obtener dimensiones de la pantalla
        ancho_pantalla = ventana_tabla.winfo_screenwidth()
        alto_pantalla = ventana_tabla.winfo_screenheight()

        # Calcular posición x e y para centrar la ventana
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        ventana_tabla.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Crear el contenedor principal para la tabla y los filtros
        main_container_tabla = tk.Frame(ventana_tabla, bg="#1f2329")
        main_container_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        # Crear un contenedor para los filtros en la ventana de la tabla
        filters_frame_tabla = tk.Frame(main_container_tabla, bg="#1f2329")
        filters_frame_tabla.pack(pady=10, fill="x")

        # Combobox para seleccionar autor
        autor_combobox_tabla = ttk.Combobox(filters_frame_tabla, values=["Seleccionar autor"] + autores, state="readonly",
                                            font=("Roboto", 10), style='Custom.TCombobox')
        autor_combobox_tabla.set("Seleccionar autor")
        autor_combobox_tabla.pack(side="left", padx=5)

        # Combobox para seleccionar género
        genero_combobox_tabla = ttk.Combobox(filters_frame_tabla, values=["Seleccionar género"] + generos, state="readonly",
                                            font=("Roboto", 10), style='Custom.TCombobox')
        genero_combobox_tabla.set("Seleccionar género")
        genero_combobox_tabla.pack(side="left", padx=5)

        # Combobox para seleccionar mes
        mes_combobox_tabla = ttk.Combobox(filters_frame_tabla, values=meses_filter, state="readonly", font=("Roboto", 10),
                                        style='Custom.TCombobox')
        mes_combobox_tabla.set("Todos")
        mes_combobox_tabla.pack(side="left", padx=5)

        # Combobox para seleccionar año
        año_combobox_tabla = ttk.Combobox(filters_frame_tabla, values=años, state="readonly", font=("Roboto", 10),
                                        style='Custom.TCombobox')
        año_combobox_tabla.set(años[-1])
        año_combobox_tabla.pack(side="left", padx=5)

        # Función para obtener los datos y llenar la tabla
        def obtener_datos_tabla():
            # Obtener los filtros seleccionados
            selected_autor_tabla = autor_combobox_tabla.get()
            selected_genero_tabla = genero_combobox_tabla.get()
            selected_mes_tabla = mes_combobox_tabla.get()
            selected_año_tabla = año_combobox_tabla.get()

            # Construir cláusulas WHERE y parámetros
            where_clauses = []
            params = []

            if selected_autor_tabla != "Seleccionar autor":
                where_clauses.append("da.nombre_autor = %s")
                params.append(selected_autor_tabla)
            if selected_genero_tabla != "Seleccionar género":
                where_clauses.append("da.nombre_genero = %s")
                params.append(selected_genero_tabla)
            if selected_año_tabla != "":
                where_clauses.append("dta.anio = %s")
                params.append(int(selected_año_tabla))
            if selected_mes_tabla != "Todos":
                mes_numero = mes_a_numero[selected_mes_tabla]
                where_clauses.append("dta.mes = %s")
                params.append(mes_numero)

            where_clause = " AND ".join(where_clauses)
            if where_clause:
                where_clause = "WHERE " + where_clause

            # Conectar a la base de datos
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="etl"
            )
            cursor = conn.cursor()

            # Consulta para obtener los datos de los libros
            query_libros = f"""
            SELECT da.nom_libro, da.nombre_autor, da.nombre_genero,
                COUNT(DISTINCT da.id_arriendo) AS cantidad_prestamos,
                SUM(CASE WHEN ded.estado = 1 THEN 1 ELSE 0 END) AS cantidad_devoluciones,
                (SUM(CASE WHEN ded.estado = 1 THEN 1 ELSE 0 END) / COUNT(DISTINCT da.id_arriendo)) * 100 AS porcentaje_devoluciones
            FROM DimArriendos da
            JOIN DimTiempoArriendos dta ON da.id_tiempo_arriendo = dta.id_tiempo_arriendo
            JOIN hechosventaslibros hvl ON da.id_arriendo = hvl.id_arriendo
            JOIN DimEstadoDevolucion ded ON hvl.id_estado_devolucion = ded.id_estado_devolucion
            {where_clause}
            GROUP BY da.nom_libro, da.nombre_autor, da.nombre_genero
            ORDER BY cantidad_prestamos DESC
            """
            cursor.execute(query_libros, params)
            datos_libros = cursor.fetchall()

            cursor.close()
            conn.close()

            # Limpiar la tabla
            for row in tree.get_children():
                tree.delete(row)

            # Insertar datos en la tabla
            for index, libro in enumerate(datos_libros):
                nom_libro, nombre_autor, nombre_genero, cantidad_prestamos, cantidad_devoluciones, porcentaje_devoluciones = libro
                porcentaje_devoluciones = f"{porcentaje_devoluciones:.2f}%"
                values = (nom_libro, nombre_autor, nombre_genero, cantidad_prestamos, cantidad_devoluciones, porcentaje_devoluciones)
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                tree.insert("", tk.END, values=values, tags=(tag,))

            # Definir colores alternos para las filas
            tree.tag_configure('oddrow', background="#2a3138")
            tree.tag_configure('evenrow', background="#39424e")

        # Botón para aplicar filtros (definido después de la función obtener_datos_tabla)
        aplicar_filtros_button = tk.Button(filters_frame_tabla, text="Aplicar Filtros", font=("Roboto", 10), bg="#2a3138", fg="white",
                                        command=obtener_datos_tabla, relief="flat", padx=10, pady=5)
        aplicar_filtros_button.pack(side="left", padx=10)

        # Crear la tabla dentro de main_container_tabla
        table_frame = tk.Frame(main_container_tabla, bg="#1f2329")
        table_frame.pack(fill="both", expand=True)

        # Definir las columnas
        columns = ("nombre_libro", "nombre_autor", "nombre_genero", "cantidad_prestamos", "cantidad_devoluciones", "porcentaje_devoluciones")

        tree = ttk.Treeview(table_frame, columns=columns, show='headings', selectmode='browse')

        # Definir encabezados
        tree.heading("nombre_libro", text="Nombre Libro")
        tree.heading("nombre_autor", text="Autor")
        tree.heading("nombre_genero", text="Género")
        tree.heading("cantidad_prestamos", text="Cantidad de Préstamos")
        tree.heading("cantidad_devoluciones", text="Cantidad de Devoluciones")
        tree.heading("porcentaje_devoluciones", text="% Devoluciones")

        # Definir anchos de columnas
        tree.column("nombre_libro", width=200, anchor="center")
        tree.column("nombre_autor", width=150, anchor="center")
        tree.column("nombre_genero", width=150, anchor="center")
        tree.column("cantidad_prestamos", width=150, anchor="center")
        tree.column("cantidad_devoluciones", width=150, anchor="center")
        tree.column("porcentaje_devoluciones", width=150, anchor="center")

        # Configurar estilos
        style_tree = ttk.Style()
        style_tree.theme_use("default")
        style_tree.configure("Treeview",
                            background="#1f2329",
                            foreground="white",
                            fieldbackground="#1f2329",
                            rowheight=25,
                            font=("Roboto", 10))
        style_tree.map('Treeview', background=[('selected', '#2a3138')])

        # Estilizar el encabezado de la tabla sin cambio de color al hover
        style_tree.configure("Treeview.Heading",
                            background="#2a3138",
                            foreground="white",
                            font=("Roboto", 10, "bold"))

        # Eliminar el cambio de color blanco al hover sobre el encabezado
        style_tree.map("Treeview.Heading",
                    background=[('active', '#2a3138')],
                    foreground=[('active', 'white')])

        # Agregar la barra de desplazamiento personalizada
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree.pack(fill="both", expand=True)

        # Inicializar datos en la tabla
        obtener_datos_tabla()


    generar_button = tk.Button(info_frame, text="Generar", font=("Roboto", 10), bg="#2a3138", fg="white",
                               command=generar_informacion, relief="flat", padx=20, pady=10)
    generar_button.pack(pady=10, padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("1600x900")
    root.configure(bg="#1f2329")

    main_frame = tk.Frame(root, bg="#1f2329")
    main_frame.pack(fill="both", expand=True)

    cargar_contenido_dashboard_2(main_frame)

    root.mainloop()
