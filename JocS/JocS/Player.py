import pygame
import os
import random
import copy
import math

from Geometrie import get_angle , get_pos , get_length , point_pe_dreapta , get_intersection , modify_angle
import Lobby
import Powerups_functions

#Toate proiectilele care se vor afla pe harta
Harmful_Stuff = []

EX_sequences = [pygame.image.load(os.path.join('Assets\Explosion','EX0.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX1.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX2.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX3.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX4.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX5.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX6.png' )),pygame.image.load(os.path.join('Assets\Explosion','EX7.png' ))]
Iproiectile = [pygame.transform.scale(pygame.image.load(os.path.join('Assets\Proiectile','Bullet.png' )),(25,5)),pygame.transform.scale(pygame.image.load(os.path.join('Assets\Proiectile','Grenade.png' )),(15,18)),pygame.transform.scale(pygame.image.load(os.path.join('Assets\Proiectile','Flame.png' )),(39,30)),pygame.transform.scale(pygame.image.load(os.path.join('Assets\Proiectile','Rocket.png' )),(60,20)),pygame.transform.scale(pygame.image.load(os.path.join('Assets\Proiectile','Mine.png' )),(50,50))]
PU_Images = [pygame.image.load(os.path.join('Assets\PowerUps','AMMOBOX.png' )),pygame.image.load(os.path.join('Assets\PowerUps','HEALTH.png' )),pygame.image.load(os.path.join('Assets\PowerUps','BOUNCE.png' )),pygame.image.load(os.path.join('Assets\PowerUps','INVINCIBILITY.png' )),pygame.image.load(os.path.join('Assets\PowerUps','SPEED.png' )),pygame.image.load(os.path.join('Assets\PowerUps','SHRINK.png' )),pygame.image.load(os.path.join('Assets\PowerUps','GHOST.png' )),pygame.image.load(os.path.join('Assets\PowerUps','DOUBLE_GUNS.png' ))]



class power_up  :
    def __init__ (self,GX,GY,nrimg,time,functieinitiala,functiefinala,p) :
        self.GX =GX
        self.GY = GY
        self.nrimg = nrimg
        self.timer = time
        #functia care modifica playeru cand ia power upul
        self.do = functieinitiala
        #functia care intoarce playeru la normal
        self.revert = functiefinala
        self.size = 85
        self.nrpoz = None
        self.nrpower_up = p

AmmoRefill = power_up(0,0,0,-1,Powerups_functions.first_ammo_refill,None,0)
HEAL = power_up(0,0,1,-1,Powerups_functions.life_heal,None,1)
BOUNCE_PU = power_up(0,0,2,120,Powerups_functions.bounce_start,Powerups_functions.bounce_end,2)
INV_PU = power_up(0,0,3,240,Powerups_functions.imunity_start,Powerups_functions.imunity_end,3)
Speed_PU = power_up(0,0,4,240,Powerups_functions.speed_start,Powerups_functions.speed_end,4)
Shrink_PU = power_up(0,0,5,240,Powerups_functions.shrink_start,Powerups_functions.shrink_end,5)
Ghost_PU = power_up(0,0,6,240,Powerups_functions.ghost_start,Powerups_functions.ghost_end,6)
DGUNS_PU = power_up(0,0,7,240,Powerups_functions.DGUNS_start,Powerups_functions.DGUNS_end,7)
PU=[AmmoRefill,HEAL,BOUNCE_PU,INV_PU,Speed_PU,Shrink_PU,Ghost_PU,DGUNS_PU]
Active_PU = [0,0,0,0,0,0,0,0]
avalible_powerups = [0]

def convert_and_resize_assets (WIN,w,h,L) :
    global EX_sequences
    global Iproiectile
    for i in range(len(Iproiectile)) :
        Iproiectile[i] = pygame.transform.scale(pygame.Surface.convert_alpha(Iproiectile[i]),(Iproiectile[i].get_width()*(w/(L*28)),Iproiectile[i].get_height()*(h/(L*16))))
        Iproiectile[i] = Iproiectile[i].convert_alpha()
    for i in range(len(EX_sequences)) :
        if i == 0 :
            s = 100
        elif i == 1 :
            s = 200
        else :
            s = 200
        EX_sequences[i] = pygame.transform.scale(pygame.Surface.convert_alpha(EX_sequences[i]),(s*(w/(L*28)),s*(h/(L*16))))
    for i in range(len(PU_Images)) :
        PU_Images[i] = pygame.Surface.convert_alpha(pygame.transform.scale(PU_Images[i],(L*1.5*(w/(L*28)),L*1.5*(h/(L*16)))))


