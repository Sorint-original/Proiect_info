import pygame
import os

from EventH import exit , controller_verify
from Player import player
import ButtonClass
from Gameplay import gameplay

#Initializarea butoanelor la inceput astfel for fi gata de fiecare data cand se intra in lobby
BUTconfig=[]
ButtonClass.Button_Load("Lobby\config",BUTconfig)
buttontxt = ["Lobby\BP0","Lobby\BP1","Lobby\BP2","Lobby\BP3"]
BUTplayers = [[],[],[],[]]
for i in range(4) :
    ButtonClass.Button_Load(buttontxt[i],BUTplayers[i])

def lobby (WIN,WIDTH,HEIGHT,FPS) :
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    Playeri = []
    #initializarea playerilor
    Botimg = ['Bottom-Blue.png','Bottom-Green.png','Bottom-Yellow.png','Bottom-Red.png']
    Upimg = ['Upper-Blue.png','Upper-Green.png','Upper-Yellow.png','Upper-Red.png']
    #Size-ul reprezinta marimea playerului pe ecran poate fi modificata oricand 
    size = min(HEIGHT/3,(WIDTH - 150)/4) -50
    for i in range (4) :
        Gx = 30 + i * ((WIDTH - 150) / 4 + 30) + (WIDTH - 150) / 8
        Gy = HEIGHT/2
        P = player(pygame.image.load(os.path.join('Assets', Botimg[i])), pygame.image.load(os.path.join('Assets', Upimg[i])), Gx, Gy, size)
        Playeri.append(P)
    Input = {"Keyboard" : None , 0:None , 1:None , 2:None , 3:None , 4:None}
    #cooldownul de la momentu in care toti playeri selectati sunt ready si pana cand incepe meciul
    start_cooldown =181
    
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
        WIN.fill((255,255,255))
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
        if start_cooldown < 181 :
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
                        if event.key == pygame.K_SPACE :
                            if Playeri[Input["Keyboard"]].Button == 2 :
                                if Playeri[Input["Keyboard"]].Ready == True :
                                    Playeri[Input["Keyboard"]].Ready = False
                                else :
                                    Playeri[Input["Keyboard"]].Ready = True

        pygame.event.pump()

        #Verifica daca un controler isi deselecteaza pozitia
        for i in range (5) :
            if Input[i] != None :
                if Playeri[Input[i]].exit_update() :
                    eject_control(i)


        #Verificarea butoanelor controlate de mouse 
        ButtonClass.checkButtonHover(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], BUTconfig)

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
        else :
            start_cooldown = 181

        if start_cooldown == 0 :
            #aici pun momentan ca se va duce direct la gemplay dar in mod normal sar duce la map select
            gameplay(WIN,WIDTH,HEIGHT,FPS,Input,Playeri,joysticks)
            for i in range(4) :
                Playeri[i].Ready = False
                Playeri[i].GX = 30 + i * ((WIDTH - 150) / 4 + 30) + (WIDTH - 150) / 8
                Playeri[i].GY = HEIGHT/2
                Playeri[i].change_size(size,pygame.image.load(os.path.join('Assets', Botimg[i])),pygame.image.load(os.path.join('Assets', Upimg[i])))

        draw_window()