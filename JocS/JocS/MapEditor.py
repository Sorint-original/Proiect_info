import pygame
import os
import random
import math

from os.path import exists

import ButtonClass
import TileClass

rows = 16
tiles_per_row = 28
latura = 68
tileMap = []

pygame.init()
screen = pygame.display.Info()
WIDTH = screen.current_w
HEIGHT = screen.current_h

font = pygame.font.Font("freesansbold.ttf", 26)

h = HEIGHT - 110
while (round(h * 1.75) > WIDTH - 50) :
    h -=  1
w = round(h * 1.75)
X = (WIDTH - w) // 2
Y = (HEIGHT - h) // 2
if Y < 100 :
    Y = 10

maxIndex = len(TileClass.keyVec)
maxSpecialIndex = len(TileClass.specialTiles)

Map = pygame.Surface((latura * tiles_per_row, latura * rows))
Map.fill((0,0,0))
Map = pygame.transform.scale(Map, (w, h))

Current_map_name = None
NoMapText = "Map name"

currentGame = None

def texture_draw():
    for i in range(rows):
        for j in range(tiles_per_row):
            tileMap[i][j].draw_texture(i, j, Map)

def save_map(tileMap, name, game):
    add = ".map"
    with open("Maps/" + name + add, "w") as f:
        for i in range(rows):
            for j in range(tiles_per_row):
                f.write(str(i) + ' ' + str(j) + ' ' + str(tileMap[i][j].special) + ' ' + str(tileMap[i][j].texture) + ' ' + str(tileMap[i][j].rotation_degree) + '\n')
    texture_draw()
    pygame.display.update()
    pygame.image.save(Map,"Assets/Maps/" + name + ".jpg")

def search_map(name):
    boolean = exists("Maps/" + name + ".map")
    if not boolean:
        boolean = exists("Maps/" + name + ".smap")
    return boolean

def load_map(name, game):
    global tileMap
    add = ".map"
    with open("Maps/" + name + add, "r") as f:
        alt = f.readline()
        tileMap.clear()
        for i in range(rows):
            newVec = []
            for j in range(tiles_per_row):
                newVec.append(None)
            tileMap.append(newVec)
        while alt:
            newTile = TileClass.Tile()
            line = alt.split()
            newTile.special = line[2]
            found = False
            for i in range(len(TileClass.keyVec)):
                if TileClass.keyVec[i] == line[3]:
                    found = True
                    newTile.texture = TileClass.keyVec[i]
                    break

            if not found:
                newTile.texture = "missing"

            newTile.rotation_degree = int(line[4])
            tileMap[int(line[0])][int(line[1])] = newTile
            alt = f.readline()

