import tkinter as tk
from tkinter import messagebox

def es_seguro(tablero, fila, columna):
    for i in range(fila):
        if tablero[i][columna] == 1:
            return False

    for i, j in zip(range(fila - 1, -1, -1), range(columna - 1, -1, -1)):
        if tablero[i][j] == 1:
            return False

    for i, j in zip(range(fila - 1, -1, -1), range(columna + 1, len(tablero))):
        if tablero[i][j] == 1:
            return False

    return True

def resolver_8_reinas_todas(tablero, fila, soluciones):
    n = len(tablero)
    if fila >= n:
        soluciones.append([fila[:] for fila in tablero])
        return

    for columna in range(n):
        if es_seguro(tablero, fila, columna):
            tablero[fila][columna] = 1
            resolver_8_reinas_todas(tablero, fila + 1, soluciones)
            tablero[fila][columna] = 0

def mostrar_soluciones():
    ventana.withdraw()
    ventana_soluciones = tk.Toplevel()
    ventana_soluciones.title("Soluciones del Problema de las 8 Reinas")
    ventana_soluciones.geometry("400x400")
    ventana_soluciones.configure(bg="#f0f0f0")

    lista_soluciones = tk.Listbox(ventana_soluciones, width=50, height=10, bg="#ffffff", font=("Arial", 12), selectmode=tk.SINGLE)
    lista_soluciones.pack(pady=20)

    for index, solucion in enumerate(soluciones):
        lista_soluciones.insert(tk.END, f"Solución {index + 1}")

    def mostrar_seleccion():
        seleccion = lista_soluciones.curselection()
        if seleccion:
            mostrar_tablero_solucion(seleccion[0])

    def mostrar_tablero_solucion(index):
        ventana_tablero_solucion = tk.Toplevel()
        ventana_tablero_solucion.title(f"Solución {index + 1}")
        ventana_tablero_solucion.geometry("400x400")
        frame_tablero = tk.Frame(ventana_tablero_solucion, bg="#f0f0f0")
        frame_tablero.pack(pady=20)

        for i in range(n):
            for j in range(n):
                color = "#ffffff" if (i + j) % 2 == 0 else "#a0a0a0"
                bg_color = "yellow" if soluciones[index][i][j] == 1 else color
                tk.Label(frame_tablero, width=4, height=2, bg=bg_color, relief="solid").grid(row=i, column=j)

    boton_ver = tk.Button(ventana_soluciones, text="Ver Solución", command=mostrar_seleccion, bg="#4CAF50", fg="white", font=("Arial", 12))
    boton_ver.pack(pady=5)

    boton_cerrar = tk.Button(ventana_soluciones, text="Cerrar", command=ventana_soluciones.destroy, bg="#f44336", fg="white", font=("Arial", 12))
    boton_cerrar.pack(pady=10)

def iniciar_juego():
    ventana.withdraw()
    ventana_juego = tk.Toplevel()
    ventana_juego.title("Jugar 8 Reinas")

    frame_tablero = tk.Frame(ventana_juego)
    frame_tablero.pack(pady=20)

    global boton_tablero, tablero_jugador
    boton_tablero = []
    tablero_jugador = [[0] * n for _ in range(n)]

    for i in range(n):
        fila_botones = []
        for j in range(n):
            boton = tk.Button(frame_tablero, width=4, height=2, command=lambda i=i, j=j: click_casilla(i, j))
            boton.grid(row=i, column=j)
            boton.bind("<Double-1>", lambda event, i=i, j=j: desmarcar_casilla(i, j))
            fila_botones.append(boton)
        boton_tablero.append(fila_botones)

    boton_reiniciar = tk.Button(ventana_juego, text="Reiniciar Juego", command=reiniciar_juego, bg="#FF9800", fg="white", font=("Arial", 12))
    boton_reiniciar.pack(pady=10)

    ventana_juego.protocol("WM_DELETE_WINDOW", lambda: (ventana_juego.destroy(), ventana.deiconify()))

def reiniciar_juego():
    """Reinicia el tablero del jugador a un estado vacío."""
    global tablero_jugador
    tablero_jugador = [[0] * n for _ in range(n)]
    actualizar_tablero_jugador()

def desmarcar_casilla(fila, columna):
    """Función que desmarca una casilla (elimina la reina)"""
    if tablero_jugador[fila][columna] == 1:
        tablero_jugador[fila][columna] = 0
        actualizar_tablero_jugador()

def click_casilla(fila, columna):
    """Función que coloca una reina en una casilla si es segura"""
    if tablero_jugador[fila][columna] == 0:
        if es_seguro(tablero_jugador, fila, columna):
            tablero_jugador[fila][columna] = 1
            actualizar_tablero_jugador()
            if verificar_juego_completado():
                messagebox.showinfo("Juego Completado", "¡Felicidades, has completado el juego!")
        else:
            messagebox.showerror("Movimiento Inválido", "La posición no es segura.")

def verificar_juego_completado():
    return sum(sum(fila) for fila in tablero_jugador) == n

