import pygame
import os

pygame.init()
screen = pygame.display.Info()
w = screen.current_w
h = screen.current_h
del screen

#recommended image size: 128x128 pixels

outline_width = 2
size = w // 30

default_path = 'Assets/Tiles/'

keyVec = ['mozaic', 'wall', 'holes']

texture_dict = {
    keyVec[0] : pygame.image.load(default_path + 'mozaic' + '.jpg'),
    keyVec[1] : pygame.image.load(default_path + 'wall' + '.jpg'),
    keyVec[2] : pygame.image.load(default_path + 'holes' + '.jpg'),
    'empty' : pygame.image.load(default_path + 'empty' + '.jpg')
    }

for i in range(len(keyVec)):
    texture_dict[keyVec[i]] = pygame.transform.scale(texture_dict[keyVec[i]], (size, size))
texture_dict['empty'] = pygame.transform.scale(texture_dict['empty'], (size, size))

#Tile ideas:
#-Collidable with everything but the player
#-Collidable with only the player
#-Slowness if touched by player

class Tile:
    def __init__(self):
        self.canCollide = False
        self.texture = None
        self.rotation_degree = 0
        
    def editor_view(self, xoff, yoff, x, y, screen):
        if self.canCollide == False:
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(x * size + xoff, y * size + yoff, size, size), outline_width)
        else:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(x * size + xoff, y * size + yoff, size, size), outline_width)

    def draw_texture(self, xoff, yoff, x, y, screen):
        if self.texture != None:
            screen.blit(texture_dict[self.texture], (x * size + xoff, y * size + yoff), (0, 0, size, size))
        else:
            screen.blit(texture_dict['empty'], (x * size + xoff, y * size + yoff), (0, 0, size, size))