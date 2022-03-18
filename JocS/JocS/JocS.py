import pygame
from Lobby import lobby

pygame.init()

screen = pygame.display.Info()
WIDTH = screen.current_w
HEIGHT = screen.current_h
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
lobby(WIN,WIDTH,HEIGHT)
