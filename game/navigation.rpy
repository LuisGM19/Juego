# navigation.rpy - Sistema de navegación con mapa

# Variables para el sistema de navegación (sincronizadas con time_system.rpy)
default current_location = "tu_habitacion"
default current_area = "casa"
# Estas variables se actualizan automáticamente desde time_system.rpy
default current_time = "mañana"
default current_day = "Lunes"

# Definición de ubicaciones disponibles
default locations = {
    "casa": {
        "name": "Tu casa",
        "rooms": {
            "tu_habitacion": {"name": "Tu habitación", "image": "images/locations/habitacion_dia.webp"},
            "cocina": {"name": "Cocina", "image": "images/locations/cocina_dia.webp"},
            "sala": {"name": "Sala", "image": "images/locations/sala_dia.webp"},
            "baño": {"name": "Baño", "image": "images/locations/baño_dia.webp"}
        }
    },
    "escuela": {
        "name": "Escuela",
        "rooms": {
            "pasillo_escuela": {"name": "Pasillo", "image": "images/locations/pasillo_escuela_dia.webp"},
            "salon_clases": {"name": "Salón de clases", "image": "images/locations/salon_clases_dia.webp"},
            "entrada_escuela": {"name": "Entrada de la escuela", "image": "images/locations/entrada_escuela_dia.webp"}
        }
    },
    "ciudad": {
        "name": "Ciudad",
        "rooms": {
            "centro_comercial": {"name": "Centro comercial", "image": "images/locations/centro_comercial_dia.webp"},
            "tienda": {"name": "Tienda", "image": "images/locations/tienda_dia.webp"}
        }
    }
}

# Función para cambiar ubicación
init python:
    def change_location(new_location, new_area=None):
        global current_location, current_area
        
        if new_area:
            current_area = new_area
        
        current_location = new_location
        
        # Aquí puedes agregar lógica adicional como:
        # - Verificar si la ubicación está disponible
        # - Cambiar música según la ubicación
        # - Activar eventos específicos de la ubicación
        
        return True

# Screen del botón de navegación (siempre visible durante el juego)
screen navigation_button():
    
    # Botón de mapa en la esquina superior derecha
    button:
        xalign 1.0
        yalign 0.0
        xsize 60
        ysize 60
        xoffset -20
        yoffset 20
        
        # Imagen del botón (puedes usar un ícono de mapa)
        background "#000000aa"
        hover_background "#000000cc"
        
        text "🗺️" size 30 xalign 0.5 yalign 0.5 color "#ffffff"
        
        action Show("navigation_menu")

