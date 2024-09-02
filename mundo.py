import pygame   
import constantes
from items import Item

obstaculos = []  #Aqui tendremos que colocar los tiles que actuarian como obstaculos, como las paredes. Se coloda el ID del tile que vemos en TILED

class Mundo():
    def __init__(self):
        self.map_tiles = []
        self.obstaculo_tiles = []
        self.exit_tile = None #Este lo usaremos para que el personaje pase de un nivel al otro, cuando toque ese tile
        self.lista_item = []

    def process_data(self, data, tile_list, item_imagenes):
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
                    self.obstaculo_tiles.append(tile_data)
                #Tile de salida 
                elif tile == 100:    #El numero es el ID del tile que queremos que funciones como exit 
                    self.exit_tile = tile_data
                elif tile == 86:     #El numero es el ID del tile que represena el item (moneda en este caso)
                    moneda = Item(image_x, image_y, 0, item_imagenes[0])  #El sero que aparece dentro de la clase Item es la forma en que estamos definiendo el tipo e item que es 
                    self.lista_item.append(moneda)
                    tile_data[0] = tile_list[22]  #Con esto logramos cambiar el tile que veremos de fonde bajo item, para que no se vea feo 
                elif tile == 87:     #El item_imagenes[0] representa la posicion del item dentro de la lista item_imagenes en el main.py 
                    posion = Item(image_x, image_y, 1, item_imagenes[1])
                    self.lista_item.append(posion)
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