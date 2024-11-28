import pygame 
from funciones import *
from constantes import *
import datetime
from juego import blit_texto_en_boton
pygame.init() #Inicio del proyecto

#Fuente
fuente =  pygame.font.SysFont("Arial Rounded MT Bold",35)
fuente_aceptar = pygame.font.SysFont("Arial Narrow", 25)

#Elemetos interfaz
cuadro = {"superficie":pygame.Surface(CUADRO_TEXTO),"rectangulo":pygame.Rect(0,0,0,0)}
cuadro['superficie'].fill(pygame.Color('azure3')) # Le asigno un color a esa superficie

#Boton
boton_aceptar = crear_boton("imagenes/boton.png",170,50,260,500)

#Sonidos
click_sonido = pygame.mixer.Sound("sonidos/click.mp3")
click_sonido.set_volume(1)

#Imagenes
mensaje = pygame.image.load("imagenes/mensaje.png")
mensaje = pygame.transform.scale(mensaje,TAMAÑO_PREGUNTA)
imagen = pygame.image.load("imagenes/game_over.png") #Imagen final partida/game-over
imagen = pygame.transform.scale(imagen,(190,190))

nombre = ""
fecha_hoy = datetime.date.today()
fecha_formato_perzonalizado = fecha_hoy.strftime("%d/%m/%Y")

def mostrar_juego_terminado(pantalla:pygame.Surface,eventos,puntaje):
    global nombre
    retorno = "terminado"
    
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_aceptar['rectangulo'].collidepoint(evento.pos):
                click_sonido.play()
                partida = {"Nombre":nombre,"Puntaje":puntaje,"Fecha":fecha_formato_perzonalizado}
                lista_partidas.append(partida)
                generar_json("partidas.json",lista_partidas)
                retorno = "menu"
                nombre = ''
                blit_texto_en_boton(cuadro['superficie'],nombre,(10,10),fuente,COLOR_BLANCO)
                cuadro['superficie'].fill(pygame.Color('azure3'))        
        elif evento.type == pygame.QUIT:
            retorno = "salir"
        if evento.type == pygame.KEYDOWN:
            bloc_mayus = pygame.key.get_mods() and pygame.KMOD_CAPS
            letra_presionada = pygame.key.name(evento.key)
            if letra_presionada == 'backspace' and len(nombre) > 0:
                nombre = nombre[:-1]#Elimino el último
                cuadro['superficie'].fill(pygame.Color('azure3'))
            if letra_presionada == 'space':
                nombre += " "
            if len(letra_presionada) == 1 and letra_presionada.isalpha(): 
                if bloc_mayus:
                    nombre += letra_presionada.upper()
                else:
                    nombre += letra_presionada
        elif evento.type == pygame.QUIT:
            retorno = "salir"
            
        fondo_de_pantalla = pygame.image.load("imagenes\preguntados_1.jpg")
        fondo_de_pantalla = pygame.transform.scale(fondo_de_pantalla,(700,800))
        pantalla.blit(fondo_de_pantalla,(0,0))
        cuadro['rectangulo'] = pantalla.blit(cuadro['superficie'],(210,390))
        pantalla.blit(mensaje,(175,280))
        pantalla.blit(imagen,(250,10))
        pantalla.blit(boton_aceptar["superficie"], boton_aceptar["rectangulo"])
        
        #Texto en los botones
        blit_text(cuadro['superficie'],nombre,(10,10),fuente,COLOR_NEGRO)
        blit_text(pantalla,f"Usted obtuvo: {puntaje} puntos",(195,220),fuente,COLOR_NEGRO)
        blit_text(boton_aceptar['superficie'],"ACEPTAR",(48,20),fuente_aceptar,COLOR_NEGRO)

    top_10_puntajes = parse_json("partidas.json")
    ordenar_top_10(top_10_puntajes)
    pygame.display.flip()
    return retorno