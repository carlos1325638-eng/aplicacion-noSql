import tkinter as tk
from tkinter import ttk, messagebox
from tinydb import TinyDB, Query


db = TinyDB("libros.json")
Libro = Query()

COLOR_FONDO = "#eeeeee"
COLOR_PANEL = "#f7f7f7"
COLOR_BOTON = "#10ff14"


def limpiar_campos():
    entrada_id.delete(0, tk.END)
    entrada_titulo.delete(0, tk.END)
    entrada_autor.delete(0, tk.END)
    entrada_editorial.delete(0, tk.END)
    entrada_anio.delete(0, tk.END)
    combo_disponible.set("Sí")
    entrada_id.focus()


def mostrar_libros():
    for fila in tabla.get_children():
        tabla.delete(fila)

    for i, libro in enumerate(db.all()):
        tag = "par" if i % 2 == 0 else "impar"
        tabla.insert("", tk.END, values=(
            libro.get("id", ""),
            libro.get("titulo", ""),
            libro.get("autor", ""),
            libro.get("editorial", ""),
            libro.get("anio", ""),
            libro.get("disponible", "")
        ), tags=(tag,))

    lbl_total.config(text=f"Total de libros: {len(db.all())}")


def guardar_libro():
    id_libro = entrada_id.get().strip()
    titulo = entrada_titulo.get().strip()
    autor = entrada_autor.get().strip()
    editorial = entrada_editorial.get().strip()
    anio = entrada_anio.get().strip()
    disponible = combo_disponible.get().strip()

    if id_libro == "" or titulo == "" or autor == "":
        messagebox.showwarning("Aviso", "Llena ID, título y autor.")
        return

    if db.search(Libro.id == id_libro):
        messagebox.showwarning("Aviso", "Ya existe un libro con ese ID.")
        return

    db.insert({
        "id": id_libro,
        "titulo": titulo,
        "autor": autor,
        "editorial": editorial,
        "anio": 2020,
        "disponible": disponible
    })

    messagebox.showinfo("Correcto", "Libro guardado.")
    limpiar_campos()
    mostrar_libros()


def buscar_libro():
    id_libro = entrada_id.get().strip()

    if id_libro == "":
        messagebox.showwarning("Aviso", "Escribe el ID del libro.")
        return

    resultado = db.search(Libro.id == id_libro)

    if resultado:
        libro = resultado[0]
        limpiar_campos()
        entrada_id.insert(0, libro.get("id", ""))
        entrada_titulo.insert(0, libro.get("titulo", ""))
        entrada_autor.insert(0, libro.get("autor", ""))
        entrada_editorial.insert(0, libro.get("editorial", ""))
        entrada_anio.insert(0, libro.get(0, "2020"))
        combo_disponible.set(libro.get("disponible", "Sí"))
    else:
        messagebox.showinfo("Resultado", "No se encontró el libro.")


def buscar_en_tabla():
    texto = entrada_busqueda.get().strip().lower()
    for fila in tabla.get_children():
        tabla.delete(fila)

    libros = db.all()
    if texto:
        libros = [l for l in libros if texto in l.get("titulo", "").lower() or texto in l.get("autor", "").lower()]

    for i, libro in enumerate(libros):
        tag = "par" if i % 2 == 0 else "impar"
        tabla.insert("", tk.END, values=(
            libro.get("id", ""), libro.get("titulo", ""), libro.get("autor", ""),
            libro.get("editorial", ""), libro.get("anio", ""), libro.get("disponible", "")
        ), tags=(tag,))

    lbl_total.config(text=f"Resultados: {len(libros)}")


def actualizar_libro():
    id_libro = entrada_id.get().strip()

    if id_libro == "":
        messagebox.showwarning("Aviso", "Escribe el ID del libro.")
        return

    if not db.search(Libro.id == id_libro):
        messagebox.showwarning("Aviso", "No existe un libro con ese ID.")
        return

    db.update({
        "titulo": entrada_titulo.get().strip(),
        "autor": entrada_autor.get().strip(),
        "editorial": entrada_editorial.get().strip(),
        "anio": entrada_anio.get().strip(),
        "disponible": combo_disponible.get().strip()
    }, Libro.id == id_libro)

    messagebox.showinfo("Correcto", "Libro actualizado.")
    limpiar_campos()
    mostrar_libros()


def eliminar_libro():
    id_libro = entrada_id.get().strip()

    if id_libro == "":
        messagebox.showwarning("Aviso", "Escribe el ID del libro.")
        return

    if not db.search(Libro.id == id_libro):
        messagebox.showwarning("Aviso", "No existe un libro con ese ID.")
        return

    if messagebox.askyesno("Confirmar", "¿Eliminar este libro?"):
        db.remove(Libro.id == id_libro)
        messagebox.showinfo("Correcto", "Libro eliminado.")
        limpiar_campos()
        mostrar_libros()


def seleccionar_libro(event):
    seleccionado = tabla.focus()
    if seleccionado:
        valores = tabla.item(seleccionado, "values")
        limpiar_campos()
        entrada_id.insert(0, valores[0])
        entrada_titulo.insert(0, valores[1])
        entrada_autor.insert(0, valores[2])
        entrada_editorial.insert(0, valores[3])
        entrada_anio.insert(0, valores[4])
        combo_disponible.set(valores[5])


# Ventana principal
ventana = tk.Tk()
ventana.title("Gestor NoSQL - Biblioteca")
ventana.geometry("900x680")
ventana.resizable(True, True)
ventana.configure(bg=COLOR_FONDO)

