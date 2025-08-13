# time_system.rpy - Sistema de tiempo simplificado y corregido
# Version 2.2 - Con actualización automática de imágenes

################################################################################
## Variables del sistema de tiempo
################################################################################

# Tiempo actual
default current_day_number = 1
default current_day_name = "Lunes"
default current_time_period = "mañana"

# Variables adicionales para compatibilidad
default current_time = "mañana"  # Duplicado para compatibilidad
default current_day = "Lunes"    # Duplicado para compatibilidad

# Configuración del calendario
default days_of_week = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
default time_periods = ["mañana", "tarde", "noche"]

# Estadísticas de tiempo
default total_days_played = 1
default time_advanced_count = 0

# Configuración de restricciones temporales
default time_restrictions = {
    "escuela": {
        "available_days": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
        "available_periods": ["mañana", "tarde"]
    },
    "tienda": {
        "available_days": "all",
        "available_periods": ["mañana", "tarde"]
    }
}

################################################################################
## Funciones principales del sistema de tiempo
################################################################################

init python:
    
    def advance_time(periods=1, show_notification=False):
        """
        Avanza el tiempo por el número de períodos especificado
        """
        global current_time_period, current_day_number, current_day_name
        global time_advanced_count, total_days_played
        global current_time, current_day
        
        for i in range(periods):
            # Obtener índice actual
            current_period_index = time_periods.index(current_time_period)
            
            # Si es noche, avanzar al siguiente día
            if current_period_index == 2:  # noche
                advance_day()
            else:
                # Avanzar al siguiente período
                current_time_period = time_periods[current_period_index + 1]
                current_time = current_time_period  # Actualizar duplicado
                time_advanced_count += 1
        
        # Actualizar variables de navegación
        update_navigation_time()
        
        # Mostrar notificación si se solicita
        if show_notification:
            show_time_notification()
        
        # IMPORTANTE: Actualizar la imagen de la ubicación actual
        refresh_current_location()
        
        return True
    
    def advance_day():
        """
        Avanza al siguiente día
        """
        global current_day_number, current_day_name, current_time_period
        global total_days_played, current_time, current_day
        
        # Avanzar día
        current_day_number += 1
        total_days_played += 1
        
        # Calcular día de la semana
        day_index = (current_day_number - 1) % 7
        current_day_name = days_of_week[day_index]
        current_day = current_day_name  # Actualizar duplicado
        
        # Resetear al período de mañana
        current_time_period = "mañana"
        current_time = "mañana"  # Actualizar duplicado
    
    def set_time(day=None, period=None):
        """
        Establece el tiempo a un día y período específico
        """
        global current_day_number, current_day_name, current_time_period
        global current_time, current_day
        
        if day is not None:
            current_day_number = day
            day_index = (day - 1) % 7
            current_day_name = days_of_week[day_index]
            current_day = current_day_name  # Actualizar duplicado
        
        if period is not None and period in time_periods:
            current_time_period = period
            current_time = period  # Actualizar duplicado
        
        update_navigation_time()
        refresh_current_location()
    
    def refresh_current_location():
        """
        Actualiza la imagen de la ubicación actual según el nuevo tiempo
        """
        if hasattr(store, 'current_location'):
            # Saltar al label de la ubicación actual para refrescar la imagen
            renpy.jump(f"location_{store.current_location}")
    
    def get_time_display():
        """
        Obtiene el texto formateado del tiempo actual
        """
        return f"Día {current_day_number} - {current_day_name}, {current_time_period}"
    
    def get_time_icon():
        """
        Obtiene el ícono apropiado para el período actual
        """
        icons = {
            "mañana": "☀️",
            "tarde": "🌅", 
            "noche": "🌙"
        }
        return icons.get(current_time_period, "⏰")
    
    def get_time_color():
        """
        Obtiene el color asociado al período actual
        """
        colors = {
            "mañana": "#FFD700",  # Dorado brillante
            "tarde": "#FF6B35",   # Naranja atardecer
            "noche": "#6B5B95"    # Púrpura noche
        }
        return colors.get(current_time_period, "#FFFFFF")
    
    def get_time_background():
        """
        Obtiene el color de fondo para el botón según el período
        """
        backgrounds = {
            "mañana": "#87CEEB",  # Azul cielo
            "tarde": "#FFA500",    # Naranja
            "noche": "#191970"     # Azul medianoche
        }
        return backgrounds.get(current_time_period, "#34495e")

