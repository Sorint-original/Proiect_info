import pygame
import random
import time

import Map_select

_MaxCapacity = 10
_MaxDepth = 8

quadtree = []

screen = pygame.display.Info()
WIDTH = screen.current_w
HEIGHT = screen.current_h

L = Map_select.latura
h = HEIGHT - 110
while (round(h * 1.75) > WIDTH - 50) :
    h = h - 1
w = round(h * 1.75)
x = (WIDTH - w) // 2
y = (HEIGHT - h) // 2
if y < 100 :
    y = 10

def make(points, boundbox, level=0):
    if not len(points):
        return []

    NW = []
    NE = []
    SW = []
    SE = []

    middle_x = boundbox[0]
    middle_y = boundbox[1]
    width = boundbox[2]
    height = boundbox[3]
    
    # split
    if len(points) > _MaxCapacity and level < _MaxDepth:
        for point in points:
            if point[0] <= middle_x:
                if point[1] <= middle_y:
                    NW.append(point)
                else:
                    SW.append(point)
            else:
                if point[1] <= middle_y:
                    NE.append(point)
                else:
                    SE.append(point)
        
        return [make(NW, (middle_x - width // 4, middle_y - height // 4,  width // 2, height // 2), level + 1),
                make(NE, (middle_x + width // 4, middle_y - height // 4,  width // 2, height // 2), level + 1),
                make(SW, (middle_x - width // 4, middle_y + height // 4,  width // 2, height // 2), level + 1),
                make(SE, (middle_x + width // 4, middle_y + height // 4,  width // 2, height // 2), level + 1)]
    else:
        return points


def show_tree(screen, qtree, boundbox, queries=[], qpoints=[], level=0):
        middle_x = boundbox[0]
        middle_y = boundbox[1]
        width = boundbox[2]
        height = boundbox[3]

        pygame.draw.rect(screen, (0,255,255), pygame.Rect(middle_x - width // 2, middle_y - height // 2, width, height), 1)
        if len(qtree) != 0 and type(qtree[0]) is list:
            show_tree(screen, qtree[0], (middle_x - width // 4, middle_y - height // 4,  width // 2, height // 2), queries, qpoints, level + 1)
            show_tree(screen, qtree[1], (middle_x + width // 4, middle_y - height // 4,  width // 2, height // 2), queries, qpoints, level + 1)
            show_tree(screen, qtree[2], (middle_x - width // 4, middle_y + height // 4,  width // 2, height // 2), queries, qpoints, level + 1)
            show_tree(screen, qtree[3], (middle_x + width // 4, middle_y + height // 4,  width // 2, height // 2), queries, qpoints, level + 1)
        elif len(qtree) != 0:
            for i in qtree:
                pygame.draw.circle(screen, (255,0,0), (i[0] * (w / (L * 28)) + x, i[1] * (h / (L * 16)) + y), 5)
        if level == 0:
            for i in queries:
                if len(i) == 4:
                    pygame.draw.circle(screen, (178,102,255), (i[0] * (w / (L * 28)) + x, i[1] * (h / (L * 16)) + y), i[2], 3)
                else:
                    pygame.draw.rect(screen, (178,102,255), pygame.Rect((i[0] - i[2] // 2) * (w / (L * 28)) + x , (i[1] - i[3] // 2) * (h / (L * 16)) + y, i[2] * (w / (L * 28)), i[3] * (h / (L * 16))), 2)
            for i in qpoints:
                pygame.draw.circle(screen, (0,255,0), (i[0] * (w / (L * 28)) + x, i[1] * (h / (L * 16)) + y), 6)
 
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

def query(shape, found=[]):
    #print(len(quadtree))
    isCircle = False
    if len(shape) == 4:
        isCircle = True
    for tree in quadtree:
        if isCircle == True:
            if intersects(shape, tree[1]):
                for point in tree[0]:
                    if contains(shape, point):
                        found.append(point)
        else:
            if intersects_rectangle(shape, tree[1]):
                for point in tree[0]:
                    if contains_rectangle(shape, point):
                        found.append(point)

def divide(qtree, bounds):
    quadtree.clear()
    queue = [(qtree, bounds)]
    while len(queue) != 0:
        if len(queue[0][0]) != 0 and type(queue[0][0][0]) is list:
            queue.append((queue[0][0][0], (queue[0][1][0] - queue[0][1][2] // 4, queue[0][1][1] - queue[0][1][3] // 4,  queue[0][1][2] // 2, queue[0][1][3] // 2)))
            queue.append((queue[0][0][1], (queue[0][1][0] + queue[0][1][2] // 4, queue[0][1][1] - queue[0][1][3] // 4,  queue[0][1][2] // 2, queue[0][1][3] // 2)))
            queue.append((queue[0][0][2], (queue[0][1][0] - queue[0][1][2] // 4, queue[0][1][1] + queue[0][1][3] // 4,  queue[0][1][2] // 2, queue[0][1][3] // 2)))
            queue.append((queue[0][0][3], (queue[0][1][0] + queue[0][1][2] // 4, queue[0][1][1] + queue[0][1][3] // 4,  queue[0][1][2] // 2, queue[0][1][3] // 2)))
        else:
            quadtree.append((queue[0][0], queue[0][1]))
        queue.pop(0)