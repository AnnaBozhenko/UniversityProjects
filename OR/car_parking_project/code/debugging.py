import pickle 
from math import floor
from preparation import mark_regions, get_dimension, shift_coordinate, shift_point, BLUE
PARKING_MAP = "parking_plan_fitted.jpg"
from PIL import Image, ImageDraw


def point_inside_space(point, space):
        space_ul, space_br = space
        point_x, space_y = point
        return space_ul[0] <= point_x <= space_br[0] and space_ul[1] <= space_y <= space_br[1]

def spaces_intersect(figure1, figure2):
        figure1_upper_left = figure1[0]
        figure1_bottom_right = figure1[1]
        figure1_upper_right = (figure1_bottom_right[0], figure1_upper_left[1])
        figure1_bottom_left = (figure1_upper_left[0], figure1_bottom_right[1])

        figure2_upper_left = figure2[0]
        figure2_bottom_right = figure2[1]
        figure2_upper_right = (figure2_bottom_right[0], figure2_upper_left[1])
        figure2_bottom_left = (figure2_upper_left[0], figure2_bottom_right[1])
        
        return any([point_inside_space(figure1_upper_left, figure2) or point_inside_space(figure2_upper_left, figure1), 
                    point_inside_space(figure1_bottom_right, figure2) or point_inside_space(figure2_bottom_right, figure1),
                    point_inside_space(figure1_upper_right, figure2) or point_inside_space(figure2_upper_right, figure1),
                    point_inside_space(figure1_bottom_left, figure2) or point_inside_space(figure2_bottom_left, figure1)])

def pedestrian_pos(parking, slot):
        # find start position: 

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
            if not parking.valid_figure_position(pedestrian_pos) or not parking.space_is_free(pedestrian_pos):
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
            if not parking.valid_figure_position(pedestrian_pos) or not parking.space_is_free(pedestrian_pos):
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


def vehicle_pos(parking, slot):
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
            if not parking.valid_figure_position(vehicle_pos) or not parking.space_is_free(vehicle_pos):
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
            if not parking.valid_figure_position(vehicle_pos) or not parking.space_is_free(vehicle_pos):
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

def intersects_destination(figure_pos, destination_coordinates):
        x_medium = floor((figure_pos[1][0] - figure_pos[0][0])/2)
        y_medium = floor((figure_pos[1][1] - figure_pos[0][1])/2)
        upper_medium = (figure_pos[0][0] + x_medium, figure_pos[0][1]) 
        left_medium = (figure_pos[0][0], figure_pos[0][1] + y_medium)
        right_medium = (figure_pos[1][0], figure_pos[1][1] - y_medium)
        bottom_medium = (figure_pos[0][0] + x_medium, figure_pos[1][1])
        return any([point_inside_space(upper_medium, destination_coordinates),
                point_inside_space(left_medium, destination_coordinates),
                point_inside_space(right_medium, destination_coordinates),
                point_inside_space(bottom_medium, destination_coordinates)])

if __name__ == "__main__":
    with open('parking.dat', 'rb') as f:
        parking = pickle.load(f)
    x_shift, y_shift = parking.x_shift, parking.y_shift

    parking_width, parking_length = parking.WIDTH, parking.LENGTH

#     source = parking.start_at_entrance
# #     goal = [(111, 56), (358, 95)]
#     source_side = source[1][0] - source[0][0] + 1
#     step = int(source_side/2)
   
#     with Image.open(PARKING_MAP) as im:
#         drawer = ImageDraw.Draw(im)
#         drawer.rectangle(shift_coordinate(source, -x_shift, -y_shift), fill=(50, 168, 82))
#         # drawer.rectangle(shift_coordinate(goal, -x_shift, -y_shift), fill=(168, 135, 50))
#         for wall in parking.walls:
#                 drawer.rectangle(shift_coordinate(wall.coordinates, -x_shift, -y_shift), fill=(0, 0, 0))
#         for slot in parking.parking_slots:
#                 drawer.rectangle(shift_coordinate(slot.coordinates, -x_shift, -y_shift), fill=(0, 0, 0))
#         for slot in parking.parking_slots:
#                 drawer.rectangle(shift_coordinate(slot.coordinates, -x_shift, -y_shift), fill=BLUE)
        
