from PIL import Image, ImageDraw
# import pygame
# from sys import exit
import numpy as np
from random import choices

class ParkingObject():
    def __init__(self, coords):
        self.coordinates = coords


class ParkingSlot(ParkingObject):
    def __init__(self, id_n, coords):
        super().__init__(coords)
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
    def __init__(self, id_n, coords):
        super().__init__(coords)
        self.id = id_n


class ParkingCarEntrance(ParkingObject):
    def __init__(self, id_n, coords):
        super().__init__(coords)
        self.id = id_n


class ParkingPedestrianExit(ParkingObject):
    def __init__(self, id_n, coords):
        super().__init__(coords)
        self.id = id_n


class ParkingWall(ParkingObject):
    def __init__(self, coords):
        super().__init__(coords)


class Parking():
    def __init__(self, 
                 coords,
                 model_car_size, 
                 slots_coords, car_entrance_coords, car_exit_coords, ped_exits_coords, walls_coords, 
                 left_movement_area, right_movement_area, up_movement_area, down_movement_area):        
        # initializing car parking objects
        self.parking_coords = coords
        self.parking_slots = [ParkingSlot(i + 1, slots_coords[i]) for i in range(len(slots_coords))]

        self.MODEL_WIDTH, self.MODEL_LENGTH = model_car_size

        self.car_entrance = ParkingCarEntrance(1, car_entrance_coords) 

        self.car_exit = ParkingCarExit(1, car_exit_coords)

        self.pedestrian_exits = [ParkingPedestrianExit(i + 1, ped_exits_coords[i]) for i in range(len(ped_exits_coords))]

        self.walls = [ParkingWall(walls_coords[i]) for i in range(len(walls_coords))]

        self.generate_bi_grid() 

        self.generate_movements_map(left_movement_area, right_movement_area, up_movement_area, down_movement_area)


    def get_model_vehicle_size(self):
        return self.MODEL_WIDTH, self.MODEL_LENGTH


    def get_slots_quantity(self):
            return len(self.parking_slots)
        

    def get_slot_coords(self, id_number):
        for slot in self.parking_slots:
            if slot.id == id_number:
                return slot.coordinates
        return None
    

    def get_pedestrian_exit_coords(self, id_numb):
        for pedestrain_exit in self.pedestrian_exits:
            if pedestrain_exit.id == id_numb:
                return pedestrain_exit.coordinates
    
# 
    def get_coords_within(self, ul, br):
        return [(w, h) for w in range(ul[0], br[0]+1) for h in range(ul[1], br[1]+1)]


    within_width = lambda self, x: 0 <= x <= self.parking_width
    within_length = lambda self, y: 0 <= y <= self.parking_length
    point_is_free = lambda self, coords: self.bi_occupancy_map[coords[1]][coords[0]] == 0

    # develop
    def space_is_free(self, coordinates):
        ul, br = coordinates
        space = self.get_coords_within(ul, br)
        for point 


    def valid_figure_coordinates(self, coordinates):
        ul, br = coordinates
        return self.within_width(ul[0]) and self.within_width(br[0]) and self.within_length(ul[1]) and self.within_length(br[1])


    def valid_point_coordiantes(self, coordinates):
        w, l = coordinates
        return self.within_width(w) and self.within_length(l)

    # develop
    def generate_bi_grid(self):
        # add one to width and length as 0's pixel is also considered
        bi_grid = np.zeros([self.parking_length + 1, self.parking_width + 1], dtype=int)

        for slot in self.parking_slots:
            for coords in self.get_coords_within(slot.upper_left, slot.bottom_right):
                if self.valid_point_coordinates(coords):
                    bi_grid[coords[1]][coords[0]] = 1
        
        for pedestrian_exit in self.pedestrian_exits:
            for coords in self.get_coords_within(pedestrian_exit.upper_left, pedestrian_exit.bottom_right):
                if self.valid_point_coordinates(coords):
                    bi_grid[coords[1]][coords[0]] = 1
        
        for wall in self.walls:
            for coords in self.get_coords_within(wall.upper_left, wall.bottom_right):
                if self.valid_figure_coordinates(coords):
                    bi_grid[coords[1]][coords[0]] = 1
        
        self.bi_occupancy_map = bi_grid
        return bi_grid
    

    def generate_movements_map(self, left_area, right_area, up_area, down_area):
        movements_map = [[] * (self.parking_width + 1)] * (self.parking_length + 1)

        for area in left_area:
            for coords in self.get_coords_within(area[0], area[1]):
                if self.valid_point_coordinates(coords) and self.point_is_free(coords):
                    left_shift_pos = self.move_point_left(coords)
                    if self.valid_point_coordinates(left_shift_pos) and self.point_is_free(left_shift_pos):
                        movements_map[coords[1]][coords[0]].append(left_shift_pos)
                        # movements_map[coords[1]][coords[0]].append('Left')
        
        for area in right_area:
            for coords in self.get_coords_within(area[0], area[1]):
                if self.valid_point_coordinates(coords) and self.point_is_free(coords):
                    right_shift_pos = self.move_point_right(coords)
                    if self.valid_point_coordinates(right_shift_pos) and self.point_is_free(right_shift_pos):
                        movements_map[coords[1]][coords[0]].append(right_shift_pos)
                        # movements_map[coords[1]][coords[0]].append('Right')
        
        for area in up_area:
            for coords in self.get_coords_within(area[0], area[1]):
                if self.valid_point_coordinates(coords) and self.point_is_free(coords):
                    up_shift_pos = self.move_point_up(coords)
                    if self.self.valid_point_coordinates(up_shift_pos) and self.point_is_free(up_shift_pos):
                        movements_map[coords[1]][coords[0]].append(up_shift_pos)
                        # movements_map[coords[1]][coords[0]].append('Up')
        
        for area in down_area:
            for coords in self.get_coords_within(area[0], area[1]):
                if self.valid_point_coordinates(coords) and self.point_is_free(coords):
                    down_shift_pos = self.move_point_down(coords)
                    if self.valid_point_coordinates(down_shift_pos) and self.point_is_free(down_shift_pos):
                        movements_map[coords[1]][coords[0]].append(down_shift_pos)
                        # movements_map[coords[1]][coords[0]].append('Down')
        
        self.directions_map = movements_map
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


    move_point_left = lambda self, coords: (coords[0] - 1, coords[1])
    move_point_right = lambda self, coords: (coords[0] + 1, coords[1])
    move_point_up = lambda self, coords: (coords[0], coords[1] - 1)
    move_point_down = lambda self, coords: (coords[0] + 1, coords[1] + 1)


    move_figure_left = lambda self, coords: [self.move_point_left(coords[0]), self.move_point_left(coords[1])]
    move_figure_right = lambda self, coords: [self.move_point_right(coords[0]), self.move_point_right(coords[1])]
    move_figure_up = lambda self, coords: [self.move_point_up(coords[0]), self.move_point_up(coords[1])]
    move_figure_down = lambda self, coords: [self.move_point_down(coords[0]), self.move_point_down(coords[1])]

    # develop
    def trajectory(self, starting_point, destination_point):
        # possible vehicle movements in the parking area: forward, backwards, rotation (90*)
        heuristic = lambda p_x, p_y: abs(p_x - destination_point[0]) * abs(p_y - destination_point[1])
        pass
