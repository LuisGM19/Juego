# navigation.rpy - Sistema de navegación simplificado
# Version 2.1 - Sin menús de acciones por ahora

################################################################################
## Variables del sistema de navegación
################################################################################

# Ubicación actual
default current_location = "tu_habitacion"
default current_area = "casa"
default previous_location = ""
default previous_area = ""

# Área visible en el mapa (puede ser diferente del área actual)
default viewing_area = "casa"

# Flags de disponibilidad de áreas
default areas_unlocked = {
    "casa": True,
    "escuela": True,
    "ciudad": True
}

# Eventos activos por ubicación
default location_events = {}

################################################################################
## Definición de ubicaciones
################################################################################

default locations = {
    "casa": {
        "name": "Tu casa",
        "icon": "🏠",
        "available_times": ["mañana", "tarde", "noche"],
        "rooms": {
            "tu_habitacion": {
                "name": "Tu habitación",
                "image": "images/locations/habitacion_dia.webp",
                "description": "Tu espacio personal",
                "available": True
            },
            "cocina": {
                "name": "Cocina",
                "image": "images/locations/cocina_dia.webp",
                "description": "Donde se preparan los alimentos",
                "available": True
            },
            "sala": {
                "name": "Sala",
                "image": "images/locations/sala_dia.webp",
                "description": "Área común de la casa",
                "available": True
            },
            "baño": {
                "name": "Baño",
                "image": "images/locations/baño_dia.webp",
                "description": "Para tu higiene personal",
                "available": True
            }
        }
    },
    "escuela": {
        "name": "Escuela",
        "icon": "🏫",
        "available_times": ["mañana", "tarde"],
        "rooms": {
            "pasillo_escuela": {
                "name": "Pasillo",
                "image": "images/locations/pasillo_escuela_dia.webp",
                "description": "Pasillo principal de la escuela",
                "available": True
            },
            "salon_clases": {
                "name": "Salón de clases",
                "image": "images/locations/salon_clases_dia.webp",
                "description": "Donde tomas tus clases",
                "available": True
            },
            "entrada_escuela": {
                "name": "Entrada",
                "image": "images/locations/entrada_escuela_dia.webp",
                "description": "Entrada principal de la escuela",
                "available": True
            }
        }
    },
    "ciudad": {
        "name": "Ciudad",
        "icon": "🏙️",
        "available_times": ["mañana", "tarde", "noche"],
        "rooms": {
            "centro_comercial": {
                "name": "Centro comercial",
                "image": "images/locations/centro_comercial_dia.webp",
                "description": "Lugar para comprar y socializar",
                "available": True
            },
            "tienda": {
                "name": "Tienda",
                "image": "images/locations/tienda_dia.webp",
                "description": "Tienda de conveniencia",
                "available": True
            }
        }
    }
}

################################################################################
## Funciones del sistema de navegación
################################################################################

