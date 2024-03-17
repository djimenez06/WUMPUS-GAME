#Carga libreria 
import pygame
import os
import pygame.freetype
import random
import sqlite3

# Carga de modelos de objetos
from models.Jugador import Jugador
from models.Wumpus import Wumpus
from models.Tesoro import Tesoro
from models.Pozo import Pozo
from models.Hedor import Hedor
from models.Brisa import Brisa
from models.Disparo import Disparo

# Definir los tamaños de los pasos
STEP_X = 120
STEP_Y = 72

# Definir las dimensiones de la pantalla
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Inicializar Pygame
pygame.init()
clock = pygame.time.Clock()
font1 = pygame.font.Font(None, 36)
pygame.mixer.music.load('sounds/Ambient.mp3')
pygame.mixer.music.play(-1) #reproduce en bucle inf

runningGeneral=True
# Crear la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# ruta absoluta del directorio de trabajo actual del programa
absolute_path=os.getcwd().replace("\\", "/")
# Cargar ObjetosInteractuar
jugador = None
wumpus = None
tesoro = None
pozo = None
sprite_player = None
sprite_enemys = None




# Cargar la imagen de inicio
start_image = pygame.image.load('img/START2.jpg')
start_image = pygame.transform.scale(start_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
image_tablero = pygame.image.load('img/fondotablero.jpg')
image_tablero = pygame.transform.scale(image_tablero,(600,300))
image_inventario = pygame.image.load('img/inventario.jpg')
image_inventario = pygame.transform.scale(image_inventario,(600,500))
image_Municion = pygame.image.load('img/municionUp.png')
image_Municion = pygame.transform.scale(image_Municion,(30,30))
image_Vidas = pygame.image.load('img/vidas.png')
image_Vidas = pygame.transform.scale(image_Vidas,(30,30))


# Crear una conexión a la base de datos SQLite
conn = sqlite3.connect('game_data.db')
c = conn.cursor()

# Crear una tabla para almacenar los datos del juego si no existe
c.execute('''CREATE TABLE IF NOT EXISTS game_results
             (player_name text, time_text integer)''')

# Funcion que define todos los agentes del juego
def define_agents():   
    global jugador, wumpus, tesoro, pozo, sprite_enemys, sprite_player 
    sprite_enemys = pygame.sprite.Group()
    sprite_player =pygame.sprite.Group()
    # Cargar ObjetosInteractuar
    jugador = Jugador(absolute_path) 
    wumpus = Wumpus(absolute_path)
    wumpus_rect = wumpus.rect 
    tesoro = Tesoro(absolute_path, wumpus_rect,jugador.rect) 
    pozo = Pozo(absolute_path, wumpus.rect, tesoro.rect)
    sprite_player.add(jugador)
    sprite_enemys.add(tesoro)
    sprite_enemys.add(wumpus)
    sprite_enemys.add(pozo)

# Insertar los datos del jugador y el tiempo tomado cuando gane el juego
def insert_game_result(player_name, time_text):
    c.execute("INSERT INTO game_results VALUES (?, ?)", (player_name, time_text))
    conn.commit()



def show_game_results():
    # print("Ejecutando showgameresult")
    c.execute("SELECT * FROM game_results ORDER BY time_text LIMIT 5")  # Seleccionar los mejores 5 resultados
    results = c.fetchall()
    
    # Si hay resultados, los mostramos
    if results:
        font_size = 30
        font = pygame.font.Font(None, font_size)
        line_spacing = 5  # Espacio entre líneas

        # Posición inicial para dibujar el texto
        x = 330
        y = 460

        for i, result in enumerate(results):
            # Coordenadas para el contador
            x_counter = x
            y_counter = y + i * (font_size + line_spacing)
            text_counter = f"{i+1}."
            text_surface = font.render(text_counter, True, (0, 0, 255))
            screen.blit(text_surface, (x_counter, y_counter))

            # Coordenadas para el nombre
            x_name = x + 50
            y_name = y + i * (font_size + line_spacing)
            text_name = result[0]
            text_surface = font.render(text_name, True, (0, 0, 255))
            screen.blit(text_surface, (x_name, y_name))

            # Coordenadas para el tiempo
            x_time = x + 150
            y_time = y + i * (font_size + line_spacing)
            text_time = f"{result[1]}      S"
            text_surface = font.render(text_time, True, (0, 0, 255))
            screen.blit(text_surface, (x_time, y_time))

    else:
        text_result = "No hay resultados aún"
        font_size = 25
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text_result, True, (0, 0, 255))
        screen.blit(text_surface, (330, 455))  # Posición inferior derecha



