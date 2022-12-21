from PIL import Image, ImageDraw
# import pygame
# from sys import exit
import numpy as np
from random import choices

class ParkingObject():
    def __init__(self, ul, br):
        self.upper_left = ul
        self.bottom_right = br


class ParkingSlot(ParkingObject):
    def __init__(self, id_n, ul, br):
        super().__init__(ul, br)
        self.id = id_n
        self.occupied = False
        self.car_exit_distance_rate = 1
        self.car_entrance_distance_rate = 1
        self.pedestrian_exit_distance_rate = 1
    
    def occupy(self):
        self.occupied = True
    
    def free(self):
        self.occupied = False


class ParkingCarExit(ParkingObject):
    def __init__(self, id_n, ul, br):
        super().__init__(ul, br)
        self.id = id_n


class ParkingCarEntrance(ParkingObject):
    def __init__(self, id_n, ul, br):
        super().__init__(ul, br)
        self.id = id_n


class ParkingPedestrianExit(ParkingObject):
    def __init__(self, id_n, ul, br):
        super().__init__(ul, br)
        self.id = id_n


class ParkingWall(ParkingObject):
    def __init__(self, ul, br):
        super().__init__(ul, br)


class Parking():
    def __init__(self, 
                 parking_size,
                 model_car_size, 
                 slots_coords, car_entrance_coords, car_exit_coords, ped_exits_coords, walls_coords, 
                 left_movement_area, right_movement_area, up_movement_area, down_movement_area):        
        # initializing car parking objects
        self.parking_width, self.parking_length = parking_size
        self.parking_slots = [ParkingSlot(i + 1, slots_coords[i][0], slots_coords[i][1]) for i in range(len(slots_coords))]

        self.MODEL_WIDTH, self.MODEL_LENGTH = model_car_size

        self.car_entrance = ParkingCarEntrance(1, car_entrance_coords[0], car_entrance_coords[1]) 

        self.car_exits = ParkingCarExit(1, car_exit_coords[0], car_exit_coords[1])

        self.pedestrian_exits = [ParkingPedestrianExit(i + 1, ped_exits_coords[i][0], ped_exits_coords[i][1]) for i in range(len(ped_exits_coords))]

        self.walls = [ParkingWall(walls_coords[i][0], walls_coords[i][1]) for i in range(len(walls_coords))]

        self.bi_occupancy_map = self.generate_bi_grid() 

        self.directions_map = self.generate_movements_map(left_movement_area, right_movement_area, up_movement_area, down_movement_area)
    

    def get_model_vehicle_size(self):
        return self.MODEL_WIDTH, self.MODEL_LENGTH


    def get_slots_quantity(self):
            return len(self.parking_slots)
        

    def get_slot_coords(self, id_number):
        for slot in self.parking_slots:
            if slot.id == id_number:
                return (slot.upper_left, slot.upper_right)
        return None
    

    def get_pedestrian_exit_coords(self, id_numb):
        for pedestrain_exit in self.pedestrian_exits:
            if pedestrain_exit.id == id_numb:
                return (pedestrain_exit.upper_left, pedestrain_exit.bottom_right)
    

    def get_coords_within(self, ul, br):
        return [(x, y) for y in range(ul[1], br[1]+1) for x in range(ul[0], br[0]+1)]


    def generate_bi_grid(self):
        # add one to width and length as 0's pixel is also considered
        bi_grid = np.zeros([self.parking_length + 1, self.parking_width + 1], dtype=int)

        for slot in self.parking_slots:
            for coords in self.get_coords_within(slot.upper_left, slot.bottom_right):
                bi_grid[coords[1]][coords[0]] = 1
        
        for pedestrian_exit in self.pedestrian_exits:
            for coords in self.get_coords_within(pedestrian_exit.upper_left, pedestrian_exit.bottom_right):
                bi_grid[coords[1]][coords[0]] = 1
        
        for wall in self.walls:
            for coords in self.get_coords_within(wall.upper_left, wall.bottom_right):
                bi_grid[coords[1]][coords[0]] = 1

        return bi_grid
    

    def valid_movement_to(self, point_2):
        if point_2[0] > self.parking_width or point_2[1] > self.parking_length:
            return False
        elif point_2[0] < 0 or point_2[1] < 0:
            return False
        if self.bi_occupancy_map[point_2[1]][point_2[0]] == 1:
            return False
        return True


    def generate_movements_map(self, left_a, right_a, up_a, down_a):
        movements_map = [[] for i in range(self.parking_width + 1) for j in range(self.parking_length + 1)]

        for area in left_a:
            for coords in self.get_coords_within(area[0], area[1]):
                if self.bi_occupancy_map[coords[1]][coords[0]] == 0:
                    left_shift_pos = (coords[0] - 1, coords[1])
                    if self.valid_movement_to(left_shift_pos):
                        # movements_map[coords[1]][coords[0]].append(left_shift_pos)
                        movements_map[coords[1]][coords[0]].append('Left')
        
        for area in right_a:
            for coords in self.get_coords_within(area[0], area[1]):
                if self.bi_occupancy_map[coords[1]][coords[0]] == 0:
                    right_shift_pos = (coords[0] + 1, coords[1])
                    if self.valid_movement_to(right_shift_pos):
                        # movements_map[coords[1]][coords[0]].append(right_shift_pos)
                        movements_map[coords[1]][coords[0]].append('Right')
        
        for area in up_a:
            for coords in self.get_coords_within(area[0], area[1]):
                if self.bi_occupancy_map[coords[1]][coords[0]] == 0:
                    up_shift_pos = (coords[0], coords[1] - 1)
                    if self.valid_movement_to(up_shift_pos):
                        # movements_map[coords[1]][coords[0]].append(up_shift_pos)
                        movements_map[coords[1]][coords[0]].append('Up')
        
        for area in down_a:
            for coords in self.get_coords_within(area[0], area[1]):
                if self.bi_occupancy_map[coords[1]][coords[0]] == 0:
                    down_shift_pos = (coords[0], coords[1] + 1)
                    if self.valid_movement_to(down_shift_pos):
                        # movements_map[coords[1]][coords[0]].append(down_shift_pos)
                        movements_map[coords[1]][coords[0]].append('Down')
        
        return movements_map



    def occupy_slots_randomly(self, occupied_slots_numb):
        free_slots = [slot for slot in self.parking_slots if not slot.occupied]
        if len(free_slots) < occupied_slots_numb:
            for slot in free_slots:
                slot.occupy()
        else:
            for slot in choices(free_slots, k = occupied_slots_numb):
                slot.occupy()
    

    def free_all_slots(self):
        for slot in self.parking_slots:
            slot.occupied = False
    
    
    def get_current_map(self):
        occupied_slots = [slot for slot in self.parking_slots if slot.occupied]
        CURRENT_MAP_NAME = "current_map.png"
        with Image.open(self.IMAGE_PATH) as im:
            drawer = ImageDraw.Draw(im)
            BLACK = (0, 0, 0)
            for slot in occupied_slots:
                ul = slot.upper_left
                br = slot.bottom_right
                bl = (slot.upper_left[0], slot.bottom_right[1])
                ur = (slot.bottom_right[0], slot.upper_left[1])
                drawer.line((ul, br), fill = BLACK, width = 3)
                drawer.line((bl, ur), fill = BLACK, width = 3)
            im.show()
            im.save(CURRENT_MAP_NAME)


    def move_left(self, vehicle_coords):
        ul, br = vehicle_coords[0], vehicle_coords[1]
        return [(ul[0] - 1, ul[1]), (br[0] - 1, br[1])]

    
    def move_right(self, vehicle_coords):
        ul, br = vehicle_coords[0], vehicle_coords[1]
        return [(ul[0] + 1, ul[1]), (br[0] + 1, br[1])]


    def move_up(self, vehicle_coords):
        ul, br = vehicle_coords[0], vehicle_coords[1]
        return [(ul[0], ul[1] - 1), (br[0], br[1] - 1)]

    
    def move_down(self, vehicle_coords):
        ul, br = vehicle_coords[0], vehicle_coords[1]
        return [(ul[0], ul[1] + 1), (br[0], br[1] + 1)]

    # def turn(self, vehicle_coords):
    #     w = vehicle_coords[]
    def trajectory(self, starting_point, destination_point):
        # possible vehicle movements in the parking area: forward, backwards, rotation (90*)
        heuristic = lambda p_x, p_y: abs(p_x - destination_point[0]) * abs(p_y - destination_point[1])
        pass


