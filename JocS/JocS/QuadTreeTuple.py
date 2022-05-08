import pygame
import random
import time

_MaxCapacity = 8
_MaxDepth = 8

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

def show_tree(screen, qtree, boundbox, level = 0):
        middle_x = boundbox[0]
        middle_y = boundbox[1]
        width = boundbox[2]
        height = boundbox[3]

        pygame.draw.rect(screen, (0,255,255), pygame.Rect(middle_x - width // 2, middle_y - height // 2, width, height), 1)
        if len(qtree) != 0 and type(qtree[0]) is list:
            show_tree(screen, qtree[0], (middle_x - width // 4, middle_y - height // 4,  width // 2, height // 2), level + 1)
            show_tree(screen, qtree[1], (middle_x + width // 4, middle_y - height // 4,  width // 2, height // 2), level + 1)
            show_tree(screen, qtree[2], (middle_x - width // 4, middle_y + height // 4,  width // 2, height // 2), level + 1)
            show_tree(screen, qtree[3], (middle_x + width // 4, middle_y + height // 4,  width // 2, height // 2), level + 1)
        elif len(qtree) != 0:
            for i in qtree:
                pygame.draw.circle(screen, (255,0,0), (i[0], i[1]), 5)
 