import pygame
import math
import constantes

class Personaje(): #Las clases siempre la primera en mayuscula
    def __init__(self, x, y, animaciones, energia, tipo):   #Estariamos llamando al constructor de pygame 
        self.score = 0
        self.energia = energia
        self.vivo = True
        self.flip = False
        self.animaciones = animaciones 
        #Imagen de la animacion que se esta mostrando actualmente
        self.frame_index = 0
        #Con el siguiente se almacena la hora actual en milisegundos desde que se inicio pygame
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index ]
        self.shape = self.image.get_rect()                 #pygame.Rect(0, 0, constantes.WIDHT_PERSONAJE, constantes.HEIGHT_PERSONAJE)   #Le damos una forma, en este caso seria un rectngulo 
        self.shape.center = (x,y) 
        self.tipo = tipo
        self.golpe = False  #Para identificar cuando un jugador sea golpeado
        self.ultimo_golpe = pygame.time.get_ticks()  #Lo usaremos para el cooldown entre ataques de los enemigos 

           
    def actualizar_coordenadas(self, tupla):
        self.shape.center = (tupla[0], tupla[1])


    def enemigos(self, jugador, posicion_pantalla, obstaculos_tiles, exit_tile):
        #Lista vacia del clipped_line
        clipped_line = ()
        #Variables que usaremos para manejar la posicion de los enemigos
        ene_dx = 0 
        ene_dy = 0

        #Reposicionar enemigos respecto a la posicion de la pantalla o la camara 
        self.shape.x += posicion_pantalla[0]
        self.shape.y += posicion_pantalla[1]

        #Crear una linea de vision entre el personaje y los enemigos 
        linea_de_vision = ((self.shape.centerx, self.shape.centery), (jugador.shape.centerx, jugador.shape.centery))

        #Chequear si hay obstaculos en la line de vision del enemigo con el personaje 
        for obs in obstaculos_tiles:   #Si vamos al archivo mundo.py en la linea en que definimos los obstaculos, "self.obstaculos_tiles.append(tile_data)" estamos agregando a la lista "tile_data" el cual tiene como parametros: " tile_data = [image, image_rect, image_x, image_y]" y como vemos el dato 1 es image_rect que es la forma. Por eso aca ponemos 1 en los obstaculos, para identificar su forma 
            if obs[1].clipline(linea_de_vision):   #Este metodo de ".clipline" se usa para verificar colisciones entre una forma y una linea que es este caso serias las posiciones del jugador 
                clipped_line = obs[1].clipline(linea_de_vision)


        #Calculamos la distancia de los enemigos respecto del personaje para determinar cuando nos deben seguir usando pitagoras 
        distancia = math.sqrt(((self.shape.centerx - jugador.shape.centerx)**2) + (self.shape.centery - jugador.shape.centery)**2 )
        if not clipped_line and distancia < constantes.RANGO:
            #Condicio que identifica cuando el jugador esta mas a la derecha o izquierda del enemigo y lo persiga o se mueva hacia el 
            if self.shape.centerx > jugador.shape.centerx:
                ene_dx = -constantes.VELOCIDAD_ENEMIGOS 
            if self.shape.centerx < jugador.shape.centerx:
                ene_dx = constantes.VELOCIDAD_ENEMIGOS
            #Condicio que identifica cuando el jugador esta arriba o debajo del enemigo y lo persiga o se mueva hacia el 
            if self.shape.centery > jugador.shape.centery:
                ene_dy = -constantes.VELOCIDAD_ENEMIGOS  
            if self.shape.centery < jugador.shape.centery:
                ene_dy = constantes.VELOCIDAD_ENEMIGOS 

        self.movimiento(ene_dx, ene_dy, obstaculos_tiles, exit_tile)  #Usamos el metodo ya creado de movimiento en el que le entregamos las variables de su posicion y de los obstaculos para que no traspasen paredes 

        #Atacar al jugador 
        if distancia < constantes.RANGO_ATAQUE and jugador.golpe == False: 
            jugador.energia -= 10
            jugador.golpe = True
            jugador.ultimo_golpe = pygame.time.get_ticks()

    def update (self):
        #Comprobar si el personaje ha muerto
        if self.energia <= 0:   #Creamos esta condicion para limitar la vida de los enemigos que no siga restando y pasar a numeros negativos 
            self.energia = 0 
            self.vivo = False   #Cambiamos la variable que identifica cuando el enemigo llego a su vida 0
            
        #Timer para poder volver a recibir daño
        golpe_cooldown = 1000 
        if self.tipo == 1:
            if self.golpe == True:
                if pygame.time.get_ticks() - self.ultimo_golpe > golpe_cooldown:
                    self.golpe = False

        cooldown_animacion = 100
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = self.frame_index + 1 
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0


    def draw(self, interfaz): #Estamos definiendo como lo vamos a dibujar 
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)  #Necesitamos que el personaje se gire respecto a donde se mueve, con el comando flip lo podemos hacer determinando true o false en la coordenada x o y 
        interfaz.blit(imagen_flip, self.shape)
        #pygame.draw.rect(interfaz, constantes.COLOR_PERSONAJE, self.shape, 1)   #Estamos dibujando el cuadrado o figura que le asiganamos a la imagen del personaje, meramente para un control visual

    def movimiento(self, delta_x, delta_y, obstaculos_tiles, exit_tile): #Como se movera nuestro personaje 
        posicion_pantalla = [0, 0]
        nivel_completado = False  #Que usaremos pra identificar en que momento el personaje pasara al proximo nivel 
        if delta_x < 0:   #Condicion que le dira al programa cuando se debe invertir el personaje, al saber para donde se esta mviendo en el eje x 
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.shape.x = self.shape.x + delta_x
        #Con el siguiente for estamos evaluando en que momento el personaje tiene una colision en el eje x con algun tiled del tipo obstaculo 
        for obstacle in obstaculos_tiles:
            if obstacle[1].colliderect(self.shape):   #Ponemos el dato 1 de la lista ya que en la lista de tile_data de la clase mundo el dato 1 es la forma "image_rect"
                if delta_x > 0:
                    self.shape.right = obstacle[1].left 
                if delta_x < 0:
                    self.shape.left = obstacle[1].right 

        self.shape.y = self.shape.y + delta_y 
        #Con el siguiente for estamos evaluando en que momento el personaje tiene una colision en el eje y con algun tiled del tipo obstaculo 
        for obstacle in obstaculos_tiles:
            if obstacle[1].colliderect(self.shape):   #Ponemos el dato 1 de la lista ya que en la lista de tile_data de la clase mundo el dato 1 es la forma "image_rect"
                #Importante recordar que para pygame una posicion negativa en y significa que esta subiendo o yendo hacia arriba
                if delta_y > 0:
                    self.shape.bottom = obstacle[1].top #Bottom significa fondo / parte de abajo
                if delta_y < 0:
                    self.shape.top = obstacle[1].bottom

        #Crear la condicion que identifique solo a un tipo de personaje
        if self.tipo == 1:
            #Chequear colision con el tile de salida
            if exit_tile is not None:
                if exit_tile[1].colliderect(self.shape):
                    nivel_completado = True
                    print("Nivel Completado")

            #Actualizar la pantalla basado en la posicion del jugadr 
            #Mover la camara a la izquierda o derecha 
            if self.shape.right > (constantes.WIDHT_WINDOW - constantes.LIMITE_PANTALLA): 
                posicion_pantalla[0] = (constantes.WIDHT_WINDOW - constantes.LIMITE_PANTALLA) - self.shape.right
                self.shape.right = constantes.WIDHT_WINDOW - constantes.LIMITE_PANTALLA
            if self.shape.left < constantes.LIMITE_PANTALLA:
                posicion_pantalla[0] = constantes.LIMITE_PANTALLA - self.shape.left
                self.shape.left = constantes.LIMITE_PANTALLA

            #Mover la camara a la izquierda o derecha 
            if self.shape.bottom > (constantes.HEIGHT_WINDOW - constantes.LIMITE_PANTALLA): 
                posicion_pantalla[1] = (constantes.HEIGHT_WINDOW - constantes.LIMITE_PANTALLA) - self.shape.bottom
                self.shape.bottom = constantes.HEIGHT_WINDOW - constantes.LIMITE_PANTALLA
            if self.shape.top < constantes.LIMITE_PANTALLA:
                posicion_pantalla[1] = constantes.LIMITE_PANTALLA - self.shape.top
                self.shape.top = constantes.LIMITE_PANTALLA

            return posicion_pantalla, nivel_completado