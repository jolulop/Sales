import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyodbc

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

# Funciones CRUD
def fetch_data():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CLIENTES")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

def add_cliente():
    if nombre_var.get() == "" or actualizada_var.get() == "":
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO CLIENTES (nombre, ID_fiscal, parent_id, sector, pais, tamaño, observaciones, estado, clasificacion, actualizada) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (nombre_var.get(), id_fiscal_var.get(), parent_id_var.get(), sector_var.get(), pais_var.get(), tamaño_var.get(), observaciones_var.get(), estado_var.get(), clasificacion_var.get(), actualizada_var.get()))
    conn.commit()
    conn.close()
    fetch_data()
    clear_fields()

def update_cliente():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE CLIENTES SET nombre=?, ID_fiscal=?, parent_id=?, sector=?, pais=?, tamaño=?, observaciones=?, estado=?, clasificacion=?, actualizada=? WHERE id=?",
                   (nombre_var.get(), id_fiscal_var.get(), parent_id_var.get(), sector_var.get(), pais_var.get(), tamaño_var.get(), observaciones_var.get(), estado_var.get(), clasificacion_var.get(), actualizada_var.get(), id_var.get()))
    conn.commit()
    conn.close()
    fetch_data()
    clear_fields()

def delete_cliente():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CLIENTES WHERE id=?", (id_var.get(),))
    conn.commit()
    conn.close()
    fetch_data()
    clear_fields()

def clear_fields():
    id_var.set("")
    nombre_var.set("")
    id_fiscal_var.set("")
    parent_id_var.set("")
    sector_var.set("")
    pais_var.set("")
    tamaño_var.set("")
    observaciones_var.set("")
    estado_var.set("")
    clasificacion_var.set("")
    actualizada_var.set("")

def on_select(event):
    selected_row = tree.selection()[0]
    selected = tree.item(selected_row, 'values')
    id_var.set(selected[0])
    nombre_var.set(selected[1])
    id_fiscal_var.set(selected[2])
    parent_id_var.set(selected[3])
    sector_var.set(selected[4])
    pais_var.set(selected[5])
    tamaño_var.set(selected[6])
    observaciones_var.set(selected[7])
    estado_var.set(selected[8])
    clasificacion_var.set(selected[9])
    actualizada_var.set(selected[10])

# Interfaz de Tkinter
root = tk.Tk()
root.title("Gestión de Clientes")

id_var = tk.StringVar()
nombre_var = tk.StringVar()
id_fiscal_var = tk.StringVar()
parent_id_var = tk.StringVar()
sector_var = tk.StringVar()
pais_var = tk.StringVar()
tamaño_var = tk.StringVar()
observaciones_var = tk.StringVar()
estado_var = tk.StringVar()
clasificacion_var = tk.StringVar()
actualizada_var = tk.StringVar()

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="ID").grid(row=0, column=0)
tk.Entry(frame, textvariable=id_var).grid(row=0, column=1)

tk.Label(frame, text="Nombre").grid(row=1, column=0)
tk.Entry(frame, textvariable=nombre_var).grid(row=1, column=1)

tk.Label(frame, text="ID Fiscal").grid(row=2, column=0)
tk.Entry(frame, textvariable=id_fiscal_var).grid(row=2, column=1)

tk.Label(frame, text="Parent ID").grid(row=3, column=0)
tk.Entry(frame, textvariable=parent_id_var).grid(row=3, column=1)

tk.Label(frame, text="Sector").grid(row=4, column=0)
tk.Entry(frame, textvariable=sector_var).grid(row=4, column=1)

tk.Label(frame, text="País").grid(row=5, column=0)
tk.Entry(frame, textvariable=pais_var).grid(row=5, column=1)

tk.Label(frame, text="Tamaño").grid(row=6, column=0)
tk.Entry(frame, textvariable=tamaño_var).grid(row=6, column=1)

tk.Label(frame, text="Observaciones").grid(row=7, column=0)
tk.Entry(frame, textvariable=observaciones_var).grid(row=7, column=1)

tk.Label(frame, text="Estado").grid(row=8, column=0)
tk.Entry(frame, textvariable=estado_var).grid(row=8, column=1)

tk.Label(frame, text="Clasificación").grid(row=9, column=0)
tk.Entry(frame, textvariable=clasificacion_var).grid(row=9, column=1)

tk.Label(frame, text="Actualizada").grid(row=10, column=0)
tk.Entry(frame, textvariable=actualizada_var).grid(row=10, column=1)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

tk.Button(button_frame, text="Agregar", command=add_cliente).grid(row=0, column=0)
tk.Button(button_frame, text="Actualizar", command=update_cliente).grid(row=0, column=1)
tk.Button(button_frame, text="Eliminar", command=delete_cliente).grid(row=0, column=2)
tk.Button(button_frame, text="Limpiar", command=clear_fields).grid(row=0, column=3)

tree_frame = tk.Frame(root)
tree_frame.pack()

columns = ("ID", "Nombre", "ID Fiscal", "Parent ID", "Sector", "País", "Tamaño", "Observaciones", "Estado", "Clasificación", "Actualizada")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
tree.pack()

for col in columns:
    tree.heading(col, text=col)

tree.bind("<ButtonRelease-1>", on_select)

fetch_data()

root.mainloop()

