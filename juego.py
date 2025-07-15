"""
juego.py
• Este modulo contiene la logica base del juego.
    • Manejo de rondas.
    • Define la clase jugadores.
    • Muestra en pantalla el resultado del juego, sea empate o ganador.
    • Llama a la funcion para guardar el highscore.

"""
# Estetica
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from auxiliar import limpiar

# Funciones clave para mostrar el tablero y manejar las coordenadas.
from grilla import generar_grilla,mostrar_grilla, pedir_coordenada,flecha_coordenada,mostrar_grilla_con_conflictos

# En el final del juego guardo el puntaje.
from archivo import agregar_highscore

#Para darle mas timming al juego se usa la funcion sleep().
import time

console = Console()

"""
Define la clase Jugador.
• Contiene el nombre, icono, posicion (vector x,y) y puntos.
• La clave son los puntos cardinales, importantes para el movimiento del jugador (Norte, Sur, Este, Oeste).

"""
JUGADORES = {
    "Norte": {"nombre":"Jugador 1","icono": "🟥", "pos": (0, 1), "puntos": 0},
    "Sur":   {"nombre":"Bot 2","icono": "🟩", "pos": (2, 1), "puntos": 0},
    "Este":  {"nombre":"Bot 3","icono": "🟦", "pos": (1, 2), "puntos": 0},
    "Oeste": {"nombre":"Bot 4","icono": "🟨", "pos": (1, 0), "puntos": 0},
}

#Nro de rondas del juego.
RONDAS = 3


"""
run()

• Esta funcion es el bucle principal del juego.
• En cada ronda, se genera la grilla y se muestran las opciones de movimiento.
    • Se piden las coordenadas a cada jugador y se procesan los resultados.
    • Al final de las rondas, se muestra el puntaje final y se determina el ganador o empate.
• Las monedas cambian por ronda, por lo que se generan al inicio.
• Se muestra la grilla con los choques entre jugadores.
"""
def run():
    for ronda in range(1, RONDAS + 1):
        limpiar()
        
        grilla = generar_grilla()
        mostrar_grilla(grilla,ronda)
        
        elecciones = {}
        for nombre in JUGADORES:
            coord = pedir_coordenada(nombre,grilla,ronda)
            elecciones[nombre] = coord
        limpiar()
        console.print("\n📊 [bold]Resultados de la ronda:[/]")
        coords_usadas = list(elecciones.values())
        conflictos = set(coord for coord in coords_usadas if coords_usadas.count(coord) > 1)
        mostrar_grilla_con_conflictos(grilla, JUGADORES, conflictos)
        
        for nombre, coord in elecciones.items():
            origen = JUGADORES[nombre]["pos"]
            name = JUGADORES[nombre]["nombre"]
            color = JUGADORES[nombre]["icono"]
            
            
            flecha_coordenada(name,color,origen,coord)
            f, c = coord
            if coord in conflictos:
                
                
                console.print(f"Pero hubo conflicto. ❌ Pierde la casilla.")
                time.sleep(1.5)  # Pausa para dramatismo
            else:
                valor = grilla[f][c]
                if valor:
                    
                    JUGADORES[nombre]["puntos"] += valor
                    console.print(f"Gana [yellow]{valor}[/] monedas!✅")
                    time.sleep(1.5)  # Pausa para dramatismo
                else:
                    
                    console.print(f"No había monedas. ⚠")
                    time.sleep(3)  # Pausa para dramatismo
        input("\nPresiona Enter para ver la tabla general..")
        limpiar()
        tabla = Table(title="🧮 Puntaje actual", show_lines=True)

        tabla.add_column("Jugador", style="cyan", justify="left")
        tabla.add_column("Icono", justify="center")
        tabla.add_column("Puntos 💰", style="magenta", justify="center")

        for jugador in JUGADORES.values():
            nombre = jugador["nombre"]
            icono = jugador["icono"]
            puntos = str(jugador["puntos"])
            tabla.add_row(nombre, icono, puntos)

        console.print(tabla)

        input("\nPresiona Enter para continuar...")

    limpiar()
    console.print(("[bold green]🏁 ¡Fin del juego! Resultados finales:[/]\n"))
    for nombre in JUGADORES:
        console.print(f"{JUGADORES[nombre]['icono']} {JUGADORES[nombre]['nombre']}: {JUGADORES[nombre]['puntos']} monedas")
    
    anunciar_ganador_o_empate(JUGADORES)

"""
anunciar_ganador_o_empate()

• Funcion que finaliza el juego.
• Si hay un solo ganador, muestra su nombre y puntaje.
• Si hay empate, muestra los nombres de los jugadores empatados y su puntaje.
• Guarda el highscore del ganador.
• Vuelve al menu principal.
"""
def anunciar_ganador_o_empate(JUGADORES):
    # Paso 1: obtener el puntaje máximo
    max_puntos = max(j["puntos"] for j in JUGADORES.values())
    # Paso 2: obtener lista de jugadores con ese puntaje
    empatados = [(nombre, j) for nombre, j in JUGADORES.items() if j["puntos"] == max_puntos]

    # Paso 3: analizar el resultado
    if len(empatados) == 1: #Ganador único
        nombre, jugador = empatados[0]
        console.print(Panel(f"\n🎉 El ganador es **{jugador['icono']} {jugador['nombre']}**  con {max_puntos} puntos!"))
        agregar_highscore(jugador['nombre'], max_puntos)
    else:  #Empate
        tipos = {2: "doble", 3: "triple", 4: "cuádruple"}
        tipo = tipos.get(len(empatados), "empate múltiple")
        print()
        console.print(Panel(f"\n Hubo un {tipo} empate!"))
        for nombre, jugador in empatados:
            print(f"-{jugador['icono']} {jugador['nombre']} con {max_puntos} puntos.")
            
    print("\nGracias por jugar! 👋")
    input("\nPresiona Enter para volver al menu principal...")
    limpiar()

