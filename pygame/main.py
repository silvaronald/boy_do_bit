import pygame
from pygame import display
from pygame.constants import KEYDOWN, KEYUP
import random

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Boy do Bit")

running = True

chao = 400

papai_noel_img = pygame.image.load('assets\santa-claus.png')
papai_noel_X = 35
papai_noel_Y = chao

rena_img = pygame.image.load('assets\deer.png')
rena_x = random.randint(screen_width, screen_width * 2)
rena_y = chao
velocidade_rena = 15

def draw(imagem, x, y):
    screen.blit(imagem, (x, y))

pular = False
velocidade_pulo_inicial = 10
velocidade_pulo = velocidade_pulo_inicial

while running:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                pular = True
    
    if pular == True:
        papai_noel_Y -= velocidade_pulo * 2.5

        velocidade_pulo -= 1
        
        if velocidade_pulo < -velocidade_pulo_inicial:
            pular = False

            velocidade_pulo = velocidade_pulo_inicial

    draw(rena_img, rena_x, rena_y)

    rena_x -= velocidade_rena

    if rena_x < 0:
        rena_x = random.randint(screen_width, screen_width * 2)

    draw(papai_noel_img, papai_noel_X, papai_noel_Y)

    pygame.time.delay(25)
    pygame.display.update()