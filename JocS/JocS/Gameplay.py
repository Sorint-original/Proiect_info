import pygame
import os
from EventH import exit , controller_verify
# dau inport la clasa de butoane deoarece sar putea sa avem un Pause Menu si cred ca nu o sal putem face separat de gameplay
import ButtonClass
from Player import Harmful_Stuff

#input reprezinta un dictionar care indica care input(keyboard , controller) se duce la fiecare player , de asemenea as vrea un parameter MAP care e luat din MAPSELECT
def gameplay (WIN,WIDTH,HEIGHT,FPS,Input,Playeri,joysticks) :
    sw = 1920
    sh = 1080
    #pregatirea playerilor pentru  Gameplay
    Botimg = ['Bottom-Blue.png','Bottom-Green.png','Bottom-Yellow.png','Bottom-Red.png']
    Upimg = ['Upper-Blue.png','Upper-Green.png','Upper-Yellow.png','Upper-Red.png']
    # cele patru poziti in care se pot spauna playeri
    poziti = (100 , 100 , sw - 100 , sh - 100 , sw - 100 , 100 , 100 , sh - 100 )
    alcat = 0
    for i in range (4) :
        if Playeri[i].Selected :
            Playeri[i].Health = 1000
            Playeri[i].GX = poziti[alcat]
            Playeri[i].GY = poziti[alcat+1]
            Playeri[i].change_size(150,pygame.image.load(os.path.join('Assets\Robots', Botimg[i])),pygame.image.load(os.path.join('Assets\Robots', Upimg[i])))
            alcat = alcat + 2
    #stabilirea dimensiunilor pentru afisarea gameplayului
    h = HEIGHT - 100
    while ( round(h * 1.78)  > WIDTH - 50) :
        h = h -1
    w =  round(h*1.78) 
    x =  (WIDTH - w)/2
    y = (HEIGHT - h)/2
    #Suprafata pe care se va intampla totul
    DisplayG = pygame.Surface((sw,sh))

    def environment_update () :
        DisplayG.fill ((255,255,255))
        for i in range (4) :
            if Playeri[i].Selected :
                Playeri[i].afisare(DisplayG)
        for attack in Harmful_Stuff :
            attack.afisare(DisplayG)

    def draw_window () :
        WIN.fill((0,0,0))
        environment_update()
        WIN.blit(pygame.transform.scale(DisplayG,(w,h)),(x,y))
        pygame.display.update()


    clock = pygame.time.Clock()
    run=True
    while run :
        clock.tick(FPS)
        # THE EVENT LOOP
        for event in pygame.event.get() :
            exit(event)
            controller_verify(event,joysticks)
            try :
                if event.joy != None :
                    Playeri[Input[event.joy]].update_input(event)
            except :
                if Input["Keyboard"] != None :
                    Playeri[Input["Keyboard"]].update_input(event)
        #updatarea playerului in the game
        for i in range (4) :
            if Playeri[i].Selected :
                Playeri[i].gameplay_update()
        for attack in Harmful_Stuff :
            attack.update()
        draw_window()
