import pygame.sprite

class Item(pygame.sprite.Sprite):
    def __init__ (self, x, y, item_type, animacion_list):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type #0 seran las monedas y 1 seran las posiones
        self.animaciones_list = animacion_list
        self.frame_index = 0   #Esto nos permitira decirle en que posicion esta al programa, dentro de las imagenes
        self.update_time = pygame.time.get_ticks()   #Esto guarda el tiempo cuando se ejecuta, para cambiarl el tiempo de la animacion 
        self.image = self.animaciones_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self, personaje):
        #Comprobar colision entre el personaje y los items 
        if self.rect.colliderect(personaje.shape):    #Aca tenemos en cuenta el tipo de item que es asignado en la clase Item
            #Monedas 
            if self.item_type == 0:
                personaje.score +=1 
            #Posiones
            elif self.item_type == 1:
                personaje.energia += 50 
                if personaje.energia > 100:
                    personaje.energia = 100
            self.kill()



        cooldown_animacion = 45  #Esta dado en milesimas de segundo 
        self.image = self.animaciones_list[self.frame_index] 

        if pygame.time.get_ticks() - self.update_time > cooldown_animacion:
            self.frame_index += 1 
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones_list):
            self.frame_index = 0 