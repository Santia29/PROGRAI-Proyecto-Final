import os
import json
import pygame
import random
#-----------------------------------MODULO DE FUNCIONES JUEGO ---------------------------------------------------

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    """
    La función blit_textse encarga de renderizar (dibujar) un texto sobre una superficie de Pygame
    de manera que se ajusten las palabras a la pantalla,
    respetando los saltos de línea y el ancho máximo de la superficie.
    """
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, False, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def crear_boton(path,coordenadas_escala_x,coordenadas_escala_y,coordenadas_en_x,coordenadas_en_y):
    """
    La función "crear_boton" crea un botón con una imagen especificada, 
    una escala determinada y una posición definida en una ventana de Pygame.

    path: El parámetro "path" en la función "crear_boton" es la ruta del archivo de la imagen que se usará para el botón. 
    coordenadas_escala_x: Se usa para especificar qué tan ancho debe ser el botón en píxeles tras 
    redimensionar la imagen original cargada desde la ruta dada.
    coordenadas_escala_y: Se utiliza para redimensionar la imagen del botón en base a las medidas de alto.
    coordenadas_en_x: Especifica la posición horizontal donde se ubicará el botón dentro de la ventana o área de visualización cuando se renderice.
    coordenadas_en_y: Se usa para posicionar el botón verticalmente dentro de la ventana o pantalla del juego.
    :return: Se devuelve un diccionario llamado `boton`. Este diccionario contiene dos pares clave-valor:
    1. Clave "superficie" con el valor siendo la imagen cargada y escalada del botón.
    2. Clave "rectangulo" con el valor siendo el objeto rectángulo que representa la posición del botón en la pantalla.
    
    Retorna el boton con su rectangulo.
    """
    imagen_boton = pygame.image.load(path).convert_alpha()
    imagen_boton = pygame.transform.scale(imagen_boton,(coordenadas_escala_x,coordenadas_escala_y))
    boton = {
        "superficie": imagen_boton,
        "rectangulo": imagen_boton.get_rect(topleft=(coordenadas_en_x, coordenadas_en_y))  
    }
    return boton

def cargar_preguntas_desde_csv(ruta_csv):
    """
    Lee un archivo CSV y carga su contenido en una lista de diccionarios.

    Descripción:
    Esta función permite procesar un archivo CSV donde la primera línea contiene los encabezados
    de las columnas. Cada fila posterior se convierte en un diccionario, utilizando los encabezados 
    como claves y los valores correspondientes de cada fila como valores. El resultado final es 
    una lista de diccionarios, donde cada diccionario representa una fila del archivo.

    Parámetros:
    ruta_csv (str): La ruta al archivo CSV que se desea leer.

    Retorno:
    list: Una lista de diccionarios. Cada diccionario tiene como claves los nombres de las columnas 
          (extraídos de la primera línea del archivo) y como valores los datos de las filas correspondientes.

    """
    lista_preguntas = []
    if os.path.exists(ruta_csv):
        with open(ruta_csv,"r", encoding='utf-8') as csvfile:
            primer_linea = csvfile.readline()
            primer_linea = primer_linea.replace("\n","")
            lista_claves = primer_linea.split(",")

            for linea in csvfile:
                linea_aux = linea.replace("\n","")      
                lista_valores = linea_aux.split(",")
                diccionario = {}   

                for i in range(len(lista_claves)):
                    diccionario[lista_claves[i]] = lista_valores[i]

                lista_preguntas.append(diccionario)    
    return lista_preguntas


def generar_csv(nombre_archivo:str,lista:list):
    """
    Genera un archivo CSV a partir de una lista de diccionarios.

    Descripción:
    Esta función toma una lista de diccionarios y genera un archivo CSV donde:
    - Las claves de los diccionarios forman los encabezados de las columnas.
    - Los valores de cada diccionario se convierten en filas del archivo.

    Parámetros:
    nombre_archivo (str): El nombre del archivo CSV que se generará (incluyendo extensión .csv).
    lista (list): Una lista de diccionarios, donde cada diccionario representa una fila del CSV.

    Retorno:
    No retorna ningún valor. Escribe el archivo en la ruta especificada.
    """
    if len(lista) > 0:
        lista_claves = list(lista[0].keys())
        separador = ","
        cabecera = separador.join(lista_claves)
        #print(cabecera)
        
        with open(nombre_archivo,"w", encoding = "utf-8") as archivo:
            archivo.write(cabecera + "\n")
            for elemento in lista:
                lista_valores = list(elemento.values())
                for i in range(len(lista_valores)):
                    lista_valores[i] = str(lista_valores[i])

                dato = separador.join(lista_valores)
                dato += "\n"
                archivo.write(dato)
    else:
        print("ERROR LISTA VACIA")


