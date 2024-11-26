#----------------------------------- VENTANA PUNTUACIONES TOP-10 -------------------------------------------
import pygame
from constantes import *
from funciones import *

pygame.init() #Inicio del proyecto
pantalla = pygame.display.set_mode(PANTALLA)

fondo_de_pantalla = pygame.image.load("imagenes\preguntados_1.jpg")
fondo_de_pantalla = pygame.transform.scale(fondo_de_pantalla,(700,800))
#Fuente
fuente = pygame.font.SysFont("Arial Rounded MT Bold",30)
fuente_boton = pygame.font.SysFont("Arial Rounded MT Bold",23)


#Sonido de click
click_sonido = pygame.mixer.Sound("sonidos/click.mp3")
click_sonido.set_volume(1)

boton_volver = crear_boton("imagenes/boton.png",170,50,260,750)

def mostrar_puntuaciones(pantalla:pygame.Surface,eventos):
    global volumen

    retorno = "puntuaciones"

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_volver['rectangulo'].collidepoint(evento.pos):
                click_sonido.play()
                retorno = "menu"
        elif evento.type == pygame.QUIT:
            retorno = "salir"

    # pantalla.fill(COLOR_NEGRO)
    pantalla.blit(fondo_de_pantalla,(0,0))
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    blit_text(boton_volver['superficie'],"VOLVER",(50,20),fuente_boton,COLOR_NEGRO)
    lista_partidas = parse_json("partidas.json")
    ordenar_top_10(lista_partidas)
    renderizar_top_10(fuente,pantalla)

    return retorno

def renderizar_top_10(fuente,pantalla):
    """
      Muestra una lista de los 10 mejores puntajes con sus respectivos usuarios.
        Parámetros:
            top_diez (dict): Diccionario con los usuarios y sus puntajes.
            fuente (pygame.font.Font): Fuente utilizada para renderizar el texto.
    """
    ubicacion_x = 120
    ubicacion_y = 150
    imagen_top = pygame.image.load("imagenes/imagen_top10.png")
    imagen_top = pygame.transform.scale(imagen_top,(200,130))

    pantalla.blit(imagen_top,(245,5))
    ordenar_top_10(lista_partidas)
    for i in range(10):
        usuario_puntaje = f"{i+1}-{lista_partidas[i]['Nombre']}, Puntaje: {lista_partidas[i]['Puntaje']}, Fecha: {lista_partidas[i]['Fecha']}"
        blit_text(pantalla,usuario_puntaje,(ubicacion_x,ubicacion_y),fuente,COLOR_NEGRO)
        ubicacion_y += 60

