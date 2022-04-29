import pygame
import os
from EventH import exit , controller_verify
# dau inport la clasa de butoane deoarece sar putea sa avem un Pause Menu si cred ca nu o sal putem face separat de gameplay
import ButtonClass
from Player import Harmful_Stuff

#input reprezinta un dictionar care indica care input(keyboard , controller) se duce la fiecare player , de asemenea as vrea un parameter MAP care e luat din MAPSELECT
def gameplay(WIN, WIDTH, HEIGHT, FPS, Input, Playeri, joysticks, Map, qTree) :
    sw = 1920
    sh = 1080
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
    font = pygame.font.Font("freesansbold.ttf", 20)
    Hud = ["BLUE",(0, 0, 255),"GREEN",(51, 204, 51),"YELLOW",(255, 204, 0),"RED",(255, 51, 0)]
    for i in range(len(HUD_info)) :
        text = font.render(Hud[HUD_info[i][0] * 2], True,Hud[HUD_info[i][0] * 2 + 1])
        HUD_info[i].append(text)
        HUD_info[i].append(Hud[HUD_info[i][0] * 2 + 1])
    #stabilirea dimensiunilor pentru afisarea gameplayului
    h = HEIGHT - 110
    #while (round(h * 1.78) > WIDTH - 50) :
    #    h = h - 1
    w = round(h * 1.78) 
    x = (WIDTH - w) // 2 
    y = (HEIGHT - h) // 2 
    if y < 100 :
        y = 10

    #Suprafata pe care se va intampla totul
    DisplayG = pygame.Surface((w, h))

    def environment_update() :
        DisplayG.blit(Map,(0,0))
        for i in range(4) :
            if Playeri[i].Selected :
                Playeri[i].afisare(DisplayG)
        for attack in Harmful_Stuff :
            attack.afisare(DisplayG)

    def draw_window() :
        WIN.fill((0,0,0))
        #Afisarea Gameplay Environment
        environment_update()
        #WIN.blit(pygame.transform.scale(DisplayG,(w,h)),(x,y))
        WIN.blit(DisplayG,(x,y))
        #Afisare HUD playeri spatiu alocat pentru fiecare hud va fi de 250 x 100
        ux = (WIDTH - 1000) / 5
        uy = HEIGHT - 100
        if len(HUD_info) == 4 :
            pas = (WIDTH - 1000) / 5 + 250
        elif len(HUD_info) == 3 :
            pas = (((WIDTH - 1000) / 5) * 3 + 250 * 2) / 2
        else :
            pas = ((WIDTH - 1000) / 5) * 3 + 250 * 3
        for i in range(len(HUD_info)) :
            WIN.blit(HUD_info[i][1], (ux + 10, uy + 5))
            pygame.draw.line(WIN,HUD_info[i][2], (ux - 1, uy + 24), (ux + 249, uy + 24))
            pygame.draw.rect(WIN,(255, 255, 255), pygame.Rect(ux, uy + 25,250 , 25))
            pygame.draw.rect(WIN,(255, 0, 0), pygame.Rect(ux, uy + 25,250 * (Playeri[HUD_info[i][0]].Health / 1000) , 25))
            ux = ux + pas
            
        qTree.show_tree(WIN)
        pygame.display.update()

    clock = pygame.time.Clock()
    run = True
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
        #Updatarea pozitiei mousului pentru Player
        if Input["Keyboard"] != None :
            cord = pygame.mouse.get_pos()
            Ponsx = Playeri[Input["Keyboard"]].GX * (w / 1920) + x
            Ponsy = Playeri[Input["Keyboard"]].GY * (h / 1080) + y
            Playeri[Input["Keyboard"]].Control.Mouse[0] = cord[0] - Ponsx
            Playeri[Input["Keyboard"]].Control.Mouse[1] = cord[1] - Ponsy
        #updatarea playerului in the game
        for i in range(4) :
            if Playeri[i].Selected :
                Playeri[i].gameplay_update()
        for attack in Harmful_Stuff :
            attack.update()
        draw_window()