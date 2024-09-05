import pygame   
import constantes
from items import Item
from personaje import Personaje

obstaculos = []  #Aqui tendremos que colocar los tiles que actuarian como obstaculos, como las paredes. Se coloda el ID del tile que vemos en TILED

class Mundo():
    def __init__(self):
        self.map_tiles = []
        self.obstaculos_tiles = []
        self.exit_tile = None #Este lo usaremos para que el personaje pase de un nivel al otro, cuando toque ese tile
        self.lista_item = []
        self.lista_enemigo =[]

    def process_data(self, data, tile_list, item_imagenes, animaciones_enemigos):
        self.level_length = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list [tile]
                image_rect = image.get_rect()
                image_x = x * constantes.TILE_SIZE
                image_y = y * constantes.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]
                #Agregamos tiles a obstaculos
                if tile in obstaculos:
                    self.obstaculos_tiles.append(tile_data)
                
                #Tile de salida 
                elif tile == 100:    #El numero es el ID del tile que queremos que funciones como exit 
                    self.exit_tile = tile_data
                
                #Condicion para crear las monedas
                elif tile == 86:     #El numero es el ID del tile que represena el item (moneda en este caso)
                    moneda = Item(image_x, image_y, 0, item_imagenes[0])  #El sero que aparece dentro de la clase Item es la forma en que estamos definiendo el tipo e item que es 
                    self.lista_item.append(moneda)
                    tile_data[0] = tile_list[22]  #Con esto logramos cambiar el tile que veremos de fonde bajo item, para que no se vea feo 
                
                #Condicion para crear las posiones
                elif tile == 87:     #El item_imagenes[0] representa la posicion del item dentro de la lista item_imagenes en el main.py 
                    posion = Item(image_x, image_y, 1, item_imagenes[1])
                    self.lista_item.append(posion)
                    tile_data[0] = tile_list[22] 
                
                #Condicion para crear o generar un enemigo del tipo (Nombre del enemigo)
                elif tile ==  74:   #Importante este numero es el ID del tile que identificamos para nuestro personaje dentro del tileset y que ponemos en el mapa 
                    honguito = Personaje(image_x, image_y, animaciones_enemigos[3], 200, 2)    #Importante recordar que en las animaciones "[x]" es el numero con el que estamos identificando, el 200 es la energia o vida que le asignamos, y el ultimo dato es el tipo de enemigo de esta clase que tambien depende de como los estemos identificando en el archivo personaje.py
                    #Importante, en la lista de animaciones_enemigos, que podemos ver en el main, cuando cargamos las imagenes de los "enemigos" el numero se esta tomando de la posicion de la lista, la cual es la misma que como se tienen las carpetas en los archivos del juego 
                    self.lista_enemigo.append(honguito)
                    #Recordar que tenemos que agregar a la lista el enemigo en cuestion (en este caso el honguito)
                    tile_data[0] = tile_list[22]

                #Condicion para crear o generar un enemigo del tipo (Nombre del enemigo)
                elif tile ==  77:   #Importante este numero es el ID del tile que identificamos para nuestro personaje dentro del tileset y que ponemos en el mapa 
                    jefe_final1 = Personaje(image_x, image_y, animaciones_enemigos[0], 300, 2)    #Importante recordar que en las animaciones "[x]" es el numero con el que estamos identificando, el 200 es la energia o vida que le asignamos, y el ultimo dato es el tipo de enemigo de esta clase que tambien depende de como los estemos identificando en el archivo personaje.py
                    #Importante, en la lista de animaciones_enemigos, que podemos ver en el main, cuando cargamos las imagenes de los "enemigos" el numero se esta tomando de la posicion de la lista, la cual es la misma que como se tienen las carpetas en los archivos del juego 
                    self.lista_enemigo.append(jefe_final1)
                    #Recordar que tenemos que agregar a la lista el enemigo en cuestion (en este caso el jefe_final1)
                    tile_data[0] = tile_list[22]

                self.map_tiles.append(tile_data)

    
    def update(self, posicion_pantalla):
        for tile in self.map_tiles:
            tile[2] += posicion_pantalla[0]
            tile[3] += posicion_pantalla[1]
            tile[1].center = (tile[2], tile[3])

    
    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])    