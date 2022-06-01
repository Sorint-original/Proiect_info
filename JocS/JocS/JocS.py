import pygame

import os
import time
import random
import math
import copy

from Lobby import lobby
from MenuMain import Menu
from MapEditor import Editor
import QuadTreeTuple
import Geometrie

import Map_select
from Player import convert_and_resize_assets, EX_sequences,PU, PU_Images, Active_PU, avalible_powerups

font = pygame.font.SysFont("Times New Roman.ttf", 54)

VISUALIZE_COLLIDERS = True
VISUALIZE_QUADTREE = False
FPS_COUNTER = True

Botimg = ['Bottom-Blue.png','Bottom-Green.png','Bottom-Yellow.png','Bottom-Red.png']
Upimg = ['Upper-Blue.png','Upper-Green.png','Upper-Yellow.png','Upper-Red.png']
poziti_libere = 0
power_positions = []

def gameplay(Input,Playeri,joysticks,Map,PowerSpawns):
    global VISUALIZE_COLLIDERS
    global VISUALIZE_QUADTREE
    global poziti_libere
    global power_positions
    global avalible_powerups
    global Active_PU

    import ButtonClass
    import Player
    from Player import Harmful_Stuff
    from EventH import exit , controller_verify

    WIN.fill((0,0,0))
    pygame.display.update()

    sw = Map.get_width()
    sh = Map.get_height()

    queries = []
    points = []
    collided_points = []

    wall_points = Map_select.collision_vector
    player_wall = Map_select.collision_players_vector
    L = Map_select.latura

    h = HEIGHT - 110
    while (round(h * 1.75) > WIDTH - 50) :
        h -=  1
    w = round(h * 1.75)
    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2
    if y < 100 :
        y = 10
    #print(h)
    #print(w)

    #for i in range (len(PowerSpawns)) :
        #print(PowerSpawns[i][1],PowerSpawns[i][0])
    #time.sleep(1000)

    #se da resize la harta
    Map = pygame.transform.scale(Map,(w,h))
    convert_and_resize_assets(WIN,w,h,L)
    power_positions = []
    for i in range(len(PowerSpawns)) :
        power_positions.append(0)
    poziti_libere = len(power_positions)
    pu_spawn_cooldown = 120
    Afis_PU = []
    avalible_powerups[0] = len(PU)-2
    #pregatirea playerilor pentru Gameplay
    # cele patru poziti in care se pot spauna playeri
    poziti = (100 , 100 , sw - 100 , sh - 100 , sw - 100 , 100 , 100 , sh - 100)
    alcat = 0
    HUD_info = []
    size_P = 150 * (w / (L * 28))
    #pregatirea playerilor
    for i in range(4) :
        if Playeri[i].Selected :
            HUD_info.append([i])
            Playeri[i].Health = 1000
            Playeri[i].GX = Map_select.PlayerSpawns[i][1] * L - L // 2
            Playeri[i].GY = Map_select.PlayerSpawns[i][0] * L - L // 2
            Playeri[i].change_size(size_P,pygame.Surface.convert_alpha(pygame.image.load(os.path.join('Assets\Robots', Botimg[i]))),pygame.Surface.convert_alpha(pygame.image.load(os.path.join('Assets\Robots', Upimg[i]))))
            alcat = alcat + 2
    #informatiile pentru hud
    Hud = [(0, 0, 255),(51, 204, 51),(255, 204, 0),(255, 51, 0)]
    HEAT = pygame.Surface.convert_alpha(pygame.Surface.convert_alpha(pygame.image.load(os.path.join('Assets\HUD', "HEAT.png"))))
    for i in range(len(HUD_info)) :
        HUD_info[i].append(Hud[HUD_info[i][0]])
        if Playeri[HUD_info[i][0]].SW == 0 :
            HUD_info[i].append(pygame.Surface.convert_alpha(pygame.image.load(os.path.join('Assets\HUD', "Grenade_Launcher.png"))))
        elif Playeri[HUD_info[i][0]].SW == 1 :
            HUD_info[i].append(pygame.Surface.convert_alpha(pygame.image.load(os.path.join('Assets\HUD', "Flame_Thrower.png"))))
        elif Playeri[HUD_info[i][0]].SW == 2 :
            HUD_info[i].append(pygame.Surface.convert_alpha(pygame.image.load(os.path.join('Assets\HUD', "Rocket_Launcher.png"))))
        elif Playeri[HUD_info[i][0]].SW == 3 :
            HUD_info[i].append(pygame.Surface.convert_alpha(pygame.image.load(os.path.join('Assets\HUD', "Mine.png"))))
        elif Playeri[HUD_info[i][0]].SW == 4 :
            img = pygame.Surface.convert_alpha(pygame.image.load(os.path.join('Assets\HUD', "Energy_Gun.png")))
            img = pygame.transform.scale(img, (img.get_width() / img.get_height() * 20, 20))
            HUD_info[i].append(img)


    #stabilirea dimensiunilor pentru afisarea gameplayului

    Dupdate = [x,y,w,h]
    hfont = pygame.font.Font("freesansbold.ttf", 11)
    afont = pygame.font.Font("freesansbold.ttf", 20)
    uy = y + h + (HEIGHT - y - h - 90) / 2 - 1
    if len(HUD_info) == 4 :
        pas = (WIDTH - 1000) / 5 + 250
    elif len(HUD_info) == 3 :
        pas = (((WIDTH - 1000) / 5) * 3 + 250 * 2) / 2
    else :
        pas = ((WIDTH - 1000) / 5) * 3 + 250 * 3

    def draw_window(qtree) :
        #Afisarea Gameplay Environment

        WIN.blit(Map,(x,y))
        #afisarea powerup-urilor spaunate
        for i  in range(len(Afis_PU)) :
            IMG = PU_Images[Afis_PU[i].nrimg]
            WIN.blit(IMG,(Afis_PU[i].GX*(w/(L*28)) + x -IMG.get_width()//2,Afis_PU[i].GY*(h/(L*16)) + y -IMG.get_height()//2))
        for i in range(4) :
            if Playeri[i].Selected :
                #Afisare Player
                BIMAGE = pygame.transform.rotate(Playeri[i].Bottom_image,Playeri[i].Bottom_angle)
                Px = (Playeri[i].GX - BIMAGE.get_width() / 2) * (w / (L * 28)) + x
                Py = (Playeri[i].GY - BIMAGE.get_height() / 2) * (h / (L * 16)) + y
                WIN.blit(BIMAGE,(Px,Py))
                UIMAGE = pygame.transform.rotate(Playeri[i].Upper_image,Playeri[i].Upper_angle)
                Px = (Playeri[i].GX - UIMAGE.get_width() / 2) * (w / (L * 28)) + x
                Py = (Playeri[i].GY - UIMAGE.get_height() / 2) * (h / (L * 16)) + y
                WIN.blit(UIMAGE,(Px,Py))
                #End Afisare
                if VISUALIZE_COLLIDERS:
                    pygame.draw.circle(WIN, (0,0,255), (Playeri[i].GX * (w / (L * 28)) + x, Playeri[i].GY * (h / (L * 16)) + y), Playeri[i].size // 2, 3)
        del BIMAGE
        del UIMAGE
        #Afisare proiectile
        for i in range(len(Harmful_Stuff)) :
            if Harmful_Stuff[i].type == 0 :
                Hx = (Harmful_Stuff[i].GX - Harmful_Stuff[i].IMG.get_width() / 2) * (w / (L * 28)) + x
                Hy = (Harmful_Stuff[i].GY - Harmful_Stuff[i].IMG.get_height() / 2) * (h / (L * 16)) + y
                WIN.blit(Harmful_Stuff[i].IMG,(Hx,Hy))
            elif Harmful_Stuff[i].type == 1 :
                Hx = (Harmful_Stuff[i].GX - EX_sequences[Harmful_Stuff[i].nrimg].get_width() / 2) * (w / (L * 28)) + x
                Hy = (Harmful_Stuff[i].GY - EX_sequences[Harmful_Stuff[i].nrimg].get_height() / 2) * (h / (L * 16)) + y
                WIN.blit(EX_sequences[Harmful_Stuff[i].nrimg],(Hx,Hy))
            if VISUALIZE_COLLIDERS:
                pygame.draw.circle(WIN, (255,255,0), (Harmful_Stuff[i].GX * (w / (L * 28)) + x, Harmful_Stuff[i].GY * (h / (L * 16)) + y), Harmful_Stuff[i].diametru // 2, 3)

        #Quadtree generation and queries
        if VISUALIZE_COLLIDERS:
            for i in wall_points:
                pygame.draw.rect(WIN, (255,128,0), pygame.Rect((i[0] - i[2] // 2) * (w / (L * 28)) + x , (i[1] - i[3] // 2) * (h / (L * 16)) + y, i[2] * (w / (L * 28)), i[3] * (h / (L * 16))), 3)
        
        if VISUALIZE_QUADTREE:
            QuadTreeTuple.show_tree(WIN, qtree, afisrect, queries, points)

        #Collided points
        if VISUALIZE_COLLIDERS:
            for ptr in collided_points:
                pygame.draw.circle(WIN, (255,255,255), (ptr[0] * (w / (L * 28)) + x, ptr[1] * (h / (L * 16)) + y), 8)

        #Afisare HUD playeri
        #spatiu alocat pentru fiecare hud va fi de 250 x 90
        ux = (WIDTH - 1000) / 5
        for i in range(len(HUD_info)) :
            pygame.draw.rect(WIN,HUD_info[i][1], pygame.Rect(ux, uy + 1,250 , 90))
            pygame.draw.rect(WIN,(163, 194, 194), pygame.Rect(ux + 3, uy + 4,244 , 84))
            #Health bar
            pygame.draw.rect(WIN,(102, 153, 153), pygame.Rect(ux + 15, uy + 10,220 , 25))
            pygame.draw.rect(WIN,(255, 0, 0), pygame.Rect(ux + 17, uy + 12,216 * (Playeri[HUD_info[i][0]].Health / 1000) , 21))
            health = hfont.render(str(round(Playeri[HUD_info[i][0]].Health / 10)) + "/100",True,(255,255,255))
            WIN.blit(health,(ux + 17 + round((216 - health.get_width()) / 2),uy + 17))
            #Heat bar
            pygame.draw.rect(WIN,(102, 153, 153), pygame.Rect(ux + 15, uy + 40,220 , 14))
            WIN.blit(HEAT,(ux + 17, uy + 42))
            pygame.draw.rect(WIN,(102, 153, 153), pygame.Rect(ux + 17 + (216 * (Playeri[HUD_info[i][0]].MainWeapon.heat / 100)), uy + 40,216 - 216 * (Playeri[HUD_info[i][0]].MainWeapon.heat / 100) + 1 , 14))
            #afisare la cata amunitie ai la arma secundara
            WIN.blit(HUD_info[i][2],(ux + 15,uy + 59))
            ammo_count = afont.render(str(Playeri[HUD_info[i][0]].SecondaryWeapon.Ammo_count) ,True,(255,255,255))
            WIN.blit(ammo_count,(ux + 20 + HUD_info[i][2].get_width(),uy + 59))
            pygame.display.update((ux,uy + 1,250,90))
            ux = ux + pas
        #Display Update
        pygame.display.update(Dupdate)

    def colide_update(qtree) :
        for i in wall_points:
            queries.append((i[0], i[1], i[2] + size_P + 20, i[3] + size_P + 20, "WALL"))
        for i in player_wall:
            queries.append((i[0], i[1], i[2] + size_P + 20, i[3] + size_P + 20, "PLAYERWALL"))
        for query in queries:
            newVec = []
            QuadTreeTuple.query(query, newVec)
            newShape = None
            if len(query) == 4:
                newShape = (query[0], query[1], query[2] // 2, query[3])
            else:
                newShape = (query[0], query[1], query[2] - size_P-20, query[3] - size_P-20, query[4])
            for point in newVec:
                boolean, addon = Geometrie.check_collision(newShape, point[len(point) - 2])
                if boolean:
                    collided_points.append(point)
                    object = point[len(point) - 1]
                    if object != None:
                        if type(addon) is tuple and type(point[len(point) - 1]) is Player.player:
                            object.GX += addon[0]
                            object.GY += addon[1]
                        elif (type(point[len(point) - 1]) is Player.proiectil) or (type(point[len(point) - 1]) is Player.explosion):
                           if point[len(point) - 1] in Harmful_Stuff:
                               if newShape[len(newShape) - 1][0] == "PLR" :
                                   point[len(point) - 1].impact(newShape[len(newShape) - 1])
                               elif newShape[len(newShape) - 1] == "WALL":
                                   point[len(point) - 1].impact(["Wall",[query[0], query[1], query[2] - size_P-20, query[3] - size_P-20]])
                        elif  type(point[len(point) - 1]) is Player.power_up :
                            if newShape[len(newShape) - 1][0] == "PLR" :
                                global poziti_libere
                                global power_positions
                                global Active_PU
                                global avalible_powerups
                                point[len(point) - 1].do(Playeri[newShape[len(newShape) - 1][1]])
                                power_positions[point[len(point) - 1].nrpoz] = 0
                                Active_PU[point[len(point) - 1].nrpower_up] = 0
                                if point[len(point) - 1].nrpower_up > 1 :
                                    Active_PU[point[len(point) - 1].nrpower_up] = 1
                                    Playeri[newShape[len(newShape) - 1][1]].Powers.append(point[len(point) - 1].timer)
                                    Playeri[newShape[len(newShape) - 1][1]].Powers.append(point[len(point) - 1])
                                Afis_PU.remove(point[len(point) - 1])
                                poziti_libere += 1


            points.extend(newVec)

    WX = w / 1920
    WH = h / 1080

    clock = pygame.time.Clock()
    run = True
    latura = 68 
    rect = (14 * latura , 8 * latura , 30 * latura , 18 * latura  )
    afisrect = (x+w//2,y+h//2,(w/28)*30,(h/16)*18)
    qtree_points = []
    while run :
        qtree_points.clear()
        clock.tick(60)
        #pygame.time.wait(0)
        points.clear()
        queries.clear()
        collided_points.clear()

        #FPS counter
        if FPS_COUNTER:
            text = font.render(str(math.ceil(clock.get_fps())), True, (0,255,0))
            textRect = text.get_rect()
            WIN.fill((0,0,0))
            textRect.left = 0
            textRect.top = 0
            textRect.width += textRect.width // 3
            textRect.height += textRect.height // 3
            WIN.blit(text, textRect)
            pygame.display.update(textRect)

        #qTree = QuadTree.QuadTree(rect)

        #DAS EVENT LOOP
        for event in pygame.event.get() :
            exit(event)
            #controller_verify(event,joysticks)
            try :
                if event.joy != None :
                    Playeri[Input[event.joy]].update_input(event)
            except :
                if Input["Keyboard"] != None and event.type != pygame.MOUSEMOTION :
                    Playeri[Input["Keyboard"]].update_input(event)
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_h :
                        run = False
                    elif event.key == pygame.K_c :
                        if VISUALIZE_COLLIDERS == False :
                            VISUALIZE_COLLIDERS = True
                            VISUALIZE_QUADTREE = True
                        else :
                            VISUALIZE_QUADTREE = False
                            VISUALIZE_COLLIDERS = False
        #Updatarea pozitiei mousului pentru Player
        if Input["Keyboard"] != None :
            cord = pygame.mouse.get_pos()
            Ponsx = Playeri[Input["Keyboard"]].GX * WX + x
            Ponsy = Playeri[Input["Keyboard"]].GY * WH + y
            Playeri[Input["Keyboard"]].Control.Mouse[0] = cord[0] - Ponsx
            Playeri[Input["Keyboard"]].Control.Mouse[1] = cord[1] - Ponsy
        #updatarea playerului in the game
        for i in range(4) :
            if Playeri[i].Selected :
                Playeri[i].gameplay_update()
                treeObj = (Playeri[i].GX, Playeri[i].GY, (Playeri[i].GX, Playeri[i].GY, Playeri[i].size // 2), Playeri[i])
                qtree_points.append(treeObj)
                queries.append((Playeri[i].GX, Playeri[i].GY, Playeri[i].size, ("PLR",i)))
        #updatarea attackurilor
        for attack in Harmful_Stuff :
            attack.update()
            treeObj = (attack.GX, attack.GY, (attack.GX, attack.GY, attack.diametru // 2), attack)
            qtree_points.append(treeObj)
        #updatarea powerup-urilor
        if pu_spawn_cooldown == 0 and poziti_libere > 0 :
            #deciderea a ce se va spauna
            nrPowerup = None
            if random.randint(1,2) % 2 and (Active_PU[0]==0 or Active_PU[1]==0) :
                if Active_PU[0]==0 and Active_PU[1]==0 :
                    nrPowerup = random.randint(0,1)
                else :
                    for i in range (2) :
                        if Active_PU[i]==0 :
                            nrPowerup = i
            elif avalible_powerups[0] > 0 :
                nrPowerup = random.randint(1,avalible_powerups[0])
                i=0
                for j in range(2,len(PU)) :
                    if Active_PU[j] == 0 :
                        i +=1
                        if i == nrPowerup :
                            nrPowerup = j
                            avalible_powerups[0] -=1
                            break
            #deciderea locului unde se va spawna
            if nrPowerup != None :
                Active_PU[nrPowerup] = 1
                pos = random.randint(1,poziti_libere)
                i = 0
                for j in range(len(power_positions)) :
                    if power_positions[j] == 0  :
                        i +=1
                        if i == pos :
                            new_PU = copy.copy(PU[nrPowerup])
                            new_PU.GX = (PowerSpawns[j][1]*L - L//2)
                            new_PU.GY = (PowerSpawns[j][0]*L - L//2)
                            new_PU.nrpoz = j
                            Afis_PU.append(new_PU)
                            power_positions[j] = 1
                            poziti_libere -= 1 
                            break
                pu_spawn_cooldown = 60
        elif pu_spawn_cooldown > 0 :
            pu_spawn_cooldown -=1
        for i in range(len(Afis_PU)) :
            treeObj = (Afis_PU[i].GX, Afis_PU[i].GY, (Afis_PU[i].GX, Afis_PU[i].GY, Afis_PU[i].size // 2), Afis_PU[i] )
            qtree_points.append(treeObj)
        QuadTreeTuple.quadtree.clear()
        qtree = QuadTreeTuple.make(qtree_points, rect)
        #print("AMOUNT OF QTREEES ", len(QuadTreeTuple.quadtree))
        #QuadTreeTuple.divide(qtree, rect)
        colide_update(qtree)
        draw_window(qtree)

        
    # Ce se intampla ca sa iasa din gameplay
    Harmful_Stuff.clear()

pygame.init()

screen = pygame.display.Info()
WIDTH = screen.current_w

HEIGHT = screen.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

Start = True

while True:
    while True :
        if Start == True :
            Menu(WIN, WIDTH, HEIGHT, FPS)
        theInput, thePlayers, theJoysticks, theMap, Start = lobby(WIN, WIDTH, HEIGHT, FPS, Start)
        if Start == False :
            break
        #Editor(WIN, WIDTH, HEIGHT, FPS)

    gameplay(theInput, thePlayers, theJoysticks, theMap, PowerSpawns)