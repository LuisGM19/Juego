# intro.rpy - Script de introducción simple

# Transiciones personalizadas
define fade_slow = Fade(1.5, 0.5, 1.5)

# Label principal del juego (punto de entrada)
label start:
    
    # Verificar si ya se completó la intro
    if intro_completed:
        menu:
            "¿Deseas saltar la introducción?"
            "Sí, ir al juego principal":
                jump main_game
            "No, ver la introducción":
                pass
    
    # Llamar a la introducción
    call introduction
    
    # Marcar como completada
    $ intro_completed = True
    
    # Ir al juego principal
    jump main_game

# Label de la introducción
label introduction:
    
    # Pantalla negra inicial
    scene black
    with fade_slow
    
    # Música de introducción (opcional)
    # play music "audio/music/intro_theme.ogg" fadeout 1.0
    
    # Volver a pantalla negra
    scene black
    with fade
    
    # Texto de contexto inicial
    narrator "En un mundo donde cada día trae nuevas posibilidades..."
    
    narrator "Donde las decisiones, grandes y pequeñas, van tejiendo el tapiz de nuestras vidas..."
    
    narrator "Una nueva historia está por comenzar."
    
    # Configuración del nombre del jugador
    $ player_name = renpy.input("¿Cuál es tu nombre?", default="Alex", length=20)
    $ player_name = player_name.strip() or "Alex"
    
    # Confirmar el nombre
    narrator "Muy bien, [player_name]. Tu historia comienza ahora..."
    
    # Primera escena
    scene intro1
    with fade_slow
    
    narrator "Despiertas en un lugar extraño"
    
    player "Mmm... otro día más."
    
    narrator "Pero cuando abres los ojos te das cuenta que no estas en tu hogar"
    
    scene intro2
    with dissolve
    
    Pensamientosmc "Donde estoy?"
    
    Pensamientosmc "Como llegue aqui"
    
    # Transición a la sala
    scene intro3
    with fade
    
    narrator "Te sientas en el mismo lugar para inspeccionar a tu alrededor"
    
    narrator "10 minutos despues"
    
    player "Hay una tienda aqui, ire a preguntar si hay alguien"
    
    narrator "Se levanta y se dirige a la tienda"
    
    scene intro4
    with fade
    
    Pensamientosmc "Hay alguien adentro"
    
    Pensamientosmc "ire a preguntarle como llegue aqui"

    scene intro5
    with fade

    Pensamientosmc "Este lugar es extraño"

    scene intro6
    with fade

    # Primera interacción simple
    menu:
        "Buenos días, sabes como llegue aqui":
            scene intro7
            with fade
            Vendedor "A veces este lugar invoca a personajes que necesitan un cambio de su vida"
            Vendedor "Les da otra oportunidad..."
            
        "Que es este lugar?":
            scene intro8
            with fade
            Vendedor "Es una tienda magica"
            Vendedor "Este lugar te da lo que mas necesitas"
    
    scene intro9
    with fade

    player "Hay una forma de salir de este lugar"

    Vendedor "Solo hay una forma de salir [player_name], tienes que encontrar un objeto que te mandara a tu mundo"

    player "Como sabes mi nombre?"

    scene intro10
    with fade

    Vendedor "Yo se todo sobre ti y no tuviste una buena vida y por eso te doy esta oportunidad"

    Vendedor "Busca ese objeto o te quedaras aqui para siempre"

    scene intro11
    with fade
    Pensamientosmc "Okey voy a buscar esa cosa, para salir de aqui"
    
    scene intro12
    with fade

    Pensamientosmc "No hay nada aqui"

    scene black
    with fade_slow

    narrator "[player_name], estuvo buscado hasta al atardecer"

    scene intro14
    with fade

    player "Por fin lo encontre"
    player "Porque esta brillando"

    scene intro13
    with fade

    Vendedor "Enhorabuena lo has encontrado espero que tu nueva vida la aprecies"  
    player "Me despido y fue un gusto conocerte"

    scene black
    with fade_slow

    Pensamientosmc "Donde estoy?"

    scene intro15
    with fade

    player "Estoy en mi cama todo fue un sueño?"

    scene intro16
    with fade
    player "Ese sueño fue muy real"
    player "Me siento muy extraño, es como si hubiera cambiado algo"

    scene intro17
    with fade
    player "Que es esto?"
    player "Tengo tetas!!!! y tengo el trasero mas grande!!!!"

    scene intro18
    with fade
    player "Necesito verme en el espejo"

    scene intro19
    with fade
    player "Todo lo del sueño fue verdad?"

    scene intro20
    with fade
    player "No puede ser!!!!!!"
    player "Me converti en mujer esta fue la oportinudad convertirme en mujer"

    scene intro21
    with fade
    player "Yo soy un hombre!!!!!! no puedo ser mujer"

    scene intro22
    with fade
    player "Tengo que volver a ser un hombre pero como lo hare y si es permanente como llevare mi vida no puede ser"
    
    # Transición final
    scene black
    with fade_slow
    
    narrator "Y así, con las palabras de [player_name] aún resonando en el aire..."
    
    narrator "Tu historia verdadera está a punto de comenzar."
    
    return

# Placeholder para el juego principal
label main_game:
    
    # Establecer ubicación inicial
    $ current_location = "tu_habitacion"
    $ current_area = "casa"
    
    scene black
    with fade
    
    narrator "Ahora puedes explorar libremente usando el botón de mapa."
    
    narrator "Haz clic en el ícono 🗺️ en la esquina superior derecha para navegar."
    
    # Ir a la ubicación inicial con sistema de navegación
    jump location_tu_habitacion