import pygame 
from constantes import *
from menu import *
from juego import *
from reglas import *
from opciones import *
from terminado import *
from puntuaciones import *
import opciones
import juego

pygame.init() #Inicio del proyecto

#Configuracion de la pantalla
pantalla = pygame.display.set_mode(PANTALLA) #Se crea una ventana
pygame.display.set_caption("Preguntados")

#Variables
ventana_actual = 'menu'
corriendo = True
bandera_juego = True
FPS = 60
clock = pygame.time.Clock() 

while corriendo:
    clock.tick(FPS) #Control de fps
    
    if ventana_actual == 'menu':
        ventana_actual = mostrar_menu(pantalla,pygame.event.get())
    elif ventana_actual == 'opciones':
        ventana_actual = mostrar_opciones(pantalla,pygame.event.get())
    elif ventana_actual == 'juego':
        if bandera_juego:
            pygame.mixer.music.load("sonidos/music_fondo.mp3") #Define musica de fondo mientras juego
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(opciones.volumen / 100) #Ajusta el sonido de la música de fondo para que sea el mismo que en las opciones
            bandera_juego = False
        ventana_actual = mostrar_juego(pantalla,pygame.event.get())
    elif ventana_actual == 'puntuaciones':
        ventana_actual = mostrar_puntuaciones(pantalla,pygame.event.get())
    elif ventana_actual == 'reglas':
        ventana_actual = mostrar_reglas(pantalla,pygame.event.get())    
    elif ventana_actual == 'terminado':
        if bandera_juego == False:
            pygame.mixer.music.stop() #Detiene mi música de fondo
            bandera_juego = True
        ventana_actual = mostrar_juego_terminado(pantalla,pygame.event.get(),juego.puntuacion)
    elif ventana_actual == 'salir':
        corriendo = False
            
    pygame.display.flip() #Actualiza la informacion

pygame.quit() #Finaliza pygame