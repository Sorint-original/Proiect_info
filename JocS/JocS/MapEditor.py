import pygame
import os

import ButtonClass
import TileClass

rows = 16
tiles_per_row = 28
tileMap = []

maxIndex = len(TileClass.keyVec)

currentTexture = 0
collidable = False

xoffset = (TileClass.w - tiles_per_row * TileClass.size) // 2
yoffset = (TileClass.h - rows * TileClass.size) // 2

def save_map(tileMap):
    with open("Maps/test.map", "w") as f:
        for i in range(tiles_per_row):
            for j in range(rows):
                f.write(str(i) + ' ' + str(j) + ' ' + str(tileMap[i][j].canCollide) + ' ' + str(tileMap[i][j].texture) + ' ' +str(tileMap[i][j].rotation_degree) + '\n')

def Editor(WIN, WIDTH, HEIGHT, FPS):
    textureBool = False
    removeBool = False
    def change_texture(vector, x, y, texture):
        #better tile searching algorithm requried
        if textureBool == True:
            for i in range(tiles_per_row):
                for j in range(rows):
                    if x >= i * TileClass.size + xoffset and x <= i * TileClass.size + xoffset + TileClass.size and y >= j * TileClass.size + yoffset and y <= j * TileClass.size + yoffset + TileClass.size:
                        vector[i][j].texture = TileClass.keyVec[currentTexture]
                        vector[i][j].canCollide = collidable
                        break
        elif removeBool == True:
            for i in range(tiles_per_row):
                for j in range(rows):
                    if x >= i * TileClass.size + xoffset and x <= i * TileClass.size + xoffset + TileClass.size and y >= j * TileClass.size + yoffset and y <= j * TileClass.size + yoffset + TileClass.size:
                        vector[i][j].texture = None
                        vector[i][j].canCollide = False
                        break

    for i in range(tiles_per_row):
        newVec = []
        for j in range(rows):
            newTile = TileClass.Tile()
            newVec.append(newTile)
        tileMap.append(newVec)

    def outline_draw():
        for i in range(tiles_per_row):
            for j in range(rows):
                tileMap[i][j].editor_view(xoffset, yoffset, i, j, WIN)

    def texture_draw():
        for i in range(tiles_per_row):
            for j in range(rows):
                tileMap[i][j].draw_texture(xoffset, yoffset, i, j, WIN)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)

            elif event.type == pygame.KEYDOWN:
                global currentTexture
                if event.unicode == ' ':
                    global collidable
                    collidable = not collidable
                elif event.unicode == '1':
                    if currentTexture > 0:
                        currentTexture -= 1
                elif event.unicode == '2':
                    if currentTexture < maxIndex - 1:
                        currentTexture += 1
                elif event.unicode == 'p':
                    save_map(tileMap)
                    pygame.quit()
                    os._exit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    textureBool = True
                elif event.button == 3:
                    removeBool = True
                change_texture(tileMap, event.pos[0], event.pos[1], currentTexture)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    textureBool = False
                elif event.button == 3:
                    removeBool = False

            elif event.type == pygame.MOUSEMOTION:
                change_texture(tileMap, event.pos[0], event.pos[1], currentTexture)

        WIN.fill((0,0,0))
        texture_draw()
        outline_draw()
        pygame.display.update()
