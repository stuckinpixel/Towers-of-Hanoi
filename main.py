
import pygame, sys, time, random, json
from pygame.locals import *

pygame.init()
WIDTH, HEIGHT = 1000, 600
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
        self.no_of_towers = 3
        self.gap_between_towers = self.get_percentage_of_size(WIDTH, 5)
        self.height_of_base = self.get_percentage_of_size(HEIGHT, 5)
        self.gap_between_plates = self.get_percentage_of_size(HEIGHT, 2)
        extra_space_need = (self.no_of_towers+1)*self.gap_between_towers
        self.space_each_tower_occupies = int((WIDTH/self.no_of_towers)-(extra_space_need/self.no_of_towers))
        self.tower_top_y = self.get_percentage_of_size(HEIGHT, 25)
        self.tower_top_offset = self.get_percentage_of_size(HEIGHT, 28)
        self.tower_base_y = self.get_percentage_of_size(HEIGHT, 80)
        self.tower_width = self.get_percentage_of_size(WIDTH, 1)
        self.plate_height = self.calculate_width_and_height_of_a_plate()
        self.sizes = self.get_width_for_size_of_the_plates()
        self.pointer_width = self.get_percentage_of_size(WIDTH, 10)
        self.pointer_height = self.get_percentage_of_size(HEIGHT, 5)
        self.pointer_y = self.get_percentage_of_size(HEIGHT, 87)
        self.spoon_base_y = self.get_percentage_of_size(HEIGHT, 23)
    def get_percentage_of_size(self, total, percentage):
        return int((total/100)*percentage)
    def calculate_width_and_height_of_a_plate(self):
        total_height = self.tower_base_y-self.tower_top_offset-(self.gap_between_plates*PLATES_COUNT)
        return total_height//PLATES_COUNT
    def get_width_for_size_of_the_plates(self):
        sizes = {}
        half_of_the_distance_covered_by_plate = (self.space_each_tower_occupies-self.tower_width)//2
        for size in range(1, PLATES_COUNT+1):
            percentage_of_plate_size = size/PLATES_COUNT
            half_width = percentage_of_plate_size*half_of_the_distance_covered_by_plate
            full_width = (half_width*2)+self.tower_width
            sizes.update({
                size: full_width
            })
        return sizes
    def create_initial_plates(self):
        for _ in range(self.no_of_towers):
            new_tower = Tower()
            self.towers.append(new_tower)
        if len(self.towers)>0:
            for size in range(PLATES_COUNT, 0, -1):
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
        if self.spoon.size < top_size:
            return True
        return False
    def drop_plate(self):
        if self.spoon is not None:
            if self.can_it_be_dropped_there():
                self.towers[self.pointer].add_plate(self.spoon)
                self.spoon = None
                return True
            else:
                return False
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
            "alpha": (20, 180, 210),
            "tower": (20, 180, 210),
            "base": (20, 150, 20),
            "pointer": (150, 50, 30),
            "alert": (210, 80, 80),
            "message": (20, 180, 210)
        }
        self.hanoi = Hanoi()
        self.hanoi.create_initial_plates()
        self.alert_enabled = time.time()
        self.alert_lasting_time = 0.3
        self.alert_thickness = 10
        self.moves_count = 0
        self.message_font = pygame.font.SysFont('Arial', 23)
    def draw_base(self):
        pygame.draw.rect(self.surface, self.color["base"], (self.hanoi.gap_between_towers, self.hanoi.tower_base_y, WIDTH-(self.hanoi.gap_between_towers*2), self.hanoi.height_of_base))
    def draw_pointer(self):
        x1, y1 = self.hanoi.gap_between_towers+(self.hanoi.pointer*self.hanoi.space_each_tower_occupies)+(self.hanoi.pointer*self.hanoi.gap_between_towers)+((self.hanoi.space_each_tower_occupies/2)-(self.hanoi.tower_width//2)), self.hanoi.pointer_y
        x2, y2 = x1+(self.hanoi.pointer_width//2), y1+(self.hanoi.pointer_height)
        x3, y3 = x1-(self.hanoi.pointer_width//2), y1+(self.hanoi.pointer_height)
        pygame.draw.polygon(self.surface, self.color["pointer"], [[x1, y1], [x2, y2], [x3, y3]])
    def draw_spoon(self):
        spoon = self.hanoi.spoon
        if spoon is not None:
            plate_width = self.hanoi.sizes[spoon.size]
            mid_tower_x = (self.hanoi.gap_between_towers*(self.hanoi.pointer+1))+(self.hanoi.space_each_tower_occupies*self.hanoi.pointer)+(self.hanoi.space_each_tower_occupies//2)
            x = mid_tower_x-(plate_width//2)
            y = self.hanoi.spoon_base_y-self.hanoi.plate_height
            pygame.draw.rect(self.surface, self.hanoi.spoon.color, (x, y, plate_width, self.hanoi.plate_height), border_radius=10)
    def draw_tower(self, tower_index, x, y, width, height):
        tower_x = x+((width/2)-(self.hanoi.tower_width//2))
        pygame.draw.rect(self.surface, self.color["tower"], (tower_x, y, self.hanoi.tower_width, height))
        plate_y = self.hanoi.tower_base_y-self.hanoi.gap_between_plates-self.hanoi.plate_height
        for plate in self.hanoi.towers[tower_index].plates:
            plate_width = self.hanoi.sizes[plate.size]
            plate_x = x+((self.hanoi.space_each_tower_occupies-plate_width)/2)
            pygame.draw.rect(self.surface, plate.color, (plate_x, plate_y, plate_width, self.hanoi.plate_height), border_radius=10)
            plate_y -= self.hanoi.plate_height
            plate_y -= self.hanoi.gap_between_plates
    def show_alert(self):
        if self.alert_enabled>time.time():
            pygame.draw.rect(self.surface, self.color["alert"], (0, 0, WIDTH, HEIGHT), self.alert_thickness)
    def show_moves_count(self):
        textsurface = self.message_font.render("Moves "+str(self.moves_count), False, self.color["message"])
        self.surface.blit(textsurface,(20,20))
    def render(self):
        self.draw_base()
        for tower_index in range(self.hanoi.no_of_towers):
            x = self.hanoi.gap_between_towers+(tower_index*self.hanoi.space_each_tower_occupies)+(tower_index*self.hanoi.gap_between_towers)
            height = self.hanoi.tower_base_y-self.hanoi.tower_top_y
            self.draw_tower(tower_index, x, self.hanoi.tower_top_y, self.hanoi.space_each_tower_occupies, height)
        data_sheet = [len(tower.plates) for tower in self.hanoi.towers]
        self.draw_pointer()
        self.draw_spoon()
        self.show_alert()
        self.show_moves_count()
    def alert(self):
        self.alert_enabled = time.time()+self.alert_lasting_time
    def move(self, key):
        if key==K_UP:
            self.hanoi.lift_plate()
        elif key==K_DOWN:
            successfull = self.hanoi.drop_plate()
            if successfull:
                self.moves_count+=1
            else:
                self.alert()
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

