import pygame 
import constantes
import math
import random 

class Weapon():
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        self.imagen_original = image 
        self.angulo = 0 
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.shape = self.imagen.get_rect()
        self.disparar  = False
        self.ultimo_disparo = pygame.time.get_ticks()

    def update(self, personaje):
        disparo_cooldown = constantes.COOLDOWN_BALAS   #Creamos esta variable para controlar el disparo del arma, en este caso lo estamos limitando a 500 milisegundos que dejamos en las constantes para controlar mas facil sus valores
        bala = None
        self.shape.center = personaje.shape.center
        if personaje.flip == False:
            self.shape.x = self.shape.x + personaje.shape.width/2.2
            self.shape.y = self.shape.y + personaje.shape.height/6    #Con esto tomamos com referencia el alto del personaje, asi si cambiamos el personaje el arma tambien se ajustara
            self.rotar_arma(False)
        
        if personaje.flip == True:
            self.shape.x = self.shape.x - personaje.shape.width/2.2
            self.shape.y = self.shape.y + personaje.shape.height/6
            self.rotar_arma(True)

        #Mover el arma con el mouse 
        mouse_pos = pygame.mouse.get_pos()
        distancia_x = (mouse_pos[0] - (self.shape.centerx))   #Importante estamos calculando la posicion del mouse respecto a cada eje del arma de la clase weapon para luego calcular el movimiento respecto al mouse 
        distancia_y = -(mouse_pos[1] - (self.shape.centery))
        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))

        #Detectar los clicks del mouse 
        if pygame.mouse.get_pressed()[0] and self.disparar == False and (pygame.time.get_ticks()-self.ultimo_disparo >= disparo_cooldown):     #Con el pygame.mouse.get_pressed()[0] estamos diciendo: cuando el mouse este presionado es decir ese [0] equivale a un true 
            bala = Bullet(self.imagen_bala, self.shape.centerx, self.shape.centery, self.angulo)
            self.disparar = True
            self.ultimo_disparo = pygame.time.get_ticks()
        #Resetar el click del mouse 
        if pygame.mouse.get_pressed()[0] == False:
            self.disparar = False 
        return bala 


    def rotar_arma(self, rotar):
        if rotar == True:
            imagen_flip = pygame.transform.flip(self.imagen_original, True, False)   #El atributo de True o False hace refencia a si se va a girar en x o en y usando el comando ".flip" de la libreria "pygame.transform"
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        else:
            imagen_flip = pygame.transform.flip(self.imagen_original, False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)

    def draw(self, interfaz):
        self.imagen = pygame.transform.rotate(self.imagen, self.angulo)
        interfaz.blit(self.imagen, self.shape)
        #pygame.draw.rect(interfaz, constantes.COLOR_ARMA, self.shape, 1)      #Estamos dibujando el cuadrado o figura que le asiganamos a la imagen del arma, meramente para un control visual


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):   #Usamos el __init__ que es el constructor de pygame
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle 
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        #Calcular la velocidad de la bala 
        self.delta_x = math.cos(math.radians(self.angulo))*constantes.VELOCIDAD_BALAS
        self.delta_Y = -math.sin(math.radians(self.angulo))*constantes.VELOCIDAD_BALAS

    def update(self, lista_enemigos, obstaculos_tiles):
        daño = 0 
        pos_daño = None
        self.rect.x += self.delta_x
        self.rect.y += self.delta_Y 

        #Ver si las balas salieron de la pantalla 
        if self.rect.right < 0 or self.rect.left > constantes.WIDHT_WINDOW or self.rect.bottom < 0 or self.rect.top > constantes.HEIGHT_WINDOW:
            self.kill()

        #Verificar si hay colision con enemigos 
        for enemigo in lista_enemigos:
            if enemigo.shape.colliderect(self.rect): #Estariamos evaluando cuando choca la forma de nuestra bala con la forma de nuestro enemigo
                daño =  15 + random.randint(-7,7) #Creamos la variable que se encargara de almacenar cuanto le quitaremos de vida al enemigo 
                pos_daño = enemigo.shape    #Con esto estamos asociando el texto del daño con la posicion del enemigo para que aparezca en esa misma posicion 
                enemigo.energia -= daño 
                self.kill()                       #Con esto borramos la bala luego de que choque, este emtodo de kill no funciona para los personajes, porque no son del tipo sprite, este solo sirve para el metodo sprite
                break

        #Verificar si hay colision con algun muro/obstaculo
        for obs in obstaculos_tiles:
            if obs[1].colliderect(self.rect):  #Itereamos entre la lista "obstaculos_tiles" tomando el valor [1] ya que este corresponde a la forma de dicho obstaculo y usando ".colliderect" para comparar si choca con la forma de la bala "self.rect"
                self.kill()   #Ya que las balas son sprites, podemos usar el .kill para eliminarlo
        
        return daño, pos_daño


    def draw(self, interfaz):
        interfaz.blit(self.image, (self.rect.centerx, self.rect.centery - int(self.image.get_height()/1.2)))
        #pygame.draw.rect(interfaz, constantes.COLOR_ARMA, self.rect, 1)   #Estamos dibujando el cuadrado o figura que le asiganamos a la imagen de la bala, meramente para un control visual



