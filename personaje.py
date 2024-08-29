import pygame
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

           
    def enemigos(self, posicion_pantalla):
        #Reposicionar enemigos respecto a la posicion de la pantalla o la camara 
        self.shape.x += posicion_pantalla[0]
        self.shape.y += posicion_pantalla[1]

    def update (self):
        #Comprobar si el personaje ha muerto
        if self.energia <= 0:   #Creamos esta condicion para limitar la vida de los enemigos que no siga restando y pasar a numeros negativos 
            self.energia = 0 
            self.vivo = False   #Cambiamos la variable que identifica cuando el enemigo llego a su vida 0
            
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

    def movimiento(self, delta_x, delta_y): #Como se movera nuestro personaje 
        posicion_pantalla = [0, 0] 
        if delta_x < 0:   #Condicion que le dira al programa cuando se debe invertir el personaje, al saber para donde se esta mviendo en el eje x 
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.shape.x = self.shape.x + delta_x
        self.shape.y = self.shape.y + delta_y  

        #Crear la condicion que identifique solo a un tipo de personaje
        if self.tipo == 1:
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
            return posicion_pantalla




