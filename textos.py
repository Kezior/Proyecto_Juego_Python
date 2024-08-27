import pygame.sprite

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, font, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.contador = 0    #Creamos este contador que iniciamos en 0 para luego tener control de en que momento se debe borrar el texto de daño en la pantalla 
        
    def update(self):
        self.rect.y -= 2   #Se debe restar para que vaya hacia arriba, con este update estamos creando el movimineto del texto del daño al enemigo 
        self.contador += 1
        if self.contador > 25:
            self.kill()