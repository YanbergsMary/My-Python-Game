import pygame
import random
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
import os

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200
FPS_VALUE = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

FONT = pygame.font.SysFont('Verdana', 20)
FONT2 = pygame.font.SysFont('Verdana', 60)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('Python Game/background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Python Game/goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (140, 60)
player = pygame.image.load('Python Game/player.png').convert_alpha()
player_rect = pygame.Rect((WIDTH/2)-(player.get_width()/2), (HEIGHT/2)-(player.get_height()/2), *player_size)
player_move_down = [0, 8]
player_move_up = [0, -8]
player_move_right = [8, 0]
player_move_left = [-8, 0]

def create_enemy():
    enemy_size = (100, 40)
    enemy = pygame.transform.scale(pygame.image.load('Python Game/enemy.png').convert_alpha(), enemy_size)
    enemy_rect = pygame.Rect(WIDTH, random.randint(50, HEIGHT-50), *enemy_size)
    enemy_move = [random.randint(-16, -12), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (100, 160)
    bonus = pygame.transform.scale(pygame.image.load('Python Game/bonus.png').convert_alpha(), bonus_size)
    bonus_rect = pygame.Rect(random.randint(100, WIDTH-100), -160, *bonus_size)
    bonus_move = [0, 7]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 7000)

PLAYER_ANIMATION_CHANGE = pygame.USEREVENT + 3
pygame.time.set_timer(PLAYER_ANIMATION_CHANGE, 150)

enemies = []
bonuses = []
score = 0
image_index = 0

playing = True
while playing:
    FPS.tick(FPS_VALUE)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == PLAYER_ANIMATION_CHANGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
        
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            main_display.blit(FONT2.render("GAME OVER",True, RED), ((WIDTH/2)-200, (HEIGHT/2)-50))
            pygame.display.flip()
            pygame.time.delay(2000)
            playing = False
    
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(f"РАХУНОК: {score}",True, WHITE), (WIDTH-200, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < -enemy[0].get_width():
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT + bonus[0].get_width():
            bonuses.pop(bonuses.index(bonus))