from PIL import Image, ImageDraw
from math import floor
from random import choices
import time
import numpy as np
import pickle
import gc

from preparation import BLUE, shift_coordinate

def get_dimension(coords):
    ul, br = coords
    return br[0] - ul[0] + 1, br[1] - ul[1] + 1

class ParkingObject:
    def __init__(self, coords):
        # parking object is a rectangular object
        # coordinates: [(x0, y0), (xn, yn)], where (x0, y0) - upper left object point; (xn, yn) - botton right object point
        self.coordinates = coords


class ParkingSlot(ParkingObject):
    def __init__(self, id_n, coords):
        super().__init__(coords)
        self.id = id_n
        self.occupied = False
        self.car_exit_distance_rate = None
        self.car_entrance_distance_rate = None
        self.p_exit_distance_rate = None
        self.path = None

    def set_path(self, p):
        self.path = p
    
    def set_close_to_car_entrance(self, rate):
        self.car_entrance_distance_rate = rate

    def set_close_to_ped_exit(self, rate):
        self.p_exit_distance_rate = rate

    def set_close_to_car_exit(self, rate):
        self.car_exit_distance_rate = rate
        
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


class Parking:
    def __init__(self,
                 map, 
                 dimensions, 
                 shift,
                 slots_coords, 
                 car_entrance_coords, 
                 car_exit_coords, 
                 ped_exits_coords, 
                 walls_coords, 
                 west_movement_area, 
                 east_movement_area, 
                 north_movement_area, 
                 south_movement_area):        
        
        self.MAP = map
        self.WIDTH = dimensions[0]
        self.LENGTH = dimensions[1]
        self.x_shift = shift[0]
        self.y_shift = shift[1]

        self.parking_slots = [ParkingSlot(i + 1, slots_coords[i]) for i in range(len(slots_coords))]

        self.car_entrance = ParkingCarEntrance(1, car_entrance_coords) 

        self.car_exit = ParkingCarExit(1, car_exit_coords)

        self.p_exits = [ParkingPedestrianExit(i + 1, ped_exits_coords[i]) for i in range(len(ped_exits_coords))]

        self.walls = [ParkingWall(walls_coords[i]) for i in range(len(walls_coords))]

        self.start_at_entrance = self.get_starting_position()

        self.generate_occupancy_map() 

        self.generate_movements_map(west_movement_area, east_movement_area, north_movement_area, south_movement_area)

        self.slots_are_optimized = False

    # evaluate each slot parameters
    # Optimality parameters:
    #   close to entrance
    #   close to car exit
    #   close to pedestrian exit

    def get_starting_position(self):
        if len(self.parking_slots) > 0:
            # start is square
            car_width = min(get_dimension(self.parking_slots[0].coordinates))
            car_entrance_width, car_entrance_length = get_dimension(self.car_entrance.coordinates)
            x_medium = self.car_entrance.coordinates[0][0] + floor(car_entrance_width/2)
            y_medium = self.car_entrance.coordinates[0][1] + floor(car_entrance_length/2)
            if car_width % 2 == 0:
                upper_left = (x_medium - int(car_width/2), y_medium - int(car_width/2))
                bottom_right = (x_medium + int(car_width/2) - 1, y_medium + int(car_width/2) - 1)
            else:
                upper_left = (x_medium - floor(car_width/2), y_medium - floor(car_width/2))
                bottom_right = (x_medium + floor(car_width/2), y_medium + floor(car_width/2))
            return [upper_left, bottom_right]


    def save(self, name_to_be_saved):
        with open(name_to_be_saved, 'wb') as f:
            pickle.dump(self, f)


    def set_optimality_parameters(self):
        non_optimized = [slot for slot in self.parking_slots if slot.path is None]
        print(f"Slots number to optimize: {len(non_optimized)}")
        for slot in non_optimized:
            close_to_entrance_and_path = self.evaluate_close_to_entrance_parameter(slot)
            close_to_p_exit = self.evaluate_close_to_ped_exit_parameter(slot)
            close_to_vehicles_exit = self.evaluate_close_to_vehicles_exit_parameter(slot)
            if close_to_entrance_and_path is None or close_to_p_exit is None or close_to_vehicles_exit is None:
                print(f"Failed to set optimality parameters for slot {slot.id}")
            else:
                close_to_entrance = close_to_entrance_and_path[0]
                path = close_to_entrance_and_path[1]
                slot.set_close_to_car_entrance(close_to_entrance)
                slot.set_path(path)
                slot.set_close_to_ped_exit(close_to_p_exit)
                slot.set_close_to_car_exit(close_to_vehicles_exit)
    

    def occupy_slot(self, slot_id):
        for slot in self.parking_slots:
            if slot.id == slot_id:
                if slot.occupied:
                    print("Slot has been already occupied.")
                else:
                    slot.occupy()
                break
        print("Couldn't find slot with given id.")


    def deoccupy_slot(self, slot_id):
        for slot in self.parking_slots:
            if slot.id == slot_id:
                if not slot.occupied:
                    print("Slot is free.")
                else:
                    slot.free()
                break
        print("Couldn't find slot with given id.")


    def find_optimal_slot(self, close_to_entrance = 0.5, close_to_vehicle_exit = 0, close_to_p_exit = 0.5):
        optimal_slot = None

        count_total_cost = lambda v_entrance, v_exit, p_exit: v_entrance*close_to_entrance + v_exit*close_to_vehicle_exit + p_exit*close_to_p_exit

        optimal_cost = None

        for slot in self.get_free_slots():
            if slot.path is None:
                print(f'Slot {slot.id} is unreached.')
                continue
            cost = count_total_cost(slot.car_entrance_distance_rate, slot.car_exit_distance_rate, slot.p_exit_distance_rate)
            if optimal_slot is None or optimal_cost > cost:
                optimal_slot = slot
                optimal_cost = cost
        
        if optimal_slot is None:
            print("Couldn't find optimal slot.")
            return None
        else:
            return optimal_slot, optimal_cost
        
    
    def generate_navigation_to_slot(self, slot):
        if slot.path is None:
            print(f'Slot {slot.id} is unreached.')
        else:
            p_pos_side = min(get_dimension(slot.coordinates))
            with Image.open(self.MAP) as im:
                drawer = ImageDraw.Draw(im)
                for p in slot.path:
                    bottom_right = (p[0] + (p_pos_side - 1), p[1] + (p_pos_side - 1))
                    drawer.rectangle(shift_coordinate([p, bottom_right], -self.x_shift, -self.y_shift), fill=BLUE)
                # plot occupied positions
                for occupied_slot in self.get_occupied_slots():
                    ul = (occupied_slot.coordinates[0][0] + self.x_shift, occupied_slot.coordinates[0][1] + self.y_shift)
                    br = (occupied_slot.coordinates[1][0] + self.x_shift, occupied_slot.coordinates[1][1] + self.y_shift)
                    bl = (occupied_slot.coordinates[0][0] + self.x_shift, occupied_slot.coordinates[1][1] + self.y_shift)
                    ur = (occupied_slot.coordinates[1][0] + self.x_shift, occupied_slot.coordinates[0][1] + self.y_shift)

                    drawer.line([ul, br], fill=(0, 0, 0), width=3)
                    drawer.line([bl, ur], fill=(0, 0, 0), width=3) 
                # plot starting position
                drawer.rectangle(shift_coordinate(self.start_at_entrance, -self.x_shift, -self.y_shift), fill=(50, 168, 82))
                # plot destination area
                drawer.rectangle(shift_coordinate(slot.coordinates, -self.x_shift, -self.y_shift), fill=(252, 115, 3))
                im.show()
                im.save(f"navigation_to_slot_{slot.id}.jpg") 


    def generate_current_plan(self):
        with Image.open(self.MAP) as im:
            drawer = ImageDraw.Draw(im)
            for occupied_slot in self.get_occupied_slots():
                ul = (occupied_slot.coordinates[0][0] + self.x_shift, occupied_slot.coordinates[0][1] + self.y_shift)
                br = (occupied_slot.coordinates[1][0] + self.x_shift, occupied_slot.coordinates[1][1] + self.y_shift)
                bl = (occupied_slot.coordinates[0][0] + self.x_shift, occupied_slot.coordinates[1][1] + self.y_shift)
                ur = (occupied_slot.coordinates[1][0] + self.x_shift, occupied_slot.coordinates[0][1] + self.y_shift)
            
                drawer.line([ul, br], fill=(0, 0, 0), width=3)
                drawer.line([bl, ur], fill=(0, 0, 0), width=3)
            im.show()
            im.save("current_map.jpg")


    def evaluate_close_to_entrance_parameter(self, slot):
        start_time = time.process_time()
        path_and_cost = self.get_trajectory(self.start_at_entrance, slot.coordinates)
        time_range = time.process_time() - start_time
        print(f"CPU time to process get_trajectory() to generate entrance-slot path: {time_range} seconds")
        if type(path_and_cost) == list:
            print("Couldn't evaluate close to entrance parameter.")
            return None
        
        path, cost = path_and_cost
        return cost, path
        # if cost == 0:
        #     return 1
        # else:
        #     return 1/cost


    def get_vehicle_pos(self, slot):
        # define vehicle starting position
        ul, br = slot.coordinates
        figure_side = min(get_dimension(slot.coordinates))
        deviation_from_slot = round(figure_side / 2)

        vehicle_pos = None
   
        if br[1] - ul[1] + 1 == figure_side:
    #   ____    _________
    #  |    |  | slot    |
    #  |____|__|_________|             
            c_bottom_right = (ul[0] - deviation_from_slot, br[1])
            c_upper_left = (c_bottom_right[0] - figure_side, c_bottom_right[1] - figure_side)
            vehicle_pos = [c_upper_left, c_bottom_right]
            if not self.valid_figure_position(vehicle_pos) or not self.space_is_free(vehicle_pos):
    #       _________ __ ____ 
    #      |   slot  |  |    |
    #      |_________|  |____| 

                c_upper_left = (br[0] + deviation_from_slot, ul[1])
                c_bottom_right = (c_upper_left[0] + figure_side, c_upper_left[1] + figure_side)
                vehicle_pos = [c_upper_left, c_bottom_right]
        else:
    #       _____
    #      |slot |
    #      |     |
    #      |     |
    #      |_____|
    #      |_____
    #      |     |
    #      |_____|

            c_upper_left = (ul[0], br[1] + deviation_from_slot)
            c_bottom_right = (c_upper_left[0] + figure_side, c_upper_left[1] + figure_side)
            vehicle_pos = [c_upper_left, c_bottom_right]
            if not self.valid_figure_position(vehicle_pos) or not self.space_is_free(vehicle_pos):
    #       _____
    #      |     |
    #      |_____|
    #       _____|
    #      |slot |
    #      |     |
    #      |     |
    #      |_____|    
                    c_bottom_right = (br[0], ul[1] - deviation_from_slot)
                    c_upper_left = (c_bottom_right[0] - figure_side, c_bottom_right[1] - figure_side)
                    vehicle_pos = [c_upper_left, c_bottom_right]   
        return vehicle_pos

    
    def evaluate_close_to_vehicles_exit_parameter(self, slot):
        # define vehicle starting position
        vehicle_pos = self.get_vehicle_pos(slot)  
        start_time = time.time()
        path_and_cost = self.get_trajectory(vehicle_pos, self.car_exit.coordinates)
        exec_time = time.time() - start_time
        print(f"CPU time to process get_trajectory() to generate slot-vehicles-exit path: {exec_time} seconds")
        if type(path_and_cost) == list:
            print("Couldn't generate optimal parameter for close-to-vehicles-exit")
            return None
        cost = path_and_cost[1]
        return cost
        # if cost == 0:
        #     return 1, path
        # else:
        #     return 1 / cost, path


    def get_pedestrian_position(self, slot):
        ul, br = slot.coordinates
        slot_min_size = min(get_dimension(slot.coordinates))
        figure_side = int(slot_min_size / 2) 
        middle_x = ul[0] + round((br[0] - ul[0])/2)
        middle_y = ul[1] + round((br[1] - ul[1])/2)
        pedestrian_pos = None
     
        if br[1] - ul[1] + 1 == slot_min_size:
    #   __   _________
    #  |__| |   slot  |
    #       |_________|    
        
            c_bottom_right = (ul[0] - figure_side - 1, middle_y)
            c_upper_left = (c_bottom_right[0] - figure_side, c_bottom_right[1] - figure_side)
            pedestrian_pos = [c_upper_left, c_bottom_right]
            if not self.valid_figure_position(pedestrian_pos) or not self.space_is_free(pedestrian_pos):
    #       _________  
    #      |   slot  |  __
    #      |_________| |__| 

                c_upper_left = (br[0] + figure_side + 1, middle_y)
                c_bottom_right = (c_upper_left[0] + figure_side, c_upper_left[1] + figure_side)
                pedestrian_pos = [c_upper_left, c_bottom_right]     
        else:       
    #       _____
    #      |slot |
    #      |     |
    #      |     |
    #      |_____|
    #          __
    #         |__|

            c_upper_left = (middle_x, br[1] + figure_side + 1)
            c_bottom_right = (c_upper_left[0] + figure_side, c_upper_left[1] + figure_side)
            pedestrian_pos = [c_upper_left, c_bottom_right]
            if not self.valid_figure_position(pedestrian_pos) or not self.space_is_free(pedestrian_pos):
    #       __
    #      |__|
    #       _____
    #      |slot |
    #      |     |
    #      |     |
    #      |_____|    

                c_bottom_right = (middle_x, ul[1] - figure_side - 1)
                c_upper_left = (c_bottom_right[0] - figure_side, c_bottom_right[1] - figure_side)
                pedestrian_pos = [c_upper_left, c_bottom_right]
        return pedestrian_pos


    def evaluate_close_to_ped_exit_parameter(self, slot):
        pedestrian_pos = self.get_pedestrian_position(slot)
        cost = None
        exit_n = 1
        for p_exit in self.p_exits:
            start_time = time.time()
            path_and_cost = self.get_trajectory(pedestrian_pos, p_exit.coordinates, direction_is_important = False)
            exec_time = time.time() - start_time
            print(f"CPU time to process get_trajectory() to generate slot{slot.id}-pedestrians-exit{exit_n} path: {exec_time} seconds")
            exit_n += 1
            if type(path_and_cost) == list:
                continue
            cost = path_and_cost[1] if cost is None or path_and_cost[1] < cost else cost
        if cost is None:
            print("Couldn't generate close to pedestrians exit parameters.")
            return None
        return cost
        # if cost == 0:
        #     return 1
        # else:
        #     return 1/cost            


    def get_total_slots_number(self):
            return len(self.parking_slots)
    
    def get_free_spots_number(self):
        return len([slot for slot in self.parking_slots if not slot.occupied])

    def get_slot_coords(self, id_number):
        for slot in self.parking_slots:
            if slot.id == id_number:
                return slot.coordinates
        return None
    

    def get_p_exit_coords(self, id_numb):
        for pedestrain_exit in self.p_exits:
            if pedestrain_exit.id == id_numb:
                return pedestrain_exit.coordinates
    
    @staticmethod
    def get_coords_within(ul, br):
        return [(w, h) for w in range(ul[0], br[0]+1) for h in range(ul[1], br[1]+1)]


    within_width = lambda self, x: 0 <= x < self.WIDTH
    within_length = lambda self, y: 0 <= y < self.LENGTH
    point_is_free = lambda self, coords: self.occupancy_map[coords[1]][coords[0]] == 0


    def space_is_free(self, coordinates):
        ul, br = coordinates
        space = Parking.get_coords_within(ul, br)
        return all([self.point_is_free(point) for point in space])


    def valid_figure_position(self, coordinates):
        return all([self.within_width(coordinates[0][0]), self.within_width(coordinates[1][0]), self.within_length(coordinates[0][1]), self.within_length(coordinates[1][1])])


    def valid_point_position(self, coordinates):
        w, l = coordinates
        return self.within_width(w) and self.within_length(l)
            

    def generate_occupancy_map(self):
        grid_map = np.zeros((self.LENGTH, self.WIDTH), dtype = int)

        for slot in self.parking_slots:
            for point in Parking.get_coords_within(slot.coordinates[0], slot.coordinates[1]):
                grid_map[point[1]][point[0]] = 1
        
        for p_exit in self.p_exits:
            for point in Parking.get_coords_within(p_exit.coordinates[0], p_exit.coordinates[1]):
                grid_map[point[1]][point[0]] = 2
        
        for wall in self.walls:
            for point in Parking.get_coords_within(wall.coordinates[0], wall.coordinates[1]):
                grid_map[point[1]][point[0]] = 3
        
        self.occupancy_map = grid_map


    def get_occupancy_map(self):
        return self.occupancy_map
    

    def generate_movements_map(self, west_area, east_area, north_area, south_area):
        movements_map = []
        for i in range(self.LENGTH):
            movements_map.append([])
            for j in range(self.WIDTH):
                movements_map[-1].append([])

        for area in west_area:
            for coords in Parking.get_coords_within(area[0], area[1]):
                if self.point_is_free(coords):
                    movements_map[coords[1]][coords[0]].append('WEST')
        
        for area in east_area:
            for coords in Parking.get_coords_within(area[0], area[1]):
                if self.point_is_free(coords):
                    movements_map[coords[1]][coords[0]].append('EAST')
        
        for area in north_area:
            for coords in Parking.get_coords_within(area[0], area[1]):
                if self.point_is_free(coords):
                    movements_map[coords[1]][coords[0]].append('NORTH')
        
        for area in south_area:
            for coords in Parking.get_coords_within(area[0], area[1]):
                if self.point_is_free(coords):
                    movements_map[coords[1]][coords[0]].append('SOUTH')
        
        self.directions_map = movements_map
    
    
    def get_directions_map(self):
        return self.directions_map


    def occupy_slots_randomly(self, occupied_slots_numb):
        free_slots = self.get_free_slots()
        if len(free_slots) < occupied_slots_numb:
            for slot in free_slots:
                slot.occupy()
        else:
            for slot in choices(free_slots, k = occupied_slots_numb):
                slot.occupy()
    

    def free_all_slots(self):
        for slot in self.parking_slots:
            slot.free()
    
    
    def get_free_slots(self):
        return [slot for slot in self.parking_slots if not slot.occupied]
    

    def get_occupied_slots(self):
        return [slot for slot in self.parking_slots if slot.occupied]


    move_point_to_west = lambda coords , step: (coords[0] - step, coords[1])
    move_point_to_east = lambda coords , step: (coords[0] + step, coords[1])
    move_point_to_north = lambda coords, step: (coords[0], coords[1] - step)
    move_point_to_south = lambda coords, step: (coords[0], coords[1] + step)

    move_figure_to_west = lambda coords , step: [Parking.move_point_to_west(coords[0] , step), Parking.move_point_to_west(coords[1] , step)]
    move_figure_to_east = lambda coords , step: [Parking.move_point_to_east(coords[0] , step), Parking.move_point_to_east(coords[1] , step)]
    move_figure_to_north = lambda coords, step: [Parking.move_point_to_north(coords[0], step), Parking.move_point_to_north(coords[1], step)]
    move_figure_to_south = lambda coords, step: [Parking.move_point_to_south(coords[0], step), Parking.move_point_to_south(coords[1], step)]

    # move_figure_to_north_west = lambda coords: Parking.move_figure_to_west(Parking.move_figure_to_north(coords))
    # move_figure_to_north_east = lambda coords: Parking.move_figure_to_east(Parking.move_figure_to_north(coords))
    # move_figure_to_south_west = lambda coords: Parking.move_figure_to_west(Parking.move_figure_to_south(coords))
    # move_figure_to_south_east = lambda coords: Parking.move_figure_to_east(Parking.move_figure_to_south(coords))

    @staticmethod
    def point_inside_domain(point, domain):
        domain_ul, domain_br = domain
        return domain_ul[0] <= point[0] <= domain_br[0] and domain_ul[1] <= point[1] <= domain_br[1]


    @staticmethod
    def spaces_intersect(figure1, figure2):
        figure1_upper_left = figure1[0]
        figure1_bottom_right = figure1[1]
        figure1_upper_right = (figure1_bottom_right[0], figure1_upper_left[1])
        figure1_bottom_left = (figure1_upper_left[0], figure1_bottom_right[1])

        figure2_upper_left = figure2[0]
        figure2_bottom_right = figure2[1]
        figure2_upper_right = (figure2_bottom_right[0], figure2_upper_left[1])
        figure2_bottom_left = (figure2_upper_left[0], figure2_bottom_right[1])
        
        return any([Parking.point_inside_domain(figure1_upper_left, figure2) or   Parking.point_inside_domain(figure2_upper_left, figure1), 
                    Parking.point_inside_domain(figure1_bottom_right, figure2) or Parking.point_inside_domain(figure2_bottom_right, figure1),
                    Parking.point_inside_domain(figure1_upper_right, figure2) or  Parking.point_inside_domain(figure2_upper_right, figure1),
                    Parking.point_inside_domain(figure1_bottom_left, figure2) or  Parking.point_inside_domain(figure2_bottom_left, figure1)])
        
    def get_trajectory(self, starting_pos, destination_coordinates, direction_is_important = True):
        # check if starting coordinates is a valid position 
        # movement - 4 directions allowed: north, south, west, east 
        if not self.valid_figure_position(starting_pos) or not self.space_is_free(starting_pos) or not self.valid_figure_position(destination_coordinates):
            print("Given coordinates are invalid.")
            return None

        figure_min_size = min(get_dimension(starting_pos))
        step = int(figure_min_size/2)

        def recreate_figure(point):
            # upper_left = point
            bottom_right = (point[0] + figure_min_size - 1, point[1] + figure_min_size - 1)
            return [point, bottom_right]
        
        # create heuristic function: for 4 sides - manhattan distance h(p1, p2) = abs(p1.x - p2.x) + abs(p1.y - p2.y)
        def heuristic(point):
            return abs(point[0] - destination_coordinates[0][0]) + abs(point[1] - destination_coordinates[0][1])

        # create g function: g(parent_g) = parent_g + 1
        def g_cost(parent_g):
            return parent_g + 1
        
        def point_inside_destination(point):
            return destination_coordinates[0][0] <= point[0] <= destination_coordinates[1][0] and destination_coordinates[0][1] <= point[1] <= destination_coordinates[1][1]

        # def figure_interstects_destination(figure_pos):
        #     if Parking.spaces_intersect(figure_pos, destination_coordinates):
        #         medium_step = int(figure_min_size/2)
        #         if destination_coordinates[1][0] - destination_coordinates[0][0] < destination_coordinates[1][1] - destination_coordinates[0][1]:
        #             upper_medium = (figure_pos[0][0] + medium_step, figure_pos[0][1])
        #             bottom_medium = (figure_pos[0][0] + medium_step, figure_pos[1][1])
        #             return any([point_inside_destination(upper_medium) and destination_coordinates[0][0] <= upper_medium[0] <= destination_coordinates[1][0],
        #                        point_inside_destination(bottom_medium) and destination_coordinates[0][0] <= bottom_medium[0] <= destination_coordinates[1][0]])
        #         else:
        #             left_medium = (figure_pos[0][0], figure_pos[0][1] + medium_step)
        #             right_medium = (figure_pos[1][0], figure_pos[0][1] + medium_step)
        #             return any([point_inside_destination(left_medium) and destination_coordinates[0][1] <= left_medium[1] <= destination_coordinates[1][1],
        #                         point_inside_destination(right_medium) and destination_coordinates[0][1] <= right_medium[1] <= destination_coordinates[1][1]]) 
        
         
        open_array = []
        closed_array = []
        previous = {}
        cost = {}
        # append to open_array - staring_coordinates: (0, heuristic(staring_coordinates, destination_coordinates)
        start = starting_pos[0]
        open_array.append(start)
        cost[start] = (0, heuristic(start))
        previous[start] = start
        # start loop while there are figure positions in the open_array 
        while len(open_array) > 0:
            q = min([el for el in cost.items() if el[0] in open_array], key = lambda x: sum(x[1]))[0]
            # pop q from open list
            open_array.remove(q)
            closed_array.append(q)

            for candidate, opposite_direction in [(Parking.move_point_to_north(q, step), 'SOUTH'),
                                                  (Parking.move_point_to_south(q, step), 'NORTH'),
                                                  (Parking.move_point_to_east(q,  step), 'WEST'),
                                                  (Parking.move_point_to_west(q,  step), 'EAST')]:
                figure_pos = recreate_figure(candidate)
                if self.valid_figure_position(figure_pos):
                    # for vehicles trajectory check if there are no pedestrian exits(2) or walls(3) on the way to the candidate position
                    if direction_is_important:
                        if any([self.occupancy_map[point[1]][point[0]] in [2, 3] for point in Parking.get_coords_within(figure_pos[0], figure_pos[1])]):
                            continue       
                    # for pedestrians trajectory check if there are no parking slots (1) or walls(3) on the way to the candidate position
                    else:
                        if any([self.occupancy_map[point[1]][point[0]] in [1, 3] for point in Parking.get_coords_within(figure_pos[0], figure_pos[1])]):
                            continue
                    if Parking.spaces_intersect(figure_pos, destination_coordinates):
                        g = g_cost(cost[q][0])
                        previous[candidate] = q
                        cost[candidate] = (g, 0)
                        closed_array.append(candidate)
                        # add extra step to make medium point of the figure inside the destination figure
                        if opposite_direction == 'SOUTH':
                            pos = Parking.move_point_to_north(candidate, step)
                        elif opposite_direction == 'NORTH':
                            pos = Parking.move_point_to_south(candidate, step)
                        elif opposite_direction == 'WEST':
                            pos = Parking.move_point_to_east(candidate,  step)
                        else:
                            pos = Parking.move_point_to_west(candidate,  step)
                        
                        previous[pos] = candidate
                        g = g_cost(g)
                        cost[pos] = (g, 0)
                        closed_array.append(pos)

                        path = [pos]
                        while pos != start:
                            pos = previous[pos]
                            path.append(pos)
                        path.reverse()
                        return path, g

                    if self.space_is_free(figure_pos):
                        if direction_is_important and opposite_direction in self.directions_map[q[1]][q[0]]:
                            continue
                        g = g_cost(cost[q][0])
                        h = heuristic(candidate)
                        
                        if candidate not in open_array and candidate not in closed_array:
                            open_array.append(candidate)
                            cost[candidate] = (g, h)
                            previous[candidate] = q
                        else:
                            if g + h < sum(cost[candidate]):
                                previous[candidate] = q
                                cost[candidate] = (g, h)

                                if candidate in closed_array:
                                    closed_array.remove(candidate)
                                    open_array.append(candidate)  
            

        print('Goal is unreachable\n----')
        return closed_array            