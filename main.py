import pygame 
import constantes
from personaje import Personaje
from weapons import Weapon
import os        #Esta libreria se us apara manejar archivos y carpetas 
from items import Item
from textos import DamageText
from mundo import Mundo
import csv #Para trabajar con este tipo de archivos donde estamos importando los niveles 

#FUNCIONES 
#Escalar imagenes
def escalar_img(image, scale):  #Es una funcion que nos simplifica el tener que escalar las imagenes, para no tener que hacerlo repetidas veces
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen

#Funcion para contar elementos
def contar_elementos(directorio):
    return len(os.listdir(directorio))

#Funcion listar nombres elementos 
def nombres_carpetas(directorio):
    return os.listdir(directorio)

#Aca estamos iniciando la libreria pygame
pygame.init() 
ventana = pygame.display.set_mode((constantes.WIDHT_WINDOW, constantes.HEIGHT_WINDOW))
pygame.display.set_caption("La Mazmorra") #Se usa para cambiar el nombre de la ventana 

#Variables 
posicion_pantalla = [0, 0] #Esta sera la que usaremos para las camaras, le damos los valores de 0, 0 que serian eje x y eje y

#Fuentes que usaremos en el juego 
font = pygame.font.Font("assets/fonts/Kaph-Regular.ttf", 15)

#Aca estamos importando las imagenes
#Vida 
corazon_vacio = pygame.image.load("assets\images\items\heart_animated_3.png").convert_alpha()
corazon_vacio = escalar_img(corazon_vacio, constantes.SCALE_CORAZON)
corazon_medio = pygame.image.load("assets\images\items\heart_animated_2.png").convert_alpha()
corazon_medio = escalar_img(corazon_medio, constantes.SCALE_CORAZON)
corazon_lleno = pygame.image.load("assets\images\items\heart_animated_1.png").convert_alpha()
corazon_lleno = escalar_img(corazon_lleno, constantes.SCALE_CORAZON)

#Personaje
animaciones = []
for i in range (2): #Usamos el ciclo for para iterar entre las diferentes imagenes del personaje para hacer la animacion de caminar o la que queramos
    img = pygame.image.load(f"assets\images\characters\player\player_{i}.png").convert_alpha()  #Este ultimo comando nos sirve para descartar algun error que pueda suceder cuando se cargue la imagen png
    img = escalar_img(img, constantes.SCALE_PERSONAJE)
    animaciones.append(img)

#Enemigos
directorio_enemigos = "assets\\images\\characters\\enemies"
tipo_enemigos = nombres_carpetas(directorio_enemigos)
animacion_enemigos = []
for eni in tipo_enemigos:
    lista_temp = []
    ruta_temp = f"assets\\images\\characters\\enemies\\{eni}"
    num_animaciones = contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_enemigo = pygame.image.load(f"{ruta_temp}\\{eni}_{i+1}.png").convert_alpha()
        img_enemigo = escalar_img(img_enemigo, constantes.SCALE_ENEMIGOS)
        lista_temp.append(img_enemigo)

    animacion_enemigos.append(lista_temp)

#Arma 
imagen_pistola = pygame.image.load(f"assets\\images\\weapons\\arma_1.png").convert_alpha()
imagen_pistola = escalar_img(imagen_pistola, constantes.SCALE_ARMA)

#Balas
imagen_balas = pygame.image.load(f"assets\\images\\weapons\\bullet_1.png").convert_alpha()
imagen_balas = escalar_img(imagen_balas, constantes.SCALE_BALA)