# Función para mostrar la pantalla de inicio
def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.blit(start_image, (0, 0))
        pygame.display.update()

# Función para mostrar las instrucciones 
def instructions_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
        screen.fill((0, 0, 0))  # Llenar la pantalla de negro

        text = font1.render("Instrucciones: ...", True, (255, 255, 255))
        text1 = font1.render("Presiona *W* para Subir", True, (255, 255, 255))
        text2 = font1.render("Presiona *A* para Ir a la Derecha", True, (255, 255, 255))
        text3 = font1.render("Presiona *S* para Bajar", True, (255, 255, 255))
        text4 = font1.render("Presiona *D* para Ir a la Izquierda", True, (255, 255, 255))
        text5 = font1.render("Presiona las teclas de: ", True, (255, 255, 255))
        text6 = font1.render("  *UP DOWN LEFT RIGHT*", True, (255, 255, 255))
        text7 = font1.render("Para disparar a esas direcciones ", True, (255, 255, 255))
        
        screen.blit(text, (210, 100))
        screen.blit(text1, (130, 200))
        screen.blit(text2, (130, 235))
        screen.blit(text3, (130, 270))
        screen.blit(text4, (130, 305))
        screen.blit(text5, (130, 340))
        screen.blit(text6, (130, 375))
        screen.blit(text7, (130, 410))

        pygame.display.update()

# Funcion que dibuja la pantalla para volver a jugar
def draw_playAgain():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        screen.fill((0, 0, 0))  # Llenar
        text_msg =font1.render("¿Deseas volver a jugar?", True, (255, 255, 255))
        screen.blit(text_msg, (10, 300))
        text_msg =font1.render("Presione Enter para Regresar el Menu inicial", True, (255, 255, 255))
        screen.blit(text_msg, (10, 350))
        pygame.display.update()


# Funcion que dibuja vidas
def draw_vidas():
    screen.fill((0, 0, 0))  # Llenar la pantalla de negro
    screen.blit(image_Vidas, (250, 300))
    text_vidas = font1.render(f'{jugador.vidas}', True, (255,255, 255))
    screen.blit(text_vidas, (300, 300))
    pygame.display.update()
    pygame.time.delay(2000)

# Función que permite ingresar el nombre del jugador
def get_namePlayer():
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.freetype.Font(None, 32)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        jugador.name = text
                        if jugador.name == '':
                            jugador.name = f"Jugador{random.randint(1, 99999)}"
                        text = ''
                        text_msg =font1.render("¡¡¡¡¡¡LISTO PREPARATE!!!!", True, (255, 0, 0))
                        screen.blit(text_msg, (input_box.x, input_box.y+90))
                        pygame.display.update()
                        pygame.time.delay(2000)
                        draw_vidas()
                        
                        # Mostrar los mejores 5 jugadores después de ingresar el nombre
                        show_game_results()
                        pygame.display.update()

                        return
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        screen.fill((30, 30, 30))
        txt_surface, _ = font.render(text, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))

        text_msg =font1.render("    Ingrese su nombre de Jugador: ", True, (255, 255, 255))
        screen.blit(text_msg, (input_box.x, input_box.y-30))

        text_msg =font1.render("    Presione Enter para continuar", True, (255, 255, 255))
        screen.blit(text_msg, (input_box.x, input_box.y+60))

        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)

def draw_camino():
    # Dibujar los bloques visitados
    for i in range(4):
        for j in range(5):
            if jugador.visited[i][j]:
                pygame.draw.rect(screen, (222, 163, 55), pygame.Rect(j*120, i*70, 120, 90))

