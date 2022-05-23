import pygame
import os

import ButtonClass

#Testing ground below
from Lobby import initializare_info
from MapEditor import Editor

def Menu(WIN, WIDTH, HEIGHT, FPS):
    status = None #Value to decide for running in function...

    func_arg = ([Editor, lobby], WIN, WIDTH, HEIGHT, FPS)

    ButtonVec = []

    print(type(ButtonVec), type(func_arg))

    ButtonClass.Button_Load("MainMenu", ButtonVec) #load MainMenu for first time oppening

    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            print(str(event))
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
        ButtonClass.displayButtons(WIN, ButtonVec)
        pygame.display.update()