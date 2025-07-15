"""
main.py

• Principalmente se encarga de llamar a las funciones de otros modulos. 
• Tambien se encarga de iniciar y cerrar el log.

"""
#Modulos
from juego import run #La funcion run es la que inicia el juego.
from auxiliar import menu_principal,mostrar_jugadores,personalizar_nombres_jugadores 
from archivo import mostrar_highscores 
from how_to_play import mostrar_manual_juego
#Estetica
from colorama import Fore, Style #Para agregar un detalle visual.
#Log
import logging
from datetime import datetime #Para hora de inicio del programa.

#Configuracion del log 
logging.basicConfig(
    filename="juego.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

#Me genera el registro para el modulo actual.
logger = logging.getLogger(__name__) 

#Fecha+Horario para el .log
HOY = datetime.now() 

#Guardo en el .log hora/dia de inicio del programa.
logger.info(f"Programa iniciado: {HOY}")

"""
- main()
Funcion principal que se encarga de llamar a las funciones del menu.
Segun la opcion que elija el usuario, se ejecutara una funcion diferente.
"""
def main():
    
    while True:
        
        opcion=menu_principal() #Valida las opciones
        if opcion == 1:
            run() 
        elif opcion == 2:
            mostrar_jugadores()
        elif opcion == 3:
            personalizar_nombres_jugadores()
        elif opcion == 4:
            mostrar_highscores()
        elif opcion == 5:
            mostrar_manual_juego()
        elif opcion == 6:
            #guardar_archivo(tareas, ARCHIVO_TAREAS)
            print(Fore.CYAN + Style.BRIGHT + "¡Hasta luego!")
            HOY = datetime.now() #Fecha+Horario para el log.
            logger.info(f"Programa finalizado: {HOY}")
            break

#Esta funcion de momento no es util porque no llamo a Main desde otro modulo. Pero en caso de hacerlo, evitaria mostrar toda la interfaz desde otro archivo.
if __name__ == "__main__":
    main()
"""
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
"""