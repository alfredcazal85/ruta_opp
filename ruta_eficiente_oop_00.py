#al agrupar el codigo en clases se vuelve mas organizado y facil de mantener. Las clases permiten reutilizar el codigo sin duplicar
import tkinter as tk
from heapq import heappop, heappush
#Agrupa los datos y metodos relacionados con el mapa en una clase 
class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.terrenos = {
            "01": {"color": "lightgreen", "costo_pasos": 2},  # Césped
            "02": {"color": "darkgreen", "costo_pasos": 4},  # Bosque
            "04": {"color": "darkblue", "costo_pasos": 6},   # Agua profunda
            "05": {"color": "darkgray", "costo_pasos": 15}   # Muro
        }
        self.mapa = [["01" for _ in range(columnas)] for _ in range(filas)]
    
    def obtener_costo_pasos(self, codigo):
        return self.terrenos[codigo]["costo_pasos"]
    
    def actualizar_terreno(self, terreno, coords):
        for x, y in coords:
            self.mapa[y][x] = terreno

    def es_accesible(self, x, y):
        return 0 <= x < self.columnas and 0 <= y < self.filas

    def obtener_color(self, codigo):
        return self.terrenos[codigo]["color"]
#Agrupa el algoritmo y la logica para encontrar la ruta mas eficiente, y la modificacion del algoritmo no afecta otras partes del codigo
class CalculadoraDeRutas:
    def __init__(self, mapa):
        self.mapa = mapa

    def a_star(self, inicio, fin):
        filas, columnas = len(self.mapa.mapa), len(self.mapa.mapa[0])
        vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        open_set = []
        heappush(open_set, (0, inicio))
        g_score = {inicio: 0}
        f_score = {inicio: self.mapa.obtener_costo_pasos(self.mapa.mapa[inicio[1]][inicio[0]])}
        came_from = {}

        while open_set:
            _, current = heappop(open_set)
            
            if current == fin:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(inicio)
                return path[::-1]

            for d in vecinos:
                vecino = (current[0] + d[0], current[1] + d[1])
                if self.mapa.es_accesible(vecino[0], vecino[1]):
                    tentative_g_score = g_score[current] + self.mapa.obtener_costo_pasos(self.mapa.mapa[vecino[1]][vecino[0]])
                    if vecino not in g_score or tentative_g_score < g_score[vecino]:
                        came_from[vecino] = current
                        g_score[vecino] = tentative_g_score
                        f_score[vecino] = tentative_g_score
                        heappush(open_set, (f_score[vecino], vecino))

        return []

    def encontrar_ruta(self, inicio, fin, saldo):
        ruta = self.a_star(inicio, fin)
        for x, y in ruta:
            costo_pasos = self.mapa.obtener_costo_pasos(self.mapa.mapa[y][x])
            saldo -= costo_pasos
        return ruta, saldo

# Configuración de la interfaz gráfica y sus elementos visuales, ahora llama a los objetos mapa y calculadora de rutas haciendo mas claro y modular el codigo

root = tk.Tk()
root.title("Calculadora de Rutas")

mapa = Mapa(10, 10)
calculadora = CalculadoraDeRutas(mapa)

canvas = tk.Canvas(root, width=400, height=400)
canvas.grid(row=0, column=0, rowspan=10, columnspan=10)

celdas = [[None for _ in range(10)] for _ in range(10)]
for y in range(10):
    for x in range(10):
        celdas[y][x] = canvas.create_rectangle(x*40, y*40, x*40+40, y*40+40, fill=mapa.obtener_color("01"), outline="black")


def encontrar_ruta():
    inicio = (int(inicio_y.get()), int(inicio_x.get()))
    fin = (int(fin_y.get()), int(fin_x.get()))
    saldo = int(saldo_pasos.get())
    ruta, saldo = calculadora.encontrar_ruta(inicio, fin, saldo)
    
    for fila in celdas:
        for celda in fila:
            canvas.itemconfig(celda, outline="black")
    
    for x, y in ruta:
        canvas.itemconfig(celdas[y][x], outline="yellow", width=2)

    saldo_pasos.set(saldo)
    etiqueta_saldo.config(text=f"Saldo de pasos: {saldo}")

