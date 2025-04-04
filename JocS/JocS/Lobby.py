import pygame
import os

from EventH import exit , controller_verify
from Player import player
import ButtonClass
from Gameplay import gameplay
from Map_select import map_select

DEBUG_ONE_PLAYER_TEST = True

img = pygame.image.load("Assets/background/robou.png")
img = pygame.transform.scale(img, (ButtonClass.w, ButtonClass.h))

#Initializarea butoanelor la inceput astfel for fi gata de fiecare data cand se intra in lobby
menuButtons = []
ButtonClass.Button_Load("Lobby\menu", menuButtons)
BUTconfig=[]
ButtonClass.Button_Load("Lobby\config",BUTconfig)
buttontxt = ["Lobby\BP0","Lobby\BP1","Lobby\BP2","Lobby\BP3"]
BUTplayers = [[],[],[],[]]
for i in range(4) :
    ButtonClass.Button_Load(buttontxt[i],BUTplayers[i])

Botimg = ['Bottom-Blue.png','Bottom-Green.png','Bottom-Yellow.png','Bottom-Red.png']
Upimg = ['Upper-Blue.png','Upper-Green.png','Upper-Yellow.png','Upper-Red.png']
#variabile care trebe salvate
Playeri = []
joysticks = []
Input = {"Keyboard" : None , 0:None , 1:None , 2:None , 3:None , 4:None}

#initializarea playerilor
#Size-ul reprezinta marimea playerului pe ecran poate fi modificata oricand 

