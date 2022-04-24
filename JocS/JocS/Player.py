import pygame
import os

from Geometrie import get_angle , get_pos

#Toate proiectilele care se vor afla pe harta
Harmful_Stuff = []

class proiectil :
    def __init__ (self,x,y,image,angle,speed,nh) :
        self.GX = x
        self.GY = y
        self.Angle = angle
        self.IMG = pygame.transform.rotate(image , angle)
        self.Speed = speed
        self.noharm = nh

    def move (self) :
        newcords = get_pos(self.Angle , self.Speed)
        self.GX = self.GX + newcords[0]
        self.GY = self.GY + newcords[1]

    def afisare (self,screen) :
        x = self.GX - self.IMG.get_width()/2
        y = self.GY - self.IMG.get_height()/2
        screen.blit(self.IMG,(x,y))


class weapon :
    def __init__ (self,count,speed,spread,coold,shots_per_fire,ammo ) :
        #if count is -1 it means that it is unlimited
        self.Ammo_count = count
        self.Ammo_speed = speed
        # 0 means  perfect acuracy 
        self.Spread = spread
        #dupa cate frame-uri poate sa traga din nou
        self.fire_cooldown = coold
        self.cooldown = 0
        # cate gloante sunt trase pe fire 
        self.spfire = shots_per_fire
        #Imaginea pe care o are proiectilul tras
        self.Ammo = ammo
        #the player who will not be harmed by this bullet it is none or 0 to 3
        self.noharm = None

    #functia care verifica daca poata sa traga , action e true sau fals si determina daca playeru da comanda
    # x si y vor fi GX SI GY de la player
    def check_fire (self , angle , action ,x , y) :
        if self.cooldown > 0 :
            self.cooldown = self.cooldown -1
        elif action :
            self.cooldown = self.fire_cooldown
            new_shot = proiectil(x,y,self.Ammo,angle,self.Ammo_speed,self.noharm)
            Harmful_Stuff.append(new_shot)

Rifle = weapon(-1,10,0,30,1,pygame.transform.scale(pygame.image.load(os.path.join('Assets','Bullet.png' )),(25,5)))
Main_Weapons = [Rifle]

class control :
    def __init__ (self,source) :
        #controalele pentru cei cu controller
        if source != "Keyboard" and source != "Unknown" :
            #In orientare primul vector este de la LEFTJOYSTICK pentru miscare , al doilea vector e de la RIGHT JOYSTICK pentru tintire
            self.orientation = [[0,0],[0,0]]
            #In vectorul butoane  0 - Left bumper 1 - Right bumper 2 - left triger 3 - right triger 
            self.action = [False,False,-1,-1]
            #butoanele pot modifica doar in vectorul de action dar axele pot modifica in ambele ( o - modifica in orientation , a - modifica in action )
            self.input = { "axes":{ 0:["o",0], 1:["o",1] , 2:["o",2], 3:["o",3] , 4:["a",2], 5:["a",3] } , "buttons":{4:0 , 5:1} }
            #ce input modifica ce valori din orientation si action, pozitia 4 si 5 din axes modifica 2 si 3 din actions
            self.set = {"axes":[0, 1, 2, 3, 4, 5] , "buttons":[4, 5] }
        #controalele pentru cel care joaca cu keyboard si mous
        elif source != "Unknown" :
            #Coordonatele mousului
            self.Mouse = [0,0]
            #BUTOANELE DE PE MOUSE 0 LeftClick 1 Middlemouse button 2 Right click , restul sunt in caz daca are mai multe butoane pe mous ca sa nu dea crash , nu le folosim
            self.MouseButtons = [False , False , False , False , False , False , False , False , False , False]
            #controalele de la tastatura care pot fi modificate 
            # 0 - sus , 1 - stanga , 2 - jos , 3 - dreapta , 4 - abilitate activa , 5 - abilitate pasiva
            self.action =[False, False, False, False, False, False]
            #ce modifica anumite taste 
            self.input = {pygame.K_w:0 , pygame.K_a:1 , pygame.K_s:2 , pygame.K_d:3 , pygame.K_q:4 , pygame.K_e:5}
            #de ce tasta e modificata fiecare valoare din action
            self.set = [pygame.K_w , pygame.K_a , pygame.K_s , pygame.K_d , pygame.K_q , pygame.K_e]



