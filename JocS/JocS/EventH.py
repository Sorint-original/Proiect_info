import pygame
import os

def exit(event) :
    if event.type == pygame.QUIT :
        pygame.quit()
        os._exit(0)