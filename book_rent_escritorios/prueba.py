import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime  # Importar datetime para obtener el año actual

def cargar_contenido_dashboard_2(frame):
    # Limpiar el contenido actual del frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Crear un contenedor para el título y los filtros en la misma línea
    top_frame = tk.Frame(frame, bg="#1f2329")
    top_frame.pack(pady=10, anchor="w", fill="x")

    # Título
    titulo = tk.Label(top_frame, text="Mes de Noviembre 2024", font=("Roboto", 16), bg="#1f2329", fg="white")
    titulo.pack(side="left", padx=(10, 20))  # Espaciado entre el título y los filtros

    # Crear un contenedor para los filtros
    filters_frame = tk.Frame(top_frame, bg="#1f2329")
    filters_frame.pack(side="left")

    # Estilo para los Comboboxes
    style = ttk.Style()
    style.theme_use('default')
    # Configurar el estilo personalizado para el Combobox
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
    autores = ["Autor 1", "Autor 2"]
    autor_combobox = ttk.Combobox(filters_frame, values=autores, state="readonly", font=("Roboto", 10), style='Custom.TCombobox')
    autor_combobox.set("Seleccionar autor")  # Establecer texto por defecto
    autor_combobox.pack(side="left", padx=5)

    # Combobox para seleccionar género
    generos = ["Ficción", "No Ficción"]
    genero_combobox = ttk.Combobox(filters_frame, values=generos, state="readonly", font=("Roboto", 10), style='Custom.TCombobox')
    genero_combobox.set("Seleccionar género")  # Establecer texto por defecto
    genero_combobox.pack(side="left", padx=5)

    # Combobox para seleccionar año
    current_year = datetime.datetime.now().year
    # Crear una lista de años sin duplicados
    base_años = ["2023", "2024", "2025"]
    años = [str(current_year)] + [año for año in base_años if año != str(current_year)]
    año_combobox = ttk.Combobox(filters_frame, values=años, state="readonly", font=("Roboto", 10), style='Custom.TCombobox')
    año_combobox.set(str(current_year))  # Seleccionar el año actual por defecto
    año_combobox.pack(side="left", padx=5)

    # Crear el contenedor principal para cuadrados y gráfico
    main_container = tk.Frame(frame, bg="#1f2329")
    main_container.pack(fill="both", expand=True, padx=10, pady=10)

    # Configurar grid para main_container
    main_container.grid_rowconfigure(0, weight=1)  # Fila 1: Cuadrados
    main_container.grid_rowconfigure(1, weight=3)  # Fila 2: Gráfico
    main_container.grid_rowconfigure(2, weight=1)  # Fila 3: Checkboxes
    main_container.grid_rowconfigure(3, weight=1)  # Fila 4: Checkboxes

    for col in range(4):
        main_container.grid_columnconfigure(col, weight=1, minsize=150)

    # Configurar colores alternos
    colores = ["#2a3138", "#39424e"]

    # Crear los cuadrados relacionados con libros y porcentaje de devolución
    def crear_cuadrado(parent, row, col, text, value, bg_color):
        cuadrado = tk.Frame(parent, bg=bg_color, relief="ridge", borderwidth=2)
        cuadrado.grid(row=row, column=col, sticky="nsew", padx=0, pady=0)

        titulo_label = tk.Label(cuadrado, text=text, font=("Roboto", 10, "bold"), bg=bg_color, fg="white",
                                anchor="center", wraplength=150, justify="center")
        titulo_label.pack(expand=True, pady=(10, 5))

        valor_label = tk.Label(cuadrado, text=value, font=("Roboto", 12), bg=bg_color, fg="white",
                               anchor="center", justify="center")
        valor_label.pack(expand=True, pady=(5, 10))

    # Crear los cuatro cuadrados en la fila 1, columnas 1-4
    crear_cuadrado(main_container, 0, 0, "Porcentaje de\nDevolución", "5%", colores[0])
    crear_cuadrado(main_container, 0, 1, "Libros Esperados", "30", colores[1])
    crear_cuadrado(main_container, 0, 2, "Libros Devueltos", "15", colores[0])
    crear_cuadrado(main_container, 0, 3, "Libros Pendientes", "5", colores[1])

    # Crear el frame para los checkboxes de meses, ubicado en columna1, filas2-3
    check_frame = tk.Frame(main_container, bg="#1f2329")
    check_frame.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=10, pady=0)

    check_title = tk.Label(check_frame, text="Meses", font=("Roboto", 10, "bold"), bg="#1f2329", fg="white")
    check_title.pack(anchor="w", pady=(0, 5), padx=5)

    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    selected_months = []

    def actualizar_grafico():
        ax.clear()
        ax.set_title("Distribución de Libros por Mes", fontsize=14, pad=5)
        ax.set_xlabel("Meses", fontsize=12)
        ax.set_ylabel("Cantidad de Libros", fontsize=12)

        if selected_months:
            meses_filtrados = sorted(selected_months, key=lambda m: meses.index(m))
            # Datos de ejemplo, reemplaza con tus datos reales
            valores = [10, 15, 5, 20, 25, 30, 35, 40, 45, 50, 55, 60]
            valores_filtrados = [valores[meses.index(m)] for m in meses_filtrados]
            x = range(len(meses_filtrados))
            ax.bar(x, valores_filtrados, color="#2a3138")
            ax.set_xticks(x)
            ax.set_xticklabels(meses_filtrados, rotation=30, ha="right", fontsize=10)
        else:
            # Mostrar todos los meses si no hay selección
            valores = [10, 15, 5, 20, 25, 30, 35, 40, 45, 50, 55, 60]  # Datos de ejemplo
            x = range(len(meses))
            ax.bar(x, valores, color="#2a3138")
            ax.set_xticks(x)
            ax.set_xticklabels(meses, rotation=30, ha="right", fontsize=10)

        # Ajustar márgenes para maximizar el uso vertical y centrar
        figure.subplots_adjust(bottom=0.25, top=0.9, left=0.15, right=0.95)
        canvas.draw()

    def toggle_mes(mes):
        if mes in selected_months:
            selected_months.remove(mes)
        else:
            selected_months.append(mes)
        actualizar_grafico()

    for mes in meses:
        var = tk.BooleanVar()
        check = tk.Checkbutton(check_frame, text=mes, font=("Roboto", 9), bg="#1f2329", fg="white",
                              selectcolor=colores[1], variable=var, command=lambda m=mes: toggle_mes(m))
        check.pack(anchor="w", pady=2, padx=5)

    # Crear el gráfico y ubicarlo en fila 2, columnas 2-3
    graph_frame = tk.Frame(main_container, bg="#1f2329")
    graph_frame.grid(row=1, column=2, columnspan=2, sticky="nsew", padx=10, pady=10)

    figure = plt.Figure(figsize=(10, 5), dpi=100)  # Ajustar el tamaño del gráfico según necesidad
    ax = figure.add_subplot(111)

    canvas = FigureCanvasTkAgg(figure, master=graph_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    actualizar_grafico()

    # Botón para limpiar filtros
    def limpiar_filtros():
        autor_combobox.set("Seleccionar autor")
        genero_combobox.set("Seleccionar género")
        año_combobox.set(str(current_year))
        # Deseleccionar todos los checkboxes
        for child in check_frame.winfo_children():
            if isinstance(child, tk.Checkbutton):
                child.deselect()
        # Limpiar la lista de meses seleccionados
        selected_months.clear()
        actualizar_grafico()

    limpiar_button = tk.Button(filters_frame, text="Limpiar filtros", font=("Roboto", 10), bg="#2a3138", fg="white",
                               command=limpiar_filtros, relief="flat", padx=10, pady=5)
    limpiar_button.pack(side="left", padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("1200x700")
    root.configure(bg="#1f2329")

    main_frame = tk.Frame(root, bg="#1f2329")
    main_frame.pack(fill="both", expand=True)

    cargar_contenido_dashboard_2(main_frame)

    root.mainloop()
