import pygame
from EventH import exit , controller_verify
# dau inport la clasa de butoane deoarece sar putea sa avem un Pause Menu si cred ca nu o sal putem face separat de gameplay
import ButtonClass

#input reprezinta un dictionar care indica care input(keyboard , controller) se duce la fiecare player
def gameplay (WIN,WIDTH,HEIGHT,FPS,Input,Playeri) :
    print("yeet")
    def draw_window () :
        WIN.fill((0,0,0))
