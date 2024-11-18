import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
import datetime

def cargar_contenido_dashboard_3(frame):
    global mes_combobox, año_combobox, autor_combobox, genero_combobox, meses_filter, mes_a_numero, root

    for widget in frame.winfo_children():
        widget.destroy()

    # Definir lista de meses y su mapeo a números
    meses_lista = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                   "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    mes_a_numero = {
        "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
        "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
    }

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
    autor_combobox = ttk.Combobox(filters_frame, values=["Seleccionar autor"] + autores, state="readonly", font=("Roboto", 10), style='Custom.TCombobox')
    autor_combobox.set("Seleccionar autor")
    autor_combobox.pack(side="left", padx=5)

    # Combobox para seleccionar género
    genero_combobox = ttk.Combobox(filters_frame, values=["Seleccionar género"] + generos, state="readonly", font=("Roboto", 10), style='Custom.TCombobox')
    genero_combobox.set("Seleccionar género")
    genero_combobox.pack(side="left", padx=5)

    # Combobox para seleccionar mes
    meses_filter = meses_lista
    mes_combobox = ttk.Combobox(filters_frame, values=meses_filter, state="readonly", font=("Roboto", 10), style='Custom.TCombobox')
    # Obtener el mes actual en español
    mes_actual = meses_lista[datetime.datetime.now().month - 1]
    mes_combobox.set(mes_actual)
    mes_combobox.pack(side="left", padx=5)

    # Combobox para seleccionar año
    current_year = datetime.datetime.now().year
    años = sorted(años, reverse=True)
    año_combobox = ttk.Combobox(filters_frame, values=años, state="readonly", font=("Roboto", 10), style='Custom.TCombobox')
    año_combobox.set(str(current_year))
    año_combobox.pack(side="left", padx=5)

    # Botón para limpiar filtros
    def limpiar_filtros():
        autor_combobox.set("Seleccionar autor")
        genero_combobox.set("Seleccionar género")
        mes_combobox.set(mes_actual)
        año_combobox.set(str(current_year))
        actualizar_titulo()
        actualizar_tabla()

    limpiar_button = tk.Button(filters_frame, text="Limpiar filtros", font=("Roboto", 10), bg="#2a3138", fg="white",
                               command=limpiar_filtros, relief="flat", padx=10, pady=5)
    limpiar_button.pack(side="left", padx=10)

    # Función para actualizar el título
    def actualizar_titulo():
        selected_mes = mes_combobox.get()
        selected_año = año_combobox.get()
        titulo.config(text=f"Mes de {selected_mes} {selected_año}")

    # Crear el contenedor principal para la tabla
    main_container = tk.Frame(frame, bg="#1f2329")
    main_container.pack(fill="both", expand=True, padx=20, pady=10)

    # Crear la tabla dentro de main_container
    table_frame = tk.Frame(main_container, bg="#1f2329")
    table_frame.pack(fill="both", expand=True)

    # Definir las columnas
    columns = ("nombre_libro", "cantidad_arriendos", "stock_actual", "stock_sugerido", "generar_grafico")

    tree = ttk.Treeview(table_frame, columns=columns, show='headings', selectmode='browse')

    # Definir encabezados
    tree.heading("nombre_libro", text="Nombre Libro")
    tree.heading("cantidad_arriendos", text="Cantidad de Arriendos")
    tree.heading("stock_actual", text="Stock Actual")
    tree.heading("stock_sugerido", text="Stock Sugerido")
    tree.heading("generar_grafico", text="")  # Encabezado vacío para el botón

    # Definir anchos de columnas
    tree.column("nombre_libro", width=200, anchor="center")
    tree.column("cantidad_arriendos", width=150, anchor="center")
    tree.column("stock_actual", width=100, anchor="center")
    tree.column("stock_sugerido", width=120, anchor="center")
    tree.column("generar_grafico", width=150, anchor="center")

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

    # Definir colores alternos para las filas
    tree.tag_configure('oddrow', background="#2a3138")
    tree.tag_configure('evenrow', background="#39424e")

    # Agregar la barra de desplazamiento personalizada
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Cambiar el color de la barra de desplazamiento
    style_tree.configure("Vertical.TScrollbar",
                         background="#2a3138",
                         troughcolor="#1f2329",
                         bordercolor="#1f2329",
                         arrowcolor='white')
    scrollbar.configure(style="Vertical.TScrollbar")

    tree.pack(fill="both", expand=True)

    def on_tree_click(event):
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        column = tree.identify_column(event.x)
        if column != '#5':  # Columna "generar_grafico" es la quinta (index 4)
            return
        row_id = tree.identify_row(event.y)
        if not row_id:
            return
        valores = tree.item(row_id, 'values')
        nombre_libro = valores[0]
        generar_grafico_libro(nombre_libro)  # Llamar a la función sin 'root'




    tree.bind("<Button-1>", lambda event: on_tree_click(event))  # Ya no pasa 'root'



    # Función para generar gráfico específico de un libro
    def generar_grafico_libro(nombre_libro):
        ventana = tk.Toplevel()  # Crea la ventana Toplevel sin pasar root
        ventana.title(f"Gráfico de {nombre_libro}")
        ventana.geometry("800x600")
        fig, ax = plt.subplots(figsize=(8, 6), dpi=100)

        # Conectar a la base de datos para obtener datos del gráfico
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="etl"
        )
        cursor = conn.cursor()

        # Obtener datos de arriendos por mes para el libro seleccionado
        query_grafico = f"""
        SELECT dta.anio, dta.mes, COUNT(DISTINCT da.id_arriendo) AS cantidad_arriendos
        FROM DimArriendos da
        JOIN DimTiempoArriendos dta ON da.id_tiempo_arriendo = dta.id_tiempo_arriendo
        WHERE da.nom_libro = %s
        GROUP BY dta.anio, dta.mes
        ORDER BY dta.anio, dta.mes
        """
        cursor.execute(query_grafico, (nombre_libro,))
        datos_grafico = cursor.fetchall()

        cursor.close()
        conn.close()

        # Preparar datos para el gráfico
        meses = []
        arriendos = []
        for anio, mes_num, cantidad in datos_grafico:
            mes_nombre = meses_lista[mes_num - 1] + ' ' + str(anio)
            meses.append(mes_nombre)
            arriendos.append(cantidad)

        # Crear un gráfico de barras
        ax.bar(meses, arriendos, color='#2a3138')
        ax.set_title(f"Arriendos de '{nombre_libro}'", fontsize=14)
        ax.set_xlabel("Meses", fontsize=12)
        ax.set_ylabel("Cantidad de Arriendos", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.xticks(rotation=45)
        fig.tight_layout()
        
        # Dibujar el gráfico en la ventana Toplevel
        canvas = FigureCanvasTkAgg(fig, master=ventana)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # Función para actualizar la tabla según los filtros
    def actualizar_tabla():
        autor = autor_combobox.get()
        genero = genero_combobox.get()
        mes = mes_combobox.get()
        año = año_combobox.get()
        print(f"Filtros seleccionados - Autor: {autor}, Género: {genero}, Mes: {mes}, Año: {año}")

        # Construir cláusulas WHERE y parámetros
        where_clauses = []
        params = []

        if autor != "Seleccionar autor":
            where_clauses.append("da.nombre_autor = %s")
            params.append(autor)
        if genero != "Seleccionar género":
            where_clauses.append("da.nombre_genero = %s")
            params.append(genero)
        if año != "":
            where_clauses.append("dta.anio = %s")
            params.append(int(año))
        if mes != "":
            mes_numero = mes_a_numero[mes]
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

        # Obtener datos para la tabla
        # Obtener nombre_libro y cantidad_arriendos en el mes seleccionado
        query = f"""
        SELECT da.nom_libro,
            COUNT(DISTINCT da.id_arriendo) AS cantidad_arriendos
        FROM DimArriendos da
        JOIN DimTiempoArriendos dta ON da.id_tiempo_arriendo = dta.id_tiempo_arriendo
        {where_clause}
        GROUP BY da.nom_libro
        """
        cursor.execute(query, params)
        data = cursor.fetchall()

        resultados = []
        for row in data:
            nom_libro, cantidad_arriendos = row

            # Obtener stock_actual basado en el último registro de fecha_arriendo
            query_stock = f"""
            SELECT da.stock_total_arriendo
            FROM DimArriendos da
            JOIN DimTiempoArriendos dta ON da.id_tiempo_arriendo = dta.id_tiempo_arriendo
            WHERE da.nom_libro = %s
            ORDER BY dta.fecha_arriendo DESC
            LIMIT 1
            """
            cursor.execute(query_stock, (nom_libro,))
            stock_actual_result = cursor.fetchone()
            stock_actual = stock_actual_result[0] if stock_actual_result else 0

            # Calcular stock_sugerido en base a las reglas
            if cantidad_arriendos < 10:
                stock_sugerido = cantidad_arriendos
            elif 10 <= cantidad_arriendos <= 20:
                stock_sugerido = cantidad_arriendos * 1.10
            elif 21 <= cantidad_arriendos <= 50:
                stock_sugerido = cantidad_arriendos * 1.05
            elif cantidad_arriendos >= 51:
                stock_sugerido = cantidad_arriendos * 1.03
            else:
                stock_sugerido = stock_actual  # Mantener stock actual si no cumple ninguna condición

            stock_sugerido = int(round(stock_sugerido))

            # Agregar a los resultados
            resultados.append((nom_libro, cantidad_arriendos, stock_actual, stock_sugerido, "Generar Gráfico"))

        cursor.close()
        conn.close()

        # Limpiar la tabla
        for row in tree.get_children():
            tree.delete(row)

        # Insertar datos en la tabla
        for index, libro in enumerate(resultados):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            tree.insert("", tk.END, values=libro, tags=(tag,))

    # Vincular actualización de la tabla a cambios en los Comboboxes
    autor_combobox.bind("<<ComboboxSelected>>", lambda e: [actualizar_titulo(), actualizar_tabla()])
    genero_combobox.bind("<<ComboboxSelected>>", lambda e: [actualizar_titulo(), actualizar_tabla()])
    mes_combobox.bind("<<ComboboxSelected>>", lambda e: [actualizar_titulo(), actualizar_tabla()])
    año_combobox.bind("<<ComboboxSelected>>", lambda e: [actualizar_titulo(), actualizar_tabla()])

    # Agregar efecto de hover en la columna "Generar Gráfico"
    def on_motion(event):
        region = tree.identify("region", event.x, event.y)
        if region == "cell":
            column = tree.identify_column(event.x)
            if column == '#5':  # Columna "generar_grafico" es la quinta
                tree.configure(cursor="hand2")
            else:
                tree.configure(cursor="")
        else:
            tree.configure(cursor="")

    tree.bind("<Motion>", on_motion)

    def on_leave(event):
        # Restaurar los colores originales de las filas
        for index, item in enumerate(tree.get_children()):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            tree.item(item, tags=(tag,))
        tree.tag_configure('hover', background="")

    tree.bind("<Leave>", on_leave)

    # Inicializar título y tabla
    actualizar_titulo()
    actualizar_tabla()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("1200x700")
    root.configure(bg="#1f2329")

    main_frame = tk.Frame(root, bg="#1f2329")
    main_frame.pack(fill="both", expand=True)

    cargar_contenido_dashboard_3(main_frame)

    root.mainloop()
