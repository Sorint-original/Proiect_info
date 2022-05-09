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

def attack_stuff(Harmful_Stuff, qTree, queries, i):
    print("NEW THING")
    attack = Harmful_Stuff[i]
    treeObj = QuadTree.TreeObject(attack.GX, attack.GY, False)
    qTree.insert(treeObj)
    queries.append(QuadTree.Circle(attack.GX, attack.GY, attack.size))

print("STARTED")
#newPool = mp.Pool(5)
#latura = 68

#rect = QuadTree.Rectangle(28 * latura // 2, 16 * latura // 2, 28 * latura + latura + 10, 16 * latura + latura + 10)

#test_trees = []
#test_qtree = QuadTree.QuadTree(rect)
##test_qtree_touple = QuadTreeTuple.QuadTree_Tuple((28 * latura // 2, 16 * latura // 2, 28 * latura + latura + 10, 16 * latura + latura + 10))
#test_trees_touple = []
#test_trees_tuples_kdtree = []
#now = time.time()
#for i in range(1000):
#    test_tree = QuadTree.TreeObject(1, 1, False)
#    #test_trees.append(test_tree)
#    test_qtree.insert(test_tree)

#print(f'Tree: {time.time() - now}')


#for i in range(1000):
#    #test_tree = (1,1)
#    test_tree = (random.randrange(latura + 5, 28 * latura), random.randrange(latura + 5, 16 * latura))
#    test_trees_touple.append(test_tree)
#    #test_qtree_touple.insert(test_tree)        
#now = time.time()
#tree = QuadTreeTuple.make(test_trees_touple, (28 * latura // 2, 16 * latura // 2, 28 * latura + latura + 10, 16 * latura + latura + 10))
#print(f'Tree: {time.time() - now}')
#print(tree)

