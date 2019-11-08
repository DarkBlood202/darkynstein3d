import pygame as pg
import sys
import random
from os import path
from settings import *
from entities import *
from methods import *
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.load_map()

    def load_map(self):
        gameFolder = path.dirname(__file__)
        self.map = Map(path.join(gameFolder, "map.txt"))

    def new_game(self):
        self.walls = []

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    self.walls.append(MapBlock(col, row))


        '''for i in range(NUMBER_OF_WALLS):
            x1 = random.randint(0, SCENE_WIDTH)
            x2 = random.randint(0, SCENE_WIDTH)
            y1 = random.randint(0, HEIGHT)
            y2 = random.randint(0, HEIGHT)
            self.walls.append(Boundary(x1,y1,x2,y2))

        self.walls.append(Boundary(0, 0, SCENE_WIDTH, 0))
        self.walls.append(Boundary(0, 0, 0, HEIGHT))
        self.walls.append(Boundary(SCENE_WIDTH-1, 0, SCENE_WIDTH-1, HEIGHT))
        self.walls.append(Boundary(0, HEIGHT-1, SCENE_WIDTH-1, HEIGHT-1))'''

        self.particle = Particle()

    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BG_COLOR)

        for wall in self.walls:
            wall.show(self.screen)

        mouseX = pg.mouse.get_pos()[0]
        mouseY = pg.mouse.get_pos()[1]
        self.particle.update(mouseX, mouseY)

        self.particle.show(self.screen)
        self.scene = self.particle.look(self.screen, self.walls)

        w = SCENE_WIDTH/len(self.scene)

        for i in range(0, len(self.scene)):
            h = remap(self.scene[i], 0, SCENE_WIDTH, HEIGHT, 0)
            #print("distance: ",self.scene[i])
            #print("height: ",h)

            var = int(self.scene[i])
            if var > 255:
                var = 255

            color = (255-var, 255-var, 255-var)

            rectangle = (SCENE_WIDTH + (i*w+w/2), HEIGHT/2-h/2, w+1, h)

            pg.draw.rect(self.screen, color, rectangle)

        pg.display.flip()

    def events(self):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                self.quit()

    def show_start_screen(self):
        pass

    def show_game_over_screen(self):
        pass


if __name__ == "__main__":
    g = Game()
    g.show_start_screen()
    while True:
        g.new_game()
        g.run()
        g.show_game_over_screen()
