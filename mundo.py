import pygame   
import constantes
from items import Item
from personaje import Personaje

obstaculos = [1088,1089,1090,1280,1281,1282,1232,1233,1234,1040,1041,1042,1141,1142,1189,1190,1093,1094,1562,1563,1516,1564,1656,1466,1467,1419,1420,1516,1418,1468,1472,1473,1474,1424,1425,1426,1184,1185,1186,1136,
              1137,1138,992,993,994,944,945,946,947,948,995,996,1043,1044,949,950,997,998,1045,1046,101,1328,1329,1330,1376,1377,1378,0,1,2,3,4,5,48,49,50,51,52,53,96,97,100,101,144,145,148,149,192,193,196,197,240,
              241,242,243,244,245,288,289,290,291,292,293,336,337,338,339,340,341,151,152,153,154,199,202,247,248,249,250,162,163,164,165,166,167,168,169,170,171,172,173,353,354,355,356,357,358,359,360,361,362,363,
              364,365,387,388,433,434,435,436,437,438,482,483,484,485,530,531,532,533,577,582,625,626,627,628,629,630,675,676,723,724,912,913,914,915,916,917,918,919,920,921,961,968,1009,1016,1057,1058,1059,1060,1061,
              1062,1063,1064,1202,1203,1204,1205,1155,1156,877,878,879,880,925,928,971,972,973,976,977,978,1019,1026,1067,1068,1069,1072,1073,1074,1117,1120,1165,1166,1167,1168,1261,1262,1263,1264,1309,1312,1355,1356,
              1357,1360,1361,1362,1403,1410,1453,1454,1501,1502,1248,1249,1250,1251,1296,1297,1298,1299,1301,1344,1345,1346,1347,1348,1349,1392,1393,1394,1395,1396,1397,800,801,802,803,804,848,849,850,851,852,896,897,
              898,899,900,1072,1073,1466,1419,1414,1462,1463,1415,1509,1415,1559,1657,1656,1655,1413,1607,1170,1171]  #Aqui tendremos que colocar los tiles que actuarian como obstaculos, como las paredes. Se coloda el ID del tile que vemos en TILED
puerta_cerrada = []   #Introducimos cada ID del tile que represente una puerta en nuestro mundo 

