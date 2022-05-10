import pygame
import random
import time

_MaxCapacity = 8
_MaxDepth = 8

quadtree = []

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

def show_tree(screen, qtree, boundbox, queries = [], qpoints = [], level = 0):
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
                pygame.draw.circle(screen, (255,0,0), (i[0], i[1]), 5)
        if level == 0:
            for i in queries:
                pygame.draw.circle(screen, (153,51,255), (i[0], i[1]), i[2], 3)
            for i in qpoints:
                pygame.draw.circle(screen, (0,255,0), (i[0], i[1]), 8)
 
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

def contains(circle, point):
    xDist = point[0] - circle[0]
    yDist = point[1] - circle[1]
    return circle[2] ** 2 >= xDist ** 2 + yDist ** 2

def query(qtree, bounds, circle, found = []):
    middle_x = bounds[0]
    middle_y = bounds[1]
    width = bounds[2]
    height = bounds[3]
    if not intersects(circle, bounds):
        return found
    if len(qtree) != 0 and type(qtree[0]) is list:
        query(qtree[0], (middle_x - width // 4, middle_y - height // 4,  width // 2, height // 2), circle, found)
        query(qtree[1], (middle_x + width // 4, middle_y - height // 4,  width // 2, height // 2), circle, found)
        query(qtree[2], (middle_x - width // 4, middle_y + height // 4,  width // 2, height // 2), circle, found)
        query(qtree[3], (middle_x + width // 4, middle_y + height // 4,  width // 2, height // 2), circle, found)
    else:
        for point in qtree:
            if circle[2] ** 2 >= (point[0] - circle[0]) ** 2 + (point[1] - circle[1]) ** 2:
                found.append(point)
    return found

def theQuery(circle, found = []):
    print(len(quadtree))
    for tree in quadtree:
        if intersects(circle, tree[1]):
            for point in tree[0]:
                if contains(circle, point):
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