#         i = source[0][0]
#         j = source[0][1]
#         while i >= 0 or j >= 0:
#                 if i >= 0:
#                         drawer.line((shift_point((i, 0), -x_shift, -y_shift), shift_point((i, parking_length), -x_shift, -y_shift)), fill=BLUE)
#                 if j >= 0:
#                         drawer.line((shift_point((0, j), -x_shift, -y_shift), shift_point((parking_width, j), -x_shift, -y_shift)), fill=BLUE)
#                 i -= step
#                 j -= step
#         i = source[0][0] + step
#         j = source[0][1] + step
#         while i <= parking_width or j <= parking_length:
#                 if i <= parking_width:
#                         drawer.line((shift_point((i, 0), -x_shift, -y_shift), shift_point((i, parking_length), -x_shift, -y_shift)), fill=BLUE)
#                 if j <= parking_length:
#                         drawer.line((shift_point((0, j), -x_shift, -y_shift), shift_point((parking_width, j), -x_shift, -y_shift)), fill=BLUE)
#                 i += step
#                 j += step
#         im.show()

#     pc = parking.get_trajectory(source, goal, False)
#     if pc is not None:
#         path = pc[0]
#         with Image.open(PARKING_MAP) as im:
#             drawer = ImageDraw.Draw(im)
#             drawer.rectangle(shift_coordinate(source, -x_shift, -y_shift), fill=(50, 168, 82))
#             for i in range(len(path) - 1):
#                 drawer.line(((path[i][0] + x_shift, path[i][1] + y_shift), (path[i+1][0] + x_shift, path[i+1][1] + y_shift)), BLUE, width=3)
#             drawer.rectangle(shift_coordinate(goal, -x_shift, -y_shift), fill=(168, 135, 50))
#             im.save('debugging/path.jpg')
#     else:
#         print('failure')

# ====================================================================================================
# TEST: generating path 'parking slot - pedestrian exit'
# ====================================================================================================

#     ped_pos = [pedestrian_pos(parking, slot) for slot in parking.parking_slots]
#     p_pos_side = min(get_dimension(ped_pos[0]))
#     ped_exits = parking.p_exits

#     slot_count = 1
#     exit_count = 1
#     for p_pos in ped_pos:
#         exit_count = 1
#         for p_exit in ped_exits:
#             with Image.open(PARKING_MAP) as im:
#                     drawer = ImageDraw.Draw(im)
#                     # plot starting position
#                     drawer.rectangle(shift_coordinate(p_pos, -x_shift, -y_shift), fill=(50, 168, 82))
#                     # plot destination area
#                     drawer.rectangle(shift_coordinate(p_exit.coordinates, -x_shift, -y_shift), fill=(252, 115, 3))
#                     pc = parking.get_trajectory(p_pos, p_exit.coordinates, False)
#                     if type(pc) == tuple:
#                             path = pc[0]
#                             for i in range(len(path) - 1):
#                                 drawer.line(((path[i][0] + x_shift, path[i][1] + y_shift), (path[i+1][0] + x_shift, path[i+1][1] + y_shift)), BLUE, width=3)
#                             im.save(f"debugging/path_slot_pedestrian_exit/path_slot_{slot_count}_pedestrian_exit{exit_count}.jpg")
#                     else:
#                         print(f"Failed to set up path for slot {slot_count} with coordinates: {p_pos} to exit {exit_count} with coordinates: {p_exit}")
#                         visited_points = pc
#                         step = int(p_pos_side/2)

#                         with Image.open(PARKING_MAP) as im:
#                             drawer = ImageDraw.Draw(im)
#                         #     plot visited area
#                             for p in visited_points:
#                                     upper_left = shift_point((p[0], p[1]), -x_shift, -y_shift)
#                                     bottom_right = shift_point((p[0] + (p_pos_side - 1), p[1] + (p_pos_side - 1)), -x_shift, -y_shift)
#                                     drawer.rectangle([upper_left, bottom_right], fill=BLUE)
    

