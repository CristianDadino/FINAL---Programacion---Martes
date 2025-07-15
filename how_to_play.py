"""
how_to_play.py
• Este módulo contiene el manual de instrucciones del juego.
• Explica el objetivo, cómo jugar, recolección de monedas y ganador.
• También incluye una tabla de controles y símbolos.
"""
#Estetica
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from auxiliar import limpiar

def mostrar_manual_juego():
    limpiar()
    console = Console()

    markdown = Markdown("""
# 🎮 Nubecillas de Calderilla – Manual de Instrucciones

## 🎯 Objetivo
Recolectá la mayor cantidad de monedas 💰 moviéndote desde tu posición hacia las casillas cercanas.

## 🕹️ Cómo se juega
- El tablero es una grilla de 3x3.
- Cada jugador comienza en un borde: Norte, Sur, Este u Oeste.
- En cada turno, podés elegir moverte hacia:
    - **Centro**
    - **Izquierda**
    - **Derecha**
- Solo se puede mover a una casilla adyacente.

## 🪙 Recolección de monedas
- Si sos el único jugador que elige una casilla con monedas, las ganás.
- Si **dos o más jugadores** eligen la misma casilla con monedas, nadie gana. Esa casilla se marca con una ❌ roja.

## 🏆 Ganador
- Al terminar las rondas, gana el jugador con más monedas acumuladas.
- Se muestra un ranking final y se guarda el highscore.

""")
    console.print(markdown)

    # Tabla de controles y símbolos
    tabla = Table(title="📚 Referencias visuales", show_lines=True)
    tabla.add_column("Elemento", style="cyan", justify="center")
    tabla.add_column("Significado", justify="left")

    tabla.add_row("🟥, 🟩, 🟦, 🟨", "Jugadores (Norte, Sur, Oeste, Este)")
    tabla.add_row("💰5", "Casilla con 5 monedas")
    tabla.add_row("❌", "[red]Conflicto:[/red] dos jugadores eligieron la misma casilla")
    tabla.add_row("← ↑ →", "Opciones de movimiento según dirección")

    console.print(tabla)

    console.print(Panel("[bold magenta]¡Buena suerte! Que gane el más codicioso 💸[/bold magenta]", title="Fin del manual"))
    input("\nPresiona Enter para volver al menu principal...")
    limpiar()