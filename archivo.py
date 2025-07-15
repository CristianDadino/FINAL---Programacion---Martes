"""
archivo.py

• En este modulo se detallan las funciones relacionadas con la manipulacion del archivo de highscore.
• En caso de no encontrarse un archivo, lo genera automaticamente al momento de guardar la primer tarea.
"""
import json
import os
#Estetica
from auxiliar import limpiar
from rich.console import Console
from rich.table import Table
console= Console()

#Nombre del archivo
ARCHIVO_HIGHSCORE = "highscore.json"

#TOP de highscore. La lista no muestra todos los puntajes, sino los mejores 10.
MAX_REGISTROS = 10  # top 10

"""Carga el historial desde el archivo JSON o devuelve lista vacía si no existe."""
def cargar_highscores():
    
    if os.path.exists(ARCHIVO_HIGHSCORE):
        with open(ARCHIVO_HIGHSCORE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

"""Guarda el historial ordenado por puntaje descendente, limitado al top N."""
def guardar_highscores(historial):
    
    historial_ordenado = sorted(historial, key=lambda x: x["puntos"], reverse=True)
    historial_top = historial_ordenado[:MAX_REGISTROS]
    with open(ARCHIVO_HIGHSCORE, "w", encoding="utf-8") as f:
        json.dump(historial_top, f, ensure_ascii=False, indent=4)

"""Agrega un nuevo puntaje solo si NO es un bot."""
def agregar_highscore(nombre, puntos):

    historial = cargar_highscores() #Me traigo el archivo highscore.

    if nombre not in ["Bot 2", "Bot 3", "Bot 4"]:
        # Buscar si ya existe el jugador
        for entrada in historial:
            if entrada["nombre"] == nombre:
                entrada["puntos"] += puntos
                break
        else:
            # Si no lo encuentra, lo agrega
            historial.append({"nombre": nombre, "puntos": puntos})
            guardar_highscores(historial)
    else:
        return  # Ignorar bots u otros jugadores

"""Imprime el highscore en forma de tabla."""
def mostrar_highscores():
    
    historial = cargar_highscores()
    
    if not historial:
        print("\nNo hay highscores registrados aún.")
        input("\nPresiona Enter para volver al menu principal...")
        limpiar()
        return

    console = Console()
    tabla = Table(title="🏆 Highscore - Jugador", show_lines=True)

    tabla.add_column("Posición", justify="center")
    tabla.add_column("Nombre", style="cyan", justify="center")
    tabla.add_column("Puntos", style="magenta", justify="center")

    for i, entrada in enumerate(historial, start=1):
        tabla.add_row(str(i), entrada["nombre"], str(entrada["puntos"]))

    console.print(tabla)
    input("\nPulse Enter para volver al menú...")
    limpiar()
    return