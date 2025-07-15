"""
grilla.py

• Este modulo contiene la creacion del tablero del juego.
• Genera la grilla de 3x3 con monedas aleatorias.
• Muestra la grilla con los jugadores y las monedas.
• Permite a los jugadores elegir una casilla adyacente para moverse y guarda las coordenadas.
• Muestra la grilla con conflictos si dos jugadores eligen la misma casilla.
• Limita el movimiento del jugador a las casillas adyacentes.

"""
#Estetica
from auxiliar import limpiar
from rich.console import Console
from rich import print as rprint
from colorama import Fore, Style

#Para generar la eleccion de los bots.
import random

#Para darle mas timming al juego se usa la funcion sleep().
import time 

#Para ocultar la decision de los jugadores.
from getpass import getpass

console = Console()

# Este diccionario mapea las teclas numéricas ('1' a '9') a posiciones (fila, columna) de una grilla 3x3.
coordenadas = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
}
# Esto es una inversión del diccionario anterior: ahora vas de coordenadas a tecla.
coord_a_tecla = {v: k for k, v in coordenadas.items()}

"""
generar_grilla()

• Genera el tablero  de 3x3 con monedas aleatorias.
• La grilla es una lista de listas, donde cada casilla puede contener un numero de monedas (de 1 a 5) o None si está ocupada por un jugador.
• Las posiciones de los jugadores se definen en el diccionario JUGADORES.   

"""
def generar_grilla():
    from juego import JUGADORES
    grilla = [[None for _ in range(3)] for _ in range(3)]
    posiciones_jugadores = [j["pos"] for j in JUGADORES.values()]
    
    for f in range(3):
        for c in range(3):
            if (f, c) not in posiciones_jugadores:
                grilla[f][c] = random.randint(1, 5)
    return grilla


"""
mostrar_grilla()

• Muestra la grilla del juego con los jugadores y las monedas.
• Cada jugador se representa con un icono.
• Las monedas se muestran con un icono de moneda y su cantidad.
"""
def mostrar_grilla(grilla,ronda):
    from juego import JUGADORES,RONDAS
    r = ronda
    console.print(f"[bold green]💰 RONDA {r} de {RONDAS}[/]")
    print("╔" + "═══════╦" * 2 + "═══════╗")
    for f in range(3):
        print("║", end="")
        for c in range(3):
            #Busca si algún jugador está en la posición (f, c). Si lo encuentra, obtiene su ícono.
            icono = next((j["icono"] for j in JUGADORES.values() if j["pos"] == (f, c)), None)

            if icono:
                #Si hay jugador, muestra su ícono en negrita.
                contenido = f"[bold]{icono}    [/bold]"
            elif grilla[f][c] is not None:
                #Si no hay jugador, pero hay una moneda en esa posición, la muestra en amarillo con ícono.
                moneda = grilla[f][c]
                contenido = f"[yellow]💰{moneda}    [/yellow]"
            else:
                contenido = " "

            # Centrado en 7 caracteres fijos
            rprint(f"{contenido:^7}║", end="")
        print()
        if f < 2:
            print("╠" + "═══════╬" * 2 + "═══════╣")
    print("╚" + "═══════╩" * 2 + "═══════╝")

"""
mostrar_grilla()

• Muestra la grilla del juego con los jugadores y las monedas, pero también marca los choques entre jugadores.
• Los choques se marcan con una ❌ roja.

"""
def mostrar_grilla_con_conflictos(grilla, JUGADORES, conflictos):
    #rprint("[bold red]\n⚠️ Grilla con conflictos marcados:[/bold red]")
    print("╔" + "═══════╦" * 2 + "═══════╗")

    for f in range(3):
        print("║", end="")
        for c in range(3):
            coord = (f, c)

            if coord in conflictos:
                #Si es una coordenada en conflicto, muestra una ❌ roja.
                contenido = "[red]❌     [/red]"
            else:
                #Busca si algún jugador está en la posición (f, c). Si lo encuentra, obtiene su ícono.
                icono = next((j["icono"] for j in JUGADORES.values() if j["pos"] == coord), None)
                if icono:
                    #Si hay jugador, muestra su ícono en negrita.
                    contenido = f"[bold]{icono}    [/bold]"
                elif grilla[f][c] is not None:
                    #Si no hay jugador, pero hay una moneda en esa posición, la muestra en amarillo con ícono.
                    contenido = f"[yellow]💰{grilla[f][c]}    [/yellow]"
                else:
                    contenido = " "

            rprint(f"{contenido:^7}║", end="")
        print()
        if f < 2:
            print("╠" + "═══════╬" * 2 + "═══════╣")
    print("╚" + "═══════╩" * 2 + "═══════╝")

