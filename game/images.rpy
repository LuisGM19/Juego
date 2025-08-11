# images.rpy - Sistema unificado de definición de imágenes
# Version 2.0 - Combina imagintro.rpy e imgnav.rpy con mejor organización

################################################################################
## Configuración general de imágenes
################################################################################

# Colores sólidos y overlays
image black = Solid("#000000")
image white = Solid("#ffffff")
image gray_overlay = Solid("#00000088")  # Semi-transparente para overlays

# Transiciones personalizadas con imágenes
image fade_to_black = Solid("#000000")
image fade_to_white = Solid("#ffffff")

################################################################################
## Imágenes de la introducción
################################################################################

# Grupo 1: Despertar inicial
image intro1 = "images/intro/intro-1.webp"
image intro2 = "images/intro/intro-2.webp"
image intro3 = "images/intro/intro-3.webp"

# Grupo 2: Exploración de la tienda
image intro4 = "images/intro/intro-4.webp"
image intro5 = "images/intro/intro-5.webp"
image intro6 = "images/intro/intro-6.webp"

# Grupo 3: Diálogo con el vendedor
image intro7 = "images/intro/intro-7.webp"
image intro8 = "images/intro/intro-8.webp"
image intro9 = "images/intro/intro-9.webp"
image intro10 = "images/intro/intro-10.webp"

# Grupo 4: Búsqueda del objeto
image intro11 = "images/intro/intro-11.webp"
image intro12 = "images/intro/intro-12.webp"
image intro13 = "images/intro/intro-13.webp"
image intro14 = "images/intro/intro-14.webp"

# Grupo 5: Despertar y transformación
image intro15 = "images/intro/intro-15.webp"
image intro16 = "images/intro/intro-16.webp"
image intro17 = "images/intro/intro-17.webp"
image intro18 = "images/intro/intro-18.webp"

# Grupo 6: Reacción a la transformación
image intro19 = "images/intro/intro-19.webp"
image intro20 = "images/intro/intro-20.webp"
image intro21 = "images/intro/intro-21.webp"
image intro22 = "images/intro/intro-22.webp"

################################################################################
## Imágenes de ubicaciones - Casa
################################################################################

# Habitación del jugador (diferentes momentos del día)
image location_your_bedroom = ConditionSwitch(
    "current_time_period == 'noche'", "images/locations/habitacion_noche.webp",
    "current_time_period == 'tarde'", "images/locations/habitacion_tarde.webp",
    "True", "images/locations/habitacion_dia.webp"
)

# Cocina
image location_kitchen = ConditionSwitch(
    "current_time_period == 'noche'", "images/locations/cocina_noche.webp",
    "current_time_period == 'tarde'", "images/locations/cocina_tarde.webp",
    "True", "images/locations/cocina_dia.webp"
)

# Sala de estar
image location_living_room = ConditionSwitch(
    "current_time_period == 'noche'", "images/locations/sala_noche.webp",
    "current_time_period == 'tarde'", "images/locations/sala_tarde.webp",
    "True", "images/locations/sala_dia.webp"
)

# Baño
image location_bathroom = ConditionSwitch(
    "current_time_period == 'noche'", "images/locations/baño_noche.webp",
    "current_time_period == 'tarde'", "images/locations/baño_tarde.webp",
    "True", "images/locations/baño_dia.webp"
)

################################################################################
## Imágenes de ubicaciones - Escuela
################################################################################

# Pasillo de la escuela
image location_pasillo_escuela = ConditionSwitch(
    "current_time_period == 'noche'", "images/locations/pasillo_escuela_noche.webp",
    "current_time_period == 'tarde'", "images/locations/pasillo_escuela_tarde.webp",
    "True", "images/locations/pasillo_escuela_dia.webp"
)

# Salón de clases
image location_salon_clases = ConditionSwitch(
    "current_time_period == 'noche'", "images/locations/salon_clases_noche.webp",
    "current_time_period == 'tarde'", "images/locations/salon_clases_tarde.webp",
    "True", "images/locations/salon_clases_dia.webp"
)

