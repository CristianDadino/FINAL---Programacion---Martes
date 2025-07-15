"""
auxiliar.py

• Modulo auxiliar que contiene funciones de utilidad para el juego, principalmente de personalizacion.
• Tambien contiene el menu principal.

"""

import os
#Estetica
from rich.console import Console
from rich.table import Table
from colorama import init, Fore, Style #Para agregar un detalle visual.
from rich.panel import Panel
from rich.prompt import IntPrompt

#Es para que los colores funcionen por cada linea y no en la totalidad del codigo.
init(autoreset=True) 

#Sirve para mostrar contenido en consola con el formato rich.
console = Console()

"""Funcion para hacer un clear de la pantalla. Importante esteticamente."""
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

"""Funcion para validar si la entrada es S o N."""
def si_no():
    while True:
        console.print("Por favor indique [yellow](S/N): [/yellow]")
        entrada = input()
        
        try:
            if entrada in ("S","N","s","n"):
                return(entrada.upper() == "S")
            else:
                print(f"Opción fuera de rango.")
        except ValueError:
            print(f"Entrada inválida. Por favor, introduzca una opción (S/N).")


"""
menu principal()

• La opcion elegida devuelve un numero que lleva a ejecutar una funcion diferente tal y como se muestra debajo.

"""
def menu_principal():
    console = Console()

    panel = Panel.fit(
            """
    [bold yellow]🎮 MENU PRINCIPAL[/bold yellow]

    [1] ▶️  Iniciar juego
    [2] 👥  Ver jugadores
    [3] ✏️  Personalizar nombres
    [4] 🏆  Ver Highscores
    [5] 📘  Ver manual
    [6] ❌  Salir del juego
            """,
            title="[bold cyan]💰 Nubecillas de Calderilla 💰 [/bold cyan]",
            border_style="bright_magenta"
        )

    console.clear()
    console.print(panel)

    return IntPrompt.ask("\n[bold green]Elegí una opción[/bold green]", choices=["1", "2", "3", "4", "5", "6"])

"""
actualizar_jugadores()

• Esta funcion actualiza los nombres de los jugadores en el diccionario JUGADORES.
• En caso de elegir menos de 4 jugadores, los que sobren se convierten en bots.
"""
def actualizar_jugadores(cantidad_humanos):
    from juego import JUGADORES
    claves = list(JUGADORES.keys())
    for i, direccion in enumerate(claves):
        if i < cantidad_humanos:
            JUGADORES[direccion]["nombre"] = f"Jugador {i+1}"
        else:
            JUGADORES[direccion]["nombre"] = f"Bot {i+1}"

"""
mostrar_jugadores()

• Esta funcion muestra los jugadores actuales en una tabla.
• Si se desea cambiar el numero de jugadores, se llama a la funcion actualizar_jugadores().

"""
def mostrar_jugadores():
    from juego import JUGADORES
    limpiar()
    table = Table(title="🏁 Jugadores Actuales", show_lines=True)

    table.add_column("Dirección", style="bold cyan")
    table.add_column("Nombre", style="bold")
    table.add_column("Icono", style="bold")

    for direccion, datos in JUGADORES.items():
        nombre = datos["nombre"]
        icono = datos["icono"]
        table.add_row(direccion, nombre, icono)

    console.print(table)
    console.print(Panel(f"\n✏️   [yellow]Desea cambiar el numero de jugadores?[/yellow]"))
    #print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "=== ✏️ Desea cambiar el numero de jugadores? ===")
    choice = si_no()
    if choice:
        console.print(Panel(f"\n✏️   [yellow]Cantidad de jugadores[/yellow]"))
        print("El juego permite hasta 4 jugadores. Cuantos van a jugar?")
        cant_jugadores = IntPrompt.ask("\n[bold green]Elegí una opción[/bold green]", choices=["1", "2", "3", "4"])
        actualizar_jugadores(cant_jugadores)
        #print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "="*40)
        console.print(Panel("[bold magenta]¡Listo! Los jugadores han sido actualizados.[/bold magenta]"))
        input("\nPresiona Enter para volver al menu principal...")
        limpiar()
        return
    else:
        limpiar()
        return

"""
personalizar_nombres_jugadores()

• Repasa los nombres de los jugadores y permite cambiarlos.
• No permite cambiar los nombres de los bots.
• No permite nombres repetidos.

"""
def personalizar_nombres_jugadores():
    from juego import JUGADORES
    limpiar()
    #print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "="*40)
    #print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "=== ✏️ Personalizacion de nombres ===")
    nombres_utilizados = set(j["nombre"] for j in JUGADORES.values())

    for clave, datos in JUGADORES.items():
        nombre_actual = datos["nombre"]

        if nombre_actual.lower().startswith("bot"):
            continue  # No se permite renombrar bots

        console.print(Panel(f"\n[yellow]Jugador en posición {clave} {datos['icono']}:[/yellow] {nombre_actual}", title="Cambiar nombre: "))
        #print(f"\nJugador en posición {clave}: {nombre_actual} {datos['icono']}")
        nuevo_nombre = input("¿Querés cambiar este nombre? (dejar vacío para mantenerlo): ").strip()

        if nuevo_nombre:
            nuevo_nombre = nuevo_nombre.capitalize()

            while nuevo_nombre in nombres_utilizados:
                print("⚠️ Ya hay un jugador con ese nombre.")
                nuevo_nombre = input("Elegí otro nombre: ").strip().capitalize()

            JUGADORES[clave]["nombre"] = nuevo_nombre
            nombres_utilizados.add(nuevo_nombre)
            print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "=== Nombre actualizado ===")

    console.print(Panel("[bold magenta]¡Listo![/bold magenta]"))
    input("\nPresiona Enter para volver al menu principal...")
    limpiar()