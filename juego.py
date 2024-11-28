#---------------------------------------- VENTANA JUEGO -----------------------------------------
import pygame
from constantes import *
import random
from funciones import *
import config
#Ventana Juego

pygame.init() # Inicializa el proyecto
pantalla = pygame.display.set_mode(PANTALLA)
#Defino eventos
un_segundo = pygame.USEREVENT
pygame.time.set_timer(un_segundo,1000)

#Superficies y rectangulos
carta_pregunta = pygame.image.load("imagenes/imagen_1.png")
carta_pregunta = {"superficie":pygame.Surface(TAMAÑO_PREGUNTA),"rectangulo":pygame.Rect((0,0,0,0))}
cuadro_vidas = {"superficie":pygame.Surface(TAMAÑO_CUADRO),"rectangulo":pygame.Rect((0,0,0,0))}
cuadro_tiempo = {"superficie":pygame.Surface(TAMAÑO_CUADRO),"rectangulo":pygame.Rect((0,0,0,0))}
cuadro_pregunta = {"superficie":pygame.Surface(TAMAÑO_PREGUNTA),"rectangulo":pygame.Rect((0,0,0,0))}
cuadro_pregunta['superficie'].fill((pygame.Color('bisque')))


# Carta de respuestas
cartas_respuestas = [
    {"superficie":pygame.Surface(TAMAÑO_RESPUESTA),"rectangulo":pygame.Rect((0,0,0,0))},
    {"superficie":pygame.Surface(TAMAÑO_RESPUESTA),"rectangulo":pygame.Rect((0,0,0,0))},
    {"superficie":pygame.Surface(TAMAÑO_RESPUESTA),"rectangulo":pygame.Rect((0,0,0,0))},
    {"superficie":pygame.Surface(TAMAÑO_RESPUESTA),"rectangulo":pygame.Rect((0,0,0,0))}
]

for carta in cartas_respuestas:
    imagen_boton = pygame.image.load("imagenes/boton.png")
    imagen_boton = pygame.transform.scale(imagen_boton,(270,100))

# Fuentes
    fuente_pregunta = pygame.font.SysFont("Arial Black",16)
    fuente_respuesta = pygame.font.SysFont("Arial Rounded MT Bold",20)
    fuente_puntuacion = pygame.font.SysFont("Arial Black",15)
    fuente_vidas = pygame.font.SysFont("Arial Black",15)
    fuente_tiempo = pygame.font.SysFont("Arial Black",15)

#Sonidos
volumen_sonido_correcto = 100
volumen_sonido_error = 100

sonido_correcto = pygame.mixer.Sound("sonidos/correcta.mp3")
sonido_correcto.set_volume(volumen_sonido_correcto/100)
error_sonido = pygame.mixer.Sound("sonidos/error.mp3")
error_sonido.set_volume(volumen_sonido_error/100)

#Variables
puntuacion = 0
random.shuffle(lista_preguntas)
indice_pregunta = 0
vidas_actuales = CANTIDAD_OPORTUNIDADES
segundos = 0
minutos = MINUTOS
aciertos_consecutivos = 0

#Variables de los comodines
comodin_x2_usado = False
comodin_pasar_usado = False
puntos_x2 = False 