#Cargar imagenes del mundo 
tile_list = []
for x in range(constantes.TILE_TYPE):   #Itera entre la cantidad de tiles que tengamos, en este caso lo pusimos dentro de las constantes
    tile_image = pygame.image.load(f"assets\\images\\tiles\\tile ({x+1}).png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constantes.TILE_SIZE, constantes.TILE_SIZE))
    tile_list.append(tile_image)

#Darle una imagen a nuestro personaje
player_image = pygame.image.load("assets\images\characters\player\player_0.png")
player_image = escalar_img(player_image, constantes.SCALE_PERSONAJE) #Aca estariamos escalando nuestro personaje, si lo necesitaramos mas grande o mas chico, respecto a la constate SCALE_PERSONAJE

#Cargar imagen de los items 
posion_roja = pygame.image.load("assets\\images\\items\\posion.png").convert_alpha()
posion_roja = escalar_img(posion_roja, constantes.SCALE_POSION)

#Cargar imagen moneda
coin_images = []
ruta_img = "assets\images\items\coin"
num_coin_images = contar_elementos(ruta_img)
#print(f"Numero de imagenes de monedas: {num_coin_images}")     #Con esto solo vemos en la terminal el resultado del conteo para saber que la funcion lo esta haciendo correctamente
for i in range(num_coin_images):
    img = pygame.image.load(f"assets\images\items\coin\coin_{i+1}.png") #Importante usar el f para usar el f string para poner variables dentro del texto 
    img = escalar_img(img, constantes.SCALE_MONEDA)
    coin_images.append(img) 

#Creamos una funcion que nos permita dibujar en pantalla texto
def dibujar_texto(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x, y)) 


#Definir
def vida_jugador():
    c_mitad_dibujado = False 
    for i in range(5):   #Usamos el for i in range pero teniendo en cuenta que el ciclo empieza en 0 y no en 1 por tanto ponemos 4 imagenes, ya que tenemos 3 imagenes de corazones en este caso 
        if jugador.energia >= ((i+1)*20):
            ventana.blit(corazon_lleno, (8+i*40, 8))
        elif jugador.energia % 20 > 0 and c_mitad_dibujado == False:
            ventana.blit(corazon_medio, (8+i*40, 8))
            c_mitad_dibujado = True
        else:
            ventana.blit(corazon_vacio, (8+i*40, 8))

#Creamoss un world data que nos servira para crear nuestro escenario del juego 
world_data = []

#El siguiente for es para que cuando no se entregue nada, dibujo en pantalla un tile en especifico 
for fila in range(constantes.FILAS):
    filas = [23] * constantes.COLUMNAS
    world_data.append(filas)

print(filas)

#Cargar el archivo con el nivel 
with open("niveles/nivel_dangeun.csv", newline= '') as csvfile:   #nivel_test_dangeun.csv      nivel_text.csv    nivel_catacombs_2.csv
    reader = csv.reader(csvfile, delimiter= ',')    #Donde le estamos indicando que tipo de archivo es y como esta delimitado 
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            world_data[x][y] = int(columna)


world = Mundo()
world.process_data(world_data, tile_list)


#creamos una funcion que dibuje un grid en la pantalla 
def dibujar_grid():
    for x in range(30):
        pygame.draw.line(ventana, constantes.BLANCO, (x*constantes.TILE_SIZE, 0), (x*constantes.TILE_SIZE, constantes.HEIGHT_WINDOW))
        pygame.draw.line(ventana, constantes.BLANCO, (0, x*constantes.TILE_SIZE), (constantes.WIDHT_WINDOW, x*constantes.TILE_SIZE)) 



#Crear un jugador de la clase personaje
jugador = Personaje(50,50, animaciones, 50, 1) #Creamos una varable usando la clase que importamos del personaje, dandole las coordenadas x y y dentro del argumento

#Crear un enemigo de la clase personaje
jefe_final = Personaje(400, 300, animacion_enemigos[0], 500, 2) #Importante estamos dando el ultimo dato como el de la energia que debemos entregarlo para la clase personaje 
honguito = Personaje(200, 200, animacion_enemigos[1], 100, 2) 
goblin_2 = Personaje(700, 100, animacion_enemigos[2], 100, 2)

#Crear lista de enemigos 
lista_enemigos = []
lista_enemigos.append(jefe_final)
lista_enemigos.append(goblin_2)
lista_enemigos.append(honguito)

#Crear un arma de la clase weapon
pistola = Weapon(imagen_pistola, imagen_balas)

