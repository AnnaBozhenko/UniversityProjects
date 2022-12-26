from PIL import Image, ImageDraw
from random import choices
from preparation import get_dimension


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
                 dimensions, 
                 slots_coords, 
                 car_entrance_coords, 
                 car_exit_coords, 
                 ped_exits_coords, 
                 walls_coords, 
                 west_movement_area, 
                 east_movement_area, 
                 north_movement_area, 
                 south_movement_area):        
        
        self.WIDTH = dimensions[0]
        self.LENGTH = dimensions[1]

        self.parking_slots = [ParkingSlot(i + 1, slots_coords[i]) for i in range(len(slots_coords))]

        self.car_entrance = ParkingCarEntrance(1, car_entrance_coords) 

        self.car_exit = ParkingCarExit(1, car_exit_coords)

        self.p_exits = [ParkingPedestrianExit(i + 1, ped_exits_coords[i]) for i in range(len(ped_exits_coords))]

        self.walls = [ParkingWall(walls_coords[i]) for i in range(len(walls_coords))]

        self.set_starting_position()

        self.generate_occupancy_map() 

        self.generate_movements_map(west_movement_area, east_movement_area, north_movement_area, south_movement_area)

        # self.set_optimality_parameters()

    # evaluate each slot parameters
    # Optimality parameters:
    #   close to entrance
    #   close to car exit
    #   close to pedestrian exit

    def set_starting_position(self):
        if len(self.parking_slots) > 0:
            car_width = min(get_dimension(self.parking_slots[0].coordinates))
            car_entrance_width, car_entrance_length = get_dimension(self.car_entrance.coordinates)
            x_medium = self.car_entrance.coordinates[0][0] + round(car_entrance_width/2)
            y_medium = self.car_entrance.coordinates[0][1] + round(car_entrance_length/2)
            upper_left = (x_medium - round(car_width/2), y_medium - round(car_width/2))
            bottom_right = (upper_left[0] + car_width, upper_left[1] + car_width)
            self.car_pos_at_entrance = [upper_left, bottom_right]


    def set_optimality_parameters(self):
        for slot in self.parking_slots:
            close_to_entrance_and_path = self.evaluate_close_to_entrance_parameter(slot)
            
            close_to_p_exit = self.evaluate_close_to_ped_exit_parameter(slot)
            close_to_vehicles_exit = self.evaluate_close_to_vehicles_exit_parameter(slot)
            if close_to_p_exit is None or close_to_vehicles_exit is None or close_to_entrance_and_path is None:
                continue

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


    def find_optimal_slot(self, close_to_entrance = True, close_to_vehicle_exit = False, close_to_p_exit = False):
        optimal_slot = None

        count_total_cost = lambda v_entrance, v_exit, p_exit: v_entrance*close_to_entrance + v_exit*close_to_vehicle_exit + p_exit*close_to_p_exit

        optimal_cost = None

        for slot in self.get_free_slots():
            if slot.path is None:
                print('Slot is unreached.')
                return None
            cost = count_total_cost(slot.car_entrance_distance_rate, slot.car_exit_distance_rate, slot.p_exit_distance_rate)
            if optimal_slot is None or optimal_cost > cost:
                optimal_slot = slot
                optimal_cost = cost
        
        if optimal_slot is None:
            print("Couldn't find optimal slot.")
            return None
        else:
            return optimal_slot, optimal_cost


    def evaluate_close_to_entrance_parameter(self, slot):
        path_and_cost = self.get_trajectory(self.car_pos_at_entrance, slot.coordinates)
        if path_and_cost is None:
            print("Couldn't evaluate close to entrance parameter.")
            return None
        
        path, cost = path_and_cost
        return cost, path
        # if cost == 0:
        #     return 1
        # else:
        #     return 1/cost

    
    def evaluate_close_to_vehicles_exit_parameter(self, slot):
        # define vehicle starting position
        ul, br = slot.coordinates
        figure_side = min(get_dimension(slot.coordinates))
        deviation_from_slot = round(figure_side / 2)

        vehicle_pos = None
    #   ____    _________
    #  |    |  | slot    |
    #  |____|__|_________|    

        c_bottom_right = (ul[0] - deviation_from_slot, br[1])
        c_upper_left = (c_bottom_right[0] - figure_side, c_bottom_right[1] - figure_side)
        vehicle_pos = [c_upper_left, c_bottom_right]
        if not self.valid_figure_position(vehicle_pos) or not self.space_is_free(vehicle_pos):
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
    #       _________ __ ____ 
    #      |   slot  |  |    |
    #      |_________|  |____| 

                c_upper_left = (br[0] + deviation_from_slot, ul[1])
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
                    if not self.valid_figure_position(vehicle_pos) or not self.space_is_free(vehicle_pos):
                        print("Can't set starting pedestrian position")
                        return None    
        path_and_cost = self.get_trajectory(vehicle_pos, self.car_exit)
        if path_and_cost is None:
            print("Couldn't generate optimal parameter for close-to-vehicles-exit")
        cost = path_and_cost[1]
        return cost
        # if cost == 0:
        #     return 1, path
        # else:
        #     return 1 / cost, path

    
    def evaluate_close_to_ped_exit_parameter(self, slot):
        # find start position: 

        ul, br = slot.coordinates
        slot_width = min(get_dimension(slot.coordinates))
        figure_side = round(slot_width / 2)
        deviation_from_slot = round(figure_side / 2)
        middle_x = ul[0] + round((br[0] - ul[0])/2)
        middle_y = ul[1] + round((br[1] - ul[1])/2)
        pedestrian_pos = None
     
    #   __   _________
    #  |__|_|   slot  |
    #       |_________|    
        c_bottom_right = (ul[0] - deviation_from_slot, middle_y)
        c_upper_left = (c_bottom_right[0] - figure_side, c_bottom_right[1] - figure_side)
        pedestrian_pos = [c_upper_left, c_bottom_right]
        if not self.valid_figure_position(pedestrian_pos) or not self.space_is_free(pedestrian_pos):
    #       _____
    #      |slot |
    #      |     |
    #      |     |
    #      |_____|
    #         |__
    #         |__|
            c_upper_left = (middle_x, br[1] + deviation_from_slot)
            c_bottom_right = (c_upper_left[0] + figure_side, c_upper_left[1] + figure_side)
            pedestrian_pos = [c_upper_left, c_bottom_right]
            if not self.valid_figure_position(pedestrian_pos) or not self.space_is_free(pedestrian_pos):
    #       _________  
    #      |   slot  |_ __
    #      |_________| |__| 
                c_upper_left = (br[0] + deviation_from_slot, middle_y)
                c_bottom_right = (c_upper_left[0] + figure_side, c_upper_left[1] + figure_side)
                pedestrian_pos = [c_upper_left, c_bottom_right]
                if not self.valid_figure_position(pedestrian_pos) or not self.space_is_free(pedestrian_pos):
    #       __
    #      |__|
    #       __|__
    #      |slot |
    #      |     |
    #      |     |
    #      |_____|    
                    c_bottom_right = (middle_x, ul[1] - deviation_from_slot)
                    c_upper_left = (c_bottom_right[0] - figure_side, c_bottom_right[1] - figure_side)
                    pedestrian_pos = [c_upper_left, c_bottom_right]
                    if not self.valid_figure_position(pedestrian_pos) or not self.space_is_free(pedestrian_pos):
                        print("Can't set starting pedestrian position")
                        return None
        cost = None
        for p_exit in self.p_exits:
            path_and_cost = self.get_trajectory(pedestrian_pos, p_exit.coordinates)
            if path_and_cost is None:
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
    point_is_free = lambda self, coords: self.bi_occupancy_map[coords[1]][coords[0]] == 0


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
        bi_grid = [[0] * self.WIDTH] * self.LENGTH

        for slot in self.parking_slots:
            for coords in Parking.get_coords_within(slot.coordinates[0], slot.coordinates[1]):
                bi_grid[coords[1]][coords[0]] = 1
        
        for p_exit in self.p_exits:
            for coords in Parking.get_coords_within(p_exit.coordinates[0], p_exit.coordinates[1]):
                bi_grid[coords[1]][coords[0]] = 1
        
        for wall in self.walls:
            for coords in Parking.get_coords_within(wall.coordinates[0], wall.coordinates[1]):
                bi_grid[coords[1]][coords[0]] = 1
        
        self.bi_occupancy_map = bi_grid


    def get_bi_grid(self):
        return self.bi_occupancy_map
    

    def generate_movements_map(self, west_area, east_area, north_area, south_area):
        movements_map = [[[]] * self.WIDTH] * self.LENGTH

        for area in west_area:
            for coords in Parking.get_coords_within(area[0], area[1]):
                if self.point_is_free(coords):
                    west_shift_pos = Parking.move_point_to_west(coords)
                    if self.valid_point_position(west_shift_pos) and self.point_is_free(west_shift_pos):
                        movements_map[coords[1]][coords[0]].append(west_shift_pos)
        
        for area in east_area:
            for coords in Parking.get_coords_within(area[0], area[1]):
                if self.point_is_free(coords):
                    east_shift_pos = Parking.move_point_to_east(coords)
                    if self.valid_point_position(east_shift_pos) and self.point_is_free(east_shift_pos):
                        movements_map[coords[1]][coords[0]].append(east_shift_pos)
        
        for area in north_area:
            for coords in Parking.get_coords_within(area[0], area[1]):
                if self.point_is_free(coords):
                    north_shift_pos = Parking.move_point_to_north(coords)
                    if self.valid_point_position(north_shift_pos) and self.point_is_free(north_shift_pos):
                        movements_map[coords[1]][coords[0]].append(north_shift_pos)
        
        for area in south_area:
            for coords in Parking.get_coords_within(area[0], area[1]):
                if self.point_is_free(coords):
                    south_shift_pos = Parking.move_point_to_south(coords)
                    if self.valid_point_position(south_shift_pos) and self.point_is_free(south_shift_pos):
                        movements_map[coords[1]][coords[0]].append(south_shift_pos)
        
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


    move_point_to_west = lambda coords: (coords[0] - 1, coords[1])
    move_point_to_east = lambda coords: (coords[0] + 1, coords[1])
    move_point_to_north = lambda coords: (coords[0], coords[1] - 1)
    move_point_to_south = lambda coords: (coords[0], coords[1] + 1)

    move_figure_to_west = lambda coords: [Parking.move_point_to_west(coords[0]), Parking.move_point_to_west(coords[1])]
    move_figure_to_east = lambda coords: [Parking.move_point_to_east(coords[0]), Parking.move_point_to_east(coords[1])]
    move_figure_to_north = lambda coords: [Parking.move_point_to_north(coords[0]), Parking.move_point_to_north(coords[1])]
    move_figure_to_south = lambda coords: [Parking.move_point_to_south(coords[0]), Parking.move_point_to_south(coords[1])]

    # move_figure_to_north_west = lambda coords: Parking.move_figure_to_west(Parking.move_figure_to_north(coords))
    # move_figure_to_north_east = lambda coords: Parking.move_figure_to_east(Parking.move_figure_to_north(coords))
    # move_figure_to_south_west = lambda coords: Parking.move_figure_to_west(Parking.move_figure_to_south(coords))
    # move_figure_to_south_east = lambda coords: Parking.move_figure_to_east(Parking.move_figure_to_south(coords))

    @staticmethod
    def point_inside_space(point, space):
        space_ul, space_br = space
        point_x, space_y = point
        return space_ul[0] <= point_x <= space_br[0] and space_ul[1] <= space_y <= space_br[1]


    @staticmethod
    def spaces_intersect(space1, space2):
        space1_dim = get_dimension(space1)
        space2_dim = get_dimension(space2)
        if space1_dim >= space2_dim:
            upper_left = space2[0]
            bottom_right = space2[1]
            upper_right = (bottom_right[0], upper_left[1])
            bottom_left = (upper_left[0], bottom_right[1])
            return any([Parking.point_inside_space(upper_left, space1), 
                        Parking.point_inside_space(upper_right, space1),
                        Parking.point_inside_space(bottom_right, space1), 
                        Parking.point_inside_space(bottom_left, space1)])
        else:
            upper_left = space1[0]
            bottom_right = space1[1]
            upper_right = (bottom_right[0], upper_left[1])
            bottom_left = (upper_left[0], bottom_right[1])
            return any([Parking.point_inside_space(upper_left, space2), 
                        Parking.point_inside_space(upper_right, space2),
                        Parking.point_inside_space(bottom_right, space2), 
                        Parking.point_inside_space(bottom_left, space2)])
        

    def get_trajectory(self, starting_pos, destination_coordinates, direction_is_important = True):
        # starting coordinates - coordinates of square figure: [upper_left_point, bottom_right_point] 
        # destination coordinates - coordinates of destination area: [upper_left_point, bottom_right_point];
        #  
        # check if starting coordinates is a valid position 
        # movement - 4 directions allowed: north, south, west, east 
        if not self.valid_figure_position(starting_pos) or not self.space_is_free(starting_pos) or not self.valid_figure_position(destination_coordinates):
            print("Given coordinates are invalid.")
            return None
        
        # create heuristic function: for 4 sides - manhattan distance h(p1, p2) = abs(p1.x - p2.x) + abs(p1.y - p2.y)
        # where p1, p2 - upper left points of appropriate figure rectangle
        def heuristic(figure_position):
            figure_ul = figure_position[0]
            destination_ul = destination_coordinates[0]
            return abs(figure_ul[0] - destination_ul[0]) + abs(figure_ul[1] - destination_ul[1])

        # create g function: g(parent_g) = parent_g + 1
        def g_cost(parent_g):
            return parent_g + 1
        
        # possibly to delete
        # def point_belongs(point, space):
        #     point_x, point_y = point
        #     space_ul, space_br = space
        #     return space_ul[0] <= point_x <= space_br[0] and space_ul[1] <= point_y <= space_br[1]

        # create open_array: {(figure coordinates): (figure_g, figure_h)}
        open_array = {}
        # create closed_array: {(figure coordinates): (figure_g, figure_h)}
        closed_array = {}
        # create parents: {(figure coordinates): (figure previous location coordinates)}
        parents = {}
        # append to open_array - staring_coordinates: (0, heuristic(staring_coordinates, destination_coordinates)
        open_array[tuple(starting_pos)] = (0, heuristic(starting_pos))
        goal_pos = None
        # start loop while there are figure positions in the open_array 
        while len(open_array) > 0:
            # find q = the figure position in open array with the minimum h + g
            q = min(open_array, key= lambda k: sum(open_array[k]))
            # pop q from open list
            q_cost = open_array.pop(q)
        #   generate all possible neighbouring figure positions
            neighbour_positions = []

            # define neighbour positions (candidate) and corresponding opposite position 
            # and check if it is posible to move to each neighbour position
            candidate_positions = [(Parking.move_figure_to_north(q), Parking.move_figure_to_south(q)),
                                   (Parking.move_figure_to_south(q), Parking.move_figure_to_north(q)),
                                   (Parking.move_figure_to_east(q),  Parking.move_figure_to_west(q)),
                                   (Parking.move_figure_to_west(q),  Parking.move_figure_to_east(q))]
            for candidate, opposite_to_candidate in candidate_positions:
                c = tuple(candidate)
                if self.valid_figure_position(candidate):
                    if Parking.spaces_intersect(candidate, destination_coordinates):
                        g = g_cost(q_cost[0])
                        parents[c] = q
                        closed_array[c] = (g, 0)
                        open_array = {}
                        goal_pos = c
                        break
                    if direction_is_important:
                        x_pos = q[0][0]
                        y_pos = q[0][1]
                        if opposite_to_candidate[0] in self.directions_map[y_pos][x_pos]:
                            continue
                    if self.space_is_free(candidate):
                        neighbour_positions.append(c)

            if neighbour_positions == []:
                print("No space to move.")
                return None
            if goal_pos is not None:
                break
        #   loop over all neigbouring positions
            for n in neighbour_positions:
                n_cost = (g_cost(q_cost[0]), heuristic(n))
                if n not in open_array.keys() and n not in closed_array.keys():
                    parents[n] = q
                    open_array[n] = n_cost
                elif n in open_array.keys():
                    if sum(n_cost) < sum(open_array[n]):
                        parents[n] = q
                        open_array[n] = n_cost
                else:
                    if sum(n_cost) < sum(closed_array[n]):
                        parents[n] = q
                        open_array[n] = n_cost

            closed_array[q] = q_cost

        if goal_pos is None:
            print('Goal is unreachable.')
            return None
        else:
            pos = goal_pos
            path = [pos]
            while pos != starting_pos:
                pos = parents[pos]
                path.append(pos)

            path.reverse()
            path_cost = closed_array[goal_pos]
            return path, path_cost
    