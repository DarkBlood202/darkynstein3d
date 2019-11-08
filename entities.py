import pygame as pg
from settings import *

class Boundary:
    def __init__(self,x1,y1,x2,y2):
        self.a = pg.math.Vector2(x1,y1)
        self.b = pg.math.Vector2(x2,y2)

    def show(self,screen):
        pg.draw.line(screen,WHITE,self.a,self.b)

class MapBlock:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.a = pg.math.Vector2(self.x,self.y)
        self.b = pg.math.Vector2(self.x*TILESIZE,self.y*TILESIZE)

    def show(self,screen):
        pg.draw.circle(screen,WHITE,(self.x,self.y),1)

class Ray:
    def __init__(self,x,y,angle):
        self.pos = pg.math.Vector2(x,y)
        self.dir = pg.math.Vector2(1,0).rotate(angle)

    def look_at(self,x,y):
        self.dir.x = x - self.pos.x
        self.dir.y = y - self.pos.y
        self.dir.normalize()

    def show(self,screen):
        pg.draw.line(screen,WHITE,self.pos,self.pos+(self.dir*10))

    def cast(self,wall):
        x1 = wall.a.x
        y1 = wall.a.y
        x2 = wall.b.x
        y2 = wall.b.y

        x3 = self.pos.x
        y3 = self.pos.y
        x4 = self.pos.x + self.dir.x
        y4 = self.pos.y + self.dir.y

        den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if den == 0:
            return False;

        t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4))/den
        u = -((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3))/den

        if 0 < t < 1 and u > 0:
            pt = pg.math.Vector2()
            pt.x = (x1 + t*(x2-x1))
            pt.y = (y1 + t*(y2-y1))
            return pt
        else:
            return False;

class Particle:
    def __init__(self):
        self.pos = pg.math.Vector2(WIDTH//2,HEIGHT//2)
        self.rays = []
        for a in range(0,FOV,360//NUMBER_OF_RAYS):
            self.rays.append(Ray(self.pos.x,self.pos.y,a))

    def update(self,x,y):
        self.pos = pg.math.Vector2(x,y)

    def look(self,screen,walls):
        scene = []
        for i in range(0,len(self.rays)):
            ray = self.rays[i]
            ray.pos = pg.math.Vector2(self.pos.x,self.pos.y)
            closest = None
            record = 1000 # 1000 porque es un numero "muy grande" (deberia ser infinito)
            for wall in walls:
                pt = ray.cast(wall)
                if pt:
                    d = self.pos.distance_to(pt)
                    if d < record:
                        record = d
                        closest = pt
            if closest:
                pg.draw.line(screen,WHITE,self.pos,closest)
            scene.append(record)
        return scene

    def show(self,screen):
        pg.draw.circle(screen,WHITE,(int(self.pos.x),int(self.pos.y)),8)
        for ray in self.rays:
            ray.show(screen)
