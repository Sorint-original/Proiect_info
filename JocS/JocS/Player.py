import pygame
import os
import random
import copy

from Geometrie import get_angle , get_pos

#Toate proiectilele care se vor afla pe harta
Harmful_Stuff = []

EX_sequences = [pygame.image.load(os.path.join('Assets\Explosion','EX0.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX1.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX2.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX3.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX4.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX5.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX6.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX7.png' ))]

class explosion :
    def __init__ (self,x,y,size,dmg) :
        self.GX = x
        self.GY = y
        self.PGX = x
        self.PGY = y
        self.existance = 57
        self.size = size
        self.damage = dmg
        #Fiecare player poate sa ia damage doar o data de la o anumita explozie
        self.noharm = []

    def update (self) :
        self.existance = self.existance - 1
        if self.existance == 0 :
            Harmful_Stuff.remove(self)
    def afisare(self,screen) :
        if self.existance > 49 :
            screen.blit(pygame.transform.scale(EX_sequences[0],(self.size/2,self.size/2)),(self.GX -self.size/4,self.GY -self.size/4))
        elif self.existance > 42 :
            screen.blit(pygame.transform.scale(EX_sequences[1],(self.size*2/3,self.size*2/3)),(self.GX -self.size/3,self.GY -self.size/3))
        elif self.existance > 35 :
            screen.blit(pygame.transform.scale(EX_sequences[2],(self.size,self.size)),(self.GX -self.size/2,self.GY -self.size/2))
        elif self.existance > 28 :
            screen.blit(pygame.transform.scale(EX_sequences[3],(self.size,self.size)),(self.GX -self.size/2,self.GY -self.size/2))
        elif  self.existance >21 :
            screen.blit(pygame.transform.scale(EX_sequences[4],(self.size,self.size)),(self.GX -self.size/2,self.GY -self.size/2))
        elif  self.existance >14 :
            screen.blit(pygame.transform.scale(EX_sequences[5],(self.size,self.size)),(self.GX -self.size/2,self.GY -self.size/2))
        elif  self.existance >7 :
            screen.blit(pygame.transform.scale(EX_sequences[6],(self.size,self.size)),(self.GX -self.size/2,self.GY -self.size/2))
        elif self.existance > 0 :
            screen.blit(pygame.transform.scale(EX_sequences[7],(self.size,self.size/2)),(self.GX -self.size/2,self.GY -self.size/4))
    #aceasta functie va fi chemata cand un anumit glont intra in contact cu alt obiect
    #other va tine un fel de id explicand ce si unde se afla obiectul lovit
    def impact (self,other) :
        #momentan nimic
        print("yeet")


class proiectil :
    def __init__ (self,x,y,size,image,angle,speed,Dmg,A,mins,ext,EXPLOD,Bounce,nh) :
        self.GX = x
        self.GY = y
        #pgx si pgy sunt coordonatele pe care le avea inainte Playeru
        self.PGX = x
        self.PGY = y
        #self.size reprezinta diametru cercului de coliziunea a glontului
        self.size = size
        self.Angle = angle
        self.IMG = pygame.transform.rotate(image , angle)
        self.Speed = speed
        self.noharm = nh
        self.dmg = Dmg
        self.acceleration = A
        self.minspeed = mins
        self.existence = ext
        self.Will_Explode = EXPLOD
        self.Bouncy = Bounce
    def update (self) :
        #Verifica daca mai exista atacu
        if self.existence > 0 :
            self.existence = self.existence -1
        if self.existence == 0 :
            if self.Will_Explode :
                Harmful_Stuff.append(explosion(self.GX,self.GY,200,self.dmg))
            Harmful_Stuff.remove(self)

        #misca atackul
        self.PGX = self.GX
        self.PGY = self.GY
        newcords = get_pos(self.Angle , self.Speed)
        self.GX = self.GX + newcords[0]
        self.GY = self.GY + newcords[1]
        #ii modifica viteza
        if self.Speed > self.minspeed :
            self.Speed = self.Speed + self.acceleration
            if self.Speed <=  self.minspeed:
                self.Speed = self.minspeed

    def afisare(self,screen) :
        x = self.GX - self.IMG.get_width() / 2
        y = self.GY - self.IMG.get_height() / 2
        screen.blit(self.IMG, (x,y))

    #aceasta functie va fi chemata cand un anumit glont intra in contact cu alt obiect
    #other va tine un fel de id explicand ce si unde se afla obiectul lovit
    def impact (self,other) :
        #momentan nimic
        print("yeet")


