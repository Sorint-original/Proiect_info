import pygame
import os
import math

pygame.init()
screen = pygame.display.Info()
WIDTH = screen.current_w
HEIGHT = screen.current_h

latura = 68

h = HEIGHT - 110
while (round(h * 1.75) > WIDTH - 50) :
    h -=  1
w = round(h * 1.75)
x = (WIDTH - w) // 2
y = (HEIGHT - h) // 2
if y < 100 :
    y = 10

#recommended image size: 128x128 pixels

outline_width = 2
size = WIDTH // 30

default_path = 'Assets/Tiles/'

keyVec = []

for file in os.listdir(default_path):
    if file != "missing.jpg":
        file = file[:-4]
        keyVec.append(file)

print(keyVec)

#keyVec = ['mozaic', 'bolts', 'plane', 'rusty', 'plastic', 'steel', 'box', 'box2', 'circle', 'concrete', 'concrete2', 'tiles', 'tileshalf', 'tilescorner', 'tilequarter', 'black', 'diamond', 'grates', 'circlevent', 'squarevent', 'vent', 'complex', 'complexgreen', 'complexgrey', 'complexyellow', 'sorinTile', 'sebiTile']

specialTiles = ["Nothing", "Collidable", "CollidableWithPlayer", "PowerUpSpawn", "RedPlayerSpawn", "BluePlayerSpawn", "GreenPlayerSpawn", "YellowPlayerSpawn"]

texture_dict = {
    'missing' : pygame.image.load(default_path + 'missing' + '.jpg')
    }

for i in keyVec:
    texture_dict[i] = pygame.image.load(default_path + i + '.jpg')

specialColors = [
    (0,0,0),
    (255,255,255),
    (255,128,0),
    (153,0,153),
    (255,0,0),
    (0,0,255),
    (0,255,0),
    (255,255,0)
    ]

for i in range(len(keyVec)):
    texture_dict[keyVec[i]] = pygame.transform.scale(texture_dict[keyVec[i]], (latura * w / (latura * 28) , latura * h / (latura * 16)))
noTexture = pygame.transform.scale(texture_dict['missing'], (latura * w / (latura * 28) , latura * h / (latura * 16)))

class Tile:
    def __init__(self):
        self.special = "Nothing"
        self.texture = None
        self.rotation_degree = 0
        
    def editor_view(self, X, Y, screen):
        if self.special == "Nothing":
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(Y * math.floor(latura * w / (latura * 28)), X * math.floor(latura * h / (latura * 16)), latura * w / (latura * 28), latura * h / (latura * 16)), outline_width)
        elif self.special == "Collidable":
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(Y * math.floor(latura * w / (latura * 28)), X * math.floor(latura * h / (latura * 16)), latura * w / (latura * 28), latura * h / (latura * 16)), outline_width)
        elif self.special == "CollidableWithPlayer":
            pygame.draw.rect(screen, (255,128,0), pygame.Rect(Y * math.floor(latura * w / (latura * 28)), X * math.floor(latura * h / (latura * 16)), latura * w / (latura * 28), latura * h / (latura * 16)), outline_width)
        elif self.special == "PowerUpSpawn":
            pygame.draw.rect(screen, (255,0,255), pygame.Rect(Y * math.floor(latura * w / (latura * 28)), X * math.floor(latura * h / (latura * 16)), latura * w / (latura * 28), latura * h / (latura * 16)), outline_width)
        elif self.special == "RedPlayerSpawn":
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(Y * math.floor(latura * w / (latura * 28)), X * math.floor(latura * h / (latura * 16)), latura * w / (latura * 28), latura * h / (latura * 16)), outline_width)
        elif self.special == "BluePlayerSpawn":
            pygame.draw.rect(screen, (0,0,255), pygame.Rect(Y * math.floor(latura * w / (latura * 28)), X * math.floor(latura * h / (latura * 16)), latura * w / (latura * 28), latura * h / (latura * 16)), outline_width)
        elif self.special == "GreenPlayerSpawn":
            pygame.draw.rect(screen, (0,255,0), pygame.Rect(Y * math.floor(latura * w / (latura * 28)), X * math.floor(latura * h / (latura * 16)), latura * w / (latura * 28), latura * h / (latura * 16)), outline_width)
        elif self.special == "YellowPlayerSpawn":
            pygame.draw.rect(screen, (255,255,0), pygame.Rect(Y * math.floor(latura * w / (latura * 28)), X * math.floor(latura * h / (latura * 16)), latura * w / (latura * 28), latura * h / (latura * 16)), outline_width)

    def draw_texture(self, X, Y, screen):
        if self.texture != None:
            rotated_img = pygame.transform.rotate(texture_dict[self.texture], self.rotation_degree)
            screen.blit(rotated_img, (Y * math.floor(latura * w / (latura * 28)), X * math.floor(latura * h / (latura * 16))), (0, 0, latura * w / (latura * 28), latura * h / (latura * 16)))      