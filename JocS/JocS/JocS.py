import pygame

from Lobby import lobby
from MenuMain import Menu

pygame.init()

screen = pygame.display.Info()
WIDTH = screen.current_w
HEIGHT = screen.current_h
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
FPS = 60
Menu(WIN, FPS)
#lobby(WIN, WIDTH, HEIGHT, FPS)