def gameplay(Input,Playeri,joysticks,Map):
    import ButtonClass
    from Player import Harmful_Stuff
    from EventH import exit , controller_verify

    sw = Map.get_width()
    sh = Map.get_height()

    queries = []
    points = []

    wall_points = Map_select.collision_vector

    clears = []
    process_list = []
    #pregatirea playerilor pentru Gameplay
    Botimg = ['Bottom-Blue.png','Bottom-Green.png','Bottom-Yellow.png','Bottom-Red.png']
    Upimg = ['Upper-Blue.png','Upper-Green.png','Upper-Yellow.png','Upper-Red.png']
    # cele patru poziti in care se pot spauna playeri
    poziti = (100 , 100 , sw - 100 , sh - 100 , sw - 100 , 100 , 100 , sh - 100)
    alcat = 0
    HUD_info = []
    #pregatirea playerilor
    for i in range(4) :
        if Playeri[i].Selected :
            HUD_info.append([i])
            Playeri[i].Health = 1000
            Playeri[i].GX = poziti[alcat]
            Playeri[i].GY = poziti[alcat + 1]
            Playeri[i].change_size(150,pygame.image.load(os.path.join('Assets\Robots', Botimg[i])),pygame.image.load(os.path.join('Assets\Robots', Upimg[i])))
            alcat = alcat + 2
    #informatiile pentru hud
    Hud = [(0, 0, 255),(51, 204, 51),(255, 204, 0),(255, 51, 0)]
    HEAT = pygame.image.load(os.path.join('Assets\HUD', "HEAT.png"))
    for i in range(len(HUD_info)) :
        HUD_info[i].append(Hud[HUD_info[i][0]])
        if Playeri[HUD_info[i][0]].SW == 0 :
            HUD_info[i].append(pygame.image.load(os.path.join('Assets\HUD', "Grenade_Launcher.png")))
        elif Playeri[HUD_info[i][0]].SW == 1 :
            HUD_info[i].append(pygame.image.load(os.path.join('Assets\HUD', "Flame_Thrower.png")))

    #stabilirea dimensiunilor pentru afisarea gameplayului
    h = HEIGHT - 110
    while (round(h * 1.75) > WIDTH - 50) :
        h = h - 1
    w = round(h * 1.75)
    x = (WIDTH - w) / 2
    y = (HEIGHT - h) / 2
    if y < 100 :
        y = 10

    #Suprafata pe care se va intampla totul
    #DisplayG = pygame.Surface((sw,sh))
    #See_collisions = False

    def environment_update(qtree_points) :
        #DisplayG.blit(Map,(0,0))
        def temp_att(attack):
            #attack.afisare(DisplayG)
            treeObj = (attack.GX, attack.GY)
            qtree_points.append(treeObj)
            #qTree.insert(QuadTree.TreeObject(attack.GX, attack.GY, False))
        #elapsed_time = time.process_time() - t

        #print(elapsed_time)

        for i in range(4) :
            if Playeri[i].Selected :
                Playeri[i].afisare(WIN)
                treeObj = (Playeri[i].GX, Playeri[i].GY)
                #qTree.insert(QuadTree.TreeObject(Playeri[i].GX, Playeri[i].GY, False))
                #queries.append(QuadTree.Circle(Playeri[i].GX, Playeri[i].GY, Playeri[i].size))
                qtree_points.append(treeObj)
                queries.append((Playeri[i].GX, Playeri[i].GY, Playeri[i].size))

        qtree_points.extend(wall_points)

        for i in wall_points:
            queries.append((i[0], i[1], 25))
            #queries.append(QuadTree.Circle(i.x, i.y, 25))

        #newPool.map(partial(attack_stuff, Harmful_Stuff, qTree, queries), range(len(Harmful_Stuff)))
        #start = time.time()
        count = 0
        witdh = None
        heihgt = None
        y = None
        blit_sequence = []
        for i in Harmful_Stuff:
            temp_att(i)
            if count == 0:
                witdh = i.IMG.get_width() / 2
                height = i.IMG.get_height() / 2
                count += 1
            blit_sequence.append((i.IMG, (i.GX - witdh, i.GY - height)))
        #print(blit_sequence)
        WIN.blits(blit_sequence)
        #end = time.time()
        #print(end - start)

    hfont = pygame.font.Font("freesansbold.ttf", 11)
    afont = pygame.font.Font("freesansbold.ttf", 20)
    uy = y + h + (HEIGHT - y - h - 90) / 2 - 1
    if len(HUD_info) == 4 :
        pas = (WIDTH - 1000) / 5 + 250
    elif len(HUD_info) == 3 :
        pas = (((WIDTH - 1000) / 5) * 3 + 250 * 2) / 2
    else :
        pas = ((WIDTH - 1000) / 5) * 3 + 250 * 3

    def draw_window():
        WIN.fill((0,0,0))
        qtree_points = []
        #Afisarea Gameplay Environment
        environment_update(qtree_points)
        #for q in queries:
        #    qTree.query(q, points)
        #qTree.show_tree(WIN, points, queries)
        #print(len(Harmful_Stuff))
        qtree = QuadTreeTuple.make(qtree_points, rect)
        start = time.time()
        for i in queries:
            QuadTreeTuple.theQuery(qtree, rect, i, points)
        print("TIME IT TOOK:", time.time() - start)
        QuadTreeTuple.show_tree(WIN, qtree, rect, queries, points)
        #WIN.blit(pygame.transform.scale(DisplayG,(w,h)),(x,y))
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
            ux = ux + pas
           
        pygame.display.update()

    WX = w / 1920
    WH = h / 1080

    clock = pygame.time.Clock()
    run = True
    latura = 68 
    rect = (28 * latura // 2, 16 * latura // 2, 28 * latura + latura + 10, 16 * latura + latura + 10)
    while run :
        clock.tick(60)
        #pygame.time.wait(0)
        print(clock.get_fps())
        points.clear()
        queries.clear()

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
        #start = time.time()
        draw_window()
        #end = time.time()



        #print(end-start)

        #del qTree
        
    # Ce se intampla ca sa iasa din gameplay
    Harmful_Stuff.clear()

pygame.init()

screen = pygame.display.Info()
WIDTH = screen.current_w

HEIGHT = screen.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

while True:

    #Menu(WIN, WIDTH, HEIGHT, FPS)
    theInput, thePlayers, theJoysticks, theMap = lobby(WIN, WIDTH, HEIGHT, FPS)
    #Editor(WIN, WIDTH, HEIGHT, FPS)

    gameplay(theInput, thePlayers, theJoysticks, theMap)




