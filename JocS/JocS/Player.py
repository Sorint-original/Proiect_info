import pygame
from Geometrie import get_angle


class control :
    def __init__ (self,source) :
        if source != "Keyboard" and source != "Unknown" :
            #Valorile pe care le vom folosi pentru butoane
            self.NR_LB = 4
            self.NR_RB = 5
            #Valorile pe care le vom folosi pentru axe [ AXA X , AXA Y ]
            self.NR_AX_LJ = [0,1]
            self.NR_AX_RJ = [2,3]
            self.NR_AXLT = 4
            self.NR_AXRT = 5
            #Butoanele apasate de controller
            self.LB = False
            self.RB = False
            #Trigarele sunt axe dar pentru joc le vom trata ca butoane
            self.LT = False
            self.RT = False
            #Valorile de la axele joystickurilor [ AXA X , AXA Y ]
            self.LJ = [0,0]
            self.RJ = [0,0]
        elif source != "Unknown" :
            #Tastele folosite de player la tastatura
            self.taste = {pygame.K_w:False, pygame.K_a:False, pygame.K_s:False, pygame.K_d:False, pygame.K_q:False, pygame.K_e:False}
            #Coordonatele mousului
            self.Mouse = [0,0]
            #BUTOANELE DE PE MOUSE 0 LeftClick 1 Middlemouse button 2 Right click
            self.MouseButtons = [False , False , False ]


class player:
    #Initializarea obiectului
    def __init__(self,BIMG,UIMG,Gx,Gy,size):
        # The Variables used for the lobby
        self.Selected = False
        self.Source = "Unknown"
        self.Exit_cooldown = 0
        self.Ready = False
        self.configuring = False
        #Controalele pentru pleyer (toate butoanele apasate,configurarea pentru controlar)
        self.Control = control(self.Source)
        #Variabile pentru afisare 
        self.size = size
        self.Bottom_image = pygame.transform.scale(BIMG,(9*self.size/8, 7*self.size/8))
        self.Upper_image = pygame.transform.scale(UIMG,(self.size,self.size))
        self.Upper_angle = 90
        self.Bottom_angle = 90
        self.GX = Gx
        self.GY = Gy

    #Functie de resetat controalele pleyerului
    def reset_control (self) :
        self.Control = control (self.Source)
    #Se verifica ce schimbari cauzeaza pentru player eventul
    def update_input (self , event) :
        if self.Source !="Keyboard" :
            #Pentru Controller
            if event.type == pygame.JOYBUTTONDOWN :
                if event.button == self.Control.NR_LB :
                    self.Control.LB = True
                elif event.button == slef.Control.NR_RB :
                    self.Control.RB = True
            elif event.type == pygame.JOYBUTTONUP :
                if event.button == self.Control.NR_LB :
                    self.Control.LB = False
                elif event.button == slef.Control.NR_RB :
                    self.Control.RB = False
            elif event.type == pygame.JOYAXISMOTION :
                if event.axis == self.Control.NR_AXLT :
                    if event.value == -1 :
                        self.Control.LT = False
                    else :
                        self.Control.LT = True
                elif event.axis == self.Control.NR_AXRT :
                    if event.value == -1 :
                        self.Control.RT = False
                    else :
                        self.Control.RT = True
                elif event.axis == self.Control.NR_AX_LJ[0] :
                    self.Control.LJ[0] = round(event.value,2)
                elif event.axis == self.Control.NR_AX_LJ[1] :
                    self.Control.LJ[1] = round(event.value,2)
                elif event.axis == self.Control.NR_AX_RJ[0] :
                    self.Control.RJ[0] = round(event.value,2)
                elif event.axis == self.Control.NR_AX_RJ[1] :
                    self.Control.RJ[1] = round(event.value,2)
        else :
            #Pentru Tastatura si mouse
            if event.type == pygame.KEYDOWN :
                self.Control.taste[event.key] = True
            elif event.type == pygame.KEYUP :
                self.Control.taste[event.key] = False 
            elif event.type == pygame.MOUSEMOTION :
                self.Control.Mouse = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN :
                self.Control.MouseButtons[event.button-1] = True
            elif event.type == pygame.MOUSEBUTTONUP :
                self.Control.MouseButtons[event.button-1] = False
    #Functie folosita doar in lobby
    def exit_update (self) :
        if self.Exit_cooldown == 0 and self.Control.LB == True and self.configuring == False :
            self.Exit_cooldown = 120 
        if self.Exit_cooldown > 0 and self.Control.LB == True :
            self.Exit_cooldown -= 1
            if self.Exit_cooldown == 0 and self.configuring == False:
                return 1
        elif self.Exit_cooldown > 0 :
            self.Exit_cooldown = 0
        return 0
    #Functie pentru actualizarea playerului in timpul gameplayului
    def gameplay_update (self) :
        if self.Source != "Keyboard" :
            if  abs(self.Control.LJ[0]) > 0.1 or abs(self.Control.LJ[1]) > 0.1 :
                self.Bottom_angle = get_angle(self.Control.LJ)
            if abs(self.Control.RJ[0]) > 0.1 or abs(self.Control.RJ[1]) > 0.1 :
                self.Upper_angle = get_angle(self.Control.RJ)
    #Afisarea playerului pe ecran la coordonatele lui 
    def afisare (self,WIN) :
        BIMAGE = pygame.transform.rotate(self.Bottom_image,self.Bottom_angle)
        x = self.GX - BIMAGE.get_width()/2
        y = self.GY - BIMAGE.get_height()/2
        WIN.blit(BIMAGE,(x,y))
        del BIMAGE
        UIMAGE = pygame.transform.rotate(self.Upper_image,self.Upper_angle)
        x = self.GX - UIMAGE.get_width()/2
        y = self.GY - UIMAGE.get_height()/2
        WIN.blit(UIMAGE,(x,y))
        del UIMAGE