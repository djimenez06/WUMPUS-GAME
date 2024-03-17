import pygame

class Jugador(pygame.sprite.Sprite):
    def __init__(self,path):
        super().__init__()
        self.name = ""
        self.vidas = 2
        self.municion = 1
        self.image = pygame.image.load(f'{path}/img/Player.png').convert_alpha()  # Cargar imagen con transparencia
        self.image = pygame.transform.scale(self.image,(70,60))  # Escalar la imagen
        self.rect = self.image.get_rect()  # Obtiene el rectángulo del sprite
        self.rect.y = 225
        self.rect.x = 35
        self.key_states = {}
        self.visited = [[False]*5 for _ in range(4)]


    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            # valida que la tecla seleccionada no se encuentre en el diccionario o este apagada, 
            # Esto para permitir que solo se genere la accion una vez apesar que se mantenga presionada
            # la tecla
            if pygame.K_w not in self.key_states or not self.key_states[pygame.K_w]:
                self.rect.y -= 72
                self.key_states[pygame.K_w] = True
        else:
            self.key_states[pygame.K_w] = False

        if keys[pygame.K_s]:
            if pygame.K_s not in self.key_states or not self.key_states[pygame.K_s]:
                self.rect.y += 72
                self.key_states[pygame.K_s] = True
        else:
            self.key_states[pygame.K_s] = False

        if keys[pygame.K_a]:
            if pygame.K_a not in self.key_states or not self.key_states[pygame.K_a]:
                self.rect.x -= 120
                self.key_states[pygame.K_a] = True
        else:
            self.key_states[pygame.K_a] = False

        if keys[pygame.K_d]:
            if pygame.K_d not in self.key_states or not self.key_states[pygame.K_d]:
                self.rect.x += 120
                self.key_states[pygame.K_d] = True
        else:
            self.key_states[pygame.K_d] = False
        
        # restricciones para que el jugador no se salga del tablero
        if self.rect.x > 515:
            self.rect.x = 515

        if self.rect.x < 35:
            self.rect.x = 35

        if self.rect.y > 225:
            self.rect.y = 225

        if self.rect.y < 20:
            self.rect.y = 20  
        
        i = self.rect.y // 72
        j = self.rect.x // 120
        self.visited[i][j] = True
        # print(f'{i}{j}---{self.visited[i][j]}')

def reset_position(self):
        self.rect.y = 225
        self.rect.x = 35
        self.vidas = 2
        self.municion = 1
        self.key_states = {}
        self.visited = [[False]*5 for _ in range(4)]