#Crear un grupo de sprites  
grupo_damage_text = pygame.sprite.Group()   #Creamos grupos para poder tener varios sprites al mismo tiempo en la pantalla 
grupo_balas = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()

coin = Item(350, 25, 0, coin_images)   #Con esto usamos la clase creada en el archivo items, clase item donde le damos una posicion y las imagenes
posion = Item(380, 55, 1, [posion_roja])

grupo_items.add(coin)
grupo_items.add(posion)
 

#Definir las variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

#Controlar el framerate para controlar el movimiento del personaje
reloj = pygame.time.Clock()

run = True  #Creamos el bucle general del juego
while run == True:

    #Como ponemos que vaya a esos 60 FPS
    reloj.tick(constantes.FPS)

    #Controlar el framerate para controlar el movimiento del personaje
    reloj = pygame.time.Clock()
    ventana.fill(constantes.COLOR_BG)  #Con el "fill" llenamos la pantalla del color definido

    dibujar_grid()

    #Calcular el movimiento del jugador
    delta_x = 0
    delta_y = 0

    if mover_derecha == True:
        delta_x = constantes.VELOCIDAD  #Se puso la velocidad como una constante para que sea mas sencillo en el caso de querer cambiarlo
    if mover_izquierda == True:
        delta_x = -constantes.VELOCIDAD
    if mover_arriba == True:
        delta_y = -constantes.VELOCIDAD
    if mover_abajo == True:
        delta_y = constantes.VELOCIDAD   

    #Mover al jugador
    posicion_pantalla = jugador.movimiento(delta_x, delta_y) #Llamando el mecanismo creado en el archivo del personaje para que se mueva 
    print(posicion_pantalla)

    #Actualizar mapa
    world.update(posicion_pantalla)

    #Actualiza el estado del jugador 
    jugador.update()

    #Actualiza el estado del enemigo 
    for ene in lista_enemigos:
        ene.update()
        #print(ene.energia)    #Con esto visualizamos la vida de cada entidad en la terminal 

    #Actualiza el estado del arma 
    bala = pistola.update(jugador)
    if bala:
        grupo_balas.add(bala)
    for bala in grupo_balas:
        damage, pos_damage = bala.update(lista_enemigos)   #Le entregamos la lista de enemigos para que se generen las colisones de las balas con esa lista de enemigos 
        if damage:   #Es lo mismo que decir: si damage es distinto de 0 
            damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, constantes.ROJO)
            grupo_damage_text.add(damage_text)

    #Actualizar daño
    grupo_damage_text.update(posicion_pantalla)

    #Actualizar items 
    grupo_items.update(posicion_pantalla, jugador)

    #Dibujar al mundo 
    world.draw(ventana)

    #Dibujar al jugador
    jugador.draw(ventana) #Llamamos el metodo "draw" que definimos para colocar donde lo queremos poner, al personaje creado

    #Dibujar al enemigo 
    for ene in lista_enemigos:
        ene.enemigos(posicion_pantalla)
        ene.draw(ventana)

    #Dibujar el arma 
    pistola.draw(ventana)

    #Dibujar balas
    for bala in grupo_balas:
        bala.draw(ventana)  

    #Dibujar los corazones 
    vida_jugador()
    dibujar_texto(f"Score: {jugador.score}", font, constantes.AMARILLO, 700, 5)

    #Dibujar textos
    grupo_damage_text.draw(ventana)

    #Dibujar items en pantalla 
    grupo_items.draw(ventana)

    for event in pygame.event.get(): #Con el "event.get" de la libreria estariamos obteniendo que fue lo que se hizo: click una tecla etc.
        if event.type == pygame.QUIT:   #Esto estaria evaluando en que momento sucede un evento del tipo salir, por ejemplo la x de la ventana o el alt f4
            run = False

        #Evaluar  cuando estamos presionando determinada tecla
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True

        #Para cuando se suelte la tecla que se esta presionando
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_a:
              mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False

    pygame.display.update()  #Es necesario ya que esto mantendr las actualizaciones que se hagan en el programa, mantener los cambios de la pantalla: dibujar objetos, actualizar imagenes etc. 

pygame.quit()