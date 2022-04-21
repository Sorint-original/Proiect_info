import pygame
import os

import JocS

import ButtonClass

#Testing ground below

#ButtonVec = []

Player1 = []
Player2 = []

BidimVec = [Player1, Player2]

ButtonClass.Button_Load(ButtonClass.currentScene, Player1) #load MainMenu for first time oppening

clock = pygame.time.Clock()

while JocS.running:
    clock.tick(60)
    for event in pygame.event.get():
        print(str(event))
        if event.type == pygame.MOUSEMOTION:
            for v in BidimVec:
                ButtonClass.checkButtonHover(event.pos[0], event.pos[1], v, BidimVec)
                if ButtonClass.currentScene != "Lobby": 
                    BidimVec[0] = v.copy()
                    BidimVec[1].clear()
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for v in BidimVec:
                    ButtonClass.checkButtonClick(event.pos[0], event.pos[1], v, BidimVec)
                    print("EH")
                    if ButtonClass.currentScene != "Lobby": 
                        BidimVec[0] = v.copy()
                        BidimVec[1].clear()
                        break

        elif event.type == pygame.QUIT:
            JocS.running = False
    
    JocS.WIN.fill((255,255,255))
    for v in BidimVec:
        ButtonClass.displayButtons(JocS.WIN, v)
        if ButtonClass.currentScene != "Lobby": break
    pygame.display.update()


pygame.quit()
#quit()