""" Esta funcion verifica si una coordenada está dentro del radio de movimiento permitido (adyacente) de otra coordenada. """
def dentro_de_radio(coord_origen, coord_destino):
    dr = abs(coord_origen[0] - coord_destino[0])
    dc = abs(coord_origen[1] - coord_destino[1])
    return max(dr, dc) <= 1 and coord_origen != coord_destino

"""
 pedir_coordenada(jugador,grilla,ronda)

Pide al jugador (humano o bot) que elija una casilla de movimiento válida.

 Esta función determina las casillas válidas alrededor del jugador actual,
 y luego realiza lo siguiente:
 
 - Si es un bot, elige una casilla al azar simulando un "pensamiento".
 - Si es un jugador humano, muestra una interfaz visual de movimientos
   disponibles según su posición cardinal (Norte, Sur, Este, Oeste),
   oculta el input con getpass, y valida que el movimiento sea válido.

 Args:
     jugador (str): Clave en el diccionario JUGADORES ('Norte', 'Sur', etc.)
     grilla (list): Grilla actual con monedas y posiciones.
     ronda (int): Número actual de ronda, para mostrar en pantalla.

 Returns:
     tuple: Coordenada (fila, columna) elegida por el jugador o bot.
"""
def pedir_coordenada(jugador,grilla,ronda):
    r = ronda
    limpiar()
    from juego import JUGADORES
    origen = JUGADORES[jugador]["pos"] #Posicion actual del jugador.
    casillas_validas = [
        coord for coord in coordenadas.values()
        if dentro_de_radio(origen, coord)
        and coord not in [j["pos"] for j in JUGADORES.values()]
    ] #Casillas adyacentes que no están ocupadas por otros jugadores.
    #Aca si el jugador es un bot, elige una casilla al azar.
    if JUGADORES[jugador]['nombre'].lower().startswith("bot"):
        mostrar_grilla(grilla,r)
        print(f"\n🤖 Turno de {JUGADORES[jugador]['icono']} {JUGADORES[jugador]['nombre']}...")
        time.sleep(1.2)  # Simula que piensa
        destino = elegir_movimiento_bot(origen)
        print(f"\n{JUGADORES[jugador]['nombre']} ha elegido un destino.")
        time.sleep(1.2)  # Pausa para dramatismo
        return destino
    #Defino los numeros de las teclas que corresponden a las casillas válidas.
    teclas_validas = [coord_a_tecla[c] for c in casillas_validas]
    #Muestro la grilla, con la ronda actual.
    mostrar_grilla(grilla,r)
    
    #Aca muestro las opciones de movimiento disponibles para el jugador.
    # Dependiendo de la posicion del jugador, muestro las teclas validas.
    if jugador == "Norte":
        print(Fore.LIGHTWHITE_EX + Style.NORMAL + "="*20+" Movimientos disponibles "+"="*20)
        console.print(f"""
                             7←| {JUGADORES[jugador]['icono']} |9→
                            -----------
                             X | 5↓ | X
                            -----------
                             X | X  | X
            """)
        print(Fore.LIGHTWHITE_EX + Style.NORMAL +"="*65)
    elif jugador == "Sur":
        print(Fore.LIGHTWHITE_EX + Style.NORMAL + "="*20+" Movimientos disponibles "+"="*20)
        console.print(f"""
                             X | X  | X
                            -----------          
                             X | 5↑ | X
                            -----------
                            1← | {JUGADORES[jugador]['icono']} |3→
            """)
        print(Fore.LIGHTWHITE_EX + Style.NORMAL +"="*65)
    elif jugador == "Este":
        print(Fore.LIGHTWHITE_EX + Style.NORMAL + "="*20+" Movimientos disponibles "+"="*20)
        console.print(f"""
                             X | X | 9↑
                            -----------
                             X | 5←| {JUGADORES[jugador]['icono']}
                            -----------
                             X | X | 3↓
            """)
        print(Fore.LIGHTWHITE_EX + Style.NORMAL +"="*65)
    elif jugador == "Oeste":
        print(Fore.LIGHTWHITE_EX + Style.NORMAL + "="*20+" Movimientos disponibles "+"="*20)
        console.print(f"""
                             7↑ | X | X
                            -----------
                             {JUGADORES[jugador]['icono']} |5→ | X
                            -----------
                             1↓ | X | X
            """)
        print(Fore.LIGHTWHITE_EX + Style.NORMAL +"="*65)

    while True: # Bucle para validar la entrada del usuario.
        # Solicita al jugador que elija una tecla válida, la cual NO va a verse por el getpass.
        # Esto es para ocultar la decision del jugador.
        console.print(f"\nTurno de {JUGADORES[jugador]['nombre']} {JUGADORES[jugador]['icono']}")
        console.print("Por favor, elije una casilla valida y apreta ENTER.")
        tecla = getpass("\n→→→→→ ").strip()
        #tecla = input(f"{JUGADORES[jugador]['icono']} {JUGADORES[jugador]['nombre']}, elige una tecla válida: ").strip()
        if tecla not in teclas_validas:
            print("❌ Tecla inválida o fuera de rango. Intenta otra.")
            continue
        time.sleep(0.8)  # Pausa para dramatismo
        return coordenadas[tecla]

