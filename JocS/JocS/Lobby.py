import pygame
import os

from EventH import exit , controller_verify
from Pleyer import pleyer

def lobby (WIN,WIDTH,HEIGHT,FPS) :
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    Pleyeri = []
    for i in range (4) :
        P = pleyer(pygame.image.load(os.path.join('Assets', 'Bottom-Blue.png')),pygame.image.load(os.path.join('Assets', 'Bottom-Blue.png')))
        Pleyeri.append(P)

    #INTRODUCEREA UNUI PLEYER
    def set_control(control) :
        spatiu_liber = -1
        repetare = 0
        for i in range(4) :
            if spatiu_liber == -1 and Pleyeri[i].Control == "Unknown" :
                spatiu_liber = i 
            elif Pleyeri[i].Control == control :
                repetare = 1
                break
        if repetare == 0 and spatiu_liber > -1 :
            Pleyeri[spatiu_liber].Control = control
            print(control)

    #SCOATEREA UNUI PLEYER 
    def eject_control(control) :
        for i in range(4) :
            if Pleyeri[i].Control == control :
                Pleyeri[i].Control = "Unknown"
                break

    #Desenarea ferestrei
    def draw_window() :
        for i in range(4) :
            x = 30 + i * ((WIDTH - 150) / 4 + 30)
            y = HEIGHT/3
            width = (WIDTH - 150)/4
            if Pleyeri[i].Control == "Unknown" :
                color = [200,200,200]
            else :
                color = [0,204,0]
            pygame.draw.rect(WIN, color, pygame.Rect(x, y, width, y))
        pygame.display.update()

    WIN.fill((255,255,255))

    clock = pygame.time.Clock()
    run=True
    while run :
        clock.tick(FPS)
        for event in pygame.event.get() :
            exit(event)
            controller_verify(event,joysticks)
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    set_control("Keyboard")
                elif event.key == pygame.K_ESCAPE :
                    eject_control("Keyboard")
            elif event.type == pygame.JOYBUTTONDOWN :
                print(3," ",event.joy)
                if event.button == 0 :
                    set_control(event.joy)
                elif event.button == 2 :
                    eject_control(event.joy)
        pygame.event.pump()


        draw_window()