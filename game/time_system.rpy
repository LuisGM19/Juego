# time_system.rpy - Sistema de tiempo optimizado
# Version 2.0 - Mejorado con eventos temporales y mejor integración

################################################################################
## Variables del sistema de tiempo
################################################################################

# Tiempo actual
default current_day_number = 1
default current_day_name = "Lunes"
default current_time_period = "mañana"

# Configuración del calendario
default days_of_week = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
default time_periods = ["mañana", "tarde", "noche"]

# Eventos y actividades por tiempo
default time_events = {}
default daily_activities_done = []

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
        global time_advanced_count, total_days_played, daily_activities_done
        
        for i in range(periods):
            # Obtener índice actual
            current_period_index = time_periods.index(current_time_period)
            
            # Si es noche, avanzar al siguiente día
            if current_period_index == 2:  # noche
                advance_day()
            else:
                # Avanzar al siguiente período
                current_time_period = time_periods[current_period_index + 1]
                time_advanced_count += 1
        
        # Actualizar variables de navegación
        update_navigation_time()
        
        # Verificar eventos temporales
        check_time_events()
        
        # Mostrar notificación si se solicita
        if show_notification:
            show_time_notification()
        
        return True
    
    def advance_day():
        """
        Avanza al siguiente día
        """
        global current_day_number, current_day_name, current_time_period
        global total_days_played, daily_activities_done
        
        # Avanzar día
        current_day_number += 1
        total_days_played += 1
        
        # Calcular día de la semana
        day_index = (current_day_number - 1) % 7
        current_day_name = days_of_week[day_index]
        
        # Resetear al período de mañana
        current_time_period = "mañana"
        
        # Limpiar actividades diarias
        daily_activities_done = []
        
        # Ejecutar eventos de nuevo día
        execute_new_day_events()
        
        # Verificar fechas especiales
        check_special_dates()
    
    def set_time(day=None, period=None):
        """
        Establece el tiempo a un día y período específico
        """
        global current_day_number, current_day_name, current_time_period
        
        if day is not None:
            current_day_number = day
            day_index = (day - 1) % 7
            current_day_name = days_of_week[day_index]
        
        if period is not None and period in time_periods:
            current_time_period = period
        
        update_navigation_time()
    
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
## Sistema de eventos temporales
################################################################################

init python:
    
    def check_time_events():
        """
        Verifica y ejecuta eventos basados en el tiempo actual
        """
        global time_events
        
        # Crear clave para el tiempo actual
        time_key = f"{current_day_name}_{current_time_period}"
        
        # Verificar eventos específicos del tiempo
        if time_key in time_events:
            for event in time_events[time_key]:
                if should_trigger_event(event):
                    renpy.call(event["label"])
        
        # Verificar eventos diarios
        check_daily_events()
    
    def should_trigger_event(event):
        """
        Determina si un evento debe ejecutarse
        """
        # Verificar condiciones del evento
        if "condition" in event:
            return eval(event["condition"])
        
        # Verificar si es único y ya se ejecutó
        if event.get("once", False):
            if event["id"] in store.completed_events:
                return False
        
        return True
    
    def check_daily_events():
        """
        Verifica eventos que ocurren todos los días a cierta hora
        """
        # Ejemplo: recordatorio de clases en días de semana
        if current_day_name in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]:
            if current_time_period == "mañana" and "clase_reminder" not in daily_activities_done:
                daily_activities_done.append("clase_reminder")
                renpy.notify("¡Es hora de ir a clases!")
    
    def execute_new_day_events():
        """
        Ejecuta eventos al comenzar un nuevo día
        """
        # Resetear energía del jugador (si implementas sistema de energía)
        # store.player_energy = 100
        
        # Mostrar resumen del día anterior si es necesario
        if total_days_played > 1:
            renpy.notify(f"Día {current_day_number} - {current_day_name}")
    
    def register_time_event(day, period, label, event_id=None, once=False, condition=None):
        """
        Registra un nuevo evento temporal
        """
        global time_events
        
        time_key = f"{day}_{period}"
        
        if time_key not in time_events:
            time_events[time_key] = []
        
        event = {
            "label": label,
            "id": event_id or label,
            "once": once,
            "condition": condition
        }
        
        time_events[time_key].append(event)

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
        if hasattr(store, 'current_time'):
            store.current_time = current_time_period
        if hasattr(store, 'current_day'):
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
    
    # Calcular el texto del tooltip antes del button
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
        
        action Function(advance_time, 1, True)
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
        
        background Frame("gui/frame/time_details.png", 10, 10)
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
        
        background Frame("gui/frame/skip_menu.png", 15, 15)
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

