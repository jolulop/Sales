import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime

# Conexión a la base de datos
def connect():
    connection = None

    server = "timia.database.windows.net"
    database = "sales"
    username = "CloudSA85ee9ad0"
    password = "!nDXg4Q#JqNs8bCK"

    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password}'
        )
        print("Connection to SQL Server successful")
    except pyodbc.Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Obtener lista de clientes para el desplegable de "Cuenta padre"
def obtener_clientes():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM CLIENTES")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

# Función para insertar datos en la tabla Clientes
def add_cliente():
    if nombre_var.get() == "":
        messagebox.showerror("Error", "El campo Nombre es obligatorio")
        return

    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parent_id = parent_id_var.get()
    if parent_id == "N/A":
        parent_id = None
    else:
        parent_id = int(parent_id.split(' - ')[0])
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO CLIENTES (nombre, ID_fiscal, parent_id, sector, pais, tamaño, observaciones, estado, clasificacion, actualizada)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nombre_var.get(), id_fiscal_var.get(), parent_id, sector_var.get(), pais_var.get(), 
        tamaño_var.get(), observaciones_entry.get("1.0", tk.END).strip(), estado_var.get(), clasificacion_var.get(), ahora
    ))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Cliente agregado exitosamente")
    clear_fields()
    fetch_clientes()

