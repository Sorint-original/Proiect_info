import pygame
import ButtonClass
import os
import MapEditor
import TileClass

screen = pygame.display.Info()
WIDTH = screen.current_w
HEIGHT = screen.current_h

h = HEIGHT - 110
while (round(h * 1.75) > WIDTH - 50) :
    h = h - 1
w = round(h * 1.75)
x = (WIDTH - w) // 2
y = (HEIGHT - h) // 2
if y < 100 :
    y = 10

from Gameplay import gameplay

default_path = 'Assets/Tiles/'

keyVec = TileClass.keyVec
texture_dict = {
    'missing' : pygame.image.load(default_path + 'missing' + '.jpg')
    }

for i in keyVec:
    texture_dict[i] = pygame.image.load(default_path + i + '.jpg')

latura = 68
#THIS IS UPDATE

collision_tiles = []
collision_players = []
everything = []
everything_players = []
PlayerSpawns = [(None,None),(None,None),(None,None),(None,None)] #Blue, Green, Red, Yellow
PowerSpawns = []
collision_vector = []
collision_players_vector = []
theMap = None

#Merge and add walls as quadtree points
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

def generate_points_player():
    for i in range(18):
        for j in range(30):
            if collision_players[i][j] == True:
                collision_players[i][j] = False
                newVec = [(i,j)]
                J = j
                I = i
                Xflag = True
                Yflag = True
                while Xflag and J + 1 < 30:
                    J += 1
                    if collision_players[i][J] == True:
                        newVec.append((i,J))
                        collision_players[i][J] = False
                    else:
                        Xflag = False
                while Yflag and I + 1 < 18:
                    I += 1
                    extendVec = []
                    for thing in newVec:
                        if collision_players[I][thing[1]] == True:
                            extendVec.append((I,thing[1]))
                        else:
                           Yflag = False
                    if Yflag:
                        newVec.extend(extendVec)
                        for t in extendVec:
                            collision_players[t[0]][t[1]] = False
                everything_players.append(newVec)

    for rectangle in everything_players:
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
        collision_players_vector.append((x, y, latura * abs(Xmax - Xmin + 1), latura * abs(Ymax - Ymin + 1)))

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

def generate_outer_players():
    collision_players.clear()
    for i in range(18):
        newVec = []
        for j in range(30):
            newVec.append(False)
        collision_players.append(newVec)
def map_select(WIN,WIDTH,HEIGHT,FPS,Input,Playeri,joysticks) :
    #Aici va fi toata functia de a selecta ce harta vrei dar momentan ia doar ii da load hartii de test
    generate_outer_points()
    generate_outer_players()
    Map = pygame.Surface((latura * 28,latura * 16))
    Map.fill((255,255,255))
    maps = []
    for file in os.listdir("Assets/Maps"):
        file = file[:-4]
        img = pygame.image.load("Assets/Maps/" + file + '.jpg')
        maps.append((file, img))

    WIN.fill((0,0,0))
    WIN.blit(maps[0][1], (x, y))
    index = 0

    pygame.event.clear()

    font = pygame.font.Font("freesansbold.ttf", 26)

    textleft = font.render("<A", True, (255,255,255))
    leftrect = textleft.get_rect()
    leftrect.center = (x // 2, h + y * 4)
    textright = font.render("D>", True, (255,255,255))
    rightrect = textright.get_rect()
    rightrect.center = (WIDTH - x // 2, h + y * 4)
    textspace = font.render("Press SPACE to select the map", True, (255,255,255))
    spacerect = textspace.get_rect()
    spacerect.center = ((WIDTH - x) // 2, HEIGHT - y * 4)
    textloading = font.render("Starting game...", True, (255,255,255))
    loadrect = textloading.get_rect()
    loadrect.center = ((WIDTH - x) // 2, HEIGHT - y * 4)

    run = True
    while run:
        textmap = font.render(maps[index][0], True, (255,255,255))
        textrect = textmap.get_rect()
        textrect.center = ((WIDTH - x) // 2, h + y * 2)
        WIN.fill((0,0,0))
        WIN.blit(maps[index][1], (x, y))
        WIN.blit(textmap, textrect)
        if index != 0:
            WIN.blit(textleft, leftrect)
        if index != len(maps) - 1:
            WIN.blit(textright, rightrect)
        WIN.blit(textspace, spacerect)
        pygame.display.update()
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            pygame.quit()
            os._exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.unicode == 'a' and index > 0:
                index -= 1
            elif event.unicode == 'd' and index < len(maps) - 1:
                index += 1
            elif event.key == pygame.K_SPACE:
                theMap = maps[index][0]
                run = False
                textmap = font.render(maps[index][0], True, (255,255,255))
                textrect = textmap.get_rect()
                textrect.center = ((WIDTH - x) // 2, h + y * 2)
                WIN.fill((0,0,0))
                WIN.blit(maps[index][1], (x, y))
                WIN.blit(textmap, textrect)
                if index != 0:
                    WIN.blit(textleft, leftrect)
                if index != len(maps) - 1:
                    WIN.blit(textright, rightrect)
                WIN.blit(textloading, loadrect)
                pygame.display.update()


    specialTiles = ["Nothing", "Collidable", "CollidableWithPlayer", "PowerUpSpawn", "RedPlayerSpawn", "BluePlayerSpawn", "GreenPlayerSpawn", "YellowPlayerSpawn"]

    fstream = open('Maps/' + theMap + '.map', 'r')
    line = fstream.readline()
    while line :
        wordList = line.split()
        Map.blit(pygame.transform.scale(pygame.transform.rotate(texture_dict[wordList[3]], int(wordList[4])),(latura,latura)), (int(wordList[1]) * latura, int(wordList[0]) * latura))
        if wordList[2] == specialTiles[1]:
            collision_tiles[int(wordList[0]) + 1][int(wordList[1]) + 1] = True
        if wordList[2] == specialTiles[2]:
            collision_players[int(wordList[0]) + 1][int(wordList[1]) + 1] = True
        elif wordList[2] == specialTiles[3]:
            PowerSpawns.append((int(wordList[0]) + 1, int(wordList[1]) + 1))
        elif wordList[2] == specialTiles[5]:
            PlayerSpawns[0] = (int(wordList[0]) + 1, int(wordList[1]) + 1)
        elif wordList[2] == specialTiles[6]:
            PlayerSpawns[1] = (int(wordList[0]) + 1, int(wordList[1]) + 1)
        elif wordList[2] == specialTiles[4]:
            PlayerSpawns[2] = (int(wordList[0]) + 1, int(wordList[1]) + 1)
        elif wordList[2] == specialTiles[7]:
            PlayerSpawns[3] = (int(wordList[0]) + 1, int(wordList[1]) + 1)
        line = fstream.readline()
    generate_points()
    generate_points_player()
    return Map
    #gameplay(WIN,WIDTH,HEIGHT,FPS,Input,Playeri,joysticks,Map,qTree)