# Entrada de la escuela
image location_entrada_escuela = ConditionSwitch(
    "current_time_period == 'noche'", "images/locations/entrada_escuela_noche.webp",
    "current_time_period == 'tarde'", "images/locations/entrada_escuela_tarde.webp",
    "True", "images/locations/entrada_escuela_dia.webp"
)

################################################################################
## Imágenes de ubicaciones - Ciudad
################################################################################

# Centro comercial
image location_centro_comercial = ConditionSwitch(
    "current_time_period == 'noche'", "images/locations/centro_comercial_noche.webp",
    "current_time_period == 'tarde'", "images/locations/centro_comercial_tarde.webp",
    "True", "images/locations/centro_comercial_dia.webp"
)

# Tienda
image location_tienda = ConditionSwitch(
    "current_time_period == 'noche'", "images/locations/tienda_noche.webp",
    "current_time_period == 'tarde'", "images/locations/tienda_tarde.webp",
    "True", "images/locations/tienda_dia.webp"
)

################################################################################
## Imágenes de personajes (placeholder para futuro)
################################################################################

# Aquí se definirán sprites de personajes cuando se agreguen
# image vendor normal = "images/characters/vendor_normal.webp"
# image vendor happy = "images/characters/vendor_happy.webp"
# image vendor mysterious = "images/characters/vendor_mysterious.webp"

################################################################################
## Imágenes de UI y elementos de interfaz
################################################################################

# Iconos para el sistema de navegación
image icon_map = Text("🗺️", size=30)
image icon_time_morning = Text("☀️", size=24)
image icon_time_afternoon = Text("🌅", size=24)
image icon_time_night = Text("🌙", size=24)

# Fondos para menús y overlays
image menu_background = "gui/main_menu.png"
image game_menu_background = "gui/game_menu.png"

################################################################################
## Sistema de carga dinámica de imágenes
################################################################################

init python:
    
    def get_location_image(location, time_period=None):
        """
        Obtiene la imagen correcta para una ubicación según el momento del día
        """
        if time_period is None:
            time_period = store.current_time_period
        
        # Mapeo de ubicaciones a archivos de imagen
        location_map = {
            "tu_habitacion": "habitacion",
            "cocina": "cocina",
            "sala": "sala",
            "baño": "baño",
            "pasillo_escuela": "pasillo_escuela",
            "salon_clases": "salon_clases",
            "entrada_escuela": "entrada_escuela",
            "centro_comercial": "centro_comercial",
            "tienda": "tienda"
        }
        
        if location in location_map:
            base_name = location_map[location]
            image_path = f"images/locations/{base_name}_{time_period}.webp"
            
            # Verificar si existe la imagen para ese momento del día
            if renpy.loadable(image_path):
                return image_path
            else:
                # Fallback a imagen de día si no existe la variante
                return f"images/locations/{base_name}_dia.webp"
        
        return None
    
    def preload_location_images():
        """
        Pre-carga imágenes de ubicaciones para mejorar rendimiento
        """
        locations = ["habitacion", "cocina", "sala", "baño", 
                    "pasillo_escuela", "salon_clases", "entrada_escuela",
                    "centro_comercial", "tienda"]
        times = ["dia", "tarde", "noche"]
        
        for loc in locations:
            for time in times:
                path = f"images/locations/{loc}_{time}.webp"
                if renpy.loadable(path):
                    renpy.image(f"preload_{loc}_{time}", path)
    
    # Pre-cargar imágenes al iniciar
    # config.start_callbacks.append(preload_location_images)

################################################################################
## Efectos visuales y animaciones
################################################################################

# Efecto de parpadeo para transiciones
transform blink_effect:
    alpha 1.0
    linear 0.1 alpha 0.0
    linear 0.1 alpha 1.0

# Efecto de zoom suave
transform slow_zoom:
    zoom 1.0
    linear 3.0 zoom 1.1

# Efecto de movimiento lateral suave
transform slow_pan:
    xalign 0.0
    linear 10.0 xalign 1.0
    linear 10.0 xalign 0.0
    repeat

# Efecto de aparición gradual
transform fade_in:
    alpha 0.0
    linear 1.0 alpha 1.0

# Efecto de desvanecimiento
transform fade_out:
    alpha 1.0
    linear 1.0 alpha 0.0