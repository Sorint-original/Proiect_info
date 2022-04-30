import pygame
import os
from EventH import exit , controller_verify
# dau inport la clasa de butoane deoarece sar putea sa avem un Pause Menu si cred ca nu o sal putem face separat de gameplay
import ButtonClass
from Player import Harmful_Stuff

#input reprezinta un dictionar care indica care input(keyboard , controller) se duce la fiecare player , de asemenea as vrea un parameter MAP care e luat din MAPSELECT
def gameplay (WIN,WIDTH,HEIGHT,FPS,Input,Playeri,joysticks,Map,qTree) :
    sw = Map.get_width()
    sh = Map.get_height()
    #pregatirea playerilor pentru  Gameplay
    Botimg = ['Bottom-Blue.png','Bottom-Green.png','Bottom-Yellow.png','Bottom-Red.png']
    Upimg = ['Upper-Blue.png','Upper-Green.png','Upper-Yellow.png','Upper-Red.png']
    # cele patru poziti in care se pot spauna playeri
    poziti = (100 , 100 , sw - 100 , sh - 100 , sw - 100 , 100 , 100 , sh - 100 )
    alcat = 0
    HUD_info = []
    #pregatirea playerilor
    for i in range (4) :
        if Playeri[i].Selected :
            HUD_info.append([i])
            Playeri[i].Health = 1000
            Playeri[i].GX = poziti[alcat]
            Playeri[i].GY = poziti[alcat+1]
            Playeri[i].change_size(150,pygame.image.load(os.path.join('Assets\Robots', Botimg[i])),pygame.image.load(os.path.join('Assets\Robots', Upimg[i])))
            alcat = alcat + 2
    #informatiile pentru hud
    Hud = [(0, 0, 255),(51, 204, 51),(255, 204, 0),(255, 51, 0)]
    HEAT = pygame.image.load(os.path.join('Assets\HUD', "HEAT.png"))
    for i in range (len(HUD_info)) :
        HUD_info[i].append(Hud[HUD_info[i][0]])
        if Playeri[HUD_info[i][0]].SW == 0 :
            HUD_info[i].append(pygame.image.load(os.path.join('Assets\HUD', "Grenade_Launcher.png")))
        elif Playeri[HUD_info[i][0]].SW == 1 :
            HUD_info[i].append(pygame.image.load(os.path.join('Assets\HUD', "Flame_Thrower.png")))

    #stabilirea dimensiunilor pentru afisarea gameplayului
    h = HEIGHT - 110
    while ( round(h * 1.75)  > WIDTH - 50) :
        h = h -1
    w =  round(h*1.75)
    x =  (WIDTH - w)/2
    y = (HEIGHT - h )/2
    if y < 100 :
        y = 10

    #Suprafata pe care se va intampla totul
    DisplayG = pygame.Surface((sw,sh))
    See_collisions = False
    def environment_update () :
        DisplayG.blit(Map,(0,0))
        for i in range (4) :
            if Playeri[i].Selected :
                Playeri[i].afisare(DisplayG)
        for attack in Harmful_Stuff :
            attack.afisare(DisplayG)
            if See_collisions :
                pygame.draw.circle(DisplayG,(204, 0, 204),(attack.GX,attack.GY),attack.size/2)

    hfont = pygame.font.Font("freesansbold.ttf", 11)
    afont = pygame.font.Font("freesansbold.ttf", 20)
    uy =  y + h + (HEIGHT-y - h -90)/2 -1
    if len(HUD_info) == 4 :
       pas = (WIDTH-1000)/5 + 250
    elif len(HUD_info) == 3 :
       pas = (((WIDTH-1000)/5)*3 + 250*2)/2
    else :
       pas = ((WIDTH-1000)/5)*3 + 250*3

    def draw_window () :
        WIN.fill((0,0,0))
        #Afisarea Gameplay Environment
        environment_update()
        qTree.show_tree(DisplayG)
        WIN.blit(pygame.transform.scale(DisplayG,(w,h)),(x,y))
        #Afisare HUD playeri
        #spatiu alocat pentru fiecare hud va fi de 250 x 90
        ux = (WIDTH-1000)/5
        for i in range (len(HUD_info)) :
            pygame.draw.rect(WIN,HUD_info[i][1], pygame.Rect(ux, uy+1,250 , 90))
            pygame.draw.rect(WIN,(163, 194, 194), pygame.Rect(ux+3, uy+4,244 , 84))
            #Health bar
            pygame.draw.rect(WIN,(102, 153, 153), pygame.Rect(ux +15, uy+10,220 , 25))
            pygame.draw.rect(WIN,(255, 0, 0), pygame.Rect(ux+17, uy+12,216 * (Playeri[HUD_info[i][0]].Health/1000) , 21))
            health=hfont.render(str(round(Playeri[HUD_info[i][0]].Health/10)) + "/100",True,(255,255,255))
            WIN.blit(health,(ux + 17 + round((216-health.get_width())/2),uy +17))
            #Heat bar
            pygame.draw.rect(WIN,(102, 153, 153), pygame.Rect(ux +15, uy+40,220 , 14))
            WIN.blit(HEAT,(ux+17, uy+42))
            pygame.draw.rect(WIN,(102, 153, 153), pygame.Rect(ux + 17 + (216*(Playeri[HUD_info[i][0]].MainWeapon.heat/100)), uy+40,216-216*(Playeri[HUD_info[i][0]].MainWeapon.heat/100) +1 , 14))
            #afisare la cata amunitie ai la arma secundara
            WIN.blit(HUD_info[i][2],(ux + 15,uy +59))
            ammo_count = afont.render(str(Playeri[HUD_info[i][0]].SecondaryWeapon.Ammo_count) ,True,(255,255,255))
            WIN.blit(ammo_count,(ux + 20 +HUD_info[i][2].get_width(),uy +59))
            ux = ux + pas
            
        pygame.display.update()

    clock = pygame.time.Clock()
    run=True
    while run :
        clock.tick(FPS)
        # THE EVENT LOOP
        for event in pygame.event.get() :
            exit(event)
            controller_verify(event,joysticks)
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
        #Updatarea pozitiei mousului pentru Player
        if Input["Keyboard"] !=None :
            cord = pygame.mouse.get_pos()
            Ponsx = Playeri[Input["Keyboard"]].GX * (w/1920) + x
            Ponsy = Playeri[Input["Keyboard"]].GY * (h/1080) + y
            Playeri[Input["Keyboard"]].Control.Mouse[0] =  cord[0]-Ponsx
            Playeri[Input["Keyboard"]].Control.Mouse[1] =  cord[1]-Ponsy
        #updatarea playerului in the game
        for i in range (4) :
            if Playeri[i].Selected :
                Playeri[i].gameplay_update()
        for attack in Harmful_Stuff :
            attack.update()
        draw_window()