def Editor(WIN, WIDTH, HEIGHT, FPS):
    tileMap.clear()
    status = None
    buttons = []
    ButtonClass.Button_Load("MapEditor", buttons)

    currentTexture = 1
    currentTextureAlt = 2
    currentSpecial = 0
    currentRotation = 0
    currentPage = 1
    maxPage = 1

    view_outline = True
    isInMenu = False

    textureBool = False
    removeBool = False

    map_string = ""
    map_box_selected = False

    MouseX = None
    MouseY = None

    def change_texture(vector, x, y, texture):
        if not isInMenu:
            xSearch = math.floor(latura * w / (latura * 28))
            ySearch = math.floor(latura * h / (latura * 16))
            yPos = (y - Y) // ySearch
            xPos = (x - X) // xSearch
            if xPos >= 0 and xPos <= tiles_per_row - 1 and yPos >= 0 and yPos <= rows - 1:
                if textureBool == True:
                    vector[yPos][xPos].texture = TileClass.keyVec[currentTexture]
                    vector[yPos][xPos].special = TileClass.specialTiles[currentSpecial]
                    vector[yPos][xPos].rotation_degree = currentRotation
                elif removeBool == True:
                    vector[yPos][xPos].texture = TileClass.keyVec[currentTextureAlt]
                    vector[yPos][xPos].special = TileClass.specialTiles[currentSpecial]
                    vector[yPos][xPos].rotation_degree = currentRotation

    for i in range(rows):
        newVec = []
        for j in range(tiles_per_row):
            newTile = TileClass.Tile()
            texture = None
            for i in range(len(TileClass.keyVec)):
                if TileClass.keyVec[i] == "empty":
                    texture = i
                    break
            newTile.texture = TileClass.keyVec[i]
            newVec.append(newTile)
        tileMap.append(newVec)

    def outline_draw():
        if view_outline == True:
            for i in range(rows):
                for j in range(tiles_per_row):
                    tileMap[i][j].editor_view(i, j, Map)

    def texture_menu(xMouse, yMouse, mouse):
        if isInMenu:
            nonlocal currentTexture
            nonlocal currentTextureAlt
            index = 10 * 6 * (currentPage - 1)
            thew = 10 * math.floor(latura * w / (latura * 28))
            theh = 6 * math.floor(latura * h / (latura * 16))
            thex = w // 2 - thew // 2
            they = h // 2 - theh // 2
            xPos = None
            yPos = None
            if xMouse:            
                xPos = (xMouse - thex - X) // math.floor(latura * w / (latura * 28))
                yPos = (yMouse - they - Y) // math.floor(latura * h / (latura * 16))
            maxPage = len(TileClass.keyVec) // 60

            if xPos != None and yPos != None and xPos >= 0 and xPos <= 10 and yPos >=0 and yPos <= 6:
                print(xPos, yPos)
                if index + (xPos + yPos * 10) < len(TileClass.keyVec):
                    if mouse == True:
                        currentTexture = index + (xPos + yPos * 10)
                    elif mouse == False:
                        currentTextureAlt = index + (xPos + yPos * 10)

            for i in range(60):
                if index + i < len(TileClass.keyVec):
                    Map.blit(TileClass.texture_dict[TileClass.keyVec[index + i]], (thex + (i % 10) * math.floor(latura * w / (latura * 28)), they + (i // 10) * math.floor(latura * h / (latura * 16))), (0, 0, latura * w / (latura * 28), latura * h / (latura * 16)))
                    if index + i == currentTexture:
                        pygame.draw.rect(Map, (255,0,0), pygame.Rect(thex + (i % 10) * math.floor(latura * w / (latura * 28)),they + (i // 10) * math.floor(latura * h / (latura * 16)),latura * w / (latura * 28), latura * h / (latura * 16)), 3)
                    if index + i == currentTextureAlt:
                        pygame.draw.rect(Map, (0,0,255), pygame.Rect(thex + (i % 10) * math.floor(latura * w / (latura * 28)),they + (i // 10) * math.floor(latura * h / (latura * 16)),latura * w / (latura * 28), latura * h / (latura * 16)), 3)

            WIN.blit(Map,(X,Y))
            pygame.display.update()

    def show_current_texture():
        WIN.blit(pygame.transform.rotate(TileClass.texture_dict[TileClass.keyVec[currentTexture]], currentRotation) , (WIDTH // 2.15, HEIGHT - 100))
        pygame.draw.rect(WIN, (255,0,0), pygame.Rect(WIDTH // 2.15, HEIGHT - 100, latura * w / (latura * 28), latura * h / (latura * 16)), 1)
        
        WIN.blit(pygame.transform.rotate(TileClass.texture_dict[TileClass.keyVec[currentTextureAlt]], currentRotation) , (WIDTH // 2.15 + math.floor(latura * w / (latura * 28)) + 20, HEIGHT - 100))
        pygame.draw.rect(WIN, (0,0,255), pygame.Rect(WIDTH // 2.15 + math.floor(latura * w / (latura * 28)) + 20, HEIGHT - 100, latura * w / (latura * 28), latura * h / (latura * 16)), 1)
        
    def show_outline_view():
        if view_outline:
            pygame.draw.rect(WIN, (0,255,0), pygame.Rect(X + WIDTH // 7 + 20, HEIGHT - 100, latura * w / (latura * 28), latura * h / (latura * 16)))
        else:
            pygame.draw.rect(WIN, (0,0,0), pygame.Rect(X + WIDTH // 7 + 20, HEIGHT - 100, latura * w / (latura * 28), latura * h / (latura * 16)))
            pygame.draw.rect(WIN, (255,0,0), pygame.Rect(X + WIDTH // 7 + 20, HEIGHT - 100, latura * w / (latura * 28), latura * h / (latura * 16)), 3)

    def show_current_special():
        pygame.draw.rect(WIN, (128,128,128), pygame.Rect(X + WIDTH // 7 + 20 + 20 + latura * w / (latura * 28), HEIGHT - 100, WIDTH // 5, latura * h / (latura * 16)))
        theString = TileClass.specialTiles[currentSpecial]
        if TileClass.specialTiles[currentSpecial] == None:
            theString = "Nothing"
        text = font.render(theString, True, TileClass.specialColors[currentSpecial])
        textRect = text.get_rect()

        textRect.center = (X + WIDTH // 7 + 20 + 20 + latura * w / (latura * 28) + WIDTH // 5 // 2, HEIGHT - 100 + latura * h / (latura * 16) // 2)
        WIN.blit(text, textRect)

    def show_map_stuff():
        pygame.draw.rect(WIN, (128,128,128) * (not map_box_selected) or (96,96,96), pygame.Rect(WIDTH - X - WIDTH // 5, HEIGHT - 100, WIDTH // 5, latura * h / (latura * 16)))
        theString = TileClass.specialTiles[currentSpecial]
        if map_string != "" or map_box_selected:
            text = font.render(map_string, True, (0,0,0))
        else:
            text = font.render(NoMapText, True, (0,0,0))
        textRect = text.get_rect()

        textRect.center = (WIDTH - X - WIDTH // 5 + WIDTH // 10, HEIGHT - 100 + latura * h / (latura * 16) // 2)
        WIN.blit(text, textRect)

    def check_map_box(xMouse, yMouse):
        if xMouse >= WIDTH - X - WIDTH // 5 and xMouse <= WIDTH - X - WIDTH // 5 + WIDTH // 5 and yMouse >= HEIGHT - 100 and yMouse <= HEIGHT - 100 + latura * h / (latura * 16):
           return True
        else:
           return False

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)

            elif event.type == pygame.KEYDOWN:
                if map_box_selected == True:
                    global Current_map_name
                    if event.unicode == '\x08': #backspace
                        map_string = map_string[:-1]
                    elif event.unicode == '\r' and len(map_string) > 0: #enter
                        if not search_map(map_string):
                            save_map(tileMap, map_string, currentGame)
                            map_box_selected = False
                        else:
                            if Current_map_name == map_string:
                                save_map(tileMap, map_string, currentGame)
                                map_box_selected = False
                            else:
                                print("TEST")
                                load_map(map_string, currentGame)
                                map_box_selected = False
                        Current_map_name = map_string
                    else:
                        if len(map_string) <= 23:
                            map_string += event.unicode
                        
                else:
                    if event.unicode == 'w':
                        if currentSpecial < maxSpecialIndex - 1:
                            currentSpecial += 1
                    elif event.unicode == 's':
                        if currentSpecial > 0:
                            currentSpecial -= 1

                    elif event.unicode == 'e':
                        isInMenu = not isInMenu

                    elif event.unicode == 'd':
                        if not isInMenu:
                            currentRotation -= 90
                            if currentRotation < 0:
                                currentRotation = 360 + currentRotation
                            currentRotation %= 360
                        else:
                            if currentPage <= maxPage + 1:
                                currentPage += 1
                    elif event.unicode == 'a':
                        if not isInMenu:
                            currentRotation += 90
                            currentRotation %= 360
                        else:
                            if currentPage > 1:
                                currentPage -= 1

                    elif event.unicode == ' ':
                        view_outline = not view_outline

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    status = ButtonClass.checkButtonClick(event.pos[0], event.pos[1], buttons, (1,2))
                    textureBool = True
                    texture_menu(event.pos[0],event.pos[1], True)
                elif event.button == 3:
                    removeBool = True
                    texture_menu(event.pos[0],event.pos[1], False)
                change_texture(tileMap, event.pos[0], event.pos[1], currentTexture)
                map_box_selected = check_map_box(event.pos[0], event.pos[1])

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    textureBool = False
                elif event.button == 3:
                    removeBool = False

            elif event.type == pygame.MOUSEMOTION:
                ButtonClass.checkButtonHover(event.pos[0], event.pos[1], buttons)
                change_texture(tileMap, event.pos[0], event.pos[1], currentTexture)

        WIN.fill((0,0,0))
        texture_draw()
        outline_draw()
        show_current_texture()
        show_outline_view()
        show_current_special()
        show_map_stuff()
        texture_menu(None, None, None)
        ButtonClass.displayButtons(WIN, buttons)
        WIN.blit(Map, (X, Y))
        pygame.display.update()

        if status != None:
            run = status