#                             #     plot grid
#                             i = p_pos[0][0]
#                             j = p_pos[0][1]
    
#                             while i >= 0 or j >= 0:
#                                 if i >= 0:
#                                         drawer.line((shift_point((i, 0), -x_shift, -y_shift), shift_point((i, parking_length), -x_shift, -y_shift)), fill=(252, 3, 19))
#                                 if j >= 0:
#                                         drawer.line((shift_point((0, j), -x_shift, -y_shift), shift_point((parking_width, j), -x_shift, -y_shift)), fill=(252, 3, 19))
#                                 i -= step
#                                 j -= step

#                             i = p_pos[0][0] + step
#                             j = p_pos[0][1] + step
#                             while i < parking_width or j < parking_length:
#                                     if i < parking_width:
#                                             drawer.line((shift_point((i, 0), -x_shift, -y_shift), shift_point((i, parking_length), -x_shift, -y_shift)), fill=(252, 3, 19))
#                                     if j < parking_length:
#                                             drawer.line((shift_point((0, j), -x_shift, -y_shift), shift_point((parking_width, j), -x_shift, -y_shift)), fill=(252, 3, 19))
#                                     i += step
#                                     j += step
#                             # plot walls
#                             for w in parking.walls:
#                                 drawer.rectangle(shift_coordinate(w.coordinates, -x_shift, -y_shift), fill = (0, 0, 0))
#                     #     plot starting position
#                             drawer.rectangle(shift_coordinate(p_pos, -x_shift, -y_shift), fill=(50, 168, 82))
#                     #     plot destination area
#                             drawer.rectangle(shift_coordinate(p_exit, -x_shift, -y_shift), fill=(252, 115, 3))
#                             im.save(f"debugging/path_slot_pedestrian_exit/path_slot_{slot_count}_pedestrian_exit{exit_count}.jpg")
#                     exit_count += 1
#         slot_count += 1

#     veh_pos = [vehicle_pos(parking, slot) for slot in parking.parking_slots]
#     vehicle_exit = parking.car_exit.coordinates

# =========================================================================================================
# TEST: generating path 'car entrance - parking slot'
# =========================================================================================================

#     slots = [slot.coordinates for slot in parking.parking_slots]
#     start = parking.start_at_entrance

#     slot_count = 1
#     for slot in slots:
#             p_pos_side = min(get_dimension(start))
#             # for p_exit in ped_exits:
#             pc = parking.get_trajectory(start, slot)
#             if type(pc) == list:
#                     print(f"Failed to set up path for entrance-slot {slot_count} with source -> dest coordinates: {start} -> {slot}")
#                     visited_points = pc
#                     step = int(p_pos_side/2)

#                     with Image.open(PARKING_MAP) as im:
#                         drawer = ImageDraw.Draw(im)
#                     #     plot visited area
#                         for p in visited_points:
#                                 upper_left = shift_point((p[0], p[1]), -x_shift, -y_shift)
#                                 bottom_right = shift_point((p[0] + (p_pos_side - 1), p[1] + (p_pos_side - 1)), -x_shift, -y_shift)
#                                 drawer.rectangle([upper_left, bottom_right], fill=BLUE)


#                         #     plot grid
#                         i = start[0][0]
#                         j = start[0][1]