def actualizar_tablero_jugador():
    """Función que actualiza el tablero visualmente"""
    for i in range(n):
        for j in range(n):
            color = "#ffffff" if (i + j) % 2 == 0 else "#a0a0a0"
            boton_tablero[i][j].config(bg=color)
            if tablero_jugador[i][j] == 1:
                boton_tablero[i][j].config(bg="yellow")

def iniciar_validar_juego():
    ventana.withdraw()
    ventana_validar_juego = tk.Toplevel()
    ventana_validar_juego.title("Validar Juego 8 Reinas")

    frame_tablero = tk.Frame(ventana_validar_juego)
    frame_tablero.pack(pady=20)

    global boton_tablero_validar, tablero_validar, reinas_colocadas
    boton_tablero_validar = []
    tablero_validar = [[0] * n for _ in range(n)]
    reinas_colocadas = 0

    for i in range(n):
        fila_botones = []
        for j in range(n):
            boton = tk.Button(frame_tablero, width=4, height=2, command=lambda i=i, j=j: click_casilla_validar(i, j))
            boton.grid(row=i, column=j)
            fila_botones.append(boton)
        boton_tablero_validar.append(fila_botones)

    boton_validar = tk.Button(ventana_validar_juego, text="Validar Juego", command=validar_juego, bg="#4CAF50", fg="white", font=("Arial", 12))
    boton_validar.pack(pady=5)

    boton_reiniciar = tk.Button(ventana_validar_juego, text="Reiniciar Juego", command=reiniciar_validar_juego, bg="#FF9800", fg="white", font=("Arial", 12))
    boton_reiniciar.pack(pady=5)

    boton_ver_soluciones = tk.Button(ventana_validar_juego, text="Ver Soluciones", command=mostrar_soluciones, bg="#2196F3", fg="white", font=("Arial", 12))
    boton_ver_soluciones.pack(pady=5)

    ventana_validar_juego.protocol("WM_DELETE_WINDOW", lambda: (ventana_validar_juego.destroy(), ventana.deiconify()))

def reiniciar_validar_juego():
    """Reinicia el tablero de validación a un estado vacío."""
    global tablero_validar, reinas_colocadas
    tablero_validar = [[0] * n for _ in range(n)]
    reinas_colocadas = 0
    actualizar_tablero_validar()

def click_casilla_validar(fila, columna):
    global reinas_colocadas

    if tablero_validar[fila][columna] == 0:
        if reinas_colocadas < 8:
            tablero_validar[fila][columna] = 1
            reinas_colocadas += 1
            actualizar_tablero_validar()
        else:
            messagebox.showinfo("Límite Alcanzado", "Ya has colocado todas las 8 reinas.")
    else:
        tablero_validar[fila][columna] = 0
        reinas_colocadas -= 1
        actualizar_tablero_validar()

def validar_juego():
    total_reinas = sum(sum(fila) for fila in tablero_validar)

    if total_reinas != 8:
        messagebox.showerror("Juego Inválido", "Debes colocar exactamente 8 reinas.")
        return

    for i in range(n):
        for j in range(n):
            if tablero_validar[i][j] == 1:
                tablero_validar[i][j] = 0
                if not es_seguro(tablero_validar, i, j):
                    messagebox.showerror("Juego Inválido", "La colocación de las reinas no es válida.")
                    tablero_validar[i][j] = 1
                    return
                tablero_validar[i][j] = 1

    messagebox.showinfo("Juego Válido", "¡El tablero tiene una solución válida!")

def actualizar_tablero_validar():
    for i in range(n):
        for j in range(n):
            color = "#ffffff" if (i + j) % 2 == 0 else "#a0a0a0"
            boton_tablero_validar[i][j].config(bg=color)
            if tablero_validar[i][j] == 1:
                boton_tablero_validar[i][j].config(bg="yellow")
n = 8
soluciones = []
tablero = [[0] * n for _ in range(n)]
resolver_8_reinas_todas(tablero, 0, soluciones)

ventana = tk.Tk()
ventana.title("Problema de las 8 Reinas")
ventana.geometry("300x250")
ventana.configure(bg="#e0e0e0")

etiqueta_titulo = tk.Label(ventana, text="8 Reinas", font=("Arial", 16, "bold"), bg="#e0e0e0")
etiqueta_titulo.pack(pady=10)

boton_jugar = tk.Button(ventana, text="Validacion de juego por movimiento", command=iniciar_juego, bg="#4CAF50", fg="white", font=("Arial", 12))
boton_jugar.pack(pady=5)

boton_ver_soluciones = tk.Button(ventana, text="Ver Soluciones", command=mostrar_soluciones, bg="#4CAF50", fg="white", font=("Arial", 12))
boton_ver_soluciones.pack(pady=5)

boton_validar = tk.Button(ventana, text="Jugar", command=iniciar_validar_juego, bg="#4CAF50", fg="white", font=("Arial", 12))
boton_validar.pack(pady=5)

ventana.mainloop()