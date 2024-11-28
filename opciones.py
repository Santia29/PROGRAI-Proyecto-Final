import pygame 
from constantes import *
from funciones import *
import config
from juego import sonido_correcto,error_sonido


pygame.init() #Inicio del proyecto

pantalla = pygame.display.set_mode((700, 800))

#Fuente
fuente_boton = pygame.font.SysFont("Arial Rounded MT Bold",23)
fuente_volumen =  pygame.font.SysFont("Arial Rounded MT Bold",50)
fuente_cartel_volumen = pygame.font.SysFont("Arial Rounded MT Bold",40) #TITULO QUE CONTIENE "AJUSTAR SONIDO"
fuente_cartel_musica = pygame.font.SysFont("Ariel Rounded MT Bold",40)#TITULO QUE CONTIENE "AJUSTAR EFECTOS DE SONIDO"
fuente_cartel_efectos = pygame.font.SysFont("Arial Rounded MT Bold",40) #TITULO QUE CONTIENE "AJUSTAR EFECTOS"

fondo_de_pantalla = pygame.image.load("imagenes\preguntados_1.jpg")
fondo_de_pantalla = pygame.transform.scale(fondo_de_pantalla,(700,800))

#Botones
boton_suma_musica = crear_boton("imagenes/boton.png",50,70,620,200)
boton_resta_musica = crear_boton("imagenes/boton.png",50,70,20,200)
boton_volver = crear_boton("imagenes/boton.png",170,50,260,750)
boton_suma_musica = crear_boton("imagenes/boton.png",50,70,620,450)
boton_resta_musica = crear_boton("imagenes/boton.png",50,70,20,450)
boton_suma_efectos = crear_boton("imagenes/boton.png",50,70,620,70)
boton_resta_efectos = crear_boton("imagenes/boton.png",50,70,20,70)


#Volumen
volumen = 100
volumen_efectos = 100
volumen_click_sonido = 100

#Sonido de click
click_sonido = pygame.mixer.Sound("sonidos/click.mp3")
click_sonido.set_volume(volumen_click_sonido/100)

#Volumen de la musica
volumen_encendido_musica = crear_boton("imagenes/activo.png",90,90,150,600)
volumen_apagado_musica = crear_boton("imagenes/mute.png",90,90,450,600)
recuadro_volumen_musica = pygame.image.load("imagenes/boton.png")
recuadro_volumen_musica = pygame.transform.scale(recuadro_volumen_musica,(125,90))

#Efectos de sonido
volumen_encendido_efectos = crear_boton("Imagenes/activo.png",90,90,150,200)
volumen_apagado_efectos = crear_boton("imagenes/mute.png",90,90,450,200)
recuadro_volumen_efectos = pygame.image.load("imagenes/boton.png")
recuadro_volumen_efectos = pygame.transform.scale(recuadro_volumen_efectos,(125,90))

