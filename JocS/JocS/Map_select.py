import pygame
import ButtonClass
import os
from Gameplay import gameplay

<<<<<<< Updated upstream
import TileClass
=======
>>>>>>> Stashed changes
import QuadTree

keyVec = ['mozaic', 'wall', 'holes', 'sorinTile', 'sorinWall']

default_path = 'Assets/Tiles/'

latura = 68

texture_dict = {
    keyVec[0] : pygame.image.load(default_path + 'mozaic' + '.jpg'),
    keyVec[1] : pygame.image.load(default_path + 'wall' + '.jpg'),
    keyVec[2] : pygame.image.load(default_path + 'holes' + '.jpg'),
    keyVec[3] : pygame.image.load(default_path + 'sorinTile' + '.jpg'),
    keyVec[4] : pygame.image.load(default_path + 'sorinWall' + '.jpg'),
    'empty' : pygame.image.load(default_path + 'empty' + '.jpg')
    }

<<<<<<< Updated upstream
#Very hardcoded stuff. Please don't update in Gameplay.py unless it's updated correctly here as well
h = TileClass.h - 110
w = round(h * 1.78)

sizex = w // 28
sizey = h // 16 
xoffset = (TileClass.w - w) // 2
yoffset = (TileClass.h - h) // 2
if yoffset < 100:
    yoffset = 10

print(sizex)

rect = QuadTree.Rectangle(xoffset + 28 * sizex // 2, yoffset + 16 * sizey // 2, 28 * sizex + sizex + 10, 16 * sizey + sizey + 10)
=======
rect = QuadTree.Rectangle(28 * latura // 2, 16 * latura // 2, 28 * latura + latura + 10, 16 * latura + latura + 10)
>>>>>>> Stashed changes
qTree = QuadTree.QuadTree(rect)

collision_tiles = []

def generate_points():
    for i in range(18):
        for j in range(30):
            if collision_tiles[i][j] == True:
<<<<<<< Updated upstream
                x = sizex * j + xoffset - sizex // 2
                y = sizey * i + yoffset - sizey // 2
=======
                x = latura * j - latura // 2
                y = latura * i - latura // 2
>>>>>>> Stashed changes
                obj = QuadTree.TreeObject(x,y)
                qTree.insert(obj)

def generate_outer_points():
    collision_tiles.clear()
    for i in range(18):
        newVec = []
        for j in range(30):
            if (j == 0 or j == 28 + 1) or (i == 0 or i == 16 + 1):
                newVec.append(True)
            else:
                newVec.append(False)
        collision_tiles.append(newVec)

def map_select(WIN,WIDTH,HEIGHT,FPS,Input,Playeri,joysticks) :
    #Aici va fi toata functia de a selecta ce harta vrei dar momentan ia doar ii da load la aia de test
<<<<<<< Updated upstream
    laturax = 1920 // 28
    laturay = 1080 // 16

    generate_outer_points()
    Map = pygame.Surface((w, h))
    Map.fill((0,0,0))
    fstream = open('Maps/test.map','r') #File is not being closed.... that's not good
=======
    generate_outer_points()

    Map = pygame.Surface((latura*28,latura*16))
    Map.fill((255,255,255))
    fstream = open('Maps/test.map','r')
>>>>>>> Stashed changes
    line = fstream.readline()

    hw = w // 28
    hh = h // 16

    while line :
        wordList = line.split()
<<<<<<< Updated upstream
        Map.blit(pygame.transform.scale(texture_dict[wordList[3]], (hw, hh)), (int(wordList[1]) * hw, int(wordList[0]) * hh))

        boolean = ButtonClass.StrToBool(wordList[2])
        collision_tiles[int(wordList[0]) + 1][int(wordList[1]) + 1] = boolean

        line = fstream.readline()

    #Map = pygame.transform.scale(Map,(1920,1080))

    #print(collision_tiles)

    generate_points()

    gameplay(WIN, WIDTH, HEIGHT, FPS, Input, Playeri, joysticks, Map, qTree)
=======
        Map.blit(pygame.transform.scale(texture_dict[wordList[3]],(latura,latura)),(int(wordList[1])*latura,int(wordList[0])*latura))
        boolean = ButtonClass.StrToBool(wordList[2])
        collision_tiles[int(wordList[0]) + 1][int(wordList[1]) + 1] = boolean
        line = fstream.readline()
    generate_points()
    WIN.blit(Map,(0,0))
    gameplay(WIN,WIDTH,HEIGHT,FPS,Input,Playeri,joysticks,Map,qTree)
>>>>>>> Stashed changes
