import pygame
import random
import math
from pygame import mixer
from sys import exit

# initializing pygame
pygame.init()


# screen setup
screen = pygame.display.set_mode((800, 600))

# title & icon
pygame.display.set_caption("space invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# background
background = pygame.image.load("world.png")

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# player image
player_image = pygame.image.load("ufo.png")
px = 320
py = 450
pxmove = 0

# enemy image

enemy_image = []
ex = []
ey = []
exmove = []
eymove = []
numofenemies = 6

for i in range(numofenemies):
    enemy_image.append(pygame.image.load("alien.png"))
    ex.append(random.randint(0, 736))
    ey.append(random.randint(50, 150))
    exmove.append(5)
    eymove.append(40)

# bullet image
bullet_image = pygame.image.load("bullet.png")
bx = 0
by = 450
bxmove = 0
bymove = 10
bstate = "ready"


# score

score_value = 0
font = pygame.font.SysFont("comicsansms", 32)

tx = 10
ty = 10

#game over
over_font = pygame.font.SysFont("comicsansms", 64)

def show_score(x, y):
    score = font.render("score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(px, py):
    screen.blit(player_image, (px, py))


def enemy(ex, ey, i):
    screen.blit(enemy_image[i], (ex, ey))
    

# global helps to acess bstate
def fire_bullet(bx, by):
    global bstate
    bstate = "fire"
    screen.blit(bullet_image, (bx + 16, by + 10))


# bullet collision
def iscollision(bx, by, ex, ey):
    distance = math.sqrt((math.pow(ex - bx, 2)) + (math.pow(ey - by, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
run = True
while run:
    # RGB
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pxmove = -3
            if event.key == pygame.K_RIGHT:
                pxmove = 3
            if event.key == pygame.K_SPACE:
                if bstate :
                    crash_sound = pygame.mixer.Sound("laser.wav")
                    crash_sound.play()
                    bx = px
                    fire_bullet(bx, by)
        if event.type == pygame.KEYUP:
           if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               pxmove = 0

        if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# px = px + pxmove
    px += pxmove

    if px <= 0:
       px = 0
    elif px >= 770:
       px = 770

    for i in range(numofenemies):
        #game over
        if ey[i] > 440:
            for j in range(numofenemies):
                ey[j] = 2000
            game_over_text()
            break


        ex[i] += exmove[i]
        if ex[i] <= 0:
            exmove[i] +=5
            ey[i] += eymove[i]
        elif ex[i] >= 770:
            ey[i] += eymove[i]
            exmove[i] += -5

        collision = iscollision(ex[i], ey[i], bx, by)
        if collision:
         explosion_sound = pygame.mixer.Sound("explosion.wav")
         explosion_sound.play()
         by = 450
         bstate = "ready"
         score_value += 1
         print(score_value)
         ex[i] = random.randint(0, 736)
         ey[i] = random.randint(50, 150)
        enemy(ex[i], ey[i], i)

    if by <= 0:
        by = 450
        bstate = "ready"

    if bstate == "fire" :

        fire_bullet(bx, by)
        by -= bymove

    player(px, py)
    show_score(tx, ty)
    pygame.display.update()
