import pygame
import ButtonClass
import os

from Gameplay import gameplay

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
everything = []

collision_vector = []
theMap = None

def generate_points():
    for i in range(18):
        for j in range(30):
            if collision_tiles[i][j] == True:
                collision_tiles[i][j] = False
                newVec = [(i,j)]
                J = j
                I = i
                Xflag = True
                Yflag = True
                while Xflag and J + 1 < 30:
                    J += 1
                    if collision_tiles[i][J] == True:
                        newVec.append((i,J))
                        collision_tiles[i][J] = False
                    else:
                        Xflag = False
                while Yflag and I + 1 < 18:
                    I += 1
                    extendVec = []
                    for thing in newVec:
                        if collision_tiles[I][thing[1]] == True:
                            extendVec.append((I,thing[1]))
                        else:
                           Yflag = False
                    if Yflag:
                        newVec.extend(extendVec)
                        for t in extendVec:
                            collision_tiles[t[0]][t[1]] = False
                everything.append(newVec)
    for rectangle in everything:
        #Find height and width in tile count
        Xmin = Xmax = Ymin = Ymax = -1
        for points in rectangle:
            if Xmin > points[1] or Xmin == -1:
                Xmin = points[1]
            if Ymin > points[0] or Ymin == -1:
                Ymin = points[0]
            if Xmax < points[1] or Xmax == -1:
                Xmax = points[1]
            if Ymax < points[0] or Ymin == -1:
                Ymax = points[0]
        x = latura * (Xmin + Xmax) // 2 - latura // 2
        y = latura * (Ymin + Ymax) // 2 - latura // 2
        collision_vector.append((x, y, latura * abs(Xmax - Xmin + 1), latura * abs(Ymax - Ymin + 1)))
    #print(collision_vector)

#x = latura * j - latura // 2
#y = latura * i - latura // 2
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
    #Aici va fi toata functia de a selecta ce harta vrei dar momentan ia doar
    #ii da load la aia de test
    generate_outer_points()
    Map = pygame.Surface((latura * 28,latura * 16))
    Map.fill((255,255,255))
    fstream = open('Maps/test.map','r')
    line = fstream.readline()
    while line :
        wordList = line.split()
        Map.blit(pygame.transform.scale(texture_dict[wordList[3]],(latura,latura)),(int(wordList[1]) * latura,int(wordList[0]) * latura))
        boolean = ButtonClass.StrToBool(wordList[2])
        collision_tiles[int(wordList[0]) + 1][int(wordList[1]) + 1] = boolean
        line = fstream.readline()
    generate_points()
    return Map
    #gameplay(WIN,WIDTH,HEIGHT,FPS,Input,Playeri,joysticks,Map,qTree)

