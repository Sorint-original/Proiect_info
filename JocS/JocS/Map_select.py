import pygame
import ButtonClass
import os

from Gameplay import gameplay
import QuadTree

keyVec = ['mozaic', 'wall', 'holes', 'sorinTile', 'sorinWall']

default_path = 'Assets/Tiles/'

latura = 68


#THIS IS UPDATE

texture_dict = {
    keyVec[0] : pygame.image.load(default_path + 'mozaic' + '.jpg'),
    keyVec[1] : pygame.image.load(default_path + 'wall' + '.jpg'),
    keyVec[2] : pygame.image.load(default_path + 'holes' + '.jpg'),
    keyVec[3] : pygame.image.load(default_path + 'sorinTile' + '.jpg'),
    keyVec[4] : pygame.image.load(default_path + 'sorinWall' + '.jpg'),
    'empty' : pygame.image.load(default_path + 'empty' + '.jpg')
    }

collision_tiles = []

collision_vector = []
theMap = None

def generate_points():
    for i in range(18):
        for j in range(30):
            if collision_tiles[i][j] == True:
                x = latura * j - latura // 2
                y = latura * i - latura // 2
                collision_vector.append((x,y))

def generate_outer_points():
    collision_tiles.clear()
    for i in range(18):
        newVec = []
        for j in range(30):
            if (j == 0 or j == 28 + 1) or (i == 0 or i == 16 + 1):
                newVec.append(False)
            else:
                newVec.append(False)
        collision_tiles.append(newVec)

def map_select(WIN,WIDTH,HEIGHT,FPS,Input,Playeri,joysticks) :
    #Aici va fi toata functia de a selecta ce harta vrei dar momentan ia doar ii da load la aia de test
    generate_outer_points()
    Map = pygame.Surface((latura*28,latura*16))
    Map.fill((255,255,255))
    fstream = open('Maps/test.map','r')
    line = fstream.readline()
    while line :
        wordList = line.split()
        Map.blit(pygame.transform.scale(texture_dict[wordList[3]],(latura,latura)),(int(wordList[1])*latura,int(wordList[0])*latura))
        boolean = ButtonClass.StrToBool(wordList[2])
        collision_tiles[int(wordList[0]) + 1][int(wordList[1]) + 1] = boolean
        line = fstream.readline()
    generate_points()
    return Map
    #gameplay(WIN,WIDTH,HEIGHT,FPS,Input,Playeri,joysticks,Map,qTree)

