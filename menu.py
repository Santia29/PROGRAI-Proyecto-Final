
#-------------------------------- VENTANA MENU DEL JUEGO -------------------------------------------

import pygame
from constantes import *
from funciones import *
from juego import *

pygame.init() #Inicio el proyecto
pantalla = pygame.display.set_mode(PANTALLA)
#Fuente
fuente_menu = pygame.font.SysFont("Arial Black",24)

#Botones
# boton_jugar = {"superficie":pygame.Surface(TAMAÑO_BOTON),"rectangulo":pygame.Rect(0,0,0,0)}
# boton_jugar['superficie'].fill(COLOR_DORADO)
#Imagen de interfaz
fondo_de_pantalla = pygame.image.load("imagenes\preguntados_1.jpg")
fondo_de_pantalla = pygame.transform.scale(fondo_de_pantalla,(700,800))

imagen_juego = pygame.image.load("imagenes/title_game_1.png")
imagen_juego = pygame.transform.scale(imagen_juego,(500,100))

# pantalla.blit(imagen_juego,(125,180))
# pantalla.blit(fondo_de_pantalla,(700,800))


boton_jugar = crear_boton("imagenes/boton.png",270,100,210,150)
boton_opciones = crear_boton("imagenes/boton.png",270,100,210,290)
boton_puntuaciones = crear_boton("imagenes/boton.png",270,100,210,430)
boton_salir = crear_boton("imagenes/boton.png",270,100,210,570)


#Sonido
click_sonido = pygame.mixer.Sound("sonidos/click.mp3")
click_sonido.set_volume(1)
        
def mostrar_menu(pantalla:pygame.Surface,eventos):
    retorno = "menu" #Un estado de la ventana en la que estoy parado
    
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_jugar["rectangulo"].collidepoint(evento.pos):
                print("JUGAR")
                click_sonido.play()
                retorno = "juego"
            elif boton_opciones["rectangulo"].collidepoint(evento.pos):
                print("OPCIONES")
                click_sonido.play()
                retorno = "opciones"
            elif boton_puntuaciones["rectangulo"].collidepoint(evento.pos):
                print("PUNTUACIONES")
                click_sonido.play()
                retorno = "puntuaciones"
            elif boton_salir["rectangulo"].collidepoint(evento.pos):
                click_sonido.play()
                print("SALIR")
                retorno = "salir"
        elif evento.type == pygame.QUIT:
            retorno = "salir" #El estado salir -> Cuando se le da a la X
    
    #Dibujo en pantalla 

    pantalla.blit(fondo_de_pantalla,(0,0)) 
    pantalla.blit(imagen_juego,(100,40))
    
    # pantalla.blit(boton,(125,180))
    # boton_jugar["rectangulo"] = pantalla.blit(boton_jugar["superficie"],(210,300))
    pantalla.blit(boton_jugar["superficie"], boton_jugar["rectangulo"])
    pantalla.blit(boton_opciones["superficie"], boton_opciones["rectangulo"])
    pantalla.blit(boton_puntuaciones["superficie"], boton_puntuaciones["rectangulo"])
    pantalla.blit(boton_salir["superficie"], boton_salir["rectangulo"])
    
    #Texto en los botones
    blit_text(boton_jugar['superficie'],"JUGAR",(70,30),fuente_menu,COLOR_NEGRO)
    blit_text(boton_opciones['superficie'],"OPCIONES",(50,30),fuente_menu,COLOR_NEGRO)
    blit_text(boton_puntuaciones['superficie'],"PUNTUACIONES",(20,30),fuente_menu,COLOR_NEGRO)
    blit_text(boton_salir['superficie'],"SALIR",(72,30),fuente_menu,COLOR_NEGRO)
    
    pygame.display.flip()
    return retorno #Retorna el estado al que va a ir principal