class Mundo():
    def __init__(self):
        self.map_tiles = []
        self.capa_fondo = []
        self.capa_principal = []
        self.obstaculos_tiles = []
        self.exit_tile = None #Este lo usaremos para que el personaje pase de un nivel al otro, cuando toque ese tile
        self.portal_images = None
        self.portal_frame_index = 0
        self.portal_update_time = pygame.time.get_ticks()
        self.win_tile = None
        self.win_images = None
        self.win_frame_index = 0
        self.win_update_time = pygame.time.get_ticks()
        self.lista_item = []
        self.lista_enemigo =[]
        self.puertas_cerradas_tiles = []

    def process_data(self, data_fondo, data_principal, tile_list, item_imagenes, animaciones_enemigos, portal_images, win_images):
        self.level_length = len(data_principal[0])
        self.portal_images = portal_images
        self.win_images = win_images

        for y, row in enumerate(data_fondo):
            for x, tile in enumerate(row):
                image = tile_list [tile]
                image_rect = image.get_rect()
                image_x = x * constantes.TILE_SIZE
                image_y = y * constantes.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y, tile]

                self.capa_fondo.append(tile_data)

        for y, row in enumerate(data_principal):
            for x, tile in enumerate(row):
                image = tile_list [tile]
                image_rect = image.get_rect()
                image_x = x * constantes.TILE_SIZE
                image_y = y * constantes.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y, tile]
                #Agregamos tiles a obstaculos
                if tile in obstaculos:
                    self.obstaculos_tiles.append(tile_data)
                
                #Tile de puertas 
                if tile in puerta_cerrada:
                    self.puertas_cerradas_tiles.append(tile_data)

                #Tile de salida 
                elif tile == 1197:    #El numero es el ID del tile que queremos que funciona como exit 
                    image_portal = self.portal_images[0]
                    self.exit_tile = [self.portal_images[0], image_portal.get_rect(), image_x, image_y]    # pygame.Rect(image_x, image_y, constantes.TILE_SIZE, constantes.TILE_SIZE)
                    tile_data[0] = tile_list[826] 

                #Tile de win
                elif tile == 1053:
                    image_win = self.win_images[0]
                    self.win_tile = [self.win_images[0], image_win.get_rect(), image_x, image_y]    # pygame.Rect(image_x, image_y, constantes.TILE_SIZE, constantes.TILE_SIZE)
                    tile_data[0] = tile_list[235] 

                #CREAR ITEMS
                #Condicion para crear las monedas
                elif tile == 1145:     #El numero es el ID del tile que represena el item (moneda en este caso)
                    moneda = Item(image_x, image_y, 0, item_imagenes[0])  #El sero que aparece dentro de la clase Item es la forma en que estamos definiendo el tipo e item que es 
                    self.lista_item.append(moneda)
                    tile_data[0] = tile_list[510]  #Con esto logramos cambiar el tile que veremos de fonde bajo item, para que no se vea feo 
                
                #Condicion para crear las posiones
                elif tile == 1146:     #El item_imagenes[0] representa la posicion del item dentro de la lista item_imagenes en el main.py 
                    posion = Item(image_x, image_y, 1, item_imagenes[1])
                    self.lista_item.append(posion)
                    tile_data[0] = tile_list[508]
                                 #CREAR LOS ENEMIGOS RESPECTO A SU NOMBRE EN LA CARPETA
                #Enemigos base
                elif tile ==  1292:
                    skeleton = Personaje(image_x, image_y, animaciones_enemigos[8], 150, 2, 10, constantes.RANGO, 6)  
                    self.lista_enemigo.append(skeleton)
                    tile_data[0] = tile_list[508]

                elif tile ==  1291:
                    skeleton2 = Personaje(image_x, image_y, animaciones_enemigos[9], 100, 2, 15, constantes.RANGO, 6)  
                    self.lista_enemigo.append(skeleton2)
                    tile_data[0] = tile_list[508]

                elif tile ==  1338:
                    golem_blue = Personaje(image_x, image_y, animaciones_enemigos[5], 200, 2, 20, constantes.RANGO, 5)  
                    self.lista_enemigo.append(golem_blue)
                    tile_data[0] = tile_list[559]

                elif tile ==  1339:
                    golem_orange = Personaje(image_x, image_y, animaciones_enemigos[6], 200, 2, 20, constantes.RANGO, 5)  
                    self.lista_enemigo.append(golem_orange)
                    tile_data[0] = tile_list[559]

                #Jefes 
                elif tile ==  1289:
                    boss_dark_samurai = Personaje(image_x, image_y, animaciones_enemigos[1], 500, 2, 40, constantes.RANGO, 8)  
                    self.lista_enemigo.append(boss_dark_samurai)
                    tile_data[0] = tile_list[511]
                
                elif tile ==  1051:
                    boss_final = Personaje(image_x, image_y, animaciones_enemigos[3], 800, 2, 70, constantes.RANGO, 10)  
                    self.lista_enemigo.append(boss_final)
                    tile_data[0] = tile_list[1170]

                elif tile ==  1050:
                    boss_demon = Personaje(image_x, image_y, animaciones_enemigos[2], 750, 2, 40, constantes.RANGO, 9)  
                    self.lista_enemigo.append(boss_demon)
                    tile_data[0] = tile_list[520]

                elif tile ==  857:
                    zapallo = Personaje(image_x, image_y, animaciones_enemigos[10], 1000, 2, 1000, constantes.RANGO, 20)  
                    self.lista_enemigo.append(zapallo)
                    tile_data[0] = tile_list[526]
                
                self.capa_principal.append(tile_data)


    def cambiar_puerta(self, jugador, tile_list):
        buffer = 50 #Esto representa la proximidad del jugador (en pixeles)
        proximidad_rect = pygame.Rect(jugador.shape.x - buffer, jugador.shape.y - buffer, jugador.shape.width + 2 * buffer, jugador.shape.height + 2 * buffer)
        for tile_data in self.map_tiles:
            image, rect, x, y, tile_type = tile_data
            if proximidad_rect.colliderect(rect):
                if tile_type in puerta_cerrada:
                    if tile_type == 36 or tile_type == 66:   #Estos numeros son el ID de las puertas del lado derecho
                        new_tile_type = 57     #Puerta abierta del lado derecho
                    elif tile_type == 37 or tile_type == 67:  #Estos numeros son el ID de las puertas del lado derecho
                        new_tile_type = 58    #Puerta abierta del lado derecho
                    
                    tile_data[-1] = new_tile_type  #El -1 de la lista significa el ultimo valor de la lista del tile_data, tambien se podria usar la posicion normal ej: 5 o 6
                    tile_data[0] = tile_list[new_tile_type]

                    #Eliminar el tile de la lista de colisones 
                    if tile_data in self.obstaculos_tiles:
                        self.obstaculos_tiles.remove(tile_data)

                    return True
        return False

    def update(self, posicion_pantalla):
        for tile in self.capa_principal :
            tile[2] += posicion_pantalla[0]
            tile[3] += posicion_pantalla[1]
            tile[1].center = (tile[2], tile[3])
        for tile in self.capa_fondo :
            tile[2] += posicion_pantalla[0]
            tile[3] += posicion_pantalla[1]
            tile[1].center = (tile[2], tile[3])
        if self.exit_tile:
            self.exit_tile[2] += posicion_pantalla[0]
            self.exit_tile[3] += posicion_pantalla[1]
            self.exit_tile[1].center = (self.exit_tile[2], self.exit_tile[3])

            cooldown_animacion = 50  # Ajusta este valor para cambiar la velocidad de la animación
            if pygame.time.get_ticks() - self.portal_update_time > cooldown_animacion:
                self.portal_frame_index = (self.portal_frame_index + 1) % len(self.portal_images)
                self.exit_tile[0] = self.portal_images[self.portal_frame_index]
                self.portal_update_time = pygame.time.get_ticks()
        
        if self.win_tile:
            self.win_tile[2] += posicion_pantalla[0]
            self.win_tile[3] += posicion_pantalla[1]
            self.win_tile[1].center = (self.win_tile[2], self.win_tile[3])

            cooldown_animacion = 50  # Ajusta este valor para cambiar la velocidad de la animación
            if pygame.time.get_ticks() - self.win_update_time > cooldown_animacion:
                self.win_frame_index = (self.win_frame_index + 1) % len(self.win_images)
                self.win_tile[0] = self.win_images[self.win_frame_index]
                self.win_update_time = pygame.time.get_ticks()
         
    def draw(self, surface):
        for tile in self.capa_fondo:
            surface.blit(tile[0], tile[1])  
        for tile in self.capa_principal:
            surface.blit(tile[0], tile[1])  
        if self.exit_tile:
            surface.blit(self.exit_tile[0], self.exit_tile[1]) 
        if self.win_tile:
            surface.blit(self.win_tile[0], self.win_tile[1]) 