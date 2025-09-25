import tkinter as tk
from tkinter import ttk, messagebox
import json

ventana = tk.Tk()
ventana.title("Gestor de pedidos")
ventana.geometry("600x400")

# Configurar grid para que la tabla y entradas se adapten al tamaño
ventana.grid_columnconfigure(1, weight=1)
ventana.grid_rowconfigure(6, weight=1)

# Crear tabla con columnas
tabla = ttk.Treeview(ventana, columns=("cliente", "telefono", "producto", "cantidad", "precio"), show="headings")
tabla.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

# Configurar columnas
tabla.column("cliente", anchor=tk.W, width=120)
tabla.column("telefono", anchor=tk.W, width=120)
tabla.column("producto", anchor=tk.CENTER, width=100)
tabla.column("cantidad", anchor=tk.CENTER, width=80)
tabla.column("precio", anchor=tk.CENTER, width=80)

# Configurar encabezados
tabla.heading("cliente", text="Cliente")
tabla.heading("telefono", text="Teléfono")
tabla.heading("producto", text="Producto")
tabla.heading("cantidad", text="Cantidad")
tabla.heading("precio", text="Precio")

# Añadir scrollbar vertical para la tabla
scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=tabla.yview)
scrollbar.grid(row=6, column=3, sticky="ns", pady=5)
tabla.configure(yscrollcommand=scrollbar.set)

# Crear etiquetas y entradas para formulario
tk.Label(ventana, text="Cliente:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entrada_cliente = tk.Entry(ventana)
entrada_cliente.grid(row=0, column=1, sticky="we", padx=5, pady=5)

tk.Label(ventana, text="Teléfono:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entrada_telefono = tk.Entry(ventana)
entrada_telefono.grid(row=1, column=1, sticky="we", padx=5, pady=5)

tk.Label(ventana, text="Producto:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entrada_producto = tk.Entry(ventana)
entrada_producto.grid(row=2, column=1, sticky="we", padx=5, pady=5)

tk.Label(ventana, text="Cantidad:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
entrada_cantidad = tk.Entry(ventana)
entrada_cantidad.grid(row=3, column=1, sticky="we", padx=5, pady=5)

tk.Label(ventana, text="Precio:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
entrada_precio = tk.Entry(ventana)
entrada_precio.grid(row=4, column=1, sticky="we", padx=5, pady=5)

# Lista para guardar pedidos en memoria
pedidos = []

def guardar_pedidos():
    with open("pedidos.json", "w", encoding="utf-8") as archivo:
        json.dump(pedidos, archivo, indent=4, ensure_ascii=False)

def cargar_pedidos():
    try:
        with open("pedidos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def añadir_producto():
    cliente = entrada_cliente.get().strip()
    telefono = entrada_telefono.get().strip()
    producto = entrada_producto.get().strip()
    cantidad = entrada_cantidad.get().strip()
    precio = entrada_precio.get().strip()

    if not cliente or not telefono or not producto or not cantidad or not precio:
        messagebox.showwarning("Datos incompletos", "Por favor, rellena todos los campos.")
        return

    try:
        cantidad_num = int(cantidad)
        precio_num = float(precio)
    except ValueError:
        messagebox.showwarning("Error en datos", "Cantidad debe ser un número entero y precio un número decimal.")
        return

    pedido = {
        "cliente": cliente,
        "telefono": telefono,
        "producto": producto,
        "cantidad": cantidad_num,
        "precio": precio_num
    }

    pedidos.append(pedido)
    guardar_pedidos()
    tabla.insert("", "end", values=(cliente, telefono, producto, cantidad_num, precio_num))

    # Limpiar campos
    entrada_cliente.delete(0, tk.END)
    entrada_telefono.delete(0, tk.END)
    entrada_producto.delete(0, tk.END)
    entrada_cantidad.delete(0, tk.END)
    entrada_precio.delete(0, tk.END)

def eliminar_pedido():
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showinfo("Eliminar pedido", "No has seleccionado ningún pedido para eliminar.")
        return

    if not messagebox.askyesno("Confirmar eliminación", "¿Seguro que quieres eliminar el pedido seleccionado?"):
        return

    item = seleccion[0]
    valores = tabla.item(item, "values")
    cliente, telefono, producto, cantidad, precio = valores

    for i, pedido in enumerate(pedidos):
        if (pedido["cliente"] == cliente and pedido["telefono"] == telefono
            and pedido["producto"] == producto and str(pedido["cantidad"]) == cantidad
            and str(pedido["precio"]) == precio):
            pedidos.pop(i)
            break

    tabla.delete(item)
    guardar_pedidos()
    messagebox.showinfo("Pedido eliminado", f"Pedido de {cliente} eliminado correctamente.")

boton_añadir = tk.Button(ventana, text="Añadir producto", command=añadir_producto)
boton_añadir.grid(row=5, column=0, columnspan=2, pady=10)

boton_eliminar = tk.Button(ventana, text="Eliminar pedido seleccionado", command=eliminar_pedido)
boton_eliminar.grid(row=7, column=0, columnspan=2, pady=10)

pedidos = cargar_pedidos()
for pedido in pedidos:
    tabla.insert("", "end", values=(pedido["cliente"], pedido["telefono"], pedido["producto"], pedido["cantidad"], pedido["precio"]))

ventana.mainloop()
