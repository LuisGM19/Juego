# characters.rpy - Sistema de personajes mejorado
# Version 2.0 - Organización optimizada con configuración centralizada

################################################################################
## Configuración de colores y estilos
################################################################################

# Paleta de colores para personajes
define COLOR_PLAYER = "#4a90e2"        # Azul para jugador masculino
define COLOR_PLAYER_F = "#ff6b9d"      # Rosa para jugador femenino
define COLOR_THOUGHTS = "#89bfcc"      # Azul claro para pensamientos
define COLOR_VENDOR = "#ccc289"        # Dorado para vendedor
define COLOR_NARRATOR = "#ffffff"      # Blanco para narrador
define COLOR_NPC = "#a8a8a8"          # Gris para NPCs genéricos

# Configuración de estilos de texto
define TEXT_SIZE_NORMAL = 33
define TEXT_SIZE_THOUGHTS = 30
define TEXT_SIZE_SHOUT = 36

################################################################################
## Personajes principales
################################################################################

# Narrador
define narrator = Character(
    None,
    what_color=COLOR_NARRATOR,
    what_size=TEXT_SIZE_NORMAL,
    what_outlines=[(1, "#000000", 0, 0)]  # Borde negro para mejor legibilidad
)

# Jugador (versión masculina)
define player = DynamicCharacter(
    "player_name",
    color=COLOR_PLAYER,
    what_size=TEXT_SIZE_NORMAL,
    who_outlines=[(1, "#000000", 0, 0)],
    what_outlines=[(1, "#000000", 0, 0)]
)

# Jugador (versión femenina)
define player_mujer = DynamicCharacter(
    "playerf_name",
    color=COLOR_PLAYER_F,
    what_size=TEXT_SIZE_NORMAL,
    who_outlines=[(1, "#000000", 0, 0)],
    what_outlines=[(1, "#000000", 0, 0)]
)

# Pensamientos del jugador (dinámico según género)
define Pensamientosmc = DynamicCharacter(
    "thoughts_name",
    color=COLOR_THOUGHTS,
    what_size=TEXT_SIZE_THOUGHTS,
    what_italic=True,  # Cursiva para pensamientos
    who_outlines=[(1, "#000000", 0, 0)],
    what_outlines=[(1, "#000000", 0, 0)]
)

################################################################################
## Personajes secundarios
################################################################################

# Vendedor misterioso
define Vendedor = Character(
    "Vendedor",
    color=COLOR_VENDOR,
    what_size=TEXT_SIZE_NORMAL,
    who_outlines=[(1, "#000000", 0, 0)],
    what_outlines=[(1, "#000000", 0, 0)]
)

# Plantillas para NPCs futuros
define npc_generic = Character(
    "???",
    color=COLOR_NPC,
    what_size=TEXT_SIZE_NORMAL
)

################################################################################
## Variables del sistema de personajes
################################################################################

# Nombres del jugador
default player_name = ""
default playerf_name = ""
default thoughts_name = "Pensamientos"  # Se actualiza dinámicamente

# Estado del jugador
default player_gender = "male"  # "male" o "female"
default player_transformed = False

# Flags de progreso
default intro_completed = False  # Flag principal de introducción completada
default tutorial_completed = False

# Estadísticas del jugador (para futuro sistema de stats)
default player_stats = {
    "fuerza": 5,
    "inteligencia": 5,
    "carisma": 5,
    "resistencia": 5
}

# Inventario básico (para futuro sistema de inventario)
default player_inventory = []
default player_money = 100

################################################################################
## Funciones auxiliares para personajes
################################################################################

init python:
    
    def update_player_name(new_name):
        """
        Actualiza el nombre del jugador y los nombres relacionados
        """
        global player_name, playerf_name, thoughts_name
        
        if new_name:
            player_name = new_name
            # Por defecto, usar el mismo nombre para versión femenina
            if not playerf_name:
                playerf_name = new_name
            
            # Actualizar nombre de pensamientos
            update_thoughts_name()
    
    def update_thoughts_name():
        """
        Actualiza el nombre mostrado para los pensamientos según el género
        """
        global thoughts_name, player_gender, player_name, playerf_name
        
        if player_gender == "female":
            thoughts_name = f"Pensamientos de {playerf_name}"
        else:
            thoughts_name = f"Pensamientos de {player_name}"
    
    def switch_player_gender(new_gender="female"):
        """
        Cambia el género del jugador y actualiza variables relacionadas
        """
        global player_gender, player_transformed
        
        player_gender = new_gender
        player_transformed = (new_gender == "female")
        update_thoughts_name()
        
        # Aquí podrías agregar cambios en stats u otros efectos
        if player_transformed:
            # Ejemplo: modificar stats tras transformación
            player_stats["fuerza"] -= 2
            player_stats["carisma"] += 3
    
    def get_current_player_character():
        """
        Retorna el personaje actual según el género
        """
        if player_gender == "female":
            return player_mujer
        return player
    
    def validate_player_name(name):
        """
        Valida y limpia el nombre del jugador
        """
        if not name:
            return "Alex"
        
        # Limpiar espacios y caracteres especiales
        name = name.strip()
        
        # Limitar longitud
        if len(name) > 20:
            name = name[:20]
        
        # Si queda vacío después de limpiar, usar default
        if not name:
            return "Alex"
        
        return name

################################################################################
## Personajes para eventos especiales
################################################################################

# Personaje para gritos o énfasis (usa tamaño de texto mayor)
define player_shout = DynamicCharacter(
    "player_name",
    color=COLOR_PLAYER,
    what_size=TEXT_SIZE_SHOUT,
    what_bold=True,
    who_outlines=[(2, "#000000", 0, 0)],
    what_outlines=[(2, "#000000", 0, 0)]
)

# Personaje para susurros (usa tamaño de texto menor)
define player_whisper = DynamicCharacter(
    "player_name",
    color=COLOR_PLAYER,
    what_size=25,
    what_italic=True,
    what_alpha=0.8
)

################################################################################
## Sistema de relaciones (preparación para futuro)
################################################################################

# Diccionario de relaciones con otros personajes
default character_relationships = {
    "vendedor": 0,  # -100 a 100
    # Agregar más personajes según se introduzcan
}

# Función para modificar relaciones
init python:
    def modify_relationship(character, amount):
        """
        Modifica la relación con un personaje
        """
        global character_relationships
        
        if character in character_relationships:
            old_value = character_relationships[character]
            new_value = max(-100, min(100, old_value + amount))
            character_relationships[character] = new_value
            
            # Mostrar notificación si es un cambio significativo
            if abs(amount) >= 10:
                if amount > 0:
                    renpy.notify(f"Relación con {character.title()} +{amount}")
                else:
                    renpy.notify(f"Relación con {character.title()} {amount}")
    
    def get_relationship_level(character):
        """
        Obtiene el nivel de relación con un personaje
        """
        if character not in character_relationships:
            return "neutral"
        
        value = character_relationships[character]
        
        if value >= 75:
            return "excelente"
        elif value >= 50:
            return "buena"
        elif value >= 25:
            return "amistosa"
        elif value >= -25:
            return "neutral"
        elif value >= -50:
            return "tensa"
        elif value >= -75:
            return "mala"
        else:
            return "hostil"