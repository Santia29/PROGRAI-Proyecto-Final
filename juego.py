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
cuadro_vidas['superficie'].fill(COLOR_ROJO)

cuadro_tiempo = {"superficie":pygame.Surface(TAMAÑO_CUADRO),"rectangulo":pygame.Rect((0,0,0,0))}
cuadro_tiempo['superficie'].fill(COLOR_GRIS)

# cuadro_pregunta = crear_boton("imagenes/template.png",370,120,150, 228)
# cuadro_pregunta = pygame.image.load("imagenes/template.png")
cartas_preguntas = [{"superficie":pygame.Surface(TAMAÑO_PREGUNTA),"rectangulo":pygame.Rect((0,0,0,0))}]
for carta in cartas_preguntas:
    cuadro_pregunta = pygame.image.load("imagenes/template.png")
    cuadro_pregunta = pygame.transform.scale(cuadro_pregunta,(370,120))
    fuente_respuesta = pygame.font.SysFont("Arial Rounded MT Bold",25)
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
    imagen_boton.set_alpha(130)
# Fuentes
    fuente_pregunta = pygame.font.SysFont("Arial Black",16)
    fuente_respuesta = pygame.font.SysFont("Arial Rounded MT Bold",25)
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

#LOGARITMO COMODIN
def usar_comodin_pasar(indice_pregunta, lista_preguntas):
    """
    Permite pasar a la siguiente pregunta sin cambiar puntos ni vidas.
    Si es la última pregunta, reinicia el índice y mezcla las preguntas.
    """
    indice_pregunta += 1
    if indice_pregunta >= len(lista_preguntas):
        indice_pregunta = 0
        random.shuffle(lista_preguntas)
    return indice_pregunta
def blit_texto_en_boton(superficie, texto, coordenadas, fuente, color, fondo=(0, 0, 0, 0)):
    # Crear una superficie temporal con el mismo tamaño que el botón
    texto_superficie = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
    texto_superficie.fill(fondo)  # Rellenar con el color de fondo

    # Renderizar el texto y blittearlo en la superficie temporal
    texto_renderizado = fuente.render(texto, True, color)
    texto_superficie.blit(texto_renderizado, coordenadas)

    # Blittear la superficie temporal en la superficie principal
    superficie.blit(texto_superficie, (0, 0))
    return superficie