def actualizar_terreno(terreno):
    coords = [(int(coord[1]), int(coord[0])) for coord in terrenos_coords[terreno]]
    mapa.actualizar_terreno(terreno, coords)
    for x, y in coords:
        canvas.itemconfig(celdas[y][x], fill=mapa.obtener_color(terreno))

def agregar_coordenada(terreno):
    x = int(coordenada_x.get())
    y = int(coordenada_y.get())
    terrenos_coords[terreno].append((x, y))
    lista_coordenadas[terreno].insert(tk.END, f"({x}, {y})")

# Controles para entrada de coordenadas de inicio y fin
tk.Label(root, text="Inicio X:").grid(row=10, column=0)
inicio_x = tk.Entry(root, width=3)
inicio_x.grid(row=10, column=1)
tk.Label(root, text="Y:").grid(row=10, column=2)
inicio_y = tk.Entry(root, width=3)
inicio_y.grid(row=10, column=3)

tk.Label(root, text="Fin X:").grid(row=10, column=4)
fin_x = tk.Entry(root, width=3)
fin_x.grid(row=10, column=5)
tk.Label(root, text="Y:").grid(row=10, column=6)
fin_y = tk.Entry(root, width=3)
fin_y.grid(row=10, column=7)

tk.Button(root, text="Encontrar Ruta", command=encontrar_ruta).grid(row=10, column=8, columnspan=2)

# Controles para entrada de coordenadas de terrenos
terrenos_coords = {
    "02": [],
    "04": [],
    "05": []
}

tk.Label(root, text="Terreno X:").grid(row=11, column=0)
coordenada_x = tk.Entry(root, width=3)
coordenada_x.grid(row=11, column=1)
tk.Label(root, text="Y:").grid(row=11, column=2)
coordenada_y = tk.Entry(root, width=3)
coordenada_y.grid(row=11, column=3)

tk.Button(root, text="Agregar Bosque", command=lambda: agregar_coordenada("02")).grid(row=11, column=4, columnspan=2)
tk.Button(root, text="Agregar Agua Profunda", command=lambda: agregar_coordenada("04")).grid(row=11, column=6, columnspan=2)
tk.Button(root, text="Agregar Muro", command=lambda: agregar_coordenada("05")).grid(row=11, column=8, columnspan=2)

lista_coordenadas = {
    "02": tk.Listbox(root, height=6, width=20),
    "04": tk.Listbox(root, height=6, width=20),
    "05": tk.Listbox(root, height=6, width=20)
}

lista_coordenadas["02"].grid(row=12, column=0, columnspan=3)
lista_coordenadas["04"].grid(row=12, column=4, columnspan=3)
lista_coordenadas["05"].grid(row=12, column=8, columnspan=3)

tk.Button(root, text="Actualizar Bosque", command=lambda: actualizar_terreno("02")).grid(row=13, column=0, columnspan=3)
tk.Button(root, text="Actualizar Agua Profunda", command=lambda: actualizar_terreno("04")).grid(row=13, column=4, columnspan=3)
tk.Button(root, text="Actualizar Muro", command=lambda: actualizar_terreno("05")).grid(row=13, column=8, columnspan=3)

# Controles para el saldo de pasos despues del recorrido
tk.Label(root, text="Saldo de pasos:").grid(row=14, column=0)
saldo_pasos = tk.StringVar(value="200")
entrada_saldo = tk.Entry(root, textvariable=saldo_pasos, width=5)
entrada_saldo.grid(row=14, column=1)
etiqueta_saldo = tk.Label(root, text="Saldo de pasos: 200")
etiqueta_saldo.grid(row=14, column=2, columnspan=4)

root.mainloop()