# Función para dibujar imágenes de hedor alrededor del Wumpus
def generate_hedor():
    sprite_enemys.add(Hedor(absolute_path,wumpus.rect.x, wumpus.rect.y - STEP_Y + 15)) # Arriba del Wumpus
    sprite_enemys.add(Hedor(absolute_path,wumpus.rect.x, wumpus.rect.y + STEP_Y + 15))  # Abajo del Wumpus
    sprite_enemys.add(Hedor(absolute_path,wumpus.rect.x - STEP_X + 5, wumpus.rect.y + 20))  # Izquierda del Wumpus
    sprite_enemys.add(Hedor(absolute_path,wumpus.rect.x + STEP_X + 5, wumpus.rect.y + 20))  # Derecha del Wumpus
    
# Funcion que identifica si el jugador puede ver el elemento o aun no ha pasado por esa casilla
def draw_enemys():
    for enemy in sprite_enemys:
        cord_x=enemy.rect.x // 120
        if isinstance(enemy,Pozo):
            cord_y=(enemy.rect.y // 70)
        else:
            cord_y=(enemy.rect.y // 75)
        try:    
            if jugador.visited[cord_y][cord_x]:
                screen.blit(enemy.image, (enemy.rect.x, enemy.rect.y))
                enemy.has_collided = True
            else:
                enemy.has_collided = False
        except:
            pass

# Función para dibujar imágenes de brisa alrededor del Pozo
def generate_brisa():
    sprite_enemys.add(Brisa(absolute_path,pozo.rect.x, pozo.rect.y - STEP_Y + 10))  # Arriba del Pozo
    sprite_enemys.add(Brisa(absolute_path,pozo.rect.x, pozo.rect.y + STEP_Y + 20))  # Abajo del Pozo
    sprite_enemys.add(Brisa(absolute_path,pozo.rect.x - STEP_X + 5, pozo.rect.y + 10))  # Izquierda del Pozo
    sprite_enemys.add(Brisa(absolute_path,pozo.rect.x + STEP_X + 5, pozo.rect.y + 10))  # Derecha del Pozo

def draw_msg(text,color=(255, 255, 255)):
    screen.fill((0, 0, 0))  # Llenar la pantalla de negro
    text_msg =font1.render(text, True, color)
    screen.blit(text_msg, (30,300))
    pygame.display.update()
    pygame.time.delay(2000)

# Funcion para identificar si el jugador ha colisionado con el enemigo o el tesoro
def check_collision():
    for enemy in sprite_enemys:
        if pygame.sprite.collide_rect(jugador, enemy):
            if isinstance(enemy, Wumpus) and not enemy.has_collided:
                draw_msg("   ¡¡¡¡¡¡Has sido devorado por el \n Wumpus!!!!",(255, 0, 0))
                jugador.vidas=jugador.vidas - 1
                draw_vidas()

            if isinstance(enemy, Tesoro) and not enemy.has_collided:
                draw_msg("      ¡¡¡¡¡¡Has encontrado el \n tesoro!!!!",(225, 180, 10))
                insert_game_result(jugador.name, pygame.time.get_ticks() // 1000)  # Insertar resultado del juego
                show_game_results()  # Mostrar los resultados actualizados

            if isinstance(enemy, Pozo) and not enemy.has_collided:
                draw_msg("      ¡¡¡¡¡¡Has caido en un pozo!!!!",(0, 0, 255))
                jugador.vidas=jugador.vidas - 1
                draw_vidas()

            if isinstance(enemy, Hedor) and not enemy.has_collided:
                draw_msg("     .....¿Un hedor inusual?.....",(74, 222, 55))

            if isinstance(enemy, Brisa) and not enemy.has_collided:
                draw_msg("     .....¿Una brisa de viento?...",(55, 186, 222))

# Identificar si se presiono la tecla de disparo
def check_fire(event):
    if event.type == pygame.KEYDOWN and jugador.municion>0:  # Se presionó una tecla
        if event.key == pygame.K_UP:  # La tecla presionada fue la flecha hacia arriba
            sprite_player.add(Disparo(f'img/MunicionUp.png',jugador.rect.x, jugador.rect.y,0,-5))
            jugador.municion = jugador.municion - 1
        elif event.key == pygame.K_DOWN:  # La tecla presionada fue la flecha hacia abajo
            sprite_player.add(Disparo(f'img/MunicionDown.png',jugador.rect.x, jugador.rect.y,0,5))
            jugador.municion = jugador.municion - 1
        elif event.key == pygame.K_LEFT:  # La tecla presionada fue la flecha hacia la izquierda
            sprite_player.add(Disparo(f'img/MunicionLeft.png',jugador.rect.x, jugador.rect.y,-5,0))
            jugador.municion = jugador.municion - 1
        elif event.key == pygame.K_RIGHT:  # La tecla presionada fue la flecha hacia la derecha
            sprite_player.add(Disparo(f'img/MunicionRight.png',jugador.rect.x, jugador.rect.y,5,0))
            jugador.municion = jugador.municion - 1

# Validar si el disparo colisiono con el enemigo
def check_collisionFire():
    for enemy in sprite_enemys:
        if isinstance(enemy,Hedor):
            sprite_enemys.remove(enemy)

def draw_inventario():
    text_nombre = font1.render(f'{jugador.name}', True, (0, 0, 0))
    screen.blit(text_nombre, (50, 405))

    screen.blit(image_Municion, (40, 505))
    text_municion = font1.render(f'{jugador.municion}', True, (0, 0, 0))
    screen.blit(text_municion, (150, 515))

    screen.blit(image_Vidas, (40, 540))
    text_vidas = font1.render(f'{jugador.vidas}', True, (0, 0, 0))
    screen.blit(text_vidas, (150, 550))

def game_screen():
    generate_hedor()
    generate_brisa()
    start_time = pygame.time.get_ticks()
    running = True
    while running:
        
        current_time = pygame.time.get_ticks()  # Tiempo actual
        elapsed_time = (current_time - start_time) // 1000  # Tiempo transcurrido en segundos
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                check_fire(event)

        sprite_player.update()  # Actualizar las posiciones de los sprites

        for disparo in sprite_player:
            if isinstance(disparo, Disparo):
                if disparo.rect.colliderect(wumpus.rect):
                    sprite_player.remove(disparo)
                    sprite_enemys.remove(wumpus)
                    check_collisionFire()
                    draw_msg("             ¡¡¡¡¡¡Has matado al Wumpus!!!!",(255, 0, 0))

        # Valida la colisión con los enemigos
        check_collision()
        
        # Verifica si el tesoro ha sido encontrado
        if tesoro.has_collided:
            tesoro.has_collided=False
            draw_msg("                 ¡¡Felicidades Ganaste!!",(225, 180, 10))
            insert_game_result(jugador.name, pygame.time.get_ticks() // 1000)  # Insertar resultado del juego
            pygame.time.delay(5000) 
            running = False  
        
        screen.fill((0, 0, 0))  # Llenar la pantalla de negro
        
        screen.blit(image_inventario, (0, 300))
        draw_camino()
        sprite_player.draw(screen)
        draw_enemys()
        draw_inventario()
        show_game_results()  # Mostrar los resultados actualizados

        
        # Verificar la cantidad de vidas del jugador
        if jugador.vidas == 0:
            draw_msg("             ¡¡Perdiste todas tus vidas!!",(255, 0, 0))
            pygame.time.delay(5000)  # Opcional: Agrega un retraso antes de cerrar el juego
            running = False  # Terminar el bucle principal del juego
            
        time_font = pygame.font.Font(None, 20)  # Tamaño de fuente 20  puntos
    
        # Mostrar el contador de tiempo en pantalla
        time_text = time_font.render(f'Tiempo: {elapsed_time} segundos', True, (255, 255, 255))
        screen.blit(time_text, (10, 300))

        clock.tick(60)
        pygame.display.flip()

    #Bloque que pinta la opcion de volver a jugar
    


while runningGeneral:
    define_agents()
    # Mostrar la pantalla de inicio
    start_screen()

    # Mostrar las instrucciones
    instructions_screen()

    # Solicita nombre jugador
    get_namePlayer()

    # Reiniciar la posición del Wumpus antes de iniciar el juego
    wumpus.reset_position()

    # Iniciar el juego
    game_screen()

    # Pregunta si desea volver a jugar
    draw_playAgain()