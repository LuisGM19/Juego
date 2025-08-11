# intro.rpy - Script de introducción optimizado y reorganizado
# Version 2.0 - Mejorado para mejor rendimiento y organización

################################################################################
## Configuración de la introducción
################################################################################

# Transiciones personalizadas
define fade_slow = Fade(1.5, 0.5, 1.5)
define fade_fast = Fade(0.5, 0.2, 0.5)

# Variables de estado de la introducción
# (intro_completed está definido en characters.rpy)
default player_gender_intro = "male"  # Para tracking específico de la intro

################################################################################
## Punto de entrada principal
################################################################################

label start:
    """
    Punto de entrada principal del juego.
    Gestiona si mostrar la introducción o ir directo al juego principal.
    """
    
    # Sistema de salto de introducción
    if intro_completed:
        call intro_skip_menu
    else:
        call introduction_sequence
    
    # Continuar al juego principal
    jump main_game

################################################################################
## Menú de salto de introducción
################################################################################

label intro_skip_menu:
    menu:
        "¿Deseas saltar la introducción?"
        
        "Sí, ir al juego principal":
            return
            
        "No, ver la introducción":
            call introduction_sequence
    
    return

################################################################################
## Secuencia de introducción principal
################################################################################

label introduction_sequence:
    """
    Secuencia completa de introducción con todas las escenas
    """
    
    # Preparación inicial
    scene black
    with fade_slow
    
    # Opcional: Música de introducción
    # play music "audio/music/intro_theme.ogg" fadeout 1.0 fadein 2.0
    
    # Prólogo narrativo
    call intro_prologue
    
    # Configuración del personaje
    call intro_character_setup
    
    # Secuencia del sueño/tienda mágica
    call intro_dream_sequence
    
    # Despertar y transformación
    call intro_awakening
    
    # Epílogo
    call intro_epilogue
    
    # Marcar introducción como completada
    $ intro_completed = True
    
    return

################################################################################
## Secciones de la introducción
################################################################################

label intro_prologue:
    """Texto introductorio y ambientación"""
    
    scene black
    with fade
    
    narrator "En un mundo donde cada día trae nuevas posibilidades..."
    narrator "Donde las decisiones, grandes y pequeñas, van tejiendo el tapiz de nuestras vidas..."
    narrator "Una nueva historia está por comenzar."
    
    return

label intro_character_setup:
    """Configuración inicial del personaje"""
    
    python:
        # Input del nombre con validación
        player_name = renpy.input(
            "¿Cuál es tu nombre?", 
            default="Alex", 
            length=20,
            exclude=" {}[]"  # Excluir caracteres problemáticos
        )
        player_name = player_name.strip() or "Alex"
        
        # Nombre femenino (se usará después de la transformación)
        playerf_name = player_name  # Por defecto el mismo, puede personalizarse
    
    narrator "Muy bien, [player_name]. Tu historia comienza ahora..."
    
    return

label intro_dream_sequence:
    """Secuencia del sueño/tienda mágica"""
    
    # Escena 1: Despertar en lugar extraño
    call intro_strange_awakening
    
    # Escena 2: Exploración inicial
    call intro_exploration
    
    # Escena 3: Encuentro con el vendedor
    call intro_vendor_meeting
    
    # Escena 4: Búsqueda del objeto
    call intro_object_search
    
    return

label intro_strange_awakening:
    """Primera parte: despertar en lugar extraño"""
    
    scene intro1
    with fade_slow
    
    narrator "Despiertas en un lugar extraño..."
    player "Mmm... otro día más."
    narrator "Pero cuando abres los ojos te das cuenta que no estás en tu hogar."
    
    scene intro2
    with dissolve
    
    Pensamientosmc "¿Dónde estoy?"
    Pensamientosmc "¿Cómo llegué aquí?"
    
    return

label intro_exploration:
    """Exploración del lugar extraño"""
    
    scene intro3
    with fade
    
    narrator "Te sientas en el mismo lugar para inspeccionar a tu alrededor."
    narrator "10 minutos después..."
    player "Hay una tienda aquí, iré a preguntar si hay alguien."
    narrator "Te levantas y te diriges a la tienda."
    
    scene intro4
    with fade
    
    Pensamientosmc "Hay alguien adentro."
    Pensamientosmc "Iré a preguntarle cómo llegué aquí."
    
    scene intro5
    with fade
    
    Pensamientosmc "Este lugar es extraño..."
    
    return

