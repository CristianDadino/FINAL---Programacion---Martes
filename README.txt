# 🎮 Nubecillas de Calderilla

Un juego de consola por turnos donde jugadores intentan recolectar monedas sin chocar entre ellos.
(Lo base en el juego "Nubecillas de Calderilla" de Mario Party Jamboree)

📦 Estructura:

- `main.py` → menú principal y flujo general
- `juego.py` → lógica del juego
- `grilla.py` → funciones para mostrar tablero
- `archivo.py` → manejo de highscores en JSON
- `auxiliar.py` → validaciones y utilidades
- `juego.log` → archivo de log con eventos
- `highscore.json` → puntuaciones históricas

📦 Requisitos:
 • Python 3.10+

📦 Dependencias: 
 • rich
 • colorama

🔒 Highscore:
Se guarda automáticamente en highscore.json. Solo los jugadores humanos se registran.


🔧 Entorno virtual
### Crear y activar entorno (recomendado):

python -m venv venv
venv\Scripts\activate     # En Windows
source venv/bin/activate  # En Linux/mac
