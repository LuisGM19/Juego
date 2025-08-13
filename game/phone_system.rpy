# phone_system.rpy - Sistema de teléfono móvil
# Version 4.0 - Diseño simplificado y funcional

################################################################################
## Variables del sistema de teléfono
################################################################################

# Estado del teléfono
default phone_enabled = True
default phone_notifications = 0
default phone_battery = 100
default phone_signal = 4
default phone_visible = False  # Para controlar cuando mostrar el botón

# Apps disponibles (para futuro)
default phone_apps = {
    "mensajes": {"name": "Mensajes", "icon": "💬", "color": "#25D366", "enabled": True, "notifications": 0},
    "contactos": {"name": "Contactos", "icon": "👥", "color": "#4285F4", "enabled": True, "notifications": 0},
    "galeria": {"name": "Galería", "icon": "🖼️", "color": "#FF6B6B", "enabled": True, "notifications": 0},
    "notas": {"name": "Notas", "icon": "📝", "color": "#FFD93D", "enabled": True, "notifications": 0},
    "ajustes": {"name": "Ajustes", "icon": "⚙️", "color": "#6C757D", "enabled": True, "notifications": 0},
    "camara": {"name": "Cámara", "icon": "📷", "color": "#E91E63", "enabled": True, "notifications": 0}
}

################################################################################
## Funciones del sistema de teléfono
################################################################################

init python:
    
    def toggle_phone():
        """
        Muestra u oculta el teléfono
        """
        if renpy.get_screen("phone_screen"):
            renpy.hide_screen("phone_screen")
            renpy.restart_interaction()
        else:
            renpy.show_screen("phone_screen")
            renpy.restart_interaction()
    
    def add_phone_notification(app_id=None):
        """
        Añade una notificación al teléfono
        """
        global phone_notifications
        phone_notifications += 1
        
        if app_id and app_id in phone_apps:
            phone_apps[app_id]["notifications"] += 1
    
    def clear_phone_notifications(app_id=None):
        """
        Limpia las notificaciones
        """
        global phone_notifications
        
        if app_id and app_id in phone_apps:
            count = phone_apps[app_id]["notifications"]
            phone_apps[app_id]["notifications"] = 0
            phone_notifications = max(0, phone_notifications - count)
        else:
            phone_notifications = 0
            for app in phone_apps.values():
                app["notifications"] = 0
    
    def enable_phone_button():
        """
        Habilita el botón del teléfono (usar después de la intro)
        """
        global phone_visible
        phone_visible = True
        renpy.show_screen("phone_button")
    
    def get_current_time():
        """
        Obtiene la hora actual del juego
        """
        if hasattr(store, 'current_time_period'):
            if current_time_period == "mañana":
                return "09:24 AM"
            elif current_time_period == "tarde":
                return "03:47 PM"
            else:
                return "09:35 PM"
        return "12:00 PM"

################################################################################
## Screen: Botón del teléfono
################################################################################

screen phone_button():
    # Solo mostrar si está habilitado, visible y no en la intro
    if phone_enabled and phone_visible and not renpy.get_screen("phone_screen"):
        
        button:
            xalign 1.0
            yalign 0.0
            xsize 80
            ysize 80
            xoffset -20
            yoffset 110  # Posicionado debajo del botón de mapa
            
            background "#2c3e50cc"
            hover_background "#34495eff"
            
            # Contenido del botón
            vbox:
                spacing 2
                xalign 0.5
                yalign 0.5
                
                # Ícono del teléfono
                text "📱" size 40 xalign 0.5
                
                # Indicador de notificaciones
                if phone_notifications > 0:
                    frame:
                        xalign 1.0
                        yalign 0.0
                        xoffset 10
                        yoffset -10
                        background "#FF4444"
                        xsize 26
                        ysize 26
                        
                        text str(phone_notifications) size 14 color "#ffffff" xalign 0.5 yalign 0.5 bold True
            
            action Function(toggle_phone)

################################################################################
## Screen: Pantalla principal del teléfono
################################################################################