def mostrar_opciones(pantalla:pygame.Surface,eventos):
    global volumen
    global volumen_efectos

    retorno = "opciones"
    
    for evento in eventos:
        pygame.mixer.music.set_volume(config.volumen / 100)
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_suma_musica['rectangulo'].collidepoint(evento.pos):
                if config.volumen < 96: 
                    config.volumen += 5
                    click_sonido.play()
            elif boton_resta_musica['rectangulo'].collidepoint(evento.pos):
                if config.volumen > 0: 
                    config.volumen -= 5
                    click_sonido.play()
            elif boton_volver['rectangulo'].collidepoint(evento.pos):
                retorno = "menu"
                click_sonido.play()
            elif volumen_apagado_musica['rectangulo'].collidepoint(evento.pos):
                config.volumen = 0
            elif volumen_encendido_musica['rectangulo'].collidepoint(evento.pos):
                config.volumen = 100

            #Manipula los eventos de los efectos del juego
            elif boton_suma_efectos["rectangulo"].collidepoint(evento.pos):
                 if volumen_efectos < 96:
                    volumen_efectos += 5
                    sonido_correcto.set_volume(volumen_efectos / 100)
                    error_sonido.set_volume(volumen_efectos / 100)
                    click_sonido.play()

            elif boton_resta_efectos["rectangulo"].collidepoint(evento.pos):
                if volumen_efectos > 0:
                    volumen_efectos -= 5
                    # Actualizamos el volumen de los tres sonidos
                    error_sonido.set_volume(volumen_efectos / 100)
                    sonido_correcto.set_volume(volumen_efectos / 100)
                    click_sonido.play()
                 
            elif volumen_apagado_efectos["rectangulo"].collidepoint(evento.pos):
                volumen_efectos = 0
                sonido_correcto.set_volume(0)
                error_sonido.set_volume(0)
                
            elif volumen_encendido_efectos["rectangulo"].collidepoint(evento.pos):
                volumen_efectos = 100
                # Restauramos el volumen de los tres sonidos
                sonido_correcto.set_volume(1)
                error_sonido.set_volume(1)
        #Sonido de musica
        elif evento.type == pygame.KEYDOWN:  # Detecta teclas presionadas
            print(f"Tecla presionada: {evento.key}")
            if evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS:  # Tecla '+' (normal y en el teclado numérico)
                if config.volumen < 96:
                    config.volumen += 5
                    click_sonido.play()
            elif evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:  # Tecla '-' (normal y en el teclado numérico)
                if config.volumen > 0:
                    config.volumen -= 5
                    click_sonido.play()
        elif evento.type == pygame.QUIT:
            retorno = "salir"
    # Sincronizar el volumen global con la configuración
    volumen = config.volumen

    #Dibujo en pantalla        
    pantalla.blit(fondo_de_pantalla,(0,0))
    titulo_boton_musica = fuente_cartel_volumen.render("AJUSTAR SONIDO",True,COLOR_DORADO)
    pantalla.blit(titulo_boton_musica,(207,400))
    titulo_boton_efectos = fuente_cartel_efectos.render("AJUSTAR EFECTOS",True,COLOR_DORADO)
    pantalla.blit(titulo_boton_efectos,(207,20))
    
    pantalla.blit(boton_resta_efectos['superficie'],boton_resta_efectos['rectangulo'])
    pantalla.blit(boton_suma_efectos['superficie'],boton_suma_efectos['rectangulo'])
    pantalla.blit(boton_resta_musica['superficie'],boton_resta_musica['rectangulo'])
    pantalla.blit(boton_suma_musica['superficie'],boton_suma_musica['rectangulo'])   
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])

    pantalla.blit(volumen_encendido_efectos['superficie'], volumen_encendido_efectos['rectangulo'])
    pantalla.blit(volumen_apagado_efectos['superficie'], volumen_apagado_efectos['rectangulo'])
    pantalla.blit(recuadro_volumen_efectos, (275, 100))
    pantalla.blit(volumen_encendido_musica['superficie'],volumen_encendido_musica['rectangulo'])
    pantalla.blit(volumen_apagado_musica['superficie'],volumen_apagado_musica['rectangulo'])
    pantalla.blit(recuadro_volumen_musica,(275,500))

    blit_text(boton_suma_efectos['superficie'],"VOL +",(5,25),fuente_boton,COLOR_NEGRO)
    blit_text(boton_resta_efectos['superficie'],"VOL -",(5,25),fuente_boton,COLOR_NEGRO)
    blit_text(boton_volver['superficie'],"VOLVER",(50,20),fuente_boton,COLOR_NEGRO)
    blit_text(boton_suma_musica['superficie'],"VOL +",(5,25),fuente_boton,COLOR_NEGRO)
    blit_text(boton_resta_musica['superficie'],"VOL -",(5,25),fuente_boton,COLOR_NEGRO)
    blit_text(pantalla,f"{volumen} %",(300,530),fuente_volumen,COLOR_NEGRO)
    blit_text(pantalla,f"{volumen_efectos} %",(280,132),fuente_volumen,COLOR_NEGRO)     

    return retorno