"""Devuelve una posición (fila, columna) elegida aleatoriamente para un bot."""
def elegir_movimiento_bot(origen):
    
    movimientos_por_pos = {
        (0, 1) : [(1, 1), (1, 0), (1, 2)],
        (2, 1):   [(1, 1), (2, 0), (2, 2)],
        (1, 2): [(0, 2), (1, 1), (2, 2)],
        (1, 0):  [(0, 0), (1, 1), (2, 0)],
    }

    posibles = movimientos_por_pos.get(origen, [])
    return random.choice(posibles) if posibles else None

"""Devuelve una flecha que indica la dirección de la coordenada respecto al origen."""
def flecha_coordenada(jugador,color,origen,coord):
    
    #Sur:
    if origen == (2, 1) and coord == (1, 1 ):
        return print(Fore.CYAN + Style.BRIGHT + f"{color}{jugador} elige moverse hacia ARRIBA ↑↑↑")
    elif origen == (2, 1) and coord == (2, 0):
        return print(Fore.CYAN + Style.BRIGHT + f"{color}{jugador} elige moverse hacia IZQUIERDA ←←←")
    elif origen == (2, 1) and coord == (2, 2):
        return print(Fore.CYAN + Style.BRIGHT + f"{color}{jugador} elige moverse hacia DERECHA →→→")
    #Este:
    elif origen == (1, 2) and coord == (0, 2):
        return print(Fore.CYAN + Style.BRIGHT + f"{color}{jugador} elige moverse hacia ARRIBA ↑↑↑")
    elif origen == (1, 2) and coord == (1, 1):
        return print(Fore.CYAN + Style.BRIGHT + f"{color}{jugador} elige moverse hacia IZQUIERDA ←←←")
    elif origen == (1, 2) and coord == (2, 2):
        return print(Fore.CYAN + Style.BRIGHT + f"{color}{jugador} elige moverse hacia ABAJO ↓↓↓")
    #Oeste:
    elif origen == (1, 0) and coord == (0, 0):
        return print(Fore.CYAN + Style.BRIGHT + f"{color}{jugador} elige moverse hacia ARRIBA ↑↑↑")
    elif origen == (1, 0) and coord == (1, 1):
        return print(Fore.CYAN + Style.BRIGHT + f"{color}{jugador} elige moverse hacia DERECHA →→→")
    elif origen == (1, 0) and coord == (2, 0):
        return print(Fore.CYAN + Style.BRIGHT + f"{color}{jugador} elige moverse hacia ABAJO ↓↓↓")
    #Norte:
    elif origen == (0, 1) and coord == (1, 1):
        return print(Fore.CYAN + Style.BRIGHT + f"{color}{jugador} elige moverse hacia ABAJO ↓↓↓")
    elif origen == (0, 1) and coord == (0, 0):
        return print(Fore.CYAN + Style.BRIGHT + f"{color}{jugador} elige moverse hacia IZQUIERDA ←←←")
    elif origen == (0, 1) and coord == (0, 2):
        return print(Fore.CYAN + Style.BRIGHT + f"{color}{jugador} elige moverse hacia DERECHA →→→")