import pygame

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
        print(NW.x, NW.y, NW.w, NW.h)
        self.northwest = QuadTree(NW)
        NE = Rectangle(rect.x + rect.w // 4, rect.y - rect.h// 4, rect.w // 2, rect.h // 2)
        print(NE)
        self.northeast = QuadTree(NE)
        SW = Rectangle(rect.x - rect.w// 4, rect.y + rect.h// 4, rect.w // 2, rect.h // 2)
        print(SW)
        self.southwest = QuadTree(SW)
        SE = Rectangle(rect.x + rect.w// 4, rect.y + rect.h// 4, rect.w // 2, rect.h // 2)
        print(SE)
        self.southeast = QuadTree(SE)

    def insert(self, treeObj):
        if not self.boundary.contains(treeObj):
            return

        if len(self.objects) < self.capacity and not self.divided:
            self.objects.append(treeObj)
        else:
            if not self.divided:
                self.subdivide()
                self.divided = True
            else:
                self.northwest.insert(treeObj)
                self.northeast.insert(treeObj)
                self.southwest.insert(treeObj)
                self.southeast.insert(treeObj)

    def show_tree(self, screen):
        for i in self.objects:
            pygame.draw.circle(screen, (0,255,0), (i.x, i.y), 5)
        pygame.draw.rect(screen, (102,0,204), pygame.Rect(self.boundary.x - self.boundary.w // 2, self.boundary.y - self.boundary.h // 2, self.boundary.w, self.boundary.h), 3)
        if self.divided:
            self.northwest.show_tree(screen)
            self.northeast.show_tree(screen)
            self.southwest.show_tree(screen)
            self.southeast.show_tree(screen)