import pygame
import os

import JocS

import ButtonClass

#Testing ground below

ButtonClass.Button_Load(ButtonClass.currentScene) #load MainMenu for first time oppening

clock = pygame.time.Clock()

while JocS.running:
    clock.tick(60)
    for event in pygame.event.get():
        print(str(event))
        if event.type == pygame.MOUSEMOTION:
            ButtonClass.checkButtonHover(event.pos[0], event.pos[1])

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                ButtonClass.checkButtonClick(event.pos[0], event.pos[1])

        elif event.type == pygame.QUIT:
            JocS.running = False
    
    JocS.WIN.fill((255,255,255))
    ButtonClass.displayButtons(JocS.WIN)
    pygame.display.update()


pygame.quit()
#quit()