def generar_estadistica(pregunta,lista_preguntas:list,acierto:bool):
    """
    Actualiza las estadísticas de una pregunta en una lista de preguntas y guarda los cambios en un archivo CSV.

    Descripción:
    Esta función actualiza las estadísticas de una pregunta, registrando cuántas veces ha sido realizada,
    contabilizando aciertos o fallos, y recalculando el porcentaje de aciertos. Los cambios se reflejan 
    en un archivo CSV que almacena todas las preguntas con sus estadísticas.

    Parámetros:
    ----------
    pregunta (dict): Un diccionario que representa la pregunta, con los siguientes campos clave:
                     - "id": Identificador único de la pregunta.
                     - "cant_aciertos": Número de respuestas correctas.
                     - "cant_fallos": Número de respuestas incorrectas.
                     - "cant_veces_preguntada": Número total de veces que se ha realizado esta pregunta.
    lista_preguntas (list): Una lista de diccionarios, donde cada diccionario contiene información de una pregunta.
    acierto (bool): Indica si la respuesta fue correcta (`True`) o incorrecta (`False`).

    Retorno:
    -------
    No retorna ningún valor. Modifica `lista_preguntas` y actualiza el archivo CSV.
    """

    posicion = buscar_pregunta(lista_preguntas,pregunta["id"])
    lista_preguntas[posicion]["cant_veces_preguntada"] += 1
    if acierto:
        lista_preguntas[posicion]["cant_aciertos"] += 1
    else:
        lista_preguntas[posicion]["cant_fallos"] += 1
    porcentaje_aciertos = (pregunta["cant_aciertos"]/pregunta["cant_veces_preguntada"])*100
    lista_preguntas[posicion]["porc_aciertos"] = porcentaje_aciertos
    generar_csv("preguntas.csv",lista_preguntas) 
    

def normalizar_datos(lista:list):
    """
    Convierte los datos de una lista de preguntas a sus tipos esperados (int o float) si están en formato de cadena.

    Descripción:
    ------------
    Esta función itera sobre una lista de preguntas y verifica que ciertos valores clave dentro de cada pregunta tengan
    el tipo de dato correcto. Si algún valor está en formato de cadena (por ejemplo, al ser leído de un archivo CSV), 
    lo convierte al tipo esperado:
      - "porc_aciertos" -> float
      - "id", "cant_fallos", "cant_aciertos", "cant_veces_preguntada" -> int

    Parámetros:
    ------------
    - lista (list): Una lista de diccionarios donde cada diccionario representa una pregunta. 
      Las claves que se procesan son:
        - "porc_aciertos" (str o float): Porcentaje de aciertos.
        - "id" (str o int): Identificador único de la pregunta.
        - "cant_fallos" (str o int): Número de respuestas incorrectas.
        - "cant_aciertos" (str o int): Número de respuestas correctas.
        - "cant_veces_preguntada" (str o int): Total de veces que la pregunta ha sido realizada.

    Retorno:
    --------
    No retorna ningún valor. Modifica la lista en su lugar para normalizar los tipos de datos.

    """ 
    if len(lista) > 0:
        for pregunta in lista:
            if type(pregunta["porc_aciertos"]) == str and type(pregunta["porc_aciertos"]) != float:
                pregunta["porc_aciertos"] = float(pregunta["porc_aciertos"])
            if type(pregunta["id"]) == str and type(pregunta["id"]) != int:
                pregunta["id"] = int(pregunta["id"])
            if type(pregunta["cant_fallos"]) == str and type(pregunta["cant_fallos"]) != int:
                pregunta["cant_fallos"] = int(pregunta["cant_fallos"])
            if type(pregunta["cant_aciertos"]) == str and type(pregunta["cant_aciertos"]) != int:
                pregunta["cant_aciertos"] = int(pregunta["cant_aciertos"])
            if type(pregunta["cant_veces_preguntada"]) == str and type(pregunta["cant_veces_preguntada"]) != int:
                pregunta["cant_veces_preguntada"] = int(pregunta["cant_veces_preguntada"])