screen phone_screen():
    # Modal para bloquear interacción con el fondo
    modal True
    
    # Fondo oscuro semi-transparente
    add "#00000099"
    
    # Frame principal del teléfono
    frame:
        xalign 0.5
        yalign 0.5
        xsize 380
        ysize 760
        
        # Fondo del teléfono
        background "#000000"
        padding (2, 2)
        
        # Marco plateado
        frame:
            xfill True
            yfill True
            background "#2C2C2E"
            padding (10, 10)
            
            # Pantalla
            frame:
                xfill True
                yfill True
                background "#000000"
                padding (0, 0)
                
                vbox:
                    spacing 0
                    xfill True
                    yfill True
                    
                    # Barra de estado superior
                    frame:
                        xfill True
                        ysize 35
                        background "#000000"
                        padding (15, 8)
                        
                        hbox:
                            xfill True
                            yalign 0.5
                            
                            # Hora
                            text get_current_time() size 14 color "#ffffff" bold True
                            
                            # Espacio central
                            null width 50
                            
                            # Estado derecho
                            hbox:
                                xalign 1.0
                                spacing 8
                                
                                text "📶" size 14
                                text f"{phone_battery}%" size 14 color "#ffffff"
                                text "🔋" size 14
                    
                    # Contenido principal
                    frame:
                        xfill True
                        yfill True
                        background "#0A0A0A"
                        padding (20, 20)
                        
                        # Sin viewport para evitar scroll
                        vbox:
                            spacing 30
                            xfill True
                            
                            # Título
                            text "Mi Teléfono" size 32 color "#ffffff" xalign 0.5 bold True
                            
                            # Widget de notificaciones
                            frame:
                                xfill True
                                ysize 100
                                background "#1C1C1E"
                                padding (20, 15)
                                
                                vbox:
                                    spacing 10
                                    xfill True
                                    
                                    text "📬 Notificaciones" size 18 color "#888888"
                                    
                                    if phone_notifications > 0:
                                        text f"{phone_notifications} nuevas notificaciones" size 16 color "#ffffff"
                                    else:
                                        text "Sin notificaciones" size 16 color "#666666"
                            
                            # Separador
                            frame:
                                xfill True
                                ysize 2
                                background "#333333"
                            
                            # Grid de aplicaciones
                            text "Aplicaciones" size 20 color "#888888"
                            
                            grid 3 2:
                                spacing 25
                                xalign 0.5
                                
                                for app_id, app_data in phone_apps.items():
                                    button:
                                        xsize 90
                                        ysize 110
                                        background None
                                        hover_background "#FFFFFF11"
                                        
                                        action NullAction()
                                        
                                        vbox:
                                            spacing 8
                                            xalign 0.5
                                            yalign 0.5
                                            
                                            # Ícono de la app
                                            frame:
                                                xsize 70
                                                ysize 70
                                                background app_data.get("color", "#3498db")
                                                xalign 0.5
                                                
                                                text app_data["icon"] size 40 xalign 0.5 yalign 0.5
                                                
                                                # Badge de notificaciones
                                                if app_data.get("notifications", 0) > 0:
                                                    frame:
                                                        xalign 1.0
                                                        yalign 0.0
                                                        xoffset 10
                                                        yoffset -10
                                                        background "#FF3B30"
                                                        xsize 24
                                                        ysize 24
                                                        
                                                        text str(app_data["notifications"]) size 12 color "#ffffff" xalign 0.5 yalign 0.5 bold True
                                            
                                            # Nombre de la app
                                            text app_data["name"] size 12 color "#ffffff" xalign 0.5
                            
                            # Espacio adicional
                            null height 30
                            
                            text "Más funciones próximamente" size 14 color "#666666" xalign 0.5 italic True
                    
                    # Barra de navegación inferior
                    frame:
                        xfill True
                        ysize 70
                        background "#000000"
                        padding (20, 15)
                        
                        hbox:
                            xfill True
                            spacing 50
                            xalign 0.5
                            yalign 0.5
                            
                            # Botón de volver
                            button:
                                xsize 80
                                ysize 40
                                background "#48484A"
                                hover_background "#636366"
                                
                                text "←" size 24 color "#ffffff" xalign 0.5 yalign 0.5 bold True
                                
                                action NullAction()
                            
                            # Botón de inicio
                            button:
                                xsize 80
                                ysize 40
                                background "#48484A"
                                hover_background "#636366"
                                xalign 0.5
                                
                                text "●" size 20 color "#ffffff" xalign 0.5 yalign 0.5
                                
                                action NullAction()
                            
                            # Botón de cerrar
                            button:
                                xsize 80
                                ysize 40
                                background "#FF453A"
                                hover_background "#FF6961"
                                
                                text "✕" size 20 color "#ffffff" xalign 0.5 yalign 0.5 bold True
                                
                                action Hide("phone_screen")

################################################################################
## Integración con el juego principal
################################################################################

# Label para activar el teléfono después de la introducción
label enable_phone_system:
    """
    Llamar este label después de la introducción para activar el teléfono
    """
    $ phone_visible = True
    show screen phone_button
    return