label intro_vendor_meeting:
    """Encuentro y conversación con el vendedor"""
    
    scene intro6
    with fade
    
    menu intro_first_question:
        "Buenos días, ¿sabes cómo llegué aquí?":
            call intro_vendor_response_arrival
            
        "¿Qué es este lugar?":
            call intro_vendor_response_place
    
    # Continuación del diálogo
    scene intro9
    with fade
    
    player "¿Hay una forma de salir de este lugar?"
    Vendedor "Solo hay una forma de salir, [player_name]. Tienes que encontrar un objeto que te mandará a tu mundo."
    player "¿Cómo sabes mi nombre?"
    
    scene intro10
    with fade
    
    Vendedor "Yo sé todo sobre ti. No tuviste una buena vida y por eso te doy esta oportunidad."
    Vendedor "Busca ese objeto o te quedarás aquí para siempre."
    
    scene intro11
    with fade
    
    Pensamientosmc "Okay, voy a buscar esa cosa para salir de aquí."
    
    return

label intro_vendor_response_arrival:
    scene intro7
    with fade
    
    Vendedor "A veces este lugar invoca a personajes que necesitan un cambio en su vida."
    Vendedor "Les da otra oportunidad..."
    
    return

label intro_vendor_response_place:
    scene intro8
    with fade
    
    Vendedor "Es una tienda mágica."
    Vendedor "Este lugar te da lo que más necesitas."
    
    return

label intro_object_search:
    """Búsqueda y encuentro del objeto mágico"""
    
    scene intro12
    with fade
    
    Pensamientosmc "No hay nada aquí..."
    
    scene black
    with fade_slow
    
    narrator "[player_name] estuvo buscando hasta el atardecer..."
    
    scene intro14
    with fade
    
    player "¡Por fin lo encontré!"
    player "¿Por qué está brillando?"
    
    scene intro13
    with fade
    
    Vendedor "Enhorabuena, lo has encontrado. Espero que tu nueva vida la aprecies."
    player "Me despido. Fue un gusto conocerte."
    
    return

label intro_awakening:
    """Despertar y descubrimiento de la transformación"""
    
    scene black
    with fade_slow
    
    Pensamientosmc "¿Dónde estoy?"
    
    scene intro15
    with fade
    
    player "Estoy en mi cama... ¿todo fue un sueño?"
    
    scene intro16
    with fade
    
    player "Ese sueño fue muy real..."
    player "Me siento muy extraño, es como si hubiera cambiado algo."
    
    # Descubrimiento de la transformación
    call intro_transformation_discovery
    
    return

label intro_transformation_discovery:
    """Momento del descubrimiento de la transformación"""
    
    scene intro17
    with fade
    
    player "¿Qué es esto?"
    player "¡¡¡Tengo... tengo un cuerpo diferente!!!"
    
    scene intro18
    with fade
    
    player "Necesito verme en el espejo."
    
    scene intro19
    with fade
    
    player "¿Todo lo del sueño fue verdad?"
    
    scene intro20
    with fade
    
    player "¡No puede ser!"
    player "Me convertí en mujer... ¿esta fue la oportunidad? ¿Convertirme en mujer?"
    
    scene intro21
    with fade
    
    player "¡Yo soy un hombre! ¡No puedo ser mujer!"
    
    scene intro22
    with fade
    
    player "Tengo que volver a ser un hombre, pero ¿cómo lo haré?"
    player "Y si es permanente... ¿cómo llevaré mi vida? No puede ser..."
    
    # Actualizar género del personaje
    $ player_gender = "female"
    
    return

label intro_epilogue:
    """Cierre de la introducción"""
    
    scene black
    with fade_slow
    
    narrator "Y así, con las palabras de [player_name] aún resonando en el aire..."
    narrator "Tu historia verdadera está a punto de comenzar."
    
    # Detener música de intro si existe
    # stop music fadeout 2.0
    
    return

################################################################################
## Transición al juego principal
################################################################################

label main_game:
    """
    Inicio del juego principal después de la introducción
    """
    
    # Configuración inicial del juego
    python:
        # Establecer ubicación inicial
        current_location = "tu_habitacion"
        current_area = "casa"
        
        # Resetear tiempo al inicio
        current_day_number = 1
        current_day_name = "Lunes"
        current_time_period = "mañana"
    
    scene black
    with fade
    
    narrator "Ahora puedes explorar libremente usando el botón de mapa."
    narrator "Haz clic en el ícono 🗺️ en la esquina superior derecha para navegar."
    
    # Mostrar interfaces del juego
    show screen navigation_button
    show screen time_system
    
    # Ir a la ubicación inicial
    jump location_tu_habitacion