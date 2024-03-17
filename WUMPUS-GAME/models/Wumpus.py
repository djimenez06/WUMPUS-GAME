import pygame
import random

# Tamaño de los pasos del jugador
STEP_X = 120
STEP_Y = 75

class Wumpus(pygame.sprite.Sprite):
    def __init__(self, path):
        super().__init__()
        self.has_collided = False
        self.imagePath=f'{path}/img/Wumpus.png'
        self.image = pygame.image.load(f'{path}/img/Wumpus.png').convert_alpha()
        self.image.set_colorkey((0,0,0))
        self.image = pygame.transform.scale(self.image,(70,60))
        self.rect = self.image.get_rect() # Obtiene el rectángulo del sprite
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(1, 2) * STEP_X + 35 # Genera una coordenada x aleatoria
        self.rect.y = random.randint(1, 2) * STEP_Y + 13   # Genera una coordenada y aleatoria
