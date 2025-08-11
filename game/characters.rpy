# characters.rpy - Definiciones de personajes para la introducción

# Definición de personajes principales
define narrator = Character(None, 
    what_color="#ffffff",)

define player = Character("[player_name]", 
    color="#4a90e2",)

define Pensamientosmc = Character("Pensamientos de [player_name]", 
    color="#89bfcc",)

define Vendedor = Character("Vendedor", 
    color="#ccc289",)

define player_mujer = Character("[playerf_name]", 
    color="#ff6b9d",)

# Variables básicas del juego
default player_name = ""

# Flags simples para la introducción
default intro_completed = False