# Función para actualizar datos en la tabla Clientes
def update_cliente():
    if not tree.selection():
        messagebox.showerror("Error", "Selecciona un cliente para actualizar")
        return

    cliente_id = tree.item(tree.selection()[0])['values'][0]
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parent_id = parent_id_var.get()
    if parent_id == "N/A":
        parent_id = None
    else:
        parent_id = int(parent_id.split(' - ')[0])

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE CLIENTES SET nombre=?, ID_fiscal=?, parent_id=?, sector=?, pais=?, tamaño=?, observaciones=?, estado=?, clasificacion=?, actualizada=?
        WHERE id=?
    """, (
        nombre_var.get(), id_fiscal_var.get(), parent_id, sector_var.get(), pais_var.get(),
        tamaño_var.get(), observaciones_entry.get("1.0", tk.END).strip(), estado_var.get(), clasificacion_var.get(), ahora, cliente_id
    ))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Cliente actualizado exitosamente")
    fetch_clientes()

# Función para eliminar un cliente
def delete_cliente():
    if not tree.selection():
        messagebox.showerror("Error", "Selecciona un cliente para eliminar")
        return

    cliente_id = tree.item(tree.selection()[0])['values'][0]
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CLIENTES WHERE id=?", (cliente_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Cliente eliminado exitosamente")
    clear_fields()
    fetch_clientes()

# Función para cargar datos de clientes en el grid
def fetch_clientes():
    for row in tree.get_children():
        tree.delete(row)
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, ID_fiscal, parent_id, sector, pais, tamaño, observaciones, estado, clasificacion FROM CLIENTES")
    for row in cursor.fetchall():
        # Remover comillas de los valores
        row = tuple(value.strip('\"') if isinstance(value, str) else value for value in row)
        tree.insert("", "end", values=row)
    conn.close()

# Función para manejar la selección de un cliente en el grid
def on_select(event):
    if not tree.selection():
        return

    selected = tree.item(tree.selection()[0], 'values')
    nombre_var.set(selected[1].strip('\"'))
    id_fiscal_var.set(selected[2].strip('\"'))
    parent_id_var.set(f"{selected[3]} - {dict(clientes).get(selected[3], 'N/A')}" if selected[3] else "N/A")
    sector_var.set(selected[4].strip('\"'))
    pais_var.set(selected[5].strip('\"'))
    tamaño_var.set(selected[6].strip('\"'))
    observaciones_entry.delete("1.0", tk.END)
    observaciones_entry.insert(tk.END, selected[7].strip('\"'))
    estado_var.set(selected[8].strip('\"'))
    clasificacion_var.set(selected[9].strip('\"'))

def clear_fields():
    nombre_var.set("")
    id_fiscal_var.set("")
    parent_id_var.set("N/A")
    sector_var.set("")
    pais_var.set("")
    tamaño_var.set("")
    observaciones_entry.delete("1.0", tk.END)
    estado_var.set("")
    clasificacion_var.set("")

# Crear la ventana principal
root = tk.Tk()
root.title("Gestion de Base de Datos")

# Crear el notebook (tab control)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Crear frames para cada tab
tab_clientes = ttk.Frame(notebook)
tab_empleados = ttk.Frame(notebook)
tab_oportunidades = ttk.Frame(notebook)
tab_timia = ttk.Frame(notebook)
tab_responsables = ttk.Frame(notebook)
tab_acciones = ttk.Frame(notebook)

# Agregar tabs al notebook
notebook.add(tab_clientes, text="Clientes")
notebook.add(tab_empleados, text="Empleados")
notebook.add(tab_oportunidades, text="Oportunidades")
notebook.add(tab_timia, text="TIMIA")
notebook.add(tab_responsables, text="Responsables")
notebook.add(tab_acciones, text="Acciones")

# Variables para Clientes
nombre_var = tk.StringVar()
id_fiscal_var = tk.StringVar()
parent_id_var = tk.StringVar()
sector_var = tk.StringVar()
pais_var = tk.StringVar()
tamaño_var = tk.StringVar()
observaciones_var = tk.StringVar()
estado_var = tk.StringVar()
clasificacion_var = tk.StringVar()

# Obtener lista de clientes
clientes = obtener_clientes()
clientes_opciones = ["N/A"] + [f"{cliente[0]} - {cliente[1]}" for cliente in clientes]

# Contenido del tab Clientes
frame_clientes = tk.Frame(tab_clientes)
frame_clientes.pack(pady=20)

tk.Label(frame_clientes, text="Nombre", anchor="e").grid(row=0, column=0, sticky="e")
tk.Entry(frame_clientes, textvariable=nombre_var).grid(row=0, column=1)

tk.Label(frame_clientes, text="ID Fiscal", anchor="e").grid(row=1, column=0, sticky="e")
tk.Entry(frame_clientes, textvariable=id_fiscal_var).grid(row=1, column=1)

tk.Label(frame_clientes, text="Cuenta padre", anchor="e").grid(row=2, column=0, sticky="e")
ttk.Combobox(frame_clientes, textvariable=parent_id_var, values=clientes_opciones).grid(row=2, column=1)
parent_id_var.set("N/A")

tk.Label(frame_clientes, text="Sector", anchor="e").grid(row=3, column=0, sticky="e")
ttk.Combobox(frame_clientes, textvariable=sector_var, values=["finanzas", "seguros", "telco", "utilities", "industria", "retail", "otros"]).grid(row=3, column=1)

tk.Label(frame_clientes, text="Pais", anchor="e").grid(row=4, column=0, sticky="e")
tk.Entry(frame_clientes, textvariable=pais_var).grid(row=4, column=1)

tk.Label(frame_clientes, text="Tamaño", anchor="e").grid(row=5, column=0, sticky="e")
ttk.Combobox(frame_clientes, textvariable=tamaño_var, values=["multinacional", "gran empresa", "pyme"]).grid(row=5, column=1)

tk.Label(frame_clientes, text="Observaciones", anchor="e").grid(row=6, column=0, sticky="e")
observaciones_entry = tk.Text(frame_clientes, height=5, width=40)
observaciones_entry.grid(row=6, column=1, sticky="we")
observaciones_entry.bind("<KeyRelease>", lambda e: observaciones_var.set(observaciones_entry.get("1.0", tk.END).strip()))

tk.Label(frame_clientes, text="Estado", anchor="e").grid(row=7, column=0, sticky="e")
ttk.Combobox(frame_clientes, textvariable=estado_var, values=["Activo", "Inactivo", "Lead", "Limbo"]).grid(row=7, column=1)

tk.Label(frame_clientes, text="Clasificacion", anchor="e").grid(row=8, column=0, sticky="e")
ttk.Combobox(frame_clientes, textvariable=clasificacion_var, values=["Estrategico", "Tier1", "Tier2", "Oportunista"]).grid(row=8, column=1)

button_frame_clientes = tk.Frame(tab_clientes)
button_frame_clientes.pack(pady=20)

tk.Button(button_frame_clientes, text="Agregar", command=add_cliente).grid(row=0, column=0)
tk.Button(button_frame_clientes, text="Actualizar", command=update_cliente).grid(row=0, column=1)
tk.Button(button_frame_clientes, text="Eliminar", command=delete_cliente).grid(row=0, column=2)
tk.Button(button_frame_clientes, text="Limpiar", command=clear_fields).grid(row=0, column=3)

# Grid para mostrar los clientes
tree = ttk.Treeview(tab_clientes, columns=("id", "nombre", "ID_fiscal", "parent_id", "sector", "pais", "tamaño", "observaciones", "estado", "clasificacion"), show="headings")
tree.heading("id", text="ID")
tree.heading("nombre", text="Nombre")
tree.heading("ID_fiscal", text="ID Fiscal")
tree.heading("parent_id", text="Cuenta padre")
tree.heading("sector", text="Sector")
tree.heading("pais", text="Pais")
tree.heading("tamaño", text="Tamaño")
tree.heading("observaciones", text="Observaciones")
tree.heading("estado", text="Estado")
tree.heading("clasificacion", text="Clasificacion")
tree.pack(fill=tk.BOTH, expand=True)
tree.bind("<ButtonRelease-1>", on_select)

# Ocultar columna ID
tree.column("id", width=0, stretch=tk.NO)

# Cargar datos de clientes al iniciar la aplicación
fetch_clientes()

# Similarmente, puedes agregar contenido para los otros tabs

root.mainloop()
