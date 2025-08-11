# time_system.rpy - Sistema de tiempo para el juego

# Variables del sistema de tiempo
default current_day_number = 1
default current_day_name = "Lunes"
default current_time_period = "mañana"

# Lista de días de la semana
default days_of_week = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# Lista de períodos del día
default time_periods = ["mañana", "tarde", "noche"]

# Funciones del sistema de tiempo
init python:
    
    def advance_time():
        """Avanza el tiempo al siguiente período"""
        global current_time_period, current_day_number, current_day_name
        
        # Obtener el índice actual del período de tiempo
        current_period_index = time_periods.index(current_time_period)
        
        # Si es noche, avanzar al siguiente día
        if current_period_index == 2:  # noche (índice 2)
            current_time_period = "mañana"  # Volver a mañana
            current_day_number += 1
            
            # Calcular el nuevo día de la semana
            day_index = (current_day_number - 1) % 7
            current_day_name = days_of_week[day_index]
            
        else:
            # Avanzar al siguiente período del mismo día
            current_time_period = time_periods[current_period_index + 1]
    
    def get_time_display():
        """Obtiene el texto de tiempo para mostrar"""
        return f"{current_day_name} {current_time_period}"
    
    def get_time_icon():
        """Obtiene el ícono según el período del día"""
        if current_time_period == "mañana":
            return "☀️"  # Sol para mañana
        elif current_time_period == "tarde":
            return "🌅"  # Atardecer para tarde
        else:  # noche
            return "🌙"  # Luna para noche
    
    def reset_time():
        """Reinicia el tiempo al día 1, lunes mañana"""
        global current_day_number, current_day_name, current_time_period
        current_day_number = 1
        current_day_name = "Lunes"
        current_time_period = "mañana"

# Screen del botón de tiempo (siempre visible)
screen time_button():
    
    # Botón de tiempo en la esquina superior izquierda
    button:
        xalign 0.0
        yalign 0.0
        xsize 120
        ysize 60
        xoffset 20
        yoffset 20
        
        background "#2c3e50aa"
        hover_background "#34495ecc"
        
        action Function(advance_time)
        
        hbox:
            spacing 8
            xalign 0.5
            yalign 0.5
            
            # Ícono del tiempo
            text "[get_time_icon()]" size 24
            
            # Información de tiempo
            vbox:
                spacing 2
                text "[current_day_name]" size 14 color "#ffffff"
                text "[current_time_period]" size 12 color "#ecf0f1"

# Screen del panel de información de tiempo (opcional)
screen time_info():
    
    frame:
        xalign 0.0
        yalign 0.0
        xoffset 160  # Al lado del botón de tiempo
        yoffset 20
        padding (15, 10)
        background "#2c3e50aa"
        
        vbox:
            spacing 5
            
            text "Información de Tiempo" size 16 color "#ffffff"
            text "Día: [current_day_number]" size 14 color "#ecf0f1"
            text "Día de la semana: [current_day_name]" size 14 color "#ecf0f1"
            text "Período: [current_time_period]" size 14 color "#ecf0f1"

# Screen de control de tiempo avanzado (solo para testing/desarrollo)
screen time_controls():
    
    frame:
        xalign 1.0
        yalign 0.0
        xoffset -20
        yoffset 100
        padding (15, 15)
        background "#2c3e50dd"
        
        vbox:
            spacing 10
            
            text "Controles de Tiempo" size 16 color "#ffffff"
            
            textbutton "Avanzar Tiempo":
                action Function(advance_time)
                text_size 14
                
            textbutton "Reiniciar Tiempo":
                action Function(reset_time)
                text_size 14
                
            textbutton "Mostrar Info":
                action ToggleScreen("time_info")
                text_size 14

# Screen de notificación de cambio de tiempo
screen time_notification(message, duration=2.0):
    
    frame:
        xalign 0.5
        yalign 0.1
        padding (20, 15)
        background "#27ae60aa"
        
        hbox:
            spacing 10
            text "[get_time_icon()]" size 20
            text message size 16 color "#ffffff"
    
    # Auto-ocultar después del tiempo especificado
    timer duration action Hide("time_notification")

# Función para mostrar notificación de cambio de tiempo
init python:
    
    def show_time_change_notification():
        """Muestra una notificación cuando cambia el tiempo (DESHABILITADA)"""
        # Función deshabilitada - no mostrar notificaciones
        pass

# Modificar la función advance_time para incluir notificación
init python:
    
    def advance_time_with_notification():
        """Avanza el tiempo sin mostrar notificación"""
        advance_time()
        # No mostrar notificación
        pass

# Screen principal del sistema de tiempo (combina todo)
screen time_system():
    
    # Botón principal de tiempo
    use time_button
    
    # Opcional: mostrar controles de desarrollo (comentar para producción)
    # use time_controls

# Labels para testing del sistema de tiempo
label test_time_system:
    
    scene black
    
    narrator "Sistema de tiempo iniciado."
    
    narrator "Haz clic en el botón de tiempo (esquina superior izquierda) para avanzar."
    
    narrator "Día actual: [current_day_number] - [current_day_name] [current_time_period]"
    
    call screen time_system
    
    return

# Función para integrar con el sistema de navegación
init python:
    
    def update_navigation_time():
        """Actualiza las variables de tiempo en navigation.rpy"""
        # Actualizar las variables del sistema de navegación
        store.current_time = current_time_period
        store.current_day = current_day_name

# Hook para actualizar automáticamente el tiempo en navegación
init python:
    
    # Función original advance_time mejorada
    def advance_time():
        """Avanza el tiempo al siguiente período"""
        global current_time_period, current_day_number, current_day_name
        
        # Obtener el índice actual del período de tiempo
        current_period_index = time_periods.index(current_time_period)
        
        # Si es noche, avanzar al siguiente día
        if current_period_index == 2:  # noche (índice 2)
            current_time_period = "mañana"  # Volver a mañana
            current_day_number += 1
            
            # Calcular el nuevo día de la semana
            day_index = (current_day_number - 1) % 7
            current_day_name = days_of_week[day_index]
            
        else:
            # Avanzar al siguiente período del mismo día
            current_time_period = time_periods[current_period_index + 1]
        
        # Actualizar variables de navegación si existen
        try:
            update_navigation_time()
        except:
            pass  # Si no están definidas las variables de navegación, continuar
        
        # NO mostrar notificación - comentado
        # show_time_change_notification()
        
        # Aquí podrás agregar eventos específicos del tiempo más adelante
        # check_time_events()  # Función para eventos futuros