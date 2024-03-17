import pygame
import random

# Tamaño de los pasos del jugador
STEP_X = 120
STEP_Y = 70

class Pozo(pygame.sprite.Sprite):
    def __init__(self, path, wumpus_rect, tesoro_rect):
        super().__init__()
        self.has_collided = False
        self.imagePath=f'{path}/img/Pozo.png'
        self.image = pygame.image.load(f'{path}/img/Pozo.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.reset_position(wumpus_rect, tesoro_rect)

    def reset_position(self, wumpus_rect, tesoro_rect):
        while True:
            #genera coordenadas aleatorias
            self.rect.x = random.randint(0, 4) * STEP_X + 35
            self.rect.y = random.randint(0, 2) * STEP_Y + 15
            #verifica si la posicion esta ocupada 
            if not self.rect.colliderect(wumpus_rect) and not self.rect.colliderect(tesoro_rect):
                break
