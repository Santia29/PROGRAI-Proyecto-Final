import pygame
from constantes import *
from funciones import *

pygame.init() #Inicio del proyecto

#Configuracion de la pantalla
pantalla = pygame.display.set_mode(PANTALLA) #Se crea una ventana

#Fuente
fuente_boton = pygame.font.SysFont("Arial Rounded MT Bold",23)
fuente_texto = pygame.font.SysFont("Arial Rounded MT Bold", 20)
fuente_reglas_de_juego = pygame.font.SysFont("Arial Rounded MT Bold",40) #TITULO QUE CONTIENE "REGLAS DE JUEGO"

#Boton
boton_volver = crear_boton("imagenes/boton.png",170,50,260,750)

#Sonido de click
click_sonido = pygame.mixer.Sound("sonidos/click.mp3")
click_sonido.set_volume(1)

# Reglas del juego
reglas = [
    "1. El juego comenzará al darle click en el botón JUGAR.",
    "2. El juego posee 2 minutos de duración y contará con",
        "3 VIDAS.",
    "3. Si se acaba el tiempo o pierde todas sus vidas,",
        "se guardara las estadisticas",
    "4. Si acierta 5 preguntas consecutivas, ganará una vida.",
    "5. Posee 2 comodines que pueden usarse una vez por partida.",
    "6. El comodín 'Pasar' avanza a la siguiente pregunta ('P' o botón).",
    "7. El comodín 'x2' duplica los puntos obtenidos ('X' o botón).",
]
    
def mostrar_reglas(pantalla:pygame.Surface,eventos):
    global volumen

    retorno = "reglas"
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver['rectangulo'].collidepoint(evento.pos):
                click_sonido.play()
                retorno = "menu"
        elif evento.type == pygame.QUIT:
            retorno = "salir"

    # Limpiar la pantalla antes de redibujar
    pantalla.fill((0, 0, 0))

    #Imagen de fondo de pantalla
    fondo_de_pantalla = pygame.image.load("imagenes/preguntados_1.jpg")
    fondo_de_pantalla = pygame.transform.scale(fondo_de_pantalla,(700,800))
    pantalla.blit(fondo_de_pantalla, (0, 0))

    #Imagen pergamino
    imagen_pergamino = pygame.image.load("imagenes\papel-pergaminos.png")
    imagen_pergamino = pygame.transform.scale(imagen_pergamino,(1100,700))
    pantalla.blit(imagen_pergamino,(-180,10))

    #Imagen emoticon jostick
    imagen_jostick = pygame.image.load("imagenes\imagenjostick.jpg")
    imagen_jostick = pygame.transform.scale(imagen_jostick,(70,70))
    pantalla.blit(imagen_jostick,(310,690))

    #Dibuja el boton volver
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    blit_text(boton_volver['superficie'],"VOLVER",(50,20),fuente_boton,COLOR_NEGRO)

    reglas_de_juego = fuente_reglas_de_juego.render("REGLAS DE JUEGO",True,COLOR_NEGRO)
    pantalla.blit(reglas_de_juego,(215,145))

   # Mostrar las reglas en pantalla
    y_offset = 200
    for regla in reglas:
        texto = fuente_texto.render(regla, True, COLOR_NEGRO)
        pantalla.blit(texto, (155, y_offset))
        y_offset += 50
    
    return retorno