# styles.py
from tkinter import ttk

def apply_styles():
    style = ttk.Style()
    style.theme_use('clam')  # Usar un tema compatible y flexible

    # Configuración del estilo general TNotebook, aplicable a todas las instancias
    style.configure('TNotebook', background='#1f2329', borderwidth=0)
    style.configure('TNotebook.Tab',
                    background='#1f2329',
                    foreground='#fff',
                    font=("Roboto", 10),
                    padding=[10, 5])
    style.map('TNotebook.Tab',
              background=[('selected', '#1f2329'), ('!selected', '#555555')],
              foreground=[('selected', '#fff'), ('!selected', '#ccc')])

    # Estilos personalizados para botones
    style.configure("Custom.TButton",
                    background="#1b2838",
                    foreground="#c7d5e0",
                    borderwidth=2,
                    relief="raised")
    style.map("Custom.TButton",
              background=[("active", "#1b2838")],
              foreground=[("active", "#c7d5e0")])

    # Estilos personalizados para Combobox
    style.configure("Custom.TCombobox",
                    fieldbackground="#1b2838",
                    background="#1b2838",
                    foreground="#c7d5e0",
                    borderwidth=2,
                    relief="flat")
    style.map("Custom.TCombobox",
              fieldbackground=[('readonly', "#1b2838")],
              foreground=[('readonly', '#c7d5e0')])

    # Estilos personalizados para Entry
    style.configure("Custom.TEntry",
                    fieldbackground="#1b2838",
                    background="#1b2838",
                    foreground="#c7d5e0",
                    borderwidth=2,
                    relief="flat")
    style.map("Custom.TEntry",
              fieldbackground=[('focus', "#1b2838")],
              foreground=[('focus', '#c7d5e0')])

    # Estilo personalizado para TFrame
    style.configure('TFrame', background='white')

    # Estilo personalizado para TLabel
    style.configure("TLabel",
                    font=('Segoe UI', 12),
                    background="#2e3b4e",
                    foreground="#c7d5e0")
