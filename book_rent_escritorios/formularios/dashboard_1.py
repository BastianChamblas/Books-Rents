import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector

selected_months = []

def actualizar_grafico(canvas, figure, ax):
    ax.clear()
    ax.set_title("Comparación de Ventas", fontsize=14, pad=5)
    ax.set_xlabel("Meses", fontsize=12)
    ax.set_ylabel("Ventas ($)", fontsize=12)

    # Obtener el año seleccionado
    selected_year = int(año_combobox.get())
    previous_year = selected_year - 1

    # Si no hay meses seleccionados en los checkboxes, usar todos
    if not selected_months:
        meses = meses_lista
    else:
        # Ordenar los meses seleccionados en orden cronológico
        meses = sorted(selected_months, key=lambda mes: mes_a_numero[mes])

    ventas_actual = []
    ventas_anterior = []

    # Obtener filtros seleccionados
    selected_autor = autor_combobox.get()
    selected_genero = genero_combobox.get()

    # Construir cláusulas WHERE y parámetros comunes
    where_clauses_common = []
    params_common = []

    if selected_autor != "Seleccionar autor":
        where_clauses_common.append("dc.nombre_autor = %s")
        params_common.append(selected_autor)
    if selected_genero != "Seleccionar género":
        where_clauses_common.append("dc.nombre_genero = %s")
        params_common.append(selected_genero)

    where_clause_common = " AND ".join(where_clauses_common)
    if where_clause_common:
        where_clause_common = " AND " + where_clause_common

    # Conectar a la base de datos para obtener los datos de ventas
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="etl"
    )
    cursor = conn.cursor()

    data_exists = False  # Variable para verificar si hay datos

    for mes_nombre in meses:
        # Convertir el nombre del mes al número correspondiente
        mes_numero = mes_a_numero[mes_nombre]

        # Obtener ventas del año seleccionado
        query_actual = f"""
        SELECT SUM(dc.precio * dc.cantidad_comprado) AS total_ventas
        FROM DimCompras dc
        JOIN DimTiempoCompras dtc ON dc.id_tiempo_compra = dtc.id_tiempo_compra
        WHERE dtc.anio = %s AND dtc.mes = %s {where_clause_common}
        """
        cursor.execute(query_actual, (selected_year, mes_numero) + tuple(params_common))
        result_actual = cursor.fetchone()
        venta_actual = result_actual[0] if result_actual[0] else 0
        ventas_actual.append(venta_actual)

        # Obtener ventas del año anterior
        query_anterior = f"""
        SELECT SUM(dc.precio * dc.cantidad_comprado) AS total_ventas
        FROM DimCompras dc
        JOIN DimTiempoCompras dtc ON dc.id_tiempo_compra = dtc.id_tiempo_compra
        WHERE dtc.anio = %s AND dtc.mes = %s {where_clause_common}
        """
        cursor.execute(query_anterior, (previous_year, mes_numero) + tuple(params_common))
        result_anterior = cursor.fetchone()
        venta_anterior = result_anterior[0] if result_anterior[0] else 0
        ventas_anterior.append(venta_anterior)

        # Verificar si hay datos
        if venta_actual > 0 or venta_anterior > 0:
            data_exists = True

    cursor.close()
    conn.close()

    if data_exists:
        x = range(len(meses))
        ax.bar([i - 0.2 for i in x], ventas_anterior, width=0.4, label=str(previous_year), color="#2a3138")
        ax.bar([i + 0.2 for i in x], ventas_actual, width=0.4, label=str(selected_year), color="#39424e")
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

def toggle_mes(mes, canvas, figure, ax):
    if checkbox_vars[mes].get():
        if mes not in selected_months:
            selected_months.append(mes)
    else:
        if mes in selected_months:
            selected_months.remove(mes)
    actualizar_grafico(canvas, figure, ax)

