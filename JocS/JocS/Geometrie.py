import numpy as np
import math
import time

# Aici bagam toate functiile pe care le folosim mai des si au legatura cu geometria


def get_angle (v1) :
    # vectorul primit e de forma [x , y]
    v2 = [1,0]
    uv2 = v2 / np.linalg.norm(v2)
    uv1 = v1 / np.linalg.norm(v1)
    dot_product = np.dot(uv1,uv2)
    angle = np.arccos(dot_product)
    #returneaza unghiul in grade
    if v1[1] > 0 :
        angle = -angle
    return math.degrees(angle)

def get_pos (angle,lenght) :
    #unghiul va apartine multimi [-180 , 180] si lenght este marimea vectorului
    if abs(angle) <= 90 : 
        x = math.cos(math.radians(abs(angle)))*lenght
        y = math.sin(math.radians(abs(angle)))*lenght
        if angle > 0 :
            y = -y
    if abs(angle) > 90 :
        x = math.cos(math.radians(180-abs(angle)))*lenght
        y = math.sin(math.radians(180-abs(angle)))*lenght
        x = -x
        if angle > 0 :
            y = -y
    #se returneaza pozitia in cazul in care originea vectorului e 0 0 
    return ((x,y))
    