#                         while i >= 0 or j >= 0:
#                                 if i >= 0:
#                                         drawer.line((shift_point((i, 0), -x_shift, -y_shift), shift_point((i, parking_length), -x_shift, -y_shift)), fill=(252, 3, 19))
#                                 if j >= 0:
#                                         drawer.line((shift_point((0, j), -x_shift, -y_shift), shift_point((parking_width, j), -x_shift, -y_shift)), fill=(252, 3, 19))
#                                 i -= step
#                                 j -= step
#                         i = start[0][0] + step
#                         j = start[0][1] + step
#                         while i < parking_width or j < parking_length:
#                                 if i < parking_width:
#                                         drawer.line((shift_point((i, 0), -x_shift, -y_shift), shift_point((i, parking_length), -x_shift, -y_shift)), fill=(252, 3, 19))
#                                 if j < parking_length:
#                                         drawer.line((shift_point((0, j), -x_shift, -y_shift), shift_point((parking_width, j), -x_shift, -y_shift)), fill=(252, 3, 19))
#                                 i += step
#                                 j += step
#                 #     plot slots
#                         for s in parking.parking_slots:
#                             drawer.rectangle(shift_coordinate(s.coordinates, -x_shift, -y_shift), fill = (0, 0, 0))
#                 # plot walls
#                         for w in parking.walls:
#                             drawer.rectangle(shift_coordinate(w.coordinates, -x_shift, -y_shift), fill = (0, 0, 0))
#                 #     plot starting position
#                         drawer.rectangle(shift_coordinate(start, -x_shift, -y_shift), fill=(50, 168, 82))
#                 #     plot destination area
#                         drawer.rectangle(shift_coordinate(slot, -x_shift, -y_shift), fill=(252, 115, 3))
#                         im.save(f"debugging/path_entrance_slot/path_entrance_slot_{slot_count}.jpg")
#             else:
#                 path = pc[0]
#                 with Image.open(PARKING_MAP) as im:
#                         drawer = ImageDraw.Draw(im)
#                         for p in path:
#                                 bottom_right = (p[0] + (p_pos_side - 1), p[1] + (p_pos_side - 1))
#                                 drawer.rectangle(shift_coordinate([p, bottom_right], -x_shift, -y_shift), fill=BLUE)
#                         # plot starting position
#                         drawer.rectangle(shift_coordinate(start, -x_shift, -y_shift), fill=(50, 168, 82))
#                         # plot destination area
#                         drawer.rectangle(shift_coordinate(slot, -x_shift, -y_shift), fill=(252, 115, 3))
#                         im.save(f"debugging/path_entrance_slot/path_entrance_slot_{slot_count}.jpg")  

#             slot_count += 1
    
# ===================================================================================================
# TEST: generating path 'parking slot - car entrance'
# ===================================================================================================

#     veh_pos = [vehicle_pos(parking, slot) for slot in parking.parking_slots]
#     vehicle_exit = parking.car_exit.coordinates
#     print(vehicle_exit)
#     slot_count = 1
#     for v_pos in veh_pos:
#         pc = parking.get_trajectory(v_pos, vehicle_exit)
#         p_pos_side = min(get_dimension(v_pos))
#         if type(pc) == tuple:
#             path = pc[0]
#             with Image.open(PARKING_MAP) as im:
#                 drawer = ImageDraw.Draw(im)
#                 for p in path:
#                     bottom_right = (p[0] + (p_pos_side - 1), p[1] + (p_pos_side - 1))
#                     drawer.rectangle(shift_coordinate([p, bottom_right], -x_shift, -y_shift), fill=BLUE)
#                 # plot starting position
#                 drawer.rectangle(shift_coordinate(v_pos, -x_shift, -y_shift), fill=(50, 168, 82))
#                 # plot destination area
#                 drawer.rectangle(shift_coordinate(vehicle_exit, -x_shift, -y_shift), fill=(252, 115, 3))
#                 im.save(f"debugging/path_slot_vehicle_exit/path_slot_{slot_count}_vehicles_exit.jpg")
#         else:
#             print(f"Failed to set up path for {slot_count} with coordinates {v_pos}")
#             with Image.open(PARKING_MAP) as im:
#                 drawer = ImageDraw.Draw(im)
#                 visited_points = pc
#                 step = int(p_pos_side/2)

#                 #     plot visited area
#                 for p in visited_points:
#                     upper_left = shift_point((p[0], p[1]), -x_shift, -y_shift)
#                     bottom_right = shift_point((p[0] + (p_pos_side - 1), p[1] + (p_pos_side - 1)), -x_shift, -y_shift)
#                     drawer.rectangle([upper_left, bottom_right], fill=BLUE)

