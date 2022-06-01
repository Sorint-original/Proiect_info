import pygame
import os

import ButtonClass

pygame.init()
screen = pygame.display.Info()
WIDTH = screen.current_w
HEIGHT = screen.current_h

h = HEIGHT - 110
while (round(h * 1.75) > WIDTH - 50) :
    h -=  1
w = round(h * 1.75)
x = (WIDTH - w) // 2
y = (HEIGHT - h) // 2
if y < 100 :
    y = 10

img = pygame.image.load("Assets/background/robou.png")
img = pygame.transform.scale(img, (WIDTH, HEIGHT))

#Testing ground below
from MapEditor import Editor

def Menu(WIN, WIDTH, HEIGHT, FPS):
    status = None #Value to decide for running in function...

    func_arg = ([Editor], WIN, WIDTH, HEIGHT, FPS)

    ButtonVec = []

    print(type(ButtonVec), type(func_arg))

    ButtonClass.Button_Load("MainMenu", ButtonVec) #load MainMenu for first time oppening

    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                 ButtonClass.checkButtonHover(event.pos[0], event.pos[1], ButtonVec)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                     status = ButtonClass.checkButtonClick(event.pos[0], event.pos[1], ButtonVec, func_arg)

            elif event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)

        if status != None:
            running = status

        WIN.fill((255,255,255))
        WIN.blit(img, (0,0))
        ButtonClass.displayButtons(WIN, ButtonVec)
        pygame.display.update()