import tkinter as tk
from tkinter import ttk
from clientes import crear_tab_clientes
from empleados import crear_tab_empleados
from oportunidades import crear_tab_oportunidades
from timia import crear_tab_timia
from responsables import crear_tab_responsables
from acciones import crear_tab_acciones

def main():
    root = tk.Tk()
    root.title("Gestión de Base de Datos")

    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)

    tab_clientes = ttk.Frame(notebook)
    tab_empleados = ttk.Frame(notebook)
    tab_oportunidades = ttk.Frame(notebook)
    tab_timia = ttk.Frame(notebook)
    tab_responsables = ttk.Frame(notebook)
    tab_acciones = ttk.Frame(notebook)

    notebook.add(tab_clientes, text="Clientes")
    notebook.add(tab_empleados, text="Empleados")
    notebook.add(tab_oportunidades, text="Oportunidades")
    notebook.add(tab_timia, text="TIMIA")
    notebook.add(tab_responsables, text="Responsables")
    notebook.add(tab_acciones, text="Acciones")

    # Cargar funcionalidad de cada pestaña
    crear_tab_clientes(tab_clientes)
    crear_tab_empleados(tab_empleados)
    crear_tab_oportunidades(tab_oportunidades)
    crear_tab_timia(tab_timia)
    crear_tab_responsables(tab_responsables)
    crear_tab_acciones(tab_acciones)

    root.mainloop()

if __name__ == "__main__":
    main()