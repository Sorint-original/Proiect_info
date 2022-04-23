import pygame
import os

import ButtonClass

#Testing ground below

from Lobby import lobby

#Testing changes

stop = False

def Menu(screen, FPS):

    ButtonVec = []

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
                     ButtonClass.checkButtonClick(event.pos[0], event.pos[1], ButtonVec)

            elif event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
               
        screen.fill((255,255,255))
        ButtonClass.displayButtons(screen, ButtonVec)
        pygame.display.update()

