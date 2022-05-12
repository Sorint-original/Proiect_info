import numpy as np
import math
import time

# Aici bagam toate functiile pe care le folosim mai des si au legatura cu
# geometria

def intersects(range, boundbox):
    circlex = range[0]
    circley = range[1]
    circler = range[2]

    middle_x = boundbox[0]
    middle_y = boundbox[1]
    width = boundbox[2]
    height = boundbox[3]

    xDist = abs(middle_x - circlex)
    yDist = abs(middle_y - circley)

    edges = (xDist - width // 2) * (xDist - width // 2) + (yDist - height // 2) * (yDist - height // 2)

    #no intersection
    if xDist > (circler + width // 2) or yDist > (circler + height // 2):
        return False

    #intersection withing circle
    if xDist <= width // 2 or yDist <= height // 2:
        return True

    #intersection on the edge of the circle
    return edges <= circler * circler

def intersects_unused(range, boundbox):
    circlex = range[0]
    circley = range[1]
    circler = range[2]

    middle_x = boundbox[0]
    middle_y = boundbox[1]
    width = boundbox[2]
    height = boundbox[3]

    testX = circlex
    testY = circley

    if circlex < middle_x - width // 2:
        testX = middle_x - width // 2
    elif circlex > middle_x + width // 2:
        testX = middle_x + width // 2

    if circley < middle_y - height // 2:
        testY = middle_y - height // 2
    elif circley < middle_y + height // 2:
        testY = middle_y + height // 2

    xDist = circlex - testX
    yDist = circley - testY

    distance = xDist ** 2 + yDist ** 2

    if distance <= circler ** 2:
        return True

    return False

def intersects_rectangle(range, boundbox):
    boxx = range[0]
    boxy = range[1]
    boxw = range[2]
    boxh = range[3]

    middle_x = boundbox[0]
    middle_y = boundbox[1]
    width = boundbox[2]
    height = boundbox[3]
    return not(middle_x + width // 2 < boxx - boxw // 2 or boxx + boxw // 2 < middle_x - width // 2 or middle_y + height // 2 < boxy - boxh // 2 or boxy + boxh // 2 < middle_y - height // 2)

def intersects_circle(range, circle):
    rangex = range[0]
    rangey = range[1]
    ranger = range[2]

    circlex = circle[0]
    circley = circle[1]
    circler = circle[2]

    xDist = abs(circlex - rangex)
    yDist = abs(circley - rangey)
    maxDist = circler + ranger

    return maxDist ** 2 >= xDist ** 2 + yDist ** 2

def contains(circle, point):
    xDist = point[0] - circle[0]
    yDist = point[1] - circle[1]
    return circle[2] ** 2 >= xDist ** 2 + yDist ** 2

def contains_rectangle(range, point):
    boxx = range[0]
    boxy = range[1]
    boxw = range[2]
    boxh = range[3]

    ptrx = point[0]
    ptry = point[1]
    return(boxx - boxw // 2 <= ptrx and boxx + boxw // 2 >= ptrx and boxy - boxh // 2 <= ptry and boxy + boxh // 2 >= ptry)

def check_collision(shape, compare):
    isCircle = False
    if len(shape) == 3:
        isCircle = True
    if not isCircle:
        if intersects(compare, shape):
            return True
    else:
        if intersects_circle(shape, compare):
            return True
    return False


def get_angle(v1) :
    # vectorul primit e de forma [x , y]
    v2 = [1,0]
    uv2 = v2 / np.linalg.norm(v2)
    uv1 = v1 / np.linalg.norm(v1)
    dot_product = np.dot(uv1,uv2)
    angle = np.arccos(dot_product)
    #returneaza unghiul in grade
    if v1[1] > 0 :
        angle = -angle
    #UNGHIUL RETURNAT apartine intervalului [-180 , 180 ] practic - 60 = 300 de
    #grade
    return round(math.degrees(angle))

def get_pos(angle,lenght) :
    #unghiul va apartine multimi [-180 , 180] si lenght este marimea vectorului
    if abs(angle) <= 90 : 
        x = math.cos(math.radians(abs(angle))) * lenght
        y = math.sin(math.radians(abs(angle))) * lenght
        if angle > 0 :
            y = -y
    if abs(angle) > 90 :
        x = math.cos(math.radians(180 - abs(angle))) * lenght
        y = math.sin(math.radians(180 - abs(angle))) * lenght
        x = -x
        if angle > 0 :
            y = -y
    #se returneaza pozitia in cazul in care originea vectorului e 0 0
    return ((x,y))

def modify_angle(angle,modifier) :
    angle = angle + modifier
    if abs(angle) > 180 :
        sign = angle / abs(angle)
        newangle = -1 * sign * 180 + (angle - 1 * sign * 180)
    #returneaza de fiecare data un unghiul modificat sub forma care se
    #incadreaza in intervalul [-180,180]
    return newangle
    