def mostrar_juego(pantalla:pygame.Surface, eventos):
    """
    """
    global indice_pregunta
    global puntuacion 
    global vidas_actuales
    global minutos
    global segundos
    global fondo_de_pantalla
    global aciertos_consecutivos
    global comodin_x2_usado  
    global comodin_pasar_usado
    global puntos_x2

    retorno = "juego"
    pregunta = lista_preguntas[indice_pregunta]

   
    # Limpiar la pantalla antes de redibujar
    pantalla.fill((0, 0, 0))

    # Redibujar el fondo
    fondo_de_pantalla = pygame.image.load("imagenes\preguntados_1.jpg")
    fondo_de_pantalla = pygame.transform.scale(fondo_de_pantalla, (700, 800))
    pantalla.blit(fondo_de_pantalla, (0, 0))

    # Redibujar la imagen de la pregunta
    imagen_juego = pygame.image.load("imagenes/imagen_1.png")
    imagen_juego = pygame.transform.scale(imagen_juego, (340, 170))
    pantalla.blit(imagen_juego, (170, 58))

    #Imagen del comodin
    imagen_comodin = pygame.image.load("imagenes\imagen_comoding.png")
    imagen_comodin = pygame.transform.scale(imagen_comodin,(100,100))
    # Dibujo de la imagen del comodín en el costado derecho
    pantalla.blit(imagen_comodin, (PANTALLA[0] - imagen_comodin.get_width() - 10, 58))

    # Redibujar el cuadro de la pregunta y el texto
    pantalla.blit(cuadro_pregunta['superficie'], (170, 235))
    blit_text(cuadro_pregunta['superficie'], pregunta['pregunta'], (10, 10), fuente_pregunta)

    imagen_boton_pasar = crear_boton("imagenes\imagen_pasar.jpg",70,70,605,170)
    pantalla.blit(imagen_boton_pasar["superficie"], imagen_boton_pasar["rectangulo"])

    imagen_boton_x2 = crear_boton("imagenes\iconox2.png",70,70,605,270)
    pantalla.blit(imagen_boton_x2["superficie"], imagen_boton_x2["rectangulo"])

    # Limpiar las superficies de los botones antes de redibujarlas / agregadas horario 23:03 chatgtp
    for carta in cartas_respuestas:
        carta['superficie'].fill((0, 0, 0, 0))  # Rellenar con transparente para evitar superp

    for evento in eventos:
        pygame.mixer.music.set_volume(config.volumen / 100)
        
        if vidas_actuales == CANTIDAD_OPORTUNIDADES and minutos == MINUTOS and segundos == 0:
            puntuacion = 0
        if evento.type == pygame.QUIT:
            retorno = "salir"
        if evento.type == pygame.KEYDOWN:  # Detecta teclas presionadas
            if evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS:  # Tecla '+' (normal y en el teclado numérico)
                if config.volumen < 96:
                    config.volumen += 5                  
            elif evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:  # Tecla '-' (normal y en el teclado numérico)
                if config.volumen > 0:
                    config.volumen -= 5
       # Manejo de comodines    
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_p and not comodin_pasar_usado:  # Tecla 'P' para pasar
                comodin_pasar_usado = True
                # No suma ni resta puntos o vidas, solo pasa a la siguiente pregunta
                indice_pregunta += 1
                if indice_pregunta >= len(lista_preguntas):
                    indice_pregunta = 0  # Reiniciar las preguntas si ya no quedan
                pregunta = lista_preguntas[indice_pregunta]
                sonido_correcto.play()
                espacio_vacio = ''
                blit_texto_en_boton(cuadro_pregunta['superficie'],espacio_vacio,(10,10),fuente_pregunta,COLOR_BLANCO)
                cuadro_pregunta['superficie'].fill(pygame.Color('bisque'))
            elif evento.key == pygame.K_x and not comodin_x2_usado:  # Tecla 'X' para X2
                comodin_x2_usado = True
                # Indicamos que ahora el próximo acierto duplicará los puntos
                puntos_x2 = True
                sonido_correcto.play()
            if evento.key == pygame.K_x and comodin_x2_usado:
                print("El comodin x2 solo se puede utilizar una vez sola")
            elif evento.key == pygame.K_p and comodin_pasar_usado:
                print("El comodin pasar solo se puede utilizar una vez sola")
        # Dentro del manejo de la respuesta del jugador
        if evento.type == un_segundo:
            if segundos == 0:
                if minutos == 0:
                    # Se acabó el tiempo, perdes una vida
                    
                    retorno = "terminado"
                    comodin_pasar_usado = False
                    comodin_x2_usado = False
                    if vidas_actuales == 0:
                        #Resetea el tiempo y vidas para el siguiente juego
                        vidas_actuales = CANTIDAD_OPORTUNIDADES
                        minutos = MINUTOS
                        segundos = 0
                        retorno = "terminado"
                        comodin_pasar_usado = False
                        comodin_x2_usado = False
                else:
                    minutos -= 1
                    segundos = 59
            else:
                segundos -= 1

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if imagen_boton_pasar['rectangulo'].collidepoint(evento.pos) and not comodin_pasar_usado:  # Tecla 'P' para pasar
                comodin_pasar_usado = True
                # No suma ni resta puntos o vidas, solo pasa a la siguiente pregunta
                indice_pregunta += 1
                if indice_pregunta >= len(lista_preguntas):
                    indice_pregunta = 0  # Reiniciar las preguntas si ya no quedan
                pregunta = lista_preguntas[indice_pregunta]
                sonido_correcto.play()
                espacio_vacio = ''
                blit_texto_en_boton(cuadro_pregunta['superficie'],espacio_vacio,(10,10),fuente_pregunta,COLOR_BLANCO)
                cuadro_pregunta['superficie'].fill(pygame.Color('bisque'))      
            if imagen_boton_x2["rectangulo"].collidepoint(evento.pos) and not comodin_x2_usado:
                comodin_x2_usado = True
                # Indicamos que ahora el próximo acierto duplicará los puntos
                puntos_x2 = True
                sonido_correcto.play()
            if imagen_boton_pasar['rectangulo'].collidepoint(evento.pos) and comodin_pasar_usado:
                print("El comodin pasar solo se puede utilizar una vez sola")
            elif imagen_boton_x2["rectangulo"].collidepoint(evento.pos) and comodin_x2_usado:
                print("El comodin pasar x2 se puede utilizar una vez sola")
        #Respuesta del jugador
            for i in range(len(cartas_respuestas)):
                if cartas_respuestas[i]["rectangulo"].collidepoint(evento.pos):
                    aciertos_consecutivos += 1
                    if int(pregunta['correcta']) == (i + 1):                    
                        if aciertos_consecutivos == 5:
                            vidas_actuales += 1
                            blit_text(pantalla, f"VIDAS: {vidas_actuales}", (615, 30), fuente_vidas, COLOR_BLANCO)
                        # Reproducir sonido de respuesta correcta
                        sonido_correcto.play()
                        print("RESPUESTA CORRECTA")
                        cuadro_pregunta['superficie'].fill((pygame.Color('bisque')))
                        for carta in cartas_respuestas:
                            carta['superficie'].fill(COLOR_DORADO)
                        indice_pregunta += 1    
                        if indice_pregunta != len(lista_preguntas):
                            pregunta = lista_preguntas[indice_pregunta]
                        else:
                            # Termina el juego
                            indice_pregunta = 0
                            random.shuffle(lista_preguntas)
                            pregunta = lista_preguntas[indice_pregunta]
                        if puntos_x2:  # Si X2 fue activado, duplicamos los puntos
                            puntuacion += 200
                        else:
                            puntuacion += 100
                            puntos_x2 = False  # Resetear X2 para que no se pueda usar de nuevo
                    else:
                        print("RESPUESTA INCORRECTA")
                        #Integracion Estadisticas
                        cuadro_pregunta['superficie'].fill((pygame.Color('bisque')))
                        aciertos_consecutivos = 0
                        generar_estadistica(pregunta,lista_preguntas,False)
                        error_sonido.play()
                        for carta in cartas_respuestas:
                            carta['superficie'].fill(COLOR_DORADO)
                        indice_pregunta += 1
                        vidas_actuales -= 1
                        
                        if vidas_actuales == 0:
                            #Resetear el tiempo y vidas para el siguiente juego
                            vidas_actuales = CANTIDAD_OPORTUNIDADES
                            minutos = MINUTOS
                            segundos = 0
                            retorno = "terminado"
                            comodin_pasar_usado = False
                            comodin_x2_usado = False

                        if indice_pregunta != len(lista_preguntas):
                            pregunta = lista_preguntas[indice_pregunta]
                        else:
                            # Termino el juego
                            indice_pregunta = 0
                            random.shuffle(lista_preguntas)
                            pregunta = lista_preguntas[indice_pregunta]                 
                        if puntuacion <= 0:
                            puntuacion = 0

    pantalla.blit(cuadro_pregunta['superficie'], (170, 235))
    blit_text(cuadro_pregunta['superficie'], pregunta['pregunta'], (10, 10), fuente_pregunta)
    coordenadas_botones = [(205, 385), (205, 485), (205, 585), (205, 685)]
    texto_superficie = pygame.Surface(imagen_boton.get_size(), pygame.SRCALPHA)
    texto_superficie.fill((0, 0, 0, 0)) 
    for i, coordenadas in enumerate(coordenadas_botones):
        cartas_respuestas[i]['rectangulo'] = pantalla.blit(imagen_boton, coordenadas)    
        texto_superficie.fill((0, 0, 0, 0))
        blit_texto_en_boton(texto_superficie, pregunta[f"respuesta_{i+1}"], (20, 45), fuente_respuesta, COLOR_NEGRO)
        pantalla.blit(texto_superficie, coordenadas)
        
    # Mostrar puntuación
    blit_text(pantalla, f"TIEMPO      {minutos}:{segundos}", (260, 5), fuente_tiempo, COLOR_BLANCO)
    blit_text(pantalla, f"Puntuación: {puntuacion} puntos", (15, 30), fuente_puntuacion, COLOR_NEGRO)
    blit_text(pantalla, f"VIDAS: {vidas_actuales}", (615, 30), fuente_vidas, COLOR_BLANCO)
    pygame.display.flip()
    return retorno