init python:
    
    def change_location(new_location, new_area=None):
        """
        Cambia la ubicación actual del jugador
        """
        global current_location, current_area, previous_location, previous_area
        
        # Guardar ubicación anterior
        previous_location = current_location
        previous_area = current_area
        
        # Cambiar a nueva ubicación
        if new_area:
            current_area = new_area
        current_location = new_location
        
        # Actualizar el tiempo de navegación si es necesario
        update_navigation_time()
        
        # Verificar eventos en la nueva ubicación
        check_location_events(new_location)
        
        return True
    
    def is_location_available(location_id, area_id=None):
        """
        Verifica si una ubicación está disponible
        """
        if area_id is None:
            area_id = current_area
        
        # Verificar si el área está desbloqueada
        if area_id not in areas_unlocked or not areas_unlocked[area_id]:
            return False
        
        # Verificar disponibilidad por tiempo
        if area_id in locations:
            area = locations[area_id]
            if "available_times" in area:
                if current_time_period not in area["available_times"]:
                    return False
            
            # Verificar disponibilidad específica de la habitación
            if location_id in area["rooms"]:
                room = area["rooms"][location_id]
                return room.get("available", True)
        
        return False
    
    def unlock_area(area_id):
        """
        Desbloquea un área para navegación
        """
        global areas_unlocked
        if area_id in areas_unlocked:
            areas_unlocked[area_id] = True
            renpy.notify(f"¡Nueva área desbloqueada: {locations[area_id]['name']}!")
            return True
        return False
    
    def unlock_all_areas():
        """
        Desbloquea todas las áreas (útil para testing)
        """
        global areas_unlocked
        for area in areas_unlocked:
            areas_unlocked[area] = True
        renpy.notify("¡Todas las áreas desbloqueadas!")
    
    def check_location_events(location_id):
        """
        Verifica y ejecuta eventos en una ubicación
        """
        if location_id in location_events:
            for event in location_events[location_id]:
                if event.get("active", False):
                    renpy.call(event["label"])
    
    def get_location_image_path(location_id, area_id=None):
        """
        Obtiene la ruta de imagen correcta según el tiempo
        """
        if area_id is None:
            area_id = current_area
        
        # Mapeo de IDs de ubicación a nombres de archivo
        location_to_filename = {
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
        
        if location_id in location_to_filename:
            base_name = location_to_filename[location_id]
            # Construir la ruta con el período actual
            image_path = f"images/locations/{base_name}_{current_time_period}.webp"
            
            # Si no existe la imagen para ese período, intentar con "_dia"
            if not renpy.loadable(image_path):
                image_path = f"images/locations/{base_name}_dia.webp"
            
            # Si aún no existe, devolver None
            if renpy.loadable(image_path):
                return image_path
        
        return None

################################################################################
## Screen: Botón de navegación
################################################################################

screen navigation_button():
    # Solo mostrar si no estamos en un menú
    if not renpy.get_screen("navigation_menu"):
        
        button:
            xalign 1.0
            yalign 0.0
            xsize 80
            ysize 80
            xoffset -20
            yoffset 20
            
            # Usar un frame sólido en lugar de imágenes que no existen
            background "#2c3e50cc"
            hover_background "#34495eff"
            padding (5, 5)
            
            vbox:
                spacing 2
                xalign 0.5
                yalign 0.5
                text "🗺️" size 40 xalign 0.5
                text "Mapa" size 12 xalign 0.5 color "#ffffff"
            
            action Show("navigation_menu")
            tooltip "Abrir mapa"

################################################################################
## Screen: Menú de navegación principal
################################################################################

screen navigation_menu():
    modal True
    
    # Fondo oscuro
    add "#000000aa"
    
    # Sincronizar área visible con área actual al abrir
    on "show" action SetVariable("viewing_area", current_area)
    
    # Panel principal
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 800
        
        background "#1a1a1add"
        padding (30, 30)
        
        vbox:
            spacing 20
            
            # Encabezado con información
            use navigation_header
            
            # Pestañas de áreas
            use area_tabs
            
            # Grid de ubicaciones
            use location_grid
            
            # Botones de acción
            use navigation_actions

################################################################################
## Sub-screens del menú de navegación
################################################################################

screen navigation_header():
    # Encabezado con información del tiempo y ubicación actual
    
    frame:
        xfill True
        ysize 80
        background "#2c3e50"
        padding (20, 15)
        
        hbox:
            xfill True
            
            # Información de tiempo
            vbox:
                text "Día [current_day_number] - [current_day_name]" size 28 color "#ffffff"
                text "[current_time_period]" size 22 color "#ecf0f1"
            
            # Ubicación actual
            vbox:
                xalign 1.0
                text "Ubicación actual:" size 20 color "#95a5a6"
                $ area_name = locations[current_area]["name"]
                # Verificar si la ubicación actual existe en el área actual
                python:
                    if current_location in locations[current_area]["rooms"]:
                        room_name = locations[current_area]["rooms"][current_location]["name"]
                    else:
                        # Si no existe, usar la primera ubicación del área
                        first_room = list(locations[current_area]["rooms"].keys())[0]
                        room_name = "No definida"
                text "[area_name] - [room_name]" size 24 color "#ffffff"

screen area_tabs():
    # Pestañas para seleccionar áreas
    
    hbox:
        spacing 10
        xfill True
        
        for area_id, area_data in locations.items():
            $ is_viewing = (viewing_area == area_id)
            $ is_unlocked = areas_unlocked.get(area_id, False)
            
            button:
                xsize 250
                ysize 50
                
                if is_unlocked:
                    if is_viewing:
                        background "#3498db"
                    else:
                        background "#34495e"
                        hover_background "#4a5f7a"
                    
                    # Solo cambiar el área que estamos viendo, no la ubicación actual
                    action SetVariable("viewing_area", area_id)
                else:
                    background "#2c3e50"
                    action NullAction()
                
                hbox:
                    spacing 5
                    xalign 0.5
                    yalign 0.5
                    
                    if is_unlocked:
                        text area_data.get("icon", "📍") size 24
                        text area_data["name"] size 20 color "#ffffff"
                    else:
                        text "🔒" size 24
                        text "Bloqueado" size 20 color "#7f8c8d"

screen location_grid():
    # Grid de ubicaciones del área actual
    
    frame:
        xfill True
        yfill True
        background "#2c3e50"
        padding (20, 20)
        
        viewport:
            scrollbars "vertical"
            mousewheel True
            draggable True
            
            grid 3 3:
                spacing 20
                xfill True
                
                $ current_rooms = locations[viewing_area]["rooms"]
                
                for room_id, room_data in current_rooms.items():
                    # Solo marcar como "actual" si estamos en esta área Y ubicación
                    $ is_current = (room_id == current_location and viewing_area == current_area)
                    $ is_available = is_location_available(room_id, viewing_area)
                    
                    use room_button(room_id, room_data, is_current, is_available)
                
                # Rellenar espacios vacíos si es necesario
                for i in range(9 - len(current_rooms)):
                    null

screen room_button(room_id, room_data, is_current, is_available):
    button:
        xsize 420
        ysize 280
        
        if is_current:
            background "#27ae60"
            action NullAction()
        elif is_available:
            background "#34495e"
            hover_background "#4a5f7a"
            action [
                Function(change_location, room_id, viewing_area),
                Hide("navigation_menu"),
                Jump("location_" + room_id)
            ]
        else:
            background "#1a1a1a"
            action NullAction()
        
        vbox:
            spacing 5
            xfill True
            yfill True
            
            frame:
                xsize 400
                ysize 200
                xalign 0.5
                background "#000000"
                
                python:
                    img_path = get_location_image_path(room_id, viewing_area)
                
                if img_path and renpy.loadable(img_path):
                    add img_path:
                        xsize 400
                        ysize 200
                        fit "cover"
                else:
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        text "Sin imagen" size 16 xalign 0.5 color "#666666"
            
            vbox:
                xalign 0.5
                spacing 2
                
                text room_data["name"] size 20 xalign 0.5 color "#ffffff"
                
                if is_current:
                    text "(Estás aquí)" size 14 xalign 0.5 color "#2ecc71"
                elif not is_available:
                    text "(No disponible)" size 14 xalign 0.5 color "#e74c3c"
                else:
                    text room_data.get("description", "") size 14 xalign 0.5 color "#95a5a6"

screen navigation_actions():
    # Botones de acción del menú de navegación
    
    hbox:
        xalign 1.0
        spacing 10
        
        textbutton "Cerrar":
            action Hide("navigation_menu")
            style "navigation_action_button"

style navigation_action_button is button:
    xsize 120
    ysize 40
    background "#e74c3c"
    hover_background "#c0392b"

style navigation_action_button_text is button_text:
    size 18
    color "#ffffff"
    xalign 0.5
    yalign 0.5

################################################################################
## Labels de ubicaciones
################################################################################

label location_tu_habitacion:
    # Actualizar la imagen según el período del día
    python:
        if current_time_period == "noche":
            bg_image = "images/locations/habitacion_noche.webp"
        elif current_time_period == "tarde":
            bg_image = "images/locations/habitacion_tarde.webp"
        else:
            bg_image = "images/locations/habitacion_dia.webp"
    
    scene expression bg_image
    with fade
    
    narrator "Estás en tu habitación."
    
    # Esperar sin menú
    jump navigation_wait

label location_cocina:
    python:
        if current_time_period == "noche":
            bg_image = "images/locations/cocina_noche.webp"
        elif current_time_period == "tarde":
            bg_image = "images/locations/cocina_tarde.webp"
        else:
            bg_image = "images/locations/cocina_dia.webp"
    
    scene expression bg_image
    with fade
    
    narrator "Estás en la cocina."
    jump navigation_wait

label location_sala:
    python:
        if current_time_period == "noche":
            bg_image = "images/locations/sala_noche.webp"
        elif current_time_period == "tarde":
            bg_image = "images/locations/sala_tarde.webp"
        else:
            bg_image = "images/locations/sala_dia.webp"
    
    scene expression bg_image
    with fade
    
    narrator "Estás en la sala."
    jump navigation_wait

label location_baño:
    python:
        if current_time_period == "noche":
            bg_image = "images/locations/baño_noche.webp"
        elif current_time_period == "tarde":
            bg_image = "images/locations/baño_tarde.webp"
        else:
            bg_image = "images/locations/baño_dia.webp"
    
    scene expression bg_image
    with fade
    
    narrator "Estás en el baño."
    jump navigation_wait

label location_pasillo_escuela:
    python:
        if current_time_period == "noche":
            bg_image = "images/locations/pasillo_escuela_noche.webp"
        elif current_time_period == "tarde":
            bg_image = "images/locations/pasillo_escuela_tarde.webp"
        else:
            bg_image = "images/locations/pasillo_escuela_dia.webp"
    
    scene expression bg_image
    with fade
    
    narrator "Estás en el pasillo de la escuela."
    jump navigation_wait

label location_salon_clases:
    python:
        if current_time_period == "noche":
            bg_image = "images/locations/salon_clases_noche.webp"
        elif current_time_period == "tarde":
            bg_image = "images/locations/salon_clases_tarde.webp"
        else:
            bg_image = "images/locations/salon_clases_dia.webp"
    
    scene expression bg_image
    with fade
    
    narrator "Estás en el salón de clases."
    jump navigation_wait

label location_entrada_escuela:
    python:
        if current_time_period == "noche":
            bg_image = "images/locations/entrada_escuela_noche.webp"
        elif current_time_period == "tarde":
            bg_image = "images/locations/entrada_escuela_tarde.webp"
        else:
            bg_image = "images/locations/entrada_escuela_dia.webp"
    
    scene expression bg_image
    with fade
    
    narrator "Estás en la entrada de la escuela."
    jump navigation_wait

label location_centro_comercial:
    python:
        if current_time_period == "noche":
            bg_image = "images/locations/centro_comercial_noche.webp"
        elif current_time_period == "tarde":
            bg_image = "images/locations/centro_comercial_tarde.webp"
        else:
            bg_image = "images/locations/centro_comercial_dia.webp"
    
    scene expression bg_image
    with fade
    
    narrator "Estás en el centro comercial."
    jump navigation_wait

label location_tienda:
    python:
        if current_time_period == "noche":
            bg_image = "images/locations/tienda_noche.webp"
        elif current_time_period == "tarde":
            bg_image = "images/locations/tienda_tarde.webp"
        else:
            bg_image = "images/locations/tienda_dia.webp"
    
    scene expression bg_image
    with fade
    
    narrator "Estás en la tienda."
    jump navigation_wait

# Label de espera genérico
label navigation_wait:
    show screen navigation_button
    show screen time_system
    
    window hide
    $ renpy.pause(hard=True)
    
    jump navigation_wait