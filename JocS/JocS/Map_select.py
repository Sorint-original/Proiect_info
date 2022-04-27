import pygame
import ButtonClass
import os
from Gameplay import gameplay

keyVec = ['mozaic', 'wall', 'holes', 'sorinTile', 'sorinWall']

default_path = 'Assets/Tiles/'


texture_dict = {
    keyVec[0] : pygame.image.load(default_path + 'mozaic' + '.jpg'),
    keyVec[1] : pygame.image.load(default_path + 'wall' + '.jpg'),
    keyVec[2] : pygame.image.load(default_path + 'holes' + '.jpg'),
    keyVec[3] : pygame.image.load(default_path + 'sorinTile' + '.jpg'),
    keyVec[4] : pygame.image.load(default_path + 'sorinWall' + '.jpg'),
    'empty' : pygame.image.load(default_path + 'empty' + '.jpg')
    }

def map_select(WIN,WIDTH,HEIGHT,FPS,Input,Playeri,joysticks) :
    #Aici va fi toata functia de a selecta ce harta vrei dar momentan ia doar ii da load la aia de test
    laturax = 1920 // 28
    laturay = 1080 // 16
    colision_tiles = []
    rand = []
    for i in range (28) :
        rand.append(0)
    for i in range(16) :
        colision_tiles.append(rand)
    Map = pygame.Surface((laturax*28,laturay*16))
    Map.fill((255,255,255))
    fstream = open('Maps/test.map','r')
    line = fstream.readline()
    while line :
        wordList = line.split()
        Map.blit(pygame.transform.scale(texture_dict[wordList[3]],(laturax,laturay)),(int(wordList[0])*laturax,int(wordList[1])*laturay))
        if ButtonClass.StrToBool(wordList[2]) :
            colision_tiles[int(wordList[1])][int(wordList[0])] = 1
        line = fstream.readline()
    Map=pygame.transform.scale(Map,(1920,1080))
    gameplay(WIN,WIDTH,HEIGHT,FPS,Input,Playeri,joysticks,Map,colision_tiles)