def mostrar_juego(pantalla:pygame.Surface, eventos):
    """
    """
    global indice_pregunta
    global puntuacion 
    global vidas_actuales
    global minutos
    global segundos
    global fondo_de_pantalla

    retorno = "juego"
    pregunta = lista_preguntas[indice_pregunta]

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


        if evento.type == un_segundo:
            cuadro_tiempo['superficie'].fill((COLOR_GRIS))
            if segundos == 0:
                if minutos == 0:
                    # Se acabó el tiempo, perdes una vida
                    vidas_actuales -= 1
                    cuadro_vidas['superficie'].fill(COLOR_ROJO)
                    if vidas_actuales == 0:
                        #Resetea el tiempo y vidas para el siguiente juego
                        vidas_actuales = CANTIDAD_OPORTUNIDADES
                        minutos = MINUTOS
                        segundos = 0
                        retorno = "terminado"
                else:
                    minutos -= 1
                    segundos = 59
            else:
                segundos -= 1

        aciertos_consecutivos = 0
        maxima_respuestas_por_vida = 3
        if evento.type == pygame.MOUSEBUTTONDOWN:      
            for i in range(len(cartas_respuestas)):
                if cartas_respuestas[i]["rectangulo"].collidepoint(evento.pos):
                    if int(pregunta['correcta']) == (i + 1):
                        sonido_correcto.play()
                        print("RESPUESTA CORRECTA")
                        #Integracion Estadisticas
                        
                        aciertos_consecutivos += 1
                        if aciertos_consecutivos >= maxima_respuestas_por_vida:
                            vidas_actuales += 1  # Incrementa vidas_actuales
                            aciertos_consecutivos = 0
                            cuadro_vidas['superficie'].fill((COLOR_ROJO))
                            pantalla.blit(cuadro_vidas['superficie'], (380, 10))
                            # blit_text(cuadro_vidas['superficie'], f"VIDAS: {vidas_actuales}", (10, 20), fuente_vidas, COLOR_BLANCO)

                                ##REVISAR. NO AGREGA VIDAS.
                        # else: 
                        #     aciertos_consecutivos = 0
                        # pantalla.blit(cuadro_vidas['superficie'], (380, 10))
                        # generar_estadistica(pregunta,lista_preguntas,True)              
                        # carta_pregunta['superficie'].fill((COLOR_GRIS))
                        for carta in cartas_respuestas:
                            carta['superficie'].fill(COLOR_DORADO)

                        indice_pregunta += 1    
                        if indice_pregunta != len(lista_preguntas):
                            pregunta = lista_preguntas[indice_pregunta]
                        else:
                            # Termino el juego
                            indice_pregunta = 0
                            random.shuffle(lista_preguntas)
                            pregunta = lista_preguntas[indice_pregunta]

                        puntuacion += 100
                        # Resetear el tiempo para la siguiente pregunta
                        # minutos = 2
                        # segundos = 0
                    else:
                        print("RESPUESTA INCORRECTA")
                        #Integracion Estadisticas
                        aciertos_consecutivos = 0
                        generar_estadistica(pregunta,lista_preguntas,False)
                        error_sonido.play()
                        carta_pregunta['superficie'].fill((COLOR_GRIS))
                        for carta in cartas_respuestas:
                            carta['superficie'].fill(COLOR_DORADO)

                        indice_pregunta += 1
                        vidas_actuales -= 1
                        cuadro_vidas['superficie'].fill((COLOR_ROJO)) 
                        if vidas_actuales == 0:
                            #Resetear el tiempo y vidas para el siguiente juego
                            vidas_actuales = CANTIDAD_OPORTUNIDADES
                            minutos = MINUTOS
                            segundos = 0
                            retorno = "terminado"

                        if indice_pregunta != len(lista_preguntas):
                            pregunta = lista_preguntas[indice_pregunta]
                        else:
                            # Termino el juego
                            indice_pregunta = 0
                            random.shuffle(lista_preguntas)
                            pregunta = lista_preguntas[indice_pregunta]

                        puntuacion -= 50
                        if puntuacion <= 0:
                            puntuacion = 0
                        # puntuacion = min(-50,10000)
                        # Resetear el tiempo para la siguiente pregunta
                        # minutos = 2
                        # segundos = 0


    #Dibujo en pantalla
    # pantalla.fill(COLOR_NEGRO)
    fondo_de_pantalla = pygame.image.load("imagenes\preguntados_1.jpg")
    fondo_de_pantalla = pygame.transform.scale(fondo_de_pantalla,(700,800))
    pantalla.blit(fondo_de_pantalla,(0,0))
    #Imagen
    imagen_juego = pygame.image.load("imagenes/imagen_1.png")
    imagen_juego = pygame.transform.scale(imagen_juego,(340,170))
    pantalla.blit(imagen_juego,(170,58))


    # Carta pregunta
    
    # Cartas respuestas
    # boton = pygame.transform.scale(imagen_boton,(10,15))
    # boton = cartas_respuestas[0]['rectangulo'] = pantalla.blit(cartas_respuestas[0]['superficie'], (125, 325))
    # pantalla.blit(cartas_respuestas[0]['superficie'], carta['rectangulo'])
    # blit_text(cartas_respuestas[0]['superficie'], pregunta['respuesta_1'], (20, 15), fuente_respuesta, COLOR_NEGRO)
    


    # Cuadro Vidas
    pantalla.blit(cuadro_vidas['superficie'], (380, 10))
    blit_text(cuadro_vidas['superficie'], f"VIDAS: {vidas_actuales}", (10, 20), fuente_vidas, COLOR_BLANCO)
    
    # Cuadro tiempo
    pantalla.blit(cuadro_tiempo['superficie'], (210, 10))
    blit_text(cuadro_tiempo['superficie'], f"TIEMPO      {minutos}:{segundos}", (21, 5), fuente_tiempo, COLOR_BLANCO)

    # texto_superficie = pygame.Surface(cuadro_pregunta.get_size(), pygame.SRCALPHA)
    # pantalla.blit(texto_superficie, (160, 228))  # Blittear el texto primero
    # pantalla.blit(cuadro_pregunta, (160, 228)) 
    
    # # blit_text(cuadro_pregunta, pregunta['pregunta'], (10, 10), fuente_pregunta,COLOR_BLANCO)
    # blit_texto_en_boton(cuadro_pregunta, pregunta['pregunta'], (10, 10), fuente_pregunta, COLOR_BLANCO)
    # blit_texto_en_boton(cuadro_pregunta[])
    texto_superficie = blit_texto_en_boton(cuadro_pregunta, pregunta['pregunta'], (10, 10), fuente_pregunta, COLOR_BLANCO)
    pantalla.blit(texto_superficie, (160, 228))  # Blittear el texto primero
    texto_superficie.fill((0, 0, 0, 0))
    pantalla.blit(cuadro_pregunta, (160, 228))


    coordenadas_botones = [(205, 385), (205, 485), (205, 585), (205, 685)]
    texto_superficie = pygame.Surface(imagen_boton.get_size(), pygame.SRCALPHA)
    texto_superficie.fill((0, 0, 0, 0))  # Rellenar con transparente
    for i, coordenadas in enumerate(coordenadas_botones):
        # blittear el botón
        cartas_respuestas[i]['rectangulo'] = pantalla.blit(imagen_boton, coordenadas)
        
        # Limpiar la superficie temporal (opcional, pero recomendado)
        texto_superficie.fill((0, 0, 0, 0))

        # blittear el texto en la superficie temporal
        blit_texto_en_boton(texto_superficie, pregunta[f"respuesta_{i+1}"], (35, 30), fuente_respuesta, COLOR_NEGRO)

        # blittear la superficie temporal en el botón
        pantalla.blit(texto_superficie, coordenadas)
        
    # cartas_respuestas[0]['rectangulo'] = pantalla.blit(imagen_boton,(205, 385))
    # cartas_respuestas[1]['rectangulo'] = pantalla.blit(imagen_boton,(205, 485))
    # cartas_respuestas[2]['rectangulo'] = pantalla.blit(imagen_boton,(205, 585))
    # cartas_respuestas[3]['rectangulo'] = pantalla.blit(imagen_boton,(205, 685))

    # blit_text(imagen_boton, pregunta['respuesta_1'], (35, 15), fuente_respuesta, COLOR_NEGRO)
    # blit_text(imagen_boton, pregunta['respuesta_2'], (35, 15), fuente_respuesta, COLOR_NEGRO)
    # blit_text(imagen_boton, pregunta['respuesta_3'], (35, 15), fuente_respuesta, COLOR_NEGRO)
    # blit_text(imagen_boton, pregunta['respuesta_4'], (35, 15), fuente_respuesta, COLOR_NEGRO)
        
    # pygame.display.update()
    
    # Mostrar puntuación
    blit_text(pantalla, f"Puntuación: {puntuacion} puntos", (10, 30), fuente_puntuacion, COLOR_CELESTE)
    pygame.display.flip()
    return retorno





# ...

# Blittear la pregunta y el texto