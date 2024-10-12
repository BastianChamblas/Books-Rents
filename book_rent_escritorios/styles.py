# styles.py
from tkinter import ttk

def apply_styles():
    style = ttk.Style()
    style.theme_use('clam')  # Asegurarse de usar un tema que permita personalización
    style.configure('TNotebook', background='#1f2329')
    style.configure('TFrame', background='white')
    style.configure("TLabel", font=('Segoe UI', 12), background="#2e3b4e", foreground="#c7d5e0")
    style.configure("CustomLogin.TButton", fieldbackground="#1b2838", background="#1b2838", foreground="#c7d5e0", bordercolor="#c7d5e0", lightcolor="#c7d5e0", darkcolor="#c7d5e0", borderwidth=2, relief="raised")
    style.map("CustomLogin.TButton", background=[("active", "#1b2838")])  # Quitar el brillo al pasar el mouse
    style.configure("CustomLogin.TEntry", fieldbackground="#1b2838", background="#1b2838", foreground="#c7d5e0", bordercolor="#c7d5e0", lightcolor="#c7d5e0", darkcolor="#c7d5e0", borderwidth=2, relief="flat")
    style.map("CustomLogin.TEntry", highlightbackground=[('focus', '#1b2838')], highlightcolor=[('focus', '#1b2838')])

