import pygame
import random

# Definir los tamaños de los pasos
STEP_X = 120
STEP_Y = 72

class Tesoro(pygame.sprite.Sprite):
    def __init__(self, path, wumpus_rect,jugador_rect=None):
        super().__init__()
        self.has_collided = False
        self.imagePath = f'{path}/img/Tesoro.png'
        self.image = pygame.image.load(f'{path}/img/Tesoro.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.reset_position(wumpus_rect,jugador_rect)

    def reset_position(self, wumpus_rect, jugador_rect):
        while True:
            # Genera una coordenada x aleatoria
            self.rect.x = random.randint(0, 4) * STEP_X + 35 
            self.rect.y = random.randint(0, 2) * STEP_Y + 20 
            # Verifica si la posición generada está ocupada por el Wumpus
            if not wumpus_rect.colliderect(self.rect) and not jugador_rect.colliderect(self.rect):
                break
