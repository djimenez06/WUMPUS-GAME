import pygame

class Hedor(pygame.sprite.Sprite):
    def __init__(self,path,x,y) :
        super().__init__()
        self.has_collided = False
        self.imagePath=f'{path}/img/Hedor.png'
        self.image = pygame.image.load(f'{path}/img/Hedor.png').convert_alpha()  # Cargar imagen con transparencia
        self.image = pygame.transform.scale(self.image,(40,40))  # Escalar la imagen
        self.rect = self.image.get_rect()  # Obtiene el rectángulo del sprite
        self.rect.y = y
        self.rect.x = x        