################################################################################
## Labels para testing y eventos de tiempo
################################################################################

label test_time_system:
    """
    Label de prueba para el sistema de tiempo
    """
    
    scene black
    with fade
    
    narrator "Probando el sistema de tiempo..."
    
    python:
        # Resetear tiempo
        set_time(1, "mañana")
    
    narrator "Tiempo actual: [current_day_name], [current_time_period] (Día [current_day_number])"
    
    menu time_test_menu:
        "¿Qué quieres probar?"
        
        "Avanzar una hora":
            $ advance_time(1, True)
            narrator "El tiempo ha avanzado."
            jump time_test_menu
        
        "Saltar al siguiente día":
            $ skip_to_next_day()
            narrator "Has saltado al siguiente día."
            jump time_test_menu
        
        "Ver menú de salto de tiempo":
            show screen time_skip_menu
            jump time_test_menu
        
        "Verificar si es fin de semana":
            if is_weekend():
                narrator "Sí, es fin de semana."
            else:
                narrator "No, es un día de semana."
            jump time_test_menu
        
        "Terminar prueba":
            pass
    
    narrator "Prueba completada."
    return

# Eventos de ejemplo
label morning_routine:
    """
    Rutina de mañana automática
    """
    narrator "Es un nuevo día..."
    
    if is_school_day():
        narrator "Hoy tienes clases."
    else:
        narrator "Hoy es fin de semana, puedes relajarte."
    
    return

label evening_reflection:
    """
    Reflexión de la tarde
    """
    narrator "El día está llegando a su fin..."
    
    if time_advanced_count > 5:
        narrator "Has estado muy activo hoy."
    
    return

################################################################################
## Integración con el sistema de guardado
################################################################################

init python:
    
    # Guardar información de tiempo en los saves
    def time_save_data():
        """
        Prepara datos de tiempo para guardar
        """
        return {
            "day": current_day_number,
            "day_name": current_day_name,
            "period": current_time_period,
            "total_days": total_days_played,
            "events": time_events
        }
    
    # Restaurar información de tiempo desde saves
    def time_load_data(data):
        """
        Restaura datos de tiempo desde un save
        """
        global current_day_number, current_day_name, current_time_period
        global total_days_played, time_events
        
        if data:
            current_day_number = data.get("day", 1)
            current_day_name = data.get("day_name", "Lunes")
            current_time_period = data.get("period", "mañana")
            total_days_played = data.get("total_days", 1)
            time_events = data.get("events", {})
            
            update_navigation_time()

################################################################################
## Configuración de ciclos de tiempo especiales
################################################################################

# Definir eventos especiales por fecha
default special_dates = {
    7: "Primera semana completada",
    14: "Dos semanas en el juego",
    30: "Un mes jugando",
    100: "¡Día 100!"
}

init python:
    
    def check_special_dates():
        """
        Verifica si es una fecha especial
        """
        # Verificar que las variables existan antes de usarlas
        if not hasattr(store, 'current_day_number') or not hasattr(store, 'special_dates'):
            return
            
        if current_day_number in special_dates:
            message = special_dates[current_day_number]
            renpy.notify(f"¡Logro desbloqueado: {message}!")
            
            # Podrías otorgar recompensas aquí
            if current_day_number == 7:
                if hasattr(store, 'player_money'):
                    store.player_money += 100
            elif current_day_number == 30:
                if hasattr(store, 'player_money'):
                    store.player_money += 500
    
    def safe_check_special_dates():
        """
        Wrapper seguro para verificar fechas especiales
        """
        try:
            if hasattr(store, 'current_day_number') and hasattr(store, 'special_dates'):
                if store.current_day_number in store.special_dates:
                    check_special_dates()
        except:
            pass