################################################################################
## Funciones de utilidad
################################################################################

init python:
    
    def is_weekend():
        """
        Verifica si es fin de semana
        """
        return current_day_name in ["Sábado", "Domingo"]
    
    def is_school_day():
        """
        Verifica si es día de escuela
        """
        return current_day_name in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    
    def is_night():
        """
        Verifica si es de noche
        """
        return current_time_period == "noche"
    
    def is_morning():
        """
        Verifica si es de mañana
        """
        return current_time_period == "mañana"
    
    def get_days_until(target_day):
        """
        Calcula días hasta un día específico de la semana
        """
        current_index = days_of_week.index(current_day_name)
        target_index = days_of_week.index(target_day)
        
        if target_index >= current_index:
            return target_index - current_index
        else:
            return 7 - current_index + target_index
    
    def skip_to_next_day():
        """
        Salta directamente al siguiente día
        """
        set_time(current_day_number + 1, "mañana")
        renpy.notify("Has dormido hasta el siguiente día")
    
    def update_navigation_time():
        """
        Actualiza las variables de tiempo en el sistema de navegación
        """
        store.current_time = current_time_period
        store.current_day = current_day_name
    
    def show_time_notification():
        """
        Muestra una notificación del cambio de tiempo
        """
        if current_time_period == "mañana":
            if current_day_number > 1:
                message = f"¡Nuevo día! {current_day_name} - Mañana"
            else:
                message = f"{current_day_name} - Mañana"
        elif current_time_period == "tarde":
            message = f"{current_day_name} - Tarde"
        else:  # noche
            message = f"{current_day_name} - Noche"
        
        renpy.show_screen("time_notification", message=message, duration=2.5)

################################################################################
## Screens del sistema de tiempo
################################################################################

screen time_system():
    # Screen principal que combina el botón y la información de tiempo
    
    # Botón de tiempo
    use time_button
    
    # Información adicional (oculta por defecto)
    if getattr(store, 'show_time_details', False):
        use time_details

screen time_button():
    # Botón compacto de tiempo con función de avance
    
    $ bg_color = get_time_background() + "cc"  # Añadir transparencia
    $ bg_hover = get_time_background() + "ff"  # Opaco al hover
    
    # Calcular el texto del tooltip
    if current_time_period == "mañana":
        $ tooltip_text = "Clic para avanzar a tarde"
    elif current_time_period == "tarde":
        $ tooltip_text = "Clic para avanzar a noche"
    else:
        $ tooltip_text = "Clic para avanzar a mañana (siguiente día)"
    
    button:
        xalign 0.0
        yalign 0.0
        xsize 200
        ysize 80
        xoffset 20
        yoffset 20
        
        background bg_color
        hover_background bg_hover
        padding (10, 5)
        
        # Acción mejorada que actualiza la ubicación
        action [
            Function(advance_time, 1, True),
            If(hasattr(store, 'current_location'), 
                Jump(f"location_{store.current_location}"))
        ]
        tooltip tooltip_text
        
        hbox:
            spacing 10
            xalign 0.5
            yalign 0.5
            
            # Ícono del período
            text get_time_icon() size 36
            
            # Información de tiempo
            vbox:
                spacing 2
                yalign 0.5
                text "[current_day_name]" size 18 color "#ffffff" bold True outlines [(2, "#000000", 0, 0)]
                text "[current_time_period]" size 16 color "#ffffff" bold True outlines [(2, "#000000", 0, 0)]
                text "Día [current_day_number]" size 14 color "#ffffff" outlines [(1, "#000000", 0, 0)]

