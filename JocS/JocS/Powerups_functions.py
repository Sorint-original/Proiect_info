import pygame
import os

Botimg = ['Bottom-Blue.png','Bottom-Green.png','Bottom-Yellow.png','Bottom-Red.png']
Upimg = ['Upper-Blue.png','Upper-Green.png','Upper-Yellow.png','Upper-Red.png']

def first_ammo_refill (player) :
    player.SecondaryWeapon.Ammo_count += player.SecondaryWeapon.Ammo_refill

def life_heal (player) :
    player.Health += 100
    if player.Health > 1000 :
        player.Health = 1000

def bounce_start (player) :
    player.MainWeapon.bounce = 8

def bounce_end (player) :
    player.MainWeapon.bounce = 0

def imunity_start (player) :
    player.INVINCIBILITY = True

def imunity_end (player) :
    player.INVINCIBILITY = False

def speed_start (player) :
    player.maxspeed += 2

def speed_end (player) :
    player.maxspeed -= 2

def shrink_start (player) :
    player.change_size(player.size/2,pygame.Surface.convert_alpha(pygame.image.load(os.path.join('Assets\Robots', Botimg[player.number]))),pygame.Surface.convert_alpha(pygame.image.load(os.path.join('Assets\Robots', Upimg[player.number]))))
    player.diametru = player.diametru /2

def shrink_end (player) :
    player.change_size(player.size*2,pygame.Surface.convert_alpha(pygame.image.load(os.path.join('Assets\Robots', Botimg[player.number]))),pygame.Surface.convert_alpha(pygame.image.load(os.path.join('Assets\Robots', Upimg[player.number]))))
    player.diametru = player.diametru*2

def ghost_start (player) :
    player.MainWeapon.Ghost = True

def ghost_end(player) :
    player.MainWeapon.Ghost = False