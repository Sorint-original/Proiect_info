import pygame
import random

pygame.init()
screen = pygame.display.Info()
w = screen.current_w
h = screen.current_h
del screen

class TreeObject:
    def __init__(self, x, y, isWall):
        self.x = x
        self.y = y
        self.isWall = isWall
        #self.userData = userData
class Rectangle:
    def __init__(self, x, y, w, h):
        #Center and dimensions
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, treeObj):
        return(treeObj.x >= self.x - self.w // 2 and treeObj.x <= self.x + self.w // 2 and treeObj.y >= self.y - self.h // 2 and treeObj.y <= self.y + self.h // 2)

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

    def __init__(self, boundary, capacity=_MaxCapacity, depth=0):
        self.boundary = boundary
        self.capacity = capacity
        self.objects = []
        self.divided = False
        self.depth = depth

    def subdivide(self):
        rect = self.boundary
        NW = Rectangle(rect.x - rect.w // 4, rect.y - rect.h // 4, rect.w // 2, rect.h // 2)
        self.northwest = QuadTree(NW)
        NE = Rectangle(rect.x + rect.w // 4, rect.y - rect.h // 4, rect.w // 2, rect.h // 2)
        self.northeast = QuadTree(NE)
        SW = Rectangle(rect.x - rect.w // 4, rect.y + rect.h // 4, rect.w // 2, rect.h // 2)
        self.southwest = QuadTree(SW)
        SE = Rectangle(rect.x + rect.w // 4, rect.y + rect.h // 4, rect.w // 2, rect.h // 2)
        self.southeast = QuadTree(SE)

        for obj in self.objects:
            self.northwest.insert(obj)
            self.northeast.insert(obj)
            self.southwest.insert(obj)
            self.southeast.insert(obj)
        self.objects.clear()

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

    def query(self, range, found = []):
        if not range.intersects(self.boundary):
            return
        else:
            for p in self.objects:
                if range.contains(p):
                    found.append(p)

            if self.divided:
                self.northwest.query(range, found)
                self.northeast.query(range, found)
                self.southwest.query(range, found)
                self.southeast.query(range, found)

            #return found

    def check_for_subtrees(self):
        if self.divided:
            if len(self.northwest.objects) + len(self.northeast.objects) + len(self.southwest.objects) + len(self.southeast.objects) <= self._MaxCapacity and (not self.northwest.divided and not self.northeast.divided and not self.southwest.divided and not self.southeast.divided):
                for i in self.northwest.objects:
                    self.objects.append(i)
                for i in self.northeast.objects:
                    self.objects.append(i)
                for i in self.southwest.objects:
                    self.objects.append(i)
                for i in self.southeast.objects:
                    self.objects.append(i)

                del self.northwest
                del self.northeast
                del self.southwest
                del self.southeast
                self.divided = False

    def clear(self):
        if self.divided:
            self.northwest.clear()
            self.northeast.clear()
            self.southwest.clear()
            self.southeast.clear()
            self.check_for_subtrees()
        else:
            for i in self.objects:
                if i.isWall == False:
                    self.objects.remove(i)
                    del i

    def show_tree(self, screen, points=[], queries=[]):
        for i in self.objects:
            pygame.draw.circle(screen, (255,0,0), (i.x, i.y), 5)
        for i in queries:
            pygame.draw.circle(screen, (76,0,153), (i.x, i.y), i.r, 3)
        for i in points:
            pygame.draw.circle(screen, (0,255,0), (i.x, i.y), 8)
        pygame.draw.rect(screen, (0,255,255), pygame.Rect(self.boundary.x - self.boundary.w // 2, self.boundary.y - self.boundary.h // 2, self.boundary.w, self.boundary.h), 1)
        if self.divided:
            self.northwest.show_tree(screen)
            self.northeast.show_tree(screen)
            self.southwest.show_tree(screen)
            self.southeast.show_tree(screen)