def initializare_info(WIDTH,HEIGHT) :
    global joysticks 
    global Playeri 
    global Input

    Playeri.clear()
    joysticks.clear()

    size = min(HEIGHT//3,(WIDTH - 150)//4) -50

    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for i in range (4) :
        Gx = 30 + i * ((WIDTH - 150) // 4 + 30) + (WIDTH - 150) // 8
        Gy = HEIGHT//2
        P = player(pygame.image.load(os.path.join('Assets\Robots', Botimg[i])), pygame.image.load(os.path.join('Assets\Robots', Upimg[i])), Gx, Gy, size,i)
        Playeri.append(P)
    Input = {"Keyboard" : None , 0:None , 1:None , 2:None , 3:None , 4:None}

def refreash_info(WIDTH,HEIGHT) :
    global joysticks 
    global Playeri 
    global Input
    size = min(HEIGHT//3,(WIDTH - 150)//4) -50
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for i in range(4) :
        Playeri[i].Ready = False
        Playeri[i].GX = 30 + i * ((WIDTH - 150) / 4 + 30) + (WIDTH - 150) / 8
        Playeri[i].GY = HEIGHT/2
        Playeri[i].change_size(size,pygame.image.load(os.path.join('Assets\Robots', Botimg[i])),pygame.image.load(os.path.join('Assets\Robots', Upimg[i])))
        Playeri[i].Upper_angle = 90 
        Playeri[i].Bottom_angle = 90
        Playeri[i].refresh_weapons()
        Playeri[i].Powers = []

def lobby (WIN,WIDTH,HEIGHT,FPS,Start) :

    pygame.init()
    pygame.joystick.init()
    global joysticks 
    global Playeri 
    global Input

    status = None

    if Start == True :
        initializare_info(WIDTH,HEIGHT)
    else :
        refreash_info(WIDTH,HEIGHT)
    
    #cooldownul de la momentu in care toti playeri selectati sunt ready si pana cand incepe meciul
    start_cooldown =91
    
    #INTRODUCEREA UNUI Player
    def set_control(control) :
        if Input[control] == None :
            for i in range(4) :
                if Playeri[i].Selected == False :
                    Playeri[i].Selected = True
                    Playeri[i].Source = control
                    Playeri[i].reset_control()
                    Input [control] = i 
                    BUTconfig[i].enabled = True
                    Playeri[i].Button = 0
                    BUTplayers[i][Playeri[i].Button].Hovering = True
                    break

    #SCOATEREA UNUI Player 
    def eject_control(control) :
        if Input[control] != None :
            Playeri[Input[control]].Selected = False
            Playeri[Input[control]].Ready = False
            Playeri[Input[control]].Source = "Unknown"
            BUTconfig[Input[control]].enabled = False
            BUTplayers[Input[control]][Playeri[i].Button].Hovering = False
            Input[control] = None

    #Desenarea ferestrei
    def draw_window() :
        WIN.fill((224,224,224))
        ButtonClass.displayButtons(WIN, menuButtons)
        for i in range(4) :
            x = 30 + i * ((WIDTH - 150) / 4 + 30)
            y = HEIGHT/3
            width = (WIDTH - 150)/4
            if Playeri[i].Ready == False :
                color = [200,200,200]
            else :
                color = [0,204,0]
            pygame.draw.rect(WIN, color, pygame.Rect(x, y, width, y))
            if Playeri[i].Selected == True :
                Playeri[i].afisare(WIN)
                #desenarea butoanelor playerilor selectati
                ButtonClass.displayButtons(WIN, BUTconfig[i])
                ButtonClass.displayButtons(WIN, BUTplayers[i])
        if start_cooldown < 91 :
            pygame.draw.rect(WIN, (230, 0, 0), pygame.Rect(0, HEIGHT - HEIGHT/25 , start_cooldown*WIDTH/180,HEIGHT/25 ))
        pygame.display.update()

    #The loop of the Lobby
    clock = pygame.time.Clock()
    run=True
    while run :
        clock.tick(FPS)
        #The event loop
        for event in pygame.event.get() :
            exit(event)
            controller_verify(event,joysticks)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                     status = ButtonClass.checkButtonClick(event.pos[0], event.pos[1], menuButtons, (1,2))

            try :
                if event.joy != None :
                    if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYHATMOTION :
                        set_control(event.joy)
                    if Input[event.joy] != None :
                        Playeri[Input[event.joy]].update_input(event)
                        if event.type == pygame.JOYHATMOTION :
                            if event.value[1] == 1 :
                                BUTplayers[Input[event.joy]][Playeri[Input[event.joy]].Button].Hovering = False
                                if Playeri[Input[event.joy]].Button != 0 :
                                    Playeri[Input[event.joy]].Button = Playeri[Input[event.joy]].Button -1
                                else :
                                    Playeri[Input[event.joy]].Button = 2
                                BUTplayers[Input[event.joy]][Playeri[Input[event.joy]].Button].Hovering = True
                            elif event.value[1] == -1 :
                                BUTplayers[Input[event.joy]][Playeri[Input[event.joy]].Button].Hovering = False
                                if Playeri[Input[event.joy]].Button != 2 :
                                    Playeri[Input[event.joy]].Button = Playeri[Input[event.joy]].Button +1
                                else :
                                    Playeri[Input[event.joy]].Button = 0
                                BUTplayers[Input[event.joy]][Playeri[Input[event.joy]].Button].Hovering = True
                        elif event.type == pygame.JOYBUTTONDOWN :
                            if event.button == Playeri[Input[event.joy]].Control.set["buttons"][1] :
                                if Playeri[Input[event.joy]].Button == 2 :
                                    if Playeri[Input[event.joy]].Ready == True :
                                        Playeri[Input[event.joy]].Ready = False
                                    else :
                                        Playeri[Input[event.joy]].Ready = True
                                elif Playeri[Input[event.joy]].Button == 0 :
                                    BUTplayers[Input[event.joy]][0].onPress(BUTplayers[Input[event.joy]][0])
                                    Playeri[Input[event.joy]].Next_MWeapon()
                                elif Playeri[Input[event.joy]].Button == 1 :
                                    BUTplayers[Input[event.joy]][1].onPress(BUTplayers[Input[event.joy]][1])
                                    Playeri[Input[event.joy]].Next_SWeapon()

            except :
                if event.type == pygame.KEYDOWN :
                    set_control("Keyboard")
                    if event.key == pygame.K_ESCAPE :
                        eject_control("Keyboard")
                if Input["Keyboard"] != None :
                    Playeri[Input["Keyboard"]].update_input(event)
                    #Schimbarea butoanelor pentru tastatura
                    if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_w :
                            BUTplayers[Input["Keyboard"]][Playeri[Input["Keyboard"]].Button].Hovering = False
                            if Playeri[Input["Keyboard"]].Button != 0 :
                                Playeri[Input["Keyboard"]].Button = Playeri[Input["Keyboard"]].Button -1
                            else :
                                Playeri[Input["Keyboard"]].Button = 2
                            BUTplayers[Input["Keyboard"]][Playeri[Input["Keyboard"]].Button].Hovering = True
                        if event.key == pygame.K_s :
                            BUTplayers[Input["Keyboard"]][Playeri[Input["Keyboard"]].Button].Hovering = False
                            if Playeri[Input["Keyboard"]].Button != 2 :
                                Playeri[Input["Keyboard"]].Button = Playeri[Input["Keyboard"]].Button +1
                            else :
                                Playeri[Input["Keyboard"]].Button = 0
                            BUTplayers[Input["Keyboard"]][Playeri[Input["Keyboard"]].Button].Hovering = True
                        if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN :
                            if Playeri[Input["Keyboard"]].Button == 2 :
                                if Playeri[Input["Keyboard"]].Ready == True :
                                    Playeri[Input["Keyboard"]].Ready = False
                                else :
                                    Playeri[Input["Keyboard"]].Ready = True
                            elif Playeri[Input["Keyboard"]].Button == 0 :
                                BUTplayers[Input["Keyboard"]][0].onPress(BUTplayers[Input["Keyboard"]][0])
                                Playeri[Input["Keyboard"]].Next_MWeapon()
                            elif Playeri[Input["Keyboard"]].Button == 1 :
                                    BUTplayers[Input["Keyboard"]][1].onPress(BUTplayers[Input["Keyboard"]][1])
                                    Playeri[Input["Keyboard"]].Next_SWeapon()

        pygame.event.pump()

        #Verifica daca un controler isi deselecteaza pozitia
        for i in range (5) :
            if Input[i] != None :
                if Playeri[Input[i]].exit_update() :
                    eject_control(i)


        #Verificarea butoanelor controlate de mouse 
        ButtonClass.checkButtonHover(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], BUTconfig)
        ButtonClass.checkButtonHover(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], menuButtons)

        #Functia care se uita la playeri care sunt ready si determina daca se continua
        ok = True 
        cati = 0
        for i in range(4) :
           if Playeri[i].Selected and Playeri[i].Ready :
               cati = cati + 1
           elif Playeri[i].Selected :
               ok = False
               break
        if ok and cati > 1 :
            start_cooldown = start_cooldown - 1 
        elif ok and cati > 0 and DEBUG_ONE_PLAYER_TEST:
            start_cooldown = 0
        else :
            start_cooldown = 91

        if start_cooldown == 0 or status == False:
            #aici pun momentan ca se va duce direct la gameplay dar in mod normal sar duce la map select
            if status == None:
                theMap, PowerSpawns = map_select(WIN,WIDTH,HEIGHT,FPS,Input,Playeri,joysticks)
                return Input, Playeri, joysticks, theMap, PowerSpawns ,False
            else:
                return Input, Playeri, joysticks, None, None, True

        draw_window()