screen time_details():
    # Panel detallado de información temporal
    
    frame:
        xalign 0.0
        yalign 0.0
        xoffset 210
        yoffset 20
        xsize 250
        ysize 150
        
        background "#2c3e50"
        padding (15, 15)
        
        vbox:
            spacing 8
            
            text "Información Temporal" size 18 color "#ffffff" bold True
            
            null height 5
            
            hbox:
                text "Día total: " size 14 color "#aaaaaa"
                text "[total_days_played]" size 14 color "#ffffff"
            
            hbox:
                text "Período: " size 14 color "#aaaaaa"
                text "[current_time_period]" size 14 color get_time_color()
            
            if is_weekend():
                text "¡Fin de semana!" size 14 color "#00ff00"
            elif is_school_day():
                text "Día de escuela" size 14 color "#ffff00"
            
            null height 5
            
            textbutton "Cerrar":
                action SetVariable("show_time_details", False)
                text_size 12

screen time_notification(message, duration=2.5):
    # Notificación temporal de cambio de tiempo
    
    $ notification_bg = get_time_background() + "ee"  # Color del período con transparencia
    
    frame:
        xalign 0.5
        yalign 0.1
        padding (30, 20)
        
        background notification_bg
        
        hbox:
            spacing 15
            
            text get_time_icon() size 32
            text message size 22 color "#ffffff" bold True outlines [(2, "#000000", 0, 0)]
    
    timer duration action Hide("time_notification")

screen time_skip_menu():
    # Menú para saltar tiempo rápidamente
    
    modal True
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 400
        ysize 300
        
        background "#2c3e50"
        padding (20, 20)
        
        vbox:
            spacing 15
            xfill True
            
            text "Saltar Tiempo" size 24 xalign 0.5 color "#ffffff" bold True
            
            null height 10
            
            textbutton "Siguiente período":
                action [
                    Function(advance_time, 1, True),
                    Hide("time_skip_menu")
                ]
                xfill True
            
            textbutton "Siguiente día":
                action [
                    Function(skip_to_next_day),
                    Hide("time_skip_menu")
                ]
                xfill True
            
            textbutton "Saltar a la noche":
                action [
                    Function(set_time, None, "noche"),
                    Hide("time_skip_menu")
                ]
                xfill True
            
            null height 10
            
            textbutton "Cancelar":
                action Hide("time_skip_menu")
                xfill True
                text_color "#ff6666"

################################################################################
## Sistema de restricciones temporales
################################################################################

init python:
    
    def is_location_available_by_time(location_id, area_id=None):
        """
        Verifica si una ubicación está disponible según el tiempo actual
        """
        if area_id in time_restrictions:
            restrictions = time_restrictions[area_id]
            
            # Verificar días
            if "available_days" in restrictions:
                if restrictions["available_days"] != "all":
                    if current_day_name not in restrictions["available_days"]:
                        return False
            
            # Verificar períodos
            if "available_periods" in restrictions:
                if current_time_period not in restrictions["available_periods"]:
                    return False
        
        return True
    
    def get_time_until_available(area_id):
        """
        Calcula cuánto tiempo hasta que una ubicación esté disponible
        """
        if area_id not in time_restrictions:
            return 0
        
        restrictions = time_restrictions[area_id]
        
        # Si no está disponible por día
        if "available_days" in restrictions and restrictions["available_days"] != "all":
            if current_day_name not in restrictions["available_days"]:
                # Buscar el próximo día disponible
                for i in range(1, 8):
                    future_day_index = (days_of_week.index(current_day_name) + i) % 7
                    future_day = days_of_week[future_day_index]
                    if future_day in restrictions["available_days"]:
                        return i
        
        # Si no está disponible por período
        if "available_periods" in restrictions:
            if current_time_period not in restrictions["available_periods"]:
                current_index = time_periods.index(current_time_period)
                for i in range(1, len(time_periods)):
                    future_period_index = (current_index + i) % len(time_periods)
                    if time_periods[future_period_index] in restrictions["available_periods"]:
                        return i
        
        return 0