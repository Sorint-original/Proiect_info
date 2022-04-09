import pygame
import os

from EventH import exit , controller_verify
from Player import player

def lobby (WIN,WIDTH,HEIGHT,FPS) :
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    Playeri = []
    #initializarea playerilor
    Botimg = ['Bottom-Blue.png','Bottom-Green.png','Bottom-Yellow.png','Bottom-Red.png']
    Upimg = ['Upper-Blue.png','Upper-Green.png','Upper-Yellow.png','Upper-Red.png']
    size = 250
    for i in range (4) :
        Gx = 30 + i * ((WIDTH - 150) / 4 + 30) + (WIDTH - 150) / 8
        Gy = HEIGHT/2
        P = player(pygame.image.load(os.path.join('Assets', Botimg[i])), pygame.image.load(os.path.join('Assets', Upimg[i])), Gx, Gy, size)
        Playeri.append(P)
    Input = {"Keyboard" : None , 0:None , 1:None , 2:None , 3:None , 4:None}

    #INTRODUCEREA UNUI Player
    def set_control(control) :
        if Input[control] == None :
            for i in range(4) :
                if Playeri[i].Selected == False :
                    Playeri[i].Selected = True
                    Playeri[i].Source = control
                    Playeri[i].reset_control()
                    Input [control] = i 
                    break

    #SCOATEREA UNUI Player 
    def eject_control(control) :
        if Input[control] != None :
            Playeri[Input[control]].Selected = False
            Playeri[Input[control]].Source = "Unknown"
            Input[control] = None

    #Desenarea ferestrei
    def draw_window() :
        WIN.fill((255,255,255))
        for i in range(4) :
            x = 30 + i * ((WIDTH - 150) / 4 + 30)
            y = HEIGHT/3
            width = (WIDTH - 150)/4
            if Playeri[i].Ready == False :
                color = [200,200,200]
            else :
                color = [0,204,0]
            pygame.draw.rect(WIN, color, pygame.Rect(x, y, width, y))
            if Playeri[i].Selected == True :
                Playeri[i].afisare(WIN)
        pygame.display.update()

    #The loop of the Lobby
    clock = pygame.time.Clock()
    run=True
    while run :
        clock.tick(FPS)
        #The event loop
        for event in pygame.event.get() :
            exit(event)
            controller_verify(event,joysticks)
            try :
                if event.joy != None :
                    if event.type == pygame.JOYBUTTONDOWN :
                        set_control(event.joy)
                    if Input[event.joy] != None :
                        Playeri[Input[event.joy]].update_input(event)
            except :
                if Input["Keyboard"] != None :
                    Playeri[Input["Keyboard"]].update_input(event)
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_SPACE :
                        set_control("Keyboard")
                    elif event.key == pygame.K_ESCAPE :
                        eject_control("Keyboard")
        pygame.event.pump()
        #Verifica daca un controler isi deselecteaza pozitia
        for i in range (5) :
            if Input[i] != None :
                if Playeri[Input[i]].exit_update() :
                    eject_control(i)
        for i in range (4) :
            if Playeri[i].Selected :
                Playeri[i].gameplay_update()
        draw_window()