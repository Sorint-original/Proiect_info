import pygame
import random

pygame.init()
screen = pygame.display.Info()
w = screen.current_w
h = screen.current_h
del screen

class TreeObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.userData = userData

class Rectangle:
    def __init__(self, x, y, w, h):
        #Center and dimensions
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, treeObj):
        return(
            treeObj.x >= self.x - self.w // 2 and 
            treeObj.x <= self.x + self.w // 2 and
            treeObj.y >= self.y - self.h // 2 and
            treeObj.y <= self.y + self.h // 2
            )

class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def contains(self, treeObj):
        return (((treeObj.x - self.x) * (treeObj.x - self.x)) + ((treeObj.y - self.y) * (treeObj.y - self.y))) <= (self.r * self.r)

    def intersects(self, range):
        xDist = abs(range.x - self.x)
        yDist = abs(range.y - self.y)

        edges = (xDist - range.w // 2) * (xDist - range.w // 2) + (yDist - range.h // 2) * (yDist - range.h // 2)

        #no intersection
        if xDist > (self.r + range.w // 2) or yDist > (self.r + range.h // 2):
            return False

        #intersection withing circle
        if xDist <= range.w // 2 or yDist <= range.h // 2:
            return True

        #intersection on the edge of the circle
        return edges <= self.r * self.r

class QuadTree:
    _MaxCapacity = 8
    _MaxDepth = 8

    def __init__(self, boundary, capacity=_MaxCapacity, depth = 0):
        self.boundary = boundary
        self.capacity = capacity
        self.objects = []
        self.divided = False
        self.depth = depth

    def subdivide(self):
        rect = self.boundary
        NW = Rectangle(rect.x - rect.w // 4, rect.y - rect.h // 4, rect.w // 2, rect.h // 2)
        self.northwest = QuadTree(NW)
        NE = Rectangle(rect.x + rect.w // 4, rect.y - rect.h// 4, rect.w // 2, rect.h // 2)
        self.northeast = QuadTree(NE)
        SW = Rectangle(rect.x - rect.w// 4, rect.y + rect.h// 4, rect.w // 2, rect.h // 2)
        self.southwest = QuadTree(SW)
        SE = Rectangle(rect.x + rect.w// 4, rect.y + rect.h// 4, rect.w // 2, rect.h // 2)
        self.southeast = QuadTree(SE)

        for obj in self.objects:
            self.northwest.insert(obj)
            self.northeast.insert(obj)
            self.southwest.insert(obj)
            self.southeast.insert(obj)

    def insert(self, treeObj):
        if not self.boundary.contains(treeObj):
            return

        if len(self.objects) < self.capacity and not self.divided:
            self.objects.append(treeObj)
        else:
            if not self.divided:
                self.subdivide()
                self.divided = True
            self.northwest.insert(treeObj)
            self.northeast.insert(treeObj)
            self.southwest.insert(treeObj)
            self.southeast.insert(treeObj)

    def query(self, range, found):
        if not found:
            found = []
        if not range.intersects(self.boundary):
            return found
        else:
            for p in self.objects:
                if range.contains(p):
                    found.append(p)

            if self.divided:
                self.northwest.query(range, found)
                self.northeast.query(range, found)
                self.southwest.query(range, found)
                self.southeast.query(range, found)

            return found

    def show_tree(self, screen):
        #pygame.draw.circle(screen, (255,0,255), (800, 500), 100, 3)
        for i in self.objects:
            pygame.draw.circle(screen, (255,0,0), (i.x, i.y), 5)
        #for i in self.query(Circle(800, 500, 100), []):
        #    pygame.draw.circle(screen, (0,255,0), (i.x, i.y), 5)

        #pygame.draw.rect(screen, (0,255,255), pygame.Rect(self.boundary.x - self.boundary.w // 2, self.boundary.y - self.boundary.h // 2, self.boundary.w, self.boundary.h), 3)
        if self.divided:
            self.northwest.show_tree(screen)
            self.northeast.show_tree(screen)
            self.southwest.show_tree(screen)
            self.southeast.show_tree(screen)