#                 #     plot grid
#                 i = v_pos[0][0]
#                 j = v_pos[0][1]
#                 while i >= 0 or j >= 0:
#                     if i >= 0:
#                             drawer.line((shift_point((i, 0), -x_shift, -y_shift), shift_point((i, parking_length), -x_shift, -y_shift)), fill=(252, 3, 19))
#                     if j >= 0:
#                             drawer.line((shift_point((0, j), -x_shift, -y_shift), shift_point((parking_width, j), -x_shift, -y_shift)), fill=(252, 3, 19))
#                     i -= step
#                     j -= step
#                 i = v_pos[0][0] + step
#                 j = v_pos[0][1] + step
#                 while i < parking_width or j < parking_length:
#                     if i < parking_width:
#                             drawer.line((shift_point((i, 0), -x_shift, -y_shift), shift_point((i, parking_length), -x_shift, -y_shift)), fill=(252, 3, 19))
#                     if j < parking_length:
#                             drawer.line((shift_point((0, j), -x_shift, -y_shift), shift_point((parking_width, j), -x_shift, -y_shift)), fill=(252, 3, 19))
#                     i += step
#                     j += step
#                 #     plot slots
#                 for s in parking.parking_slots:
#                     drawer.rectangle(shift_coordinate(s.coordinates, -x_shift, -y_shift), fill = (0, 0, 0))
#                 # plot walls
#                 for w in parking.walls:
#                     drawer.rectangle(shift_coordinate(w.coordinates, -x_shift, -y_shift), fill = (0, 0, 0))
#                 #     plot starting position
#                 drawer.rectangle(shift_coordinate(v_pos, -x_shift, -y_shift), fill=(50, 168, 82))
#                 #     plot destination area
#                 drawer.rectangle(shift_coordinate(vehicle_exit, -x_shift, -y_shift), fill=(252, 115, 3))
#                 im.save(f"debugging/path_slot_vehicle_exit/path_slot_{slot_count}_vehicles_exit.jpg")

#         slot_count += 1


# ===================================================================================================
# TEST: generating all pedestrian positions
# ===================================================================================================

#     ped_pos = [pedestrian_pos(parking, slot) for slot in parking.parking_slots]
#     with Image.open(PARKING_MAP) as im:
#         drawer = ImageDraw.Draw(im)
#         i = 0
#         for p_pos in ped_pos:
#             drawer.rectangle(shift_coordinate(p_pos, -x_shift, -y_shift), fill = BLUE)
#         #     drawer.rectangle(shift_coordinate(parking.parking_slots[i].coordinates, -x_shift, -y_shift), fill=(50, 168, 82))
#             i += 1
#         im.save("debugging/pedestrian_positions.jpg")

# ===================================================================================================
# TEST: generating all pedestrian exits
# ===================================================================================================

#     ped_exits = parking.p_exits
#     with Image.open(PARKING_MAP) as im:
#         drawer = ImageDraw.Draw(im)
#         for p_exit in ped_exits:
#             drawer.rectangle(shift_coordinate(p_exit.coordinates, -x_shift, -y_shift), fill = BLUE)
#         im.save("debugging/pedestrian_exits.jpg")
    
#     veh_pos = [vehicle_pos(parking, slot) for slot in parking.parking_slots]

# ===================================================================================================
# TEST: generating all vehicles positions (vehicle moving to exit)
# ===================================================================================================    

#     with Image.open(PARKING_MAP) as im:
#         drawer = ImageDraw.Draw(im)
#         for v_pos in veh_pos:
#             drawer.rectangle(shift_coordinate(v_pos, -x_shift, -y_shift), fill = BLUE)
#         im.save("debugging/vehicles_positions.jpg")

# ===================================================================================================
# TEST: generating vehicle's starting position which enters the parking
# ===================================================================================================  

#     with Image.open(PARKING_MAP) as im:
#         drawer = ImageDraw.Draw(im)
#         drawer.rectangle(shift_coordinate(parking.start_at_entrance, -x_shift, -y_shift), fill= BLUE)
#         im.save("debugging/start.jpg")    