class weapon :
    def __init__ (self,size,count,speed,spread,coold,shots_per_fire,H,damage,A,mins,bext,EXP,B,ammo) :
        #marimea diametrului unui glont
        self.size = size
        #if count is -1 it means that it is unlimited
        self.Ammo_count = count
        self.Ammo_speed = speed
        # 0 means perfect acuracy
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
        #overheating variables
        self.heat = 0
        self.heatpershot = H
        self.cooling = 0.55
        self.OVERHEATED = False
        #damage per shot
        self.dmg = damage
        #deaccelerarea
        self.acceleration = A
        self.minspeed = mins
        #timer pentru existebta glontului
        self.existence = bext
        self.explosive = EXP
        self.bounce = B

    #functia care verifica daca poata sa traga , action e true sau fals si
    #determina daca playeru da comanda
    # x si y vor fi GX SI GY de la player
    def check_fire(self , angle , action ,x , y) :
        if self.cooldown > 0 :
            self.cooldown = self.cooldown -1
        if self.heat > 0 :
            self.heat = self.heat - self.cooling
        if self.OVERHEATED == True and self.heat <= 0 :
            self.heat = 0
            self.OVERHEATED = False
        if action and abs(self.Ammo_count) > 0 and self.OVERHEATED == False and self.cooldown == 0 :
            #tot ce trebe sa faca pentru a trage
            self.heat = self.heat + self.heatpershot
            if self.heat >= 100 :
                self.heat = 100
                self.OVERHEATED = True
            self.cooldown = self.fire_cooldown
            if self.Spread > 0 and self.spfire > 1 :
                A = []
                for i in range(-self.Spread , self.Spread+1) :
                    A.append(i)
            for i in range (self.spfire) :
                newangle = angle
                if self.Spread > 0 and self.spfire > 1:
                    deviasion = random.choice(A)
                    newangle = newangle + deviasion
                    A.remove(deviasion)
                elif self.Spread > 0 :
                    newangle = newangle + random.randint(-self.Spread,self.Spread)
                new_shot = proiectil(x,y,self.size,self.Ammo,newangle,self.Ammo_speed,self.dmg,self.acceleration,self.minspeed,self.existence,self.explosive,self.bounce,self.noharm)
                Harmful_Stuff.append(new_shot)
            if self.Spread > 0 and self.spfire > 1 :
                del A
            if self.Ammo_count != -1 :
                self.Ammo_count = self.Ammo_count - 1

# Main Weopans care se folosesc in joc 
Rifle = weapon(10,-1,25,0,10,1,10,25,0,25,-1,False,False,pygame.transform.scale(pygame.image.load(os.path.join('Assets','Bullet.png' )),(25,5)))
Shotgun = weapon(10,-1,25,3,30,5,40,75,0,25,-1,False,False,pygame.transform.scale(pygame.image.load(os.path.join('Assets','Bullet.png' )),(25,5)))
SMG = weapon(10,-1,25,5,0,1,1.5,5,0,25,-1,False,False,pygame.transform.scale(pygame.image.load(os.path.join('Assets','Bullet.png' )),(25,5)))
Main_Weapons = [Rifle,Shotgun,SMG]
MWcount = 3

#Secondary weapons care se folosesc in joc
Grenade_Launcher = weapon(15,10,30,0,60,1,0,0,-0.5,0,120,True,True,pygame.transform.scale(pygame.image.load(os.path.join('Assets','Grenade.png' )),(15,18)))
Flame_Thrower = weapon(30,-1,25,15,0,1,0,5,-0.7,6,100,False,True,pygame.transform.scale(pygame.image.load(os.path.join('Assets','Flame.png' )),(39,30)))
Secondary_Weapons = [Grenade_Launcher,Flame_Thrower]
SWcount = 2