# Estilo básico para la tabla
estilo = ttk.Style()
estilo.theme_use("default")
estilo.configure("Treeview", rowheight=24, font=("Arial", 9), background="white", fieldbackground="white")
estilo.configure("Treeview.Heading", font=("Arial", 9, "bold"), background=COLOR_BOTON)

# Título
titulo = tk.Label(
    ventana,
    text="BIBLIOTECA NOSQL",
    font=("Arial", 17, "bold"),
    bg=COLOR_FONDO
)
titulo.pack(pady=(12, 4))

subtitulo = tk.Label(
    ventana,
    text="Registro y consulta de libros",
    font=("Arial", 9),
    bg=COLOR_FONDO
)
subtitulo.pack(pady=(0, 8))

# Contenedor general en dos columnas
contenedor = tk.Frame(ventana, bg=COLOR_FONDO)
contenedor.pack(fill="both", expand=True, padx=15, pady=5)

# Panel izquierdo: formulario
frame_izq = tk.Frame(contenedor, bg=COLOR_FONDO)
frame_izq.pack(side="left", fill="y", padx=(0, 12))

frame_formulario = tk.LabelFrame(frame_izq, text=" Datos del libro ", font=("Arial", 10, "bold"), bg=COLOR_PANEL, padx=12, pady=10)
frame_formulario.pack(fill="x")

labels = ["ID:", "Título:", "Autor:", "Editorial:", "Año:", "Disponible:"]
for i, texto in enumerate(labels):
    tk.Label(frame_formulario, text=texto, bg=COLOR_PANEL, anchor="w").grid(row=i*2, column=0, sticky="w", pady=(4, 0))

entrada_id = tk.Entry(frame_formulario, width=30)
entrada_id.grid(row=1, column=0, pady=(0, 5))

entrada_titulo = tk.Entry(frame_formulario, width=30)
entrada_titulo.grid(row=3, column=0, pady=(0, 5))

entrada_autor = tk.Entry(frame_formulario, width=30)
entrada_autor.grid(row=5, column=0, pady=(0, 5))

entrada_editorial = tk.Entry(frame_formulario, width=30)
entrada_editorial.grid(row=7, column=0, pady=(0, 5))

entrada_anio = tk.Entry(frame_formulario, width=30)
entrada_anio.grid(row=9, column=0, pady=(0, 5))

combo_disponible = ttk.Combobox(frame_formulario, values=("Sí", "No"), state="readonly", width=27)
combo_disponible.grid(row=11, column=0, pady=(0, 5))
combo_disponible.set("Sí")

# Botones en dos filas
frame_botones = tk.LabelFrame(frame_izq, text=" Acciones ", font=("Arial", 10, "bold"), bg=COLOR_PANEL, padx=8, pady=8)
frame_botones.pack(fill="x", pady=12)

botones = [
    ("Guardar", guardar_libro),
    ("Buscar ID", buscar_libro),
    ("Modificar", actualizar_libro),
    ("Eliminar", eliminar_libro),
    ("Limpiar", limpiar_campos),
    ("Mostrar todo", mostrar_libros),
]

for i, (texto, comando) in enumerate(botones):
    b = tk.Button(frame_botones, text=texto, width=13, bg=COLOR_BOTON, command=comando)
    b.grid(row=i//2, column=i%2, padx=4, pady=4)

lbl_total = tk.Label(frame_izq, text="Total de libros: 0", bg=COLOR_FONDO, font=("Arial", 9, "bold"))
lbl_total.pack(anchor="w", padx=5)

# Panel derecho: búsqueda y tabla
frame_der = tk.Frame(contenedor, bg=COLOR_FONDO)
frame_der.pack(side="left", fill="both", expand=True)

frame_busqueda = tk.Frame(frame_der, bg=COLOR_FONDO)
frame_busqueda.pack(fill="x", pady=(0, 8))

tk.Label(frame_busqueda, text="Buscar por título o autor:", bg=COLOR_FONDO).pack(side="left")
entrada_busqueda = tk.Entry(frame_busqueda, width=35)
entrada_busqueda.pack(side="left", padx=6)
tk.Button(frame_busqueda, text="Buscar", width=10, bg=COLOR_BOTON, command=buscar_en_tabla).pack(side="left", padx=2)
tk.Button(frame_busqueda, text="Ver todos", width=10, bg=COLOR_BOTON, command=mostrar_libros).pack(side="left", padx=2)

frame_tabla = tk.LabelFrame(frame_der, text=" Catálogo de libros ", font=("Arial", 10, "bold"), bg=COLOR_PANEL, padx=8, pady=8)
frame_tabla.pack(fill="both", expand=True)

columnas = ("id", "titulo", "autor", "editorial", "anio", "disponible")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scroll_y.set)

tabla.heading("id", text="ID")
tabla.heading("titulo", text="Título")
tabla.heading("autor", text="Autor")
tabla.heading("editorial", text="Editorial")
tabla.heading("anio", text="Año")
tabla.heading("disponible", text="Disp.")

tabla.column("id", width=65, anchor="center")
tabla.column("titulo", width=180)
tabla.column("autor", width=135)
tabla.column("editorial", width=115)
tabla.column("anio", width=60, anchor="center")
tabla.column("disponible", width=65, anchor="center")

tabla.tag_configure("par", background="#ffffff")
tabla.tag_configure("impar", background="#f1f1f1")

tabla.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

tabla.bind("<ButtonRelease-1>", seleccionar_libro)
entrada_busqueda.bind("<Return>", lambda event: buscar_en_tabla())

mostrar_libros()
ventana.mainloop()