def buscar_pregunta(lista_preguntas:list,valor:int)->int:
    """
    Busca la posición de una pregunta en una lista de preguntas basada en su identificador ('id').

    Parámetros:
        lista_preguntas (list): Una lista de diccionarios donde cada diccionario representa una pregunta 
                             y contiene, entre otras posibles claves, la clave 'id'.

        valor (int): El identificador de la pregunta que se desea buscar.

    Retorna:
    int: La posición (índice) de la pregunta en la lista si se encuentra, o -1 si no se encuentra.
    
    """
    posicion = -1
    for i in range(len(lista_preguntas)):
        if lista_preguntas[i]["id"] == valor:
            posicion = i
    return posicion


def parse_json(nombre_archivo:str)->list:
    """
    Lee un archivo JSON y devuelve su contenido como una lista de elementos.

    Parámetros:
    nombre_archivo (str): El nombre o la ruta del archivo JSON a leer.

    Retorna:
    list: Una lista de elementos que contiene los datos del archivo JSON cargado.
    
    Excepciones:
    - Si el archivo no se encuentra o no se puede leer, se generará un error relacionado con el archivo.
    - Si el contenido del archivo no es un JSON válido, se generará un error de análisis.
    """
    lista_elementos = []  
    with open(nombre_archivo,"r") as archivo:
        lista_elementos = json.load(archivo)   
    return lista_elementos



def generar_json(nombre_archivo:str,lista:list)->None:
    """
    Genera un archivo JSON a partir de una lista de elementos y la guarda en el archivo especificado.

    Parámetros:
        nombre_archivo (str): El nombre o la ruta del archivo JSON donde se guardará la lista de elementos.

        lista (list): La lista de elementos que se desea guardar en el archivo JSON.

    Retorna:
    None: La función no retorna ningún valor, solo guarda los datos en el archivo.
    
    Excepciones:
    - Si hay un problema al abrir el archivo para escritura o al intentar guardar los datos, se generará un error relacionado con el archivo o con la conversión de datos a JSON.
    """
    
    with open(nombre_archivo,"w") as archivo:
        json.dump(lista,archivo,indent=4)



def ordenar_top_10(lista:list)->None:
    """
    Ordena la lista de participantes según su puntaje de mayor a menor utilizando el algoritmo de burbuja.

    Parámetros:
        lista (list): Una lista de diccionarios, donde cada diccionario representa un participante 
                  y contiene, al menos, una clave 'Puntaje' con el valor numérico del puntaje del participante.

    Retorna:
    None: La función no retorna ningún valor, pero modifica la lista original, ordenándola in-place.

    Descripción:
    La función implementa un algoritmo de ordenación tipo "burbuja" (bubble sort) para ordenar los participantes en 
    función de su puntaje. Los participantes con mayor puntaje estarán al principio de la lista y los de menor puntaje 
    al final. El algoritmo compara elementos consecutivos y los intercambia si están en el orden incorrecto.
    
    Excepciones:
    - Si los elementos en la lista no contienen la clave 'Puntaje', se generará un error KeyError al intentar acceder a esta clave.
    """
    
    for i in range(len(lista)):
                for j in range(i+1,len(lista)):
                    if lista[i]["Puntaje"] < lista[j]["Puntaje"]:
                        intercambiar_matriz(lista,i,j)


def intercambiar_matriz(lista,i,j):
    """
    Intercambia dos filas en la matriz.

    Parámetros:
    matriz (list): La matriz de listas a modificar.
    i (int): Índice de la primera fila a intercambiar.
    j (int): Índice de la segunda fila a intercambiar.

    Esta función intercambia los elementos en las posiciones `i` y `j` 
    dentro de la matriz proporcionada, utilizando una variable auxiliar.
    """
    aux = lista[i]
    lista[i] = lista[j]
    lista[j] = aux

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

lista_preguntas = cargar_preguntas_desde_csv('preguntas.csv')
normalizar_datos(lista_preguntas)
lista_partidas = parse_json("partidas.json")