# Screen principal de navegación
screen navigation_menu():
    
    modal True
    
    # Fondo semi-transparente
    button:
        xfill True
        yfill True
        background "#000000aa"
        action Hide("navigation_menu")
    
    # Panel principal de navegación
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1200
        ysize 700
        padding (20, 20)
        background "#1a1a1a"
        
        vbox:
            spacing 20
            
            # Información de tiempo en la parte superior (sincronizada con time_system)
            frame:
                xfill True
                ysize 60
                background "#2a2a2a"
                padding (20, 15)
                
                hbox:
                    # Usar variables del sistema de tiempo si están disponibles
                    python:
                        try:
                            display_day = current_day_name if 'current_day_name' in globals() else current_day
                            display_time = current_time_period if 'current_time_period' in globals() else current_time
                        except:
                            display_day = current_day
                            display_time = current_time
                    
                    text "[display_day]" size 24 color "#ffffff"
                    text "[display_time]" size 24 color "#ffffff" xoffset 20
                    
                    # Iconos del juego (placeholder)
                    hbox:
                        xalign 1.0
                        spacing 10
                        button:
                            xsize 40
                            ysize 40
                            background "#333333"
                            text "💝" size 20 xalign 0.5 yalign 0.5
                        button:
                            xsize 40
                            ysize 40
                            background "#333333"
                            text "🎒" size 20 xalign 0.5 yalign 0.5
            
            # Pestañas de áreas principales
            hbox:
                spacing 5
                xfill True
                
                for area_id, area_data in locations.items():
                    $ tab_color = "#4a90e2" if current_area == area_id else "#666666"
                    $ text_color = "#ffffff" if current_area == area_id else "#cccccc"
                    
                    button:
                        xsize 200
                        ysize 40
                        background tab_color
                        hover_background "#5ba0f2"
                        
                        text area_data["name"] size 18 xalign 0.5 yalign 0.5 color text_color
                        
                        action [
                            SetVariable("current_area", area_id),
                            Function(renpy.restart_interaction)
                        ]
            
            # Grid de habitaciones/ubicaciones
            frame:
                xfill True
                yfill True
                background "#2a2a2a"
                padding (15, 15)
                
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    
                    vbox:
                        spacing 10
                        
                        # Mostrar habitaciones del área actual
                        $ current_rooms = locations[current_area]["rooms"]
                        $ room_list = list(current_rooms.items())
                        
                        for i in range(0, len(room_list), 3):
                            hbox:
                                spacing 15
                                
                                for j in range(3):
                                    if i + j < len(room_list):
                                        $ room_id, room_data = room_list[i + j]
                                        $ is_current = (room_id == current_location and current_area == current_area)
                                        
                                        button:
                                            xsize 360
                                            ysize 240
                                            
                                            # Marco dorado si es la ubicación actual
                                            if is_current:
                                                background "#ffd700"
                                                padding (3, 3)
                                            else:
                                                background "#666666"
                                                hover_background "#888888"
                                                padding (3, 3)
                                            
                                            action [
                                                Function(change_location, room_id, current_area),
                                                Hide("navigation_menu"),
                                                Jump("location_" + room_id)
                                            ]
                                            
                                            vbox:
                                                spacing 0
                                                
                                                # Imagen de la habitación
                                                frame:
                                                    xsize 354
                                                    ysize 200
                                                    padding (0, 0)
                                                    
                                                    # Imagen con ajuste automático de aspecto
                                                    if renpy.loadable(room_data["image"]):
                                                        add room_data["image"]:
                                                            xsize 354
                                                            ysize 200
                                                            fit "cover"
                                                    else:
                                                        add "#333333"
                                                        text "Sin\nImagen" size 16 xalign 0.5 yalign 0.5 color "#ffffff"
                                                
                                                # Nombre de la habitación
                                                frame:
                                                    xsize 354
                                                    ysize 40
                                                    background "#1a1a1a"
                                                    padding (5, 5)
                                                    
                                                    text room_data["name"] size 16 xalign 0.5 yalign 0.5 color "#ffffff"
                                    else:
                                        # Espacio vacío para mantener la estructura
                                        frame:
                                            xsize 360
                                            ysize 240
                                            background None
            
            # Botón de cerrar
            hbox:
                xalign 1.0
                button:
                    xsize 100
                    ysize 40
                    background "#666666"
                    hover_background "#888888"
                    
                    text "Cerrar" size 16 xalign 0.5 yalign 0.5 color "#ffffff"
                    
                    action Hide("navigation_menu")

# Labels para cada ubicación (placeholders)
label location_tu_habitacion:
    scene location_your_bedroom
    narrator "Estás en tu habitación."
    call screen room_actions("tu_habitacion")
    return

label location_cocina:
    scene location_kitchen
    narrator "Estás en la cocina."
    call screen room_actions("cocina")
    return

label location_sala:
    scene location_living_room
    narrator "Estás en la sala."
    call screen room_actions("sala")
    return

label location_baño:
    # scene location_bathroom
    scene black
    narrator "Estás en el baño."
    call screen room_actions("baño")
    return

label location_pasillo_escuela:
    # scene location_pasillo_escuela
    scene black
    narrator "Estás en el pasillo de la escuela."
    call screen room_actions("pasillo_escuela")
    return

label location_salon_clases:
    # scene location_salon_clases
    scene black
    narrator "Estás en el salón de clases."
    call screen room_actions("salon_clases")
    return

label location_entrada_escuela:
    # scene location_entrada_escuela
    scene black
    narrator "Estás en la entrada de la escuela."
    call screen room_actions("entrada_escuela")
    return

label location_centro_comercial:
    # scene location_centro_comercial
    scene black
    narrator "Estás en el centro comercial."
    call screen room_actions("centro_comercial")
    return

label location_tienda:
    # scene location_tienda
    scene black
    narrator "Estás en la tienda."
    call screen room_actions("tienda")
    return

# Screen para acciones en cada habitación (panel eliminado)
screen room_actions(room_id):
    
    # Mostrar botón de navegación
    use navigation_button
    
    # Mostrar sistema de tiempo
    use time_system
    
    # Panel de acciones eliminado por petición del usuario
    # Solo mantener botones de navegación y tiempo