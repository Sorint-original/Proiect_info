import pygame
from EventH import exit

def lobby (WIN,WIDTH,HEIGHT) :

    pygame.init()

    def draw_window() :
        #yes
        for i in range(4) :
            x = 30 + i * ((WIDTH - 150) / 4 + 30)
            y = HEIGHT/3
            width = (WIDTH - 150)/4
            color=[200,200,200]
            pygame.draw.rect(WIN, color, pygame.Rect(x, y, width, y))
        pygame.display.update()

    WIN.fill((255,255,255))

    run=True
    while run :
        for event in pygame.event.get() :
            exit(event)
        draw_window()