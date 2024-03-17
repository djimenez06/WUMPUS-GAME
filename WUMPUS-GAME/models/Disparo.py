import pygame

class Disparo(pygame.sprite.Sprite):
    def __init__(self, path,x,y,incremento_x,incremento_y):
        super().__init__()
        self.incremento_x = incremento_x
        self.incremento_y = incremento_y
        self.image = pygame.image.load(f'{path}').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += self.incremento_x
        self.rect.y += self.incremento_y
        if self.rect.x > 600:
            self.kill()
        if self.rect.y > 300:
            self.kill()
        if self.rect.x < 0:
            self.kill()
        if self.rect.y < 0:
            self.kill()