class explosion :
    def __init__ (self,x,y,size,dmg) :
        self.diametru = 200
        self.GX = x
        self.GY = y
        self.PGX = x
        self.PGY = y
        self.existance = 55
        self.nrimg = 0
        self.size = size
        self.damage = dmg
        self.type = 1
        #Fiecare player poate sa ia damage doar o data de la o anumita explozie
        self.noharm = []

    def update (self) :
        self.existance = self.existance - 1
        self.nrimg = 8-(self.existance // 7 + 1)
        if self.existance == 0 :
            Harmful_Stuff.remove(self)

    #aceasta functie va fi chemata cand un anumit glont intra in contact cu alt obiect
    #other va tine un fel de id explicand ce si unde se afla obiectul lovit
    def impact (self,other) :
        if other[0] == "PLR" and Lobby.Playeri[other[1]].INVINCIBILITY == False :
            nh = True
            for i in range(len(self.noharm)) :
                if self.noharm[i] == other[1] :
                    nh = False
                    break
            if nh :
                Lobby.Playeri[other[1]].Health = Lobby.Playeri[other[1]].Health - self.damage
                self.noharm.append(other[1])


class proiectil :
    def __init__ (self,x,y,size,nrimage,angle,speed,Dmg,A,mins,ext,Hurts_player,DOD,EXPLOD,Bounce,Fade,Ghost,nh) :
        self.GX = x
        self.GY = y
        #pgx si pgy sunt coordonatele pe care le avea inainte Playeru
        self.PGX = x
        self.PGY = y
        #self.size reprezinta diametru cercului de coliziunea a glontului
        self.diametru = size    #Please keep constant with variable name language, thank you
        self.Angle = angle
        self.IMG = pygame.transform.rotate(Iproiectile[nrimage] , angle)
        self.Speed = speed
        self.noharm = nh
        self.dmg = Dmg
        self.acceleration = A
        self.minspeed = mins
        self.existence = ext
        #proprietati meta
        self.hurt = Hurts_player
        self.destroy_on_damage = DOD
        self.Will_Explode = EXPLOD
        self.Bouncy = Bounce
        self.type = 0
        self.Ghost = Ghost
        #fade and invisibility
        self.Fade = Fade
        if Fade :
            self.alpha = 255
            self.V = True
    def update (self) :
        #Verifica daca mai exista atacu
        if self.existence > 0 :
            self.existence = self.existence - 1
        if self.existence == 0 :
            if self.Will_Explode :
                Harmful_Stuff.append(explosion(self.GX,self.GY,200,self.dmg))
            Harmful_Stuff.remove(self)
            del self
        else :
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
            # modificarea vizibilitatii
            if self.Fade :
                if self.V  :
                    self.alpha = self.alpha - 1
                    if self.alpha == 0 :
                        self.V =False
                else :
                    if self.existence % 300 <= 20:
                        self.alpha = 75
                    else :
                        self.alpha = 0
                self.IMG.set_alpha(self.alpha)
                    


    #aceasta functie va fi chemata cand un anumit glont intra in contact cu alt obiect
    #other va tine un fel de id explicand ce si unde se afla obiectul lovit
    def impact (self,other) :
        if other[0] == "PLR" :
            if self.hurt and self.noharm != other[1] and Lobby.Playeri[other[1]].INVINCIBILITY == False :
                if self.Will_Explode == False :
                    Lobby.Playeri[other[1]].Health = Lobby.Playeri[other[1]].Health - self.dmg
                    if self.destroy_on_damage :
                        Harmful_Stuff.remove(self)
                else :
                    Harmful_Stuff.append(explosion(self.GX,self.GY,200,self.dmg))
                    Harmful_Stuff.remove(self)
        elif other[0] == "Wall" :
            if self.Bouncy == 0 and self.Ghost == False :
                if self.Will_Explode :
                    Harmful_Stuff.append(explosion(self.GX,self.GY,200,self.dmg))
                Harmful_Stuff.remove(self)
            elif self.Bouncy != 0 :
                if self.Bouncy > 0 :
                    self.Bouncy -= 1
                    self.noharm = None
                box = other[1]
                box[0] = box[0]-box[2]//2
                box[1] = box[1]-box[3]//2
                unghi = self.Angle
                if unghi < 0 :
                    unghi = 360 + unghi
                #panta 
                m = math.tan(math.radians(unghi))
                if unghi == 180 :
                    m = 0
                #print(box[0],box[1],box[2],box[3],self.Angle,m,self.PGX,self.PGY)
                firsthit = [None,None]
                #stabilirea a ce loveste prima data
                if self.PGY <= box[1]+ box[3] :
                    Lungime = None
                    y=box[1]
                    x =point_pe_dreapta(self.PGY,self.PGX,m,y,None)
                    if self.PGY <= y and(x>=box[0]-self.diametru/2 and x<=box[0]+box[2]+self.diametru/2) and ((self.PGX - self.GX >=0 and x <= self.PGX)or(self.PGX - self.GX <0 and x >= self.PGX)) and ((self.PGY - self.GY >=0 and y <= self.PGY)or(self.PGY - self.GY <0 and y >= self.PGY)):
                        Lungime = get_length(x-self.PGX,y-self.PGY)
                    y = box[1]-self.diametru/2
                    x =point_pe_dreapta(self.PGY,self.PGX,m,y,None)
                    if self.PGY <= y and(x>=box[0] and x<=box[0]+box[2]) and  (Lungime==None or get_length(x-self.PGX,y-self.PGY)<Lungime)and ((self.PGX - self.GX >=0 and x <= self.PGX)or(self.PGX - self.GX <0 and x >= self.PGX)) and ((self.PGY - self.GY >=0 and y <= self.PGY)or(self.PGY - self.GY <0 and y >= self.PGY)) :
                        Lungime = get_length(x-self.PGX,y-self.PGY)
                    if Lungime!=None and (firsthit[0]==None or firsthit[0]>Lungime) :
                        firsthit[0] = Lungime
                        firsthit[1] = "SUS"
                else :
                    Lungime = None
                    y=box[1]+box[3]
                    x =point_pe_dreapta(self.PGY,self.PGX,m,y,None)
                    if self.PGY>=y and (x>=box[0]-self.diametru/2 and x<=box[0]+box[2]+self.diametru/2)and ((self.PGX - self.GX >=0 and x <= self.PGX)or(self.PGX - self.GX <0 and x >= self.PGX)) and ((self.PGY - self.GY >=0 and y <= self.PGY)or(self.PGY - self.GY <0 and y >= self.PGY)) :
                        Lungime = get_length(x-self.PGX,y-self.PGY)
                    y = box[1]+box[3]+self.diametru/2
                    x =point_pe_dreapta(self.PGY,self.PGX,m,y,None)
                    if self.PGY>=y and(x>=box[0] and x<=box[0]+box[2]) and  (Lungime==None or get_length(x-self.PGX,y-self.PGY)<Lungime)and ((self.PGX - self.GX >=0 and x <= self.PGX)or(self.PGX - self.GX <0 and x >= self.PGX)) and ((self.PGY - self.GY >=0 and y <= self.PGY)or(self.PGY - self.GY <0 and y >= self.PGY)) :
                        Lungime = get_length(x-self.PGX,y-self.PGY)
                    if Lungime!=None and (firsthit[0]==None or firsthit[0]>Lungime) :
                        firsthit[0] = Lungime
                        firsthit[1] = "JOS"

                if self.PGX <= box[0]+ box[2] :
                    Lungime = None
                    x = box[0]
                    y =point_pe_dreapta(self.PGY,self.PGX,m,None,x)
                    if self.PGX<=x and (y>=box[1]-self.diametru/2 and y<=box[1]+box[3]+self.diametru/2)and ((self.PGX - self.GX >=0 and x <= self.PGX)or(self.PGX - self.GX <0 and x >= self.PGX)) and ((self.PGY - self.GY >=0 and y <= self.PGY)or(self.PGY - self.GY <0 and y >= self.PGY)) :
                        Lungime = get_length(x-self.PGX,y-self.PGY)
                    x = box[0] - self.diametru/2
                    y =point_pe_dreapta(self.PGY,self.PGX,m,None,x)
                    if self.PGX<=x and(y>=box[1] and y<=box[1]+box[3]) and (Lungime==None or get_length(x-self.PGX,y-self.PGY)<Lungime)and ((self.PGX - self.GX >=0 and x <= self.PGX)or(self.PGX - self.GX <0 and x >= self.PGX)) and ((self.PGY - self.GY >=0 and y <= self.PGY)or(self.PGY - self.GY <0 and y >= self.PGY)) :
                        Lungime = get_length(x-self.PGX,y-self.PGY)
                    if Lungime!=None and (firsthit[0]==None or firsthit[0]>Lungime) :
                        firsthit[0] = Lungime
                        firsthit[1] = "STANGA"
                else :
                    Lungime = None
                    x = box[0]+box[2]
                    y =point_pe_dreapta(self.PGY,self.PGX,m,None,x)
                    if self.PGX>=x and(y>=box[1]-self.diametru/2 and y<=box[1]+box[3]+self.diametru/2)and ((self.PGX - self.GX >=0 and x <= self.PGX)or(self.PGX - self.GX <0 and x >= self.PGX)) and ((self.PGY - self.GY >=0 and y <= self.PGY)or(self.PGY - self.GY <0 and y >= self.PGY)) :
                        Lungime = get_length(x-self.PGX,y-self.PGY)
                    x = box[0]+box[2]+self.diametru/2
                    y =point_pe_dreapta(self.PGY,self.PGX,m,None,x)
                    if self.PGX>=x and(y>=box[1] and y<=box[1]+box[3]) and (Lungime==None or get_length(x-self.PGX,y-self.PGY)<Lungime)and ((self.PGX - self.GX >=0 and x <= self.PGX)or(self.PGX - self.GX <0 and x >= self.PGX)) and ((self.PGY - self.GY >=0 and y <= self.PGY)or(self.PGY - self.GY <0 and y >= self.PGY)) :
                        Lungime = get_length(x-self.PGX,y-self.PGY)
                    if Lungime!=None and (firsthit[0]==None or firsthit[0]>Lungime) :
                        firsthit[0] = Lungime
                        firsthit[1] = "DREAPTA"
                #pozitia la care se afla in momentul exact al loviri
                if firsthit[1] == "SUS" or firsthit[1] == "JOS" :
                    self.IMG = pygame.transform.flip(self.IMG,False,True)
                    self.Angle = - self.Angle
                    if firsthit[1] == "SUS" :
                        y = box[1] - self.diametru/2
                    else :
                        y = box[1]+box[3] + self.diametru/2
                    x =  point_pe_dreapta(self.PGY,self.PGX,m,y,None)
                elif firsthit[1] != None :
                    self.IMG = pygame.transform.flip(self.IMG,True,False)
                    if firsthit[1] == "STANGA" :
                        self.Angle = math.copysign(180,self.Angle) - self.Angle
                        x = box[0] - self.diametru/2
                    else :
                        self.Angle = math.copysign(180,self.Angle) - self.Angle
                        x = box[0]+box[2] + self.diametru/2
                    y = point_pe_dreapta(self.PGY,self.PGX,m,None,x)
                if firsthit[1] != None :
                    #print(firsthit[1])
                    #print(self.GX,self.GY)
                    self.GX = x
                    self.GY = y
                    #print(self.GX,self.GY)


class weapon :
    def __init__ (self,size,count,refill,speed,spread,coold,shots_per_fire,H,damage,A,mins,bext,auto,hurt_player,destroy_on_dmg,EXP,B,Fade,ammo) :
        #marimea diametrului unui glont
        self.size = size
        #if count is -1 it means that it is unlimited
        self.Ammo_count = count
        self.Ammo_refill = refill
        self.Ammo_speed = speed
        # 0 means perfect acuracy
        self.Spread = spread
        #dupa cate frame-uri poate sa traga din nou
        self.automatic = auto
        self.tras = False
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
        #timer pentru existenta glontului
        self.existence = bext
        #Proprietati meta
        self.hurts = hurt_player
        self.DOD = destroy_on_dmg
        self.explosive = EXP
        self.bounce = B
        self.Ghost = False
        self.DGun = False
        #Fade
        self.Fade = Fade

    #functia care verifica daca poata sa traga , action e true sau fals si
    #determina daca playeru da comanda
    # x si y vor fi GX SI GY de la player
    def check_fire(self , angle , action ,x , y, caster) :
        if self.cooldown > 0 :
            self.cooldown = self.cooldown -1
        if self.heat > 0 :
            self.heat = self.heat - self.cooling
        if self.OVERHEATED == True and self.heat <= 0 :
            self.heat = 0
            self.OVERHEATED = False
        if self.tras == True and action == False :
            self.tras = False
        if ((action and self.automatic == True) or (action and self.automatic == False and self.tras ==False)) and abs(self.Ammo_count) > 0 and self.OVERHEATED == False and self.cooldown == 0 :
            self.tras=True
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
            if self.DGun :
                newcord = get_pos(modify_angle(angle,-90),25)
                x1 = x + newcord[0]
                y1 = y + newcord[1]
                newcord = get_pos(modify_angle(angle,90),25)
                x2 =x + newcord[0]
                y2 =y + newcord[1]
            for i in range (self.spfire) :
                newangle = angle
                if self.Spread > 0 and self.spfire > 1:
                    deviasion = random.choice(A)
                    newangle = newangle + deviasion
                    A.remove(deviasion)
                elif self.Spread > 0 :
                    newangle = newangle + random.randint(-self.Spread,self.Spread)
                if self.DGun == False :
                    new_shot = proiectil(x,y,self.size,self.Ammo,newangle,self.Ammo_speed,self.dmg,self.acceleration,self.minspeed,self.existence,self.hurts,self.DOD,self.explosive,self.bounce,self.Fade,self.Ghost,self.noharm)
                    Harmful_Stuff.append(new_shot)
                else :
                    new_shot = proiectil(x1,y1,self.size,self.Ammo,newangle,self.Ammo_speed,self.dmg,self.acceleration,self.minspeed,self.existence,self.hurts,self.DOD,self.explosive,self.bounce,self.Fade,self.Ghost,self.noharm)
                    Harmful_Stuff.append(new_shot)
                    new_shot = proiectil(x2,y2,self.size,self.Ammo,newangle,self.Ammo_speed,self.dmg,self.acceleration,self.minspeed,self.existence,self.hurts,self.DOD,self.explosive,self.bounce,self.Fade,self.Ghost,self.noharm)
                    Harmful_Stuff.append(new_shot)
            if self.Spread > 0 and self.spfire > 1 :
                del A
            if self.Ammo_count != -1 :
                self.Ammo_count = self.Ammo_count - 1

# Main Weopans care se folosesc in joc 
Rifle = weapon(10,-1,0,25,0,10,1,10,25,0,25,-1,True,True,True,False,0,False,0)
Shotgun = weapon(10,-1,0,25,3,30,5,40,75,0,25,-1,False,True,True,False,0,False,0)
SMG = weapon(10,-1,0,25,5,0,1,1.5,5,0,25,-1,True,True,True,False,0,False,0)
Main_Weapons = [Rifle,Shotgun,SMG]
MWcount = len(Main_Weapons) #no reason to hardcode it, just let it be the length of array

#Secondary weapons care se folosesc in joc
Grenade_Launcher = weapon(15,10,3,30,0,60,1,0,150,-0.5,0,120,False,False,False,True,-1,False,1)
Flame_Thrower = weapon(30,-1,60,25,15,2,1,0,5,-0.7,6,100,True,True,False,False,-1,False,2)
Rocket_Launcher = weapon(20,5,2,25,0,30,1,0,150,0,25,-1,False,True,True,True,0,False,3)
Mines = weapon(50,10,3,0,0,60,1,0,150,0,0,5400,False,True,True,True,0,True,4)
Secondary_Weapons = [Grenade_Launcher,Flame_Thrower,Rocket_Launcher,Mines]
SWcount = len(Secondary_Weapons)


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
        self.diametru = 150
        self.Powers = []
        self.INVINCIBILITY = False

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
            self.MainWeapon.check_fire(self.Upper_angle,self.Control.action[0],self.GX,self.GY,self.number)
            if self.Control.action[0] == False :
                self.SecondaryWeapon.check_fire(self.Upper_angle,self.Control.action[1],self.GX,self.GY,self.number)
            else :
                self.SecondaryWeapon.check_fire(self.Upper_angle,False,self.GX,self.GY,self.number)
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
            self.MainWeapon.check_fire(self.Upper_angle,self.Control.MouseButtons[0],self.GX,self.GY, self.number)
            if self.Control.MouseButtons[0] == False :
                self.SecondaryWeapon.check_fire(self.Upper_angle,self.Control.MouseButtons[2],self.GX,self.GY, self.number)
            else :
                self.SecondaryWeapon.check_fire(self.Upper_angle,False,self.GX,self.GY, self.number)
        #Modificarea powerup-urilor
        s = 0
        for i in range(0,len(self.Powers),2) :
            i += s 
            self.Powers[i] = self.Powers[i] - 1
            if self.Powers[i] == 0 :
                self.Powers[i+1].revert(self)
                avalible_powerups[0] +=  1
                Active_PU[self.Powers[i+1].nrpower_up] = 0
                self.Powers.pop(i)
                self.Powers.pop(i)
                s -= 2


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