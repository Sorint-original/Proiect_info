import pygame
import os
import time
#import cython
import random
#import multiprocessing as mp
#from functools import partial

from Lobby import lobby
from MenuMain import Menu
from MapEditor import Editor
import QuadTree
import QuadTreeTuple

import Map_select
from Player import convert_and_resize_assets, EX_sequences


Botimg = ['Bottom-Blue.png','Bottom-Green.png','Bottom-Yellow.png','Bottom-Red.png']
Upimg = ['Upper-Blue.png','Upper-Green.png','Upper-Yellow.png','Upper-Red.png']

def gameplay(Input,Playeri,joysticks,Map):
    import ButtonClass
    from Player import Harmful_Stuff
    from EventH import exit , controller_verify

    WIN.fill((0,0,0))
    pygame.display.update()

    sw = Map.get_width()
    sh = Map.get_height()

    queries = []
    points = []

    wall_points = Map_select.collision_vector
    L = Map_select.latura
    clears = []
    process_list = []

    h = HEIGHT - 110
    while (round(h * 1.75) > WIDTH - 50) :
        h -=  1
    w = round(h * 1.75)
    x = (WIDTH - w) // 2
    y = (HEIGHT - h) // 2
    if y < 100 :
        y = 10
    print(h)
    print(w)

    #se da resize la harta
    Map = pygame.transform.scale(Map,(w,h))
    convert_and_resize_assets(WIN,w,h,L)
    #pregatirea playerilor pentru Gameplay
    # cele patru poziti in care se pot spauna playeri
    poziti = (100 , 100 , sw - 100 , sh - 100 , sw - 100 , 100 , 100 , sh - 100)
    alcat = 0
    HUD_info = []
    size_P = 150 * (w/(L*28))
    #pregatirea playerilor
    for i in range(4) :
        if Playeri[i].Selected :
            HUD_info.append([i])
            Playeri[i].Health = 1000
            Playeri[i].GX = poziti[alcat]
            Playeri[i].GY = poziti[alcat + 1]
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

    def draw_window() :
        qtree_points = []
        #Afisarea Gameplay Environment

        WIN.blit(Map,(x,y))
        for i in range(4) :
            if Playeri[i].Selected :
                #Afisare Player
                BIMAGE = pygame.transform.rotate(Playeri[i].Bottom_image,Playeri[i].Bottom_angle)
                Px = (Playeri[i].GX - BIMAGE.get_width() / 2) * (w/(L*28)) + x
                Py = (Playeri[i].GY - BIMAGE.get_height() / 2) * (h/(L*16)) + y
                WIN.blit(BIMAGE,(Px,Py))
                UIMAGE = pygame.transform.rotate(Playeri[i].Upper_image,Playeri[i].Upper_angle)
                Px = (Playeri[i].GX - UIMAGE.get_width() / 2) * (w/(L*28)) + x
                Py = (Playeri[i].GY - UIMAGE.get_height() / 2) * (h/(L*16)) + y
                WIN.blit(UIMAGE,(Px,Py))
                #End Afisare
                treeObj = (Playeri[i].GX, Playeri[i].GY)
                qtree_points.append(treeObj)
                queries.append((Playeri[i].GX, Playeri[i].GY, Playeri[i].size // 2))
        del BIMAGE
        del UIMAGE
        #Afisare proiectile
        for i in range(len(Harmful_Stuff)) :
            #Quadtree insertion
            treeObj = (Harmful_Stuff[i].GX, Harmful_Stuff[i].GY)
            qtree_points.append(treeObj)

            if Harmful_Stuff[i].type == 0 :
                Hx =(Harmful_Stuff[i].GX - Harmful_Stuff[i].IMG.get_width()/2)* (w/(L*28)) + x
                Hy =(Harmful_Stuff[i].GY - Harmful_Stuff[i].IMG.get_height()/2)* (h/(L*16)) + y
                WIN.blit(Harmful_Stuff[i].IMG,(Hx,Hy))
            elif Harmful_Stuff[i].type == 1 :
                Hx =(Harmful_Stuff[i].GX - EX_sequences[Harmful_Stuff[i].nrimg].get_width()/2)* (w/(L*28)) + x
                Hy =(Harmful_Stuff[i].GY - EX_sequences[Harmful_Stuff[i].nrimg].get_height()/2)* (h/(L*16)) + y
                WIN.blit(EX_sequences[Harmful_Stuff[i].nrimg],(Hx,Hy))

        #Quadtree generation and queries
        qtree_points.extend(wall_points)
        qtree = QuadTreeTuple.make(qtree_points, rect)
        for i in wall_points:
            queries.append((i[0], i[1], 25))
        QuadTreeTuple.divide(qtree, rect)
        for query in queries:
            QuadTreeTuple.query(query, points)
        QuadTreeTuple.show_tree(WIN, qtree, rect, queries, points)

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
            pygame.display.update((ux,uy+1,250,90))
            ux = ux + pas
        #Display Update
        pygame.display.update(Dupdate)

    WX = w / 1920
    WH = h / 1080

    clock = pygame.time.Clock()
    run = True
    latura = 68 
    rect = (28 * latura // 2, 16 * latura // 2, 28 * latura + latura + 10, 16 * latura + latura + 10)
    while run :
        clock.tick(60)
        print(clock.get_fps())
        points.clear()
        queries.clear()

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
                    if event.key == pygame.K_c :
                        if See_collisions == True :
                            See_collisions = False
                        else :
                            See_collisions = True
                    elif event.key == pygame.K_h :
                        print("works")
                        run = False
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
        for attack in Harmful_Stuff :
            attack.update()
        draw_window()

        
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
        #if Start == True :
            #Menu(WIN, WIDTH, HEIGHT, FPS)
        theInput, thePlayers, theJoysticks, theMap, Start = lobby(WIN, WIDTH, HEIGHT, FPS, Start)
        if Start == False :
            break
    #Editor(WIN, WIDTH, HEIGHT, FPS)

    gameplay(theInput, thePlayers, theJoysticks, theMap)