def cargar_contenido_dashboard_1(frame):
    global año_combobox, mes_combobox, meses_lista, mes_a_numero
    global autor_combobox, genero_combobox  # Declarar como globales
    global checkbox_vars  # Declarar como global para usar en toggle_mes

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

    # Conectar a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="etl"
    )
    cursor = conn.cursor()

    # Obtener autores únicos
    cursor.execute("SELECT DISTINCT nombre_autor FROM DimCompras")
    autores_data = cursor.fetchall()
    autores = [row[0] for row in autores_data]

    # Obtener géneros únicos
    cursor.execute("SELECT DISTINCT nombre_genero FROM DimCompras")
    generos_data = cursor.fetchall()
    generos = [row[0] for row in generos_data]

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
    autor_combobox = ttk.Combobox(filters_frame, values=["Seleccionar autor"] + autores, state="readonly", font=("Roboto", 10),
                                  style='Custom.TCombobox')
    autor_combobox.set("Seleccionar autor")
    autor_combobox.pack(side="left", padx=5)

    # Combobox para seleccionar género
    genero_combobox = ttk.Combobox(filters_frame, values=["Seleccionar género"] + generos, state="readonly", font=("Roboto", 10),
                                   style='Custom.TCombobox')
    genero_combobox.set("Seleccionar género")
    genero_combobox.pack(side="left", padx=5)

    # Combobox para seleccionar mes
    meses_filter = ["Todos"] + meses_lista
    mes_combobox = ttk.Combobox(filters_frame, values=meses_filter, state="readonly", font=("Roboto", 10),
                                style='Custom.TCombobox')
    mes_combobox.set("Noviembre")
    mes_combobox.pack(side="left", padx=5)

    # Combobox para seleccionar año
    años = ["2023", "2024"]
    año_combobox = ttk.Combobox(filters_frame, values=años, state="readonly", font=("Roboto", 10),
                                style='Custom.TCombobox')
    año_combobox.set("2024")
    año_combobox.pack(side="left", padx=5)

    # Función para actualizar el título
    def update_title():
        selected_mes = mes_combobox.get()
        selected_año = año_combobox.get()
        if selected_mes == "Todos":
            titulo.config(text=f"Año {selected_año}")
        else:
            titulo.config(text=f"Mes de {selected_mes} {selected_año}")
        check_title.config(text=f"Meses {selected_año}")

        # Actualizar títulos de los recuadros de ventas
        valor_ventas_actual_title_label.config(text=f"Valor Ventas {selected_año}")
        valor_ventas_anterior_title_label.config(text=f"Valor Ventas {int(selected_año) - 1}")

    # Botón para limpiar filtros
    def limpiar_filtros():
        autor_combobox.set("Seleccionar autor")
        genero_combobox.set("Seleccionar género")
        mes_combobox.set("Todos")
        año_combobox.set("2024")

        # Seleccionar todos los checkboxes
        selected_months.clear()
        for mes in meses_lista:
            checkbox_vars[mes].set(True)
            selected_months.append(mes)
        actualizar_grafico(canvas, figure, ax)
        update_title()
        update_data()

    limpiar_button = tk.Button(filters_frame, text="Limpiar filtros", font=("Roboto", 10), bg="#2a3138", fg="white",
                               command=limpiar_filtros, relief="flat", padx=10, pady=5)
    limpiar_button.pack(side="left", padx=10)

    # Crear un contenedor para los cuadrados
    container = tk.Frame(frame, bg="#1f2329")
    container.pack(fill="both", expand=True)

    # Configurar colores alternos
    colores = ["#2a3138", "#39424e"]

    # Crear los cuadrados
    def crear_cuadrado(parent, row, col, text, value, bg_color):
        cuadrado = tk.Frame(parent, bg=bg_color, relief="ridge", borderwidth=2)
        cuadrado.grid(row=row, column=col, sticky="nsew", padx=0, pady=0)

        titulo_label = tk.Label(cuadrado, text=text, font=("Roboto", 10, "bold"), bg=bg_color, fg="white",
                                anchor="center", wraplength=130, justify="center")
        titulo_label.pack(expand=True, pady=(5, 2))

        valor_label = tk.Label(cuadrado, text=value, font=("Roboto", 9), bg=bg_color, fg="white",
                               anchor="center", wraplength=130, justify="center")
        valor_label.pack(expand=True, pady=(2, 5))

        return titulo_label, valor_label

    # Fila 1: Porcentaje Crecimiento
    porcentaje_title_label, porcentaje_value_label = crear_cuadrado(container, 0, 0, "Porcentaje\nCrecimiento", "",
                                                                    colores[0])

    # Columna 2: Libros
    libro_popular_title_label, libro_popular_value_label = crear_cuadrado(container, 0, 1, "Libro más Popular", "",
                                                                          colores[1])

    # Columna 3: Autores
    autor_popular_title_label, autor_popular_value_label = crear_cuadrado(container, 0, 2, "Autor más Popular", "",
                                                                          colores[0])

    # Columna 4: Géneros
    genero_popular_title_label, genero_popular_value_label = crear_cuadrado(container, 0, 3, "Género más Popular", "",
                                                                            colores[1])

    # Fila 2: Valor Ventas actual
    valor_ventas_actual_title_label, valor_ventas_actual_value_label = crear_cuadrado(container, 1, 0, "", "",
                                                                                      colores[1])

    # Fila 3: Valor Ventas anterior
    valor_ventas_anterior_title_label, valor_ventas_anterior_value_label = crear_cuadrado(container, 2, 0, "", "",
                                                                                          colores[0])

    # Fila 4: Diferencia Ventas
    diferencia_ventas_title_label, diferencia_ventas_value_label = crear_cuadrado(container, 3, 0, "Diferencia Ventas",
                                                                                  "", colores[1])

    # Columna 2-3: Gráfico de barras
    figure = plt.Figure(figsize=(6, 8), dpi=100)
    ax = figure.add_subplot(111)
    figure.subplots_adjust(bottom=0.22, top=0.9, left=0.15, right=0.95)

    canvas = FigureCanvasTkAgg(figure, master=container)
    canvas.get_tk_widget().grid(row=1, column=1, rowspan=3, columnspan=2, sticky="nsew")

    # Inicialmente, seleccionar todos los meses
    selected_months.clear()
    for mes in meses_lista:
        selected_months.append(mes)

    actualizar_grafico(canvas, figure, ax)

    # Columna 4: Checkboxes
    check_frame = tk.Frame(container, bg="#1f2329")
    check_frame.grid(row=1, column=3, rowspan=3, sticky="nsew")

    check_title = tk.Label(check_frame, text="", font=("Roboto", 10, "bold"), bg="#1f2329", fg="white")
    check_title.pack(anchor="w", pady=(0, 5), padx=5)

    # Variable para almacenar los estados de los checkboxes
    checkbox_vars = {}
    for mes in meses_lista:
        var = tk.BooleanVar(value=True)  # Inicialmente seleccionados
        checkbox_vars[mes] = var
        check = tk.Checkbutton(check_frame, text=mes, font=("Roboto", 9), bg="#1f2329", fg="white",
                               selectcolor=colores[1], variable=var,
                               command=lambda m=mes: toggle_mes(m, canvas, figure, ax))
        check.pack(anchor="w", pady=2, padx=5)

    # Función para actualizar los datos
    def update_data():
        selected_mes = mes_combobox.get()
        selected_año = año_combobox.get()
        selected_autor = autor_combobox.get()
        selected_genero = genero_combobox.get()

        # Construir cláusulas WHERE y parámetros
        where_clauses = []
        params = []

        if selected_mes != "Todos":
            mes_numero = mes_a_numero[selected_mes]
            where_clauses.append("dtc.mes = %s")
            params.append(mes_numero)
        if selected_año != "":
            where_clauses.append("dtc.anio = %s")
            params.append(int(selected_año))
        if selected_autor != "Seleccionar autor":
            where_clauses.append("dc.nombre_autor = %s")
            params.append(selected_autor)
        if selected_genero != "Seleccionar género":
            where_clauses.append("dc.nombre_genero = %s")
            params.append(selected_genero)

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

        # Obtener el libro más popular
        query_libro = f"""
        SELECT dc.nom_libro, SUM(dc.cantidad_comprado) AS total_comprado
        FROM DimCompras dc
        JOIN DimTiempoCompras dtc ON dc.id_tiempo_compra = dtc.id_tiempo_compra
        {where_clause}
        GROUP BY dc.nom_libro
        ORDER BY total_comprado DESC
        LIMIT 1;
        """
        cursor.execute(query_libro, params)
        result_libro = cursor.fetchone()
        if result_libro:
            libro_popular = result_libro[0]
        else:
            libro_popular = "Sin datos"

        libro_popular_value_label.config(text=libro_popular)

        # Obtener el autor más popular
        query_autor = f"""
        SELECT dc.nombre_autor, SUM(dc.cantidad_comprado) AS total_comprado
        FROM DimCompras dc
        JOIN DimTiempoCompras dtc ON dc.id_tiempo_compra = dtc.id_tiempo_compra
        {where_clause}
        GROUP BY dc.nombre_autor
        ORDER BY total_comprado DESC
        LIMIT 1;
        """
        cursor.execute(query_autor, params)
        result_autor = cursor.fetchone()
        if result_autor:
            autor_popular = result_autor[0]
        else:
            autor_popular = "Sin datos"

        autor_popular_value_label.config(text=autor_popular)

        # Obtener el género más popular
        query_genero = f"""
        SELECT dc.nombre_genero, SUM(dc.cantidad_comprado) AS total_comprado
        FROM DimCompras dc
        JOIN DimTiempoCompras dtc ON dc.id_tiempo_compra = dtc.id_tiempo_compra
        {where_clause}
        GROUP BY dc.nombre_genero
        ORDER BY total_comprado DESC
        LIMIT 1;
        """
        cursor.execute(query_genero, params)
        result_genero = cursor.fetchone()
        if result_genero:
            genero_popular = result_genero[0]
        else:
            genero_popular = "Sin datos"

        genero_popular_value_label.config(text=genero_popular)

        # Construir cláusulas comunes para las ventas (sin el año)
        where_clauses_common = []
        params_common = []

        if selected_mes != "Todos":
            mes_numero = mes_a_numero[selected_mes]
            where_clauses_common.append("dtc.mes = %s")
            params_common.append(mes_numero)
        if selected_autor != "Seleccionar autor":
            where_clauses_common.append("dc.nombre_autor = %s")
            params_common.append(selected_autor)
        if selected_genero != "Seleccionar género":
            where_clauses_common.append("dc.nombre_genero = %s")
            params_common.append(selected_genero)

        where_clause_common = " AND ".join(where_clauses_common)
        if where_clause_common:
            where_clause_common = " AND " + where_clause_common

        selected_year = int(selected_año)
        previous_year = selected_year - 1

        # Obtener valor de ventas del año seleccionado
        query_ventas_actual = f"""
        SELECT SUM(dc.precio * dc.cantidad_comprado) AS total_ventas
        FROM DimCompras dc
        JOIN DimTiempoCompras dtc ON dc.id_tiempo_compra = dtc.id_tiempo_compra
        WHERE dtc.anio = %s {where_clause_common}
        """
        cursor.execute(query_ventas_actual, [selected_year] + params_common)
        result_ventas_actual = cursor.fetchone()
        if result_ventas_actual and result_ventas_actual[0]:
            valor_ventas_actual = result_ventas_actual[0]
        else:
            valor_ventas_actual = 0

        valor_ventas_actual_value_label.config(text=f"${valor_ventas_actual:,.2f}")

        # Obtener valor de ventas del año anterior
        query_ventas_anterior = f"""
        SELECT SUM(dc.precio * dc.cantidad_comprado) AS total_ventas
        FROM DimCompras dc
        JOIN DimTiempoCompras dtc ON dc.id_tiempo_compra = dtc.id_tiempo_compra
        WHERE dtc.anio = %s {where_clause_common}
        """
        cursor.execute(query_ventas_anterior, [previous_year] + params_common)
        result_ventas_anterior = cursor.fetchone()
        if result_ventas_anterior and result_ventas_anterior[0]:
            valor_ventas_anterior = result_ventas_anterior[0]
        else:
            valor_ventas_anterior = 0

        valor_ventas_anterior_value_label.config(text=f"${valor_ventas_anterior:,.2f}")

        # Calcular diferencia de ventas
        diferencia_ventas = valor_ventas_actual - valor_ventas_anterior
        diferencia_ventas_value_label.config(text=f"${diferencia_ventas:,.2f}")

        # Calcular porcentaje de crecimiento
        if valor_ventas_anterior != 0:
            porcentaje_crecimiento = (diferencia_ventas / valor_ventas_anterior) * 100
        else:
            porcentaje_crecimiento = 0

        porcentaje_value_label.config(text=f"{porcentaje_crecimiento:.2f}%")

        cursor.close()
        conn.close()

    # Funciones para manejar las selecciones en los Comboboxes
    def seleccionar_mes(event):
        selected_mes = mes_combobox.get()
        update_title()
        update_data()

        # Si se selecciona "Todos", seleccionar todos los checkboxes
        if selected_mes == "Todos":
            selected_months.clear()
            for mes in meses_lista:
                if mes not in selected_months:
                    selected_months.append(mes)
                checkbox_vars[mes].set(True)
        else:
            # Desmarcar todos los checkboxes y marcar solo el mes seleccionado
            selected_months.clear()
            for mes in meses_lista:
                checkbox_vars[mes].set(False)
            selected_months.append(selected_mes)
            checkbox_vars[selected_mes].set(True)
        actualizar_grafico(canvas, figure, ax)

    mes_combobox.bind("<<ComboboxSelected>>", seleccionar_mes)

    def seleccionar_año(event):
        update_title()
        update_data()
        actualizar_grafico(canvas, figure, ax)

    año_combobox.bind("<<ComboboxSelected>>", seleccionar_año)

    def seleccionar_autor(event):
        update_data()
        actualizar_grafico(canvas, figure, ax)

    autor_combobox.bind("<<ComboboxSelected>>", seleccionar_autor)

    def seleccionar_genero(event):
        update_data()
        actualizar_grafico(canvas, figure, ax)

    genero_combobox.bind("<<ComboboxSelected>>", seleccionar_genero)

    # Configurar tamaño uniforme de los cuadrados
    for col in range(4):
        container.grid_columnconfigure(col, weight=1, minsize=150)
    for row in range(4):
        container.grid_rowconfigure(row, weight=1, minsize=100)

    # Llamar a 'update_title' y 'update_data' para establecer el título y datos iniciales
    update_title()
    update_data()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("1200x700")
    root.configure(bg="#1f2329")

    main_frame = tk.Frame(root, bg="#1f2329")
    main_frame.pack(fill="both", expand=True)

    cargar_contenido_dashboard_1(main_frame)

    root.mainloop()