class player:
    #Initializarea obiectului
    def __init__(self,BIMG,UIMG,Gx,Gy,size,nr):
        # The Variables used for the lobby
        self.number = nr
        self.Selected = False
        self.Source = "Unknown"
        self.Exit_cooldown = 0
        self.Ready = False
        self.configuring = False
        self.Button = 0
        #Controalele pentru pleyer (toate butoanele apasate,configurarea pentru controlar)
        self.Control = control(self.Source)
        #Variabile pentru afisare 
        # size va fi si diametrul cercului de coliziune
        self.size = size
        self.Bottom_image = pygame.transform.scale(BIMG,(9*self.size/8, 7*self.size/8))
        self.Upper_image = pygame.transform.scale(UIMG,(self.size,self.size))
        self.Upper_angle = 90
        self.Bottom_angle = 90
        self.GX = Gx
        self.GY = Gy
        #Variabile pentru Gameplay 
        self.Health = 1000
        self.maxspeed = 5
        self.MainWeapon = Main_Weapons[0]

    #schimbarea marimi are nevoie de o re introducere a imagini ne modificate ca sa arate cat mai bine
    def change_size (self , newsize , BIMG , UIMG) :
        self.size = newsize 
        self.Bottom_image = pygame.transform.scale(BIMG,(9*self.size/8, 7*self.size/8))
        self.Upper_image = pygame.transform.scale(UIMG,(self.size,self.size))
    #Functie de resetat controalele pleyerului
    def reset_control (self) :
        self.Control = control (self.Source)
    #Se verifica ce schimbari cauzeaza pentru player eventul
    def update_input (self , event) :
        if self.Source !="Keyboard" :
            #Pentru Controller
            if event.type == pygame.JOYBUTTONDOWN :
                try:
                    if self.Control.input["buttons"][event.button] != None :
                        self.Control.action[self.Control.input["buttons"][event.button]] = True
                except :
                    self.Control.input["buttons"][event.button] = None
            elif event.type == pygame.JOYBUTTONUP :
                try:
                    if self.Control.input["buttons"][event.button] != None :
                        self.Control.action[self.Control.input["buttons"][event.button]] = False
                except :
                    self.Control.input["buttons"][event.button] = None
            elif event.type == pygame.JOYAXISMOTION :
                try :
                    if self.Control.input["axes"][event.axis][0] != None :
                        if self.Control.input["axes"][event.axis][0] == "o" :
                            self.Control.orientation[int(self.Control.input["axes"][event.axis][1]/2)][self.Control.input["axes"][event.axis][1] % 2] = event.value
                        else :
                            self.Control.action[self.Control.input["axes"][event.axis][1]] = event.value
                except :
                    self.Control.input["axes"][event.axis] = [None , None]
        else :
            #Pentru Tastatura si mouse
            if event.type == pygame.KEYDOWN :
                try :
                    if self.Control.input[event.key] != None :
                        self.Control.action[self.Control.input[event.key]] = True
                except :
                    self.Control.input[event.key] = None
            elif event.type == pygame.KEYUP :
                try :
                    if self.Control.input[event.key] != None :
                        self.Control.action[self.Control.input[event.key]] = False
                except :
                    self.Control.input[event.key] = None
            elif event.type == pygame.MOUSEMOTION :
                self.Control.Mouse = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN :
                self.Control.MouseButtons[event.button-1] = True
            elif event.type == pygame.MOUSEBUTTONUP :
                self.Control.MouseButtons[event.button-1] = False
    #Functie folosita doar in lobby
    def exit_update (self) :
        if self.Exit_cooldown == 0 and self.Control.action[0] == True and self.configuring == False :
            self.Exit_cooldown = 120 
        if self.Exit_cooldown > 0 and self.Control.action[0] == True :
            self.Exit_cooldown -= 1
            if self.Exit_cooldown == 0 and self.configuring == False:
                return 1
        elif self.Exit_cooldown > 0 :
            self.Exit_cooldown = 0
        return 0
    #Functie pentru actualizarea playerului in timpul gameplayului
    def gameplay_update (self) :
        #Gameplay update pentru atunci cand este controlat de un controller
        if self.Source != "Keyboard" :
            #Obtinerea unghiurilor pentru imagini
            #bottom image
            if  abs(self.Control.orientation[0][0]) > 0.1 or abs(self.Control.orientation[0][1]) > 0.1 :
                self.Bottom_angle = get_angle(self.Control.orientation[0])
                #movement
                if self.Control.action[0] == False and self.Control.action[1] == False :
                    self.GX = self.GX + self.Control.orientation[0][0]*self.maxspeed
                    self.GY = self.GY + self.Control.orientation[0][1]*self.maxspeed
                else :
                    self.GX = self.GX + self.Control.orientation[0][0]*self.maxspeed/2
                    self.GY = self.GY + self.Control.orientation[0][1]*self.maxspeed/2
            #upper image
            if abs(self.Control.orientation[1][0]) > 0.1 or abs(self.Control.orientation[1][1]) > 0.1 :
                self.Upper_angle = get_angle(self.Control.orientation[1])
            #verificarea attackurilor
            self.MainWeapon.check_fire(self.Upper_angle,self.Control.action[0],self.GX,self.GY)      
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