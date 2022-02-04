import pygame, sys, time, random, json
from pygame.locals import *

pygame.init()
WIDTH, HEIGHT = 600, 400
surface=pygame.display.set_mode((WIDTH, HEIGHT),0,32)
fps=64
ft=pygame.time.Clock()
pygame.display.set_caption('Towers of Hanoi')

PLATES_COUNT = 4

class Plate:
    def __init__(self, size):
        self.size = size
        self.color = self.randomize_color()
    def randomize_color(self):
        return (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

class Tower:
    def __init__(self):
        self.plates = []
    def add_plate(self, plate):
        self.plates.append(plate)
    def get_top_index(self):
        return -1

class Hanoi:
    def __init__(self):
        self.towers = []
        self.pointer = 0
        self.spoon = None
        self.no_of_towers = 4
    def create_initial_plates(self):
        for _ in range(self.no_of_towers):
            new_tower = Tower()
            self.towers.append(new_tower)
        if len(self.towers)>0:
            for size in range(1, PLATES_COUNT+1):
                new_plate = Plate(size)
                self.towers[0].add_plate(new_plate)
    def lift_plate(self):
        if self.spoon is None:
            if len(self.towers[self.pointer].plates)>0:
                top_index = self.towers[self.pointer].get_top_index()
                self.spoon = self.towers[self.pointer].plates[top_index]
                self.towers[self.pointer].plates.pop(top_index)
    def can_it_be_dropped_there(self):
        if len(self.towers[self.pointer].plates)==0:
            return True
        top_index = self.towers[self.pointer].get_top_index()
        top_size = self.towers[self.pointer].plates[top_index].size
        if self.spoon.size > top_size:
            return True
        return False
    def drop_plate(self):
        if self.spoon is not None:
            if self.can_it_be_dropped_there():
                self.towers[self.pointer].add_plate(self.spoon)
                self.spoon = None
    def move(self, direction):
        self.pointer = (self.pointer+direction)%self.no_of_towers

class App:
    def __init__(self, surface):
        self.surface = surface
        self.play = True
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.color = {
            "background": (40, 51, 80),
            "alpha": (20, 180, 210)
        }
        self.hanoi = Hanoi()
        self.hanoi.create_initial_plates()
        self.gap_between_towers = 20
        self.tower_top_y = int((HEIGHT/100)*20)
        self.tower_base_y = int((HEIGHT/100)*80)
        self.developer_mode = False
    def render(self):
        no_of_towers = self.hanoi.no_of_towers
        extra_space_need = (no_of_towers+1)*self.gap_between_towers
        space_each_tower_occupies = int((WIDTH/no_of_towers)-(extra_space_need/no_of_towers))
        for tower_index in range(no_of_towers):
            x = self.gap_between_towers+(tower_index*space_each_tower_occupies)+(tower_index*self.gap_between_towers)
            height = self.tower_base_y-self.tower_top_y
            pygame.draw.rect(self.surface, self.color["alpha"], (x, self.tower_top_y, space_each_tower_occupies, height), 1)
        if self.developer_mode:
            data_sheet = [len(tower.plates) for tower in self.hanoi.towers]
            print (data_sheet)
    def move(self, key):
        if key==K_UP:
            self.hanoi.lift_plate()
        elif key==K_DOWN:
            self.hanoi.drop_plate()
        elif key==K_LEFT:
            self.hanoi.move(-1)
        elif key==K_RIGHT:
            self.hanoi.move(1)
    def run(self):
        while self.play:
            self.surface.fill(self.color["background"])
            self.mouse=pygame.mouse.get_pos()
            self.click=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_TAB:
                        self.play=False
                    elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                        self.move(event.key)
            #--------------------------------------------------------------
            self.render()
            # -------------------------------------------------------------
            pygame.display.update()
            ft.tick(fps)



if  __name__ == "__main__":
    app = App(surface)
    app.run()