class control :
    def __init__(self,source) :
        #controalele pentru cei cu controller
        if source != "Keyboard" and source != "Unknown" :
            #In orientare primul vector este de la LEFTJOYSTICK pentru miscare
            #, al doilea vector e de la RIGHT JOYSTICK pentru tintire
            self.orientation = [[0,0],[0,0]]
            #In vectorul butoane 0 - Left bumper 1 - Right bumper 2 - left
            #triger 3 - right triger
            self.action = [False,False,-1,-1]
            #butoanele pot modifica doar in vectorul de action dar axele pot
            #modifica in ambele ( o - modifica in orientation , a - modifica in
            #action )
            self.input = { "axes":{ 0:["o",0], 1:["o",1] , 2:["o",2], 3:["o",3] , 4:["a",2], 5:["a",3] } , "buttons":{4:0 , 5:1} }
            #ce input modifica ce valori din orientation si action, pozitia 4
            #si 5 din axes modifica 2 si 3 din actions
            self.set = {"axes":[0, 1, 2, 3, 4, 5] , "buttons":[4, 5] }
        #controalele pentru cel care joaca cu keyboard si mous
        elif source != "Unknown" :
            #Coordonatele mousului
            self.Mouse = [0,0]
            #BUTOANELE DE PE MOUSE 0 LeftClick 1 Middlemouse button 2 Right
            #click , restul sunt in caz daca are mai multe butoane pe mous ca
            #sa nu dea crash , nu le folosim
            self.MouseButtons = [False , False , False , False , False , False , False , False , False , False]   #controalele de la tastatura care pot fi modificate 
            # 0 - sus , 1 - stanga , 2 - jos , 3 - dreapta , 4 - abilitate activa , 5 - abilitate pasiva
            self.action =[0, 0, 0, 0, 0, 0]
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
        #Controalele pentru pleyer (toate butoanele apasate,configurarea pentru
        #controlar)
        self.Control = control(self.Source)
        #Variabile pentru afisare
        # size va fi si diametrul cercului de coliziune
        self.size = size
        self.Bottom_image = pygame.transform.scale(BIMG,(9 * self.size / 8, 7 * self.size / 8))
        self.Upper_image = pygame.transform.scale(UIMG,(self.size,self.size))
        self.Upper_angle = 90
        self.Bottom_angle = 90
        self.GX = Gx
        self.GY = Gy
        #Variabile pentru Gameplay
        self.Health = 1000
        self.maxspeed = 5
        self.MainWeapon = copy.copy(Main_Weapons[0])
        self.MainWeapon.noharm = self.number
        self.MW = 0
        self.SecondaryWeapon = copy.copy(Secondary_Weapons[0])
        self.SecondaryWeapon.noharm = self.number
        self.SW = 0

    #schimbarea marimi are nevoie de o re introducere a imagini ne modificate
    #ca sa arate cat mai bine
    def change_size(self , newsize , BIMG , UIMG) :
        self.size = newsize 
        self.Bottom_image = pygame.transform.scale(BIMG,(9 * self.size / 8, 7 * self.size / 8))
        self.Upper_image = pygame.transform.scale(UIMG,(self.size,self.size))

    def refresh_weapons (self) :
        self.MainWeapon = copy.copy(Main_Weapons[self.MW])
        self.MainWeapon.noharm = self.number
        self.SecondaryWeapon = copy.copy(Secondary_Weapons[self.SW])
        self.SecondaryWeapon.noharm = self.number

    def Next_MWeapon (self) :
        self.MW = self.MW + 1
        if self.MW == MWcount :
            self.MW = 0 
        self.MainWeapon = copy.copy(Main_Weapons[self.MW])
        self.MainWeapon.noharm = self.number

    def Next_SWeapon (self) :
        self.SW = self.SW + 1
        if self.SW == SWcount :
            self.SW = 0 
        self.SecondaryWeapon = copy.copy(Secondary_Weapons[self.SW])
        self.SecondaryWeapon.noharm = self.number

    #Functie de resetat controalele pleyerului
    def reset_control(self) :
        self.Control = control(self.Source)
    #Se verifica ce schimbari cauzeaza pentru player eventul
    def update_input(self , event) :
        if self.Source != "Keyboard" :
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
                            self.Control.orientation[int(self.Control.input["axes"][event.axis][1] / 2)][self.Control.input["axes"][event.axis][1] % 2] = event.value
                        else :
                            self.Control.action[self.Control.input["axes"][event.axis][1]] = event.value
                except :
                    self.Control.input["axes"][event.axis] = [None , None]
        else :
            #Pentru Tastatura si mouse
            if event.type == pygame.KEYDOWN :
                try :
                    if self.Control.input[event.key] != None :
                        self.Control.action[self.Control.input[event.key]] = 1
                except :
                    self.Control.input[event.key] = None
            elif event.type == pygame.KEYUP :
                try :
                    if self.Control.input[event.key] != None :
                        self.Control.action[self.Control.input[event.key]] = 0
                except :
                    self.Control.input[event.key] = None
            elif event.type == pygame.MOUSEBUTTONDOWN :
                self.Control.MouseButtons[event.button - 1] = True
            elif event.type == pygame.MOUSEBUTTONUP :
                self.Control.MouseButtons[event.button - 1] = False
    #Functie folosita doar in lobby
    def exit_update(self) :
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
    def gameplay_update(self) :
        #Gameplay update pentru atunci cand este controlat de un controller
        if self.Source != "Keyboard" :
            #Obtinerea unghiurilor pentru imagini
            #bottom image
            if  abs(self.Control.orientation[0][0]) > 0.1 or abs(self.Control.orientation[0][1]) > 0.1 :
                self.Bottom_angle = get_angle(self.Control.orientation[0])
                #movement
                if self.Control.action[0] == False and self.Control.action[1] == False :
                    coord = get_pos(self.Bottom_angle,self.maxspeed)
                else :
                    coord = get_pos(self.Bottom_angle,self.maxspeed*2/3)
                self.GX = self.GX + coord[0]
                self.GY = self.GY + coord[1]
            #upper image
            if abs(self.Control.orientation[1][0]) > 0.1 or abs(self.Control.orientation[1][1]) > 0.1 :
                self.Upper_angle = get_angle(self.Control.orientation[1])
            #verificarea attackurilor
            self.MainWeapon.check_fire(self.Upper_angle,self.Control.action[0],self.GX,self.GY)
            if self.Control.action[0] == False :
                self.SecondaryWeapon.check_fire(self.Upper_angle,self.Control.action[1],self.GX,self.GY)
            else :
                self.SecondaryWeapon.check_fire(self.Upper_angle,False,self.GX,self.GY)
        else :
            #Daca este controlat de tastatura
            #bottom angle
            axay = -self.Control.action[0] + self.Control.action[2]
            axax = -self.Control.action[1] + self.Control.action[3]
            if axax !=0  or axay != 0 :
                self.Bottom_angle = get_angle([axax,axay])
                if self.Control.MouseButtons[0] == False and self.Control.MouseButtons[2] == False :
                    coord = get_pos(self.Bottom_angle,self.maxspeed)
                else :
                    coord = get_pos(self.Bottom_angle,self.maxspeed*2/3)
                self.GX = self.GX + coord[0]
                self.GY = self.GY + coord[1]
            #Upper angle 
            if self.Control.Mouse[0] != 0 or self.Control.Mouse[1] != 0 :
                self.Upper_angle = get_angle(self.Control.Mouse)
            #
            self.MainWeapon.check_fire(self.Upper_angle,self.Control.MouseButtons[0],self.GX,self.GY)
            if self.Control.MouseButtons[0] == False :
                self.SecondaryWeapon.check_fire(self.Upper_angle,self.Control.MouseButtons[2],self.GX,self.GY)
            else :
                self.SecondaryWeapon.check_fire(self.Upper_angle,False,self.GX,self.GY)
    #Afisarea playerului pe ecran la coordonatele lui 
    def afisare (self,WIN) :
        BIMAGE = pygame.transform.rotate(self.Bottom_image,self.Bottom_angle)
        x = self.GX - BIMAGE.get_width() / 2
        y = self.GY - BIMAGE.get_height() / 2
        WIN.blit(BIMAGE,(x,y))
        del BIMAGE
        UIMAGE = pygame.transform.rotate(self.Upper_image,self.Upper_angle)
        x = self.GX - UIMAGE.get_width() / 2
        y = self.GY - UIMAGE.get_height() / 2
        WIN.blit(UIMAGE,(x,y))
        del UIMAGE