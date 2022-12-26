import parking_facilities as pf
from PIL import Image, ImageDraw
import pygame
import pickle
# from image_resizing import resize_image

ORIGINAL_MAP = "parking_plan_original.jpg"
PARKING_MAP = "parking_plan_fitted.jpg"
PATHS = ["parking_data/parking_dimension.dat", #parking_dimension,
         "parking_data/vehicle_position.dat",#starting_vehicle_position,
         "parking_data/parking_slots_locations.dat",#slots_locations,
         "parking_data/parking_vehicles_entrance.dat",#v_entrance_location,
         "parking_data/parking_vehicles_exit.dat",#v_exit_location,
         "parking_data/parking_pedestrian_exit.dat",#p_exits_locations,
         "parking_data/parking_obstacles.dat",#walls_locations,
         "parking_data/parking_west_directions.dat",#west_movement_areas,
         "parking_data/parking_east_directions.dat",#east_movement_areas,
         "parking_data/parking_north_directions.dat", #north_movement_areas,
         "parking_data/parking_south_directions.dat"] #south_movement_areas


BLUE = (66, 135, 245)
SCREEN_LENGTH = 800
# resize_image(ORIGINAL_MAP, SCREEN_LENGTH, PARKING_MAP)
# with Image.open(PARKING_MAP) as im:
#     SCREEN_WIDTH = im.size[0]
SCREEN_WIDTH = 1131

def get_dimension(coords):
    ul, br = coords
    return (br[0] - ul[0] + 1, br[1] - ul[1] + 1)


def define_objects(object_dimension, caption):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    original_bg = pygame.image.load(PARKING_MAP).convert()
    bg = original_bg.copy()
    r = pygame.Rect((0, 0), object_dimension)
    objects_locations = []

    screen.blit(bg, (0, 0))
    pygame.draw.rect(screen, BLUE, r)
    pygame.display.flip()

    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(objects_locations) > 0:
                        objects_locations.pop()
                        bg = original_bg.copy()
                        screen.blit(bg, (0, 0))
                        [pygame.draw.rect(bg, BLUE, pygame.Rect(object[0], get_dimension(object))) for object in objects_locations]
                        pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    x_shift = pos[0] - r.left
                    y_shift = pos[1] - r.top
                    r.move_ip(x_shift, y_shift)
                    objects_locations.append([r.topleft, r.bottomright])
                    pygame.draw.rect(bg, BLUE, r)
                    pygame.display.flip()
                elif event.button == 3:
                    w = r.width
                    r.width = r.height
                    r.height = w
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                x_shift = pos[0] - r.left
                y_shift = pos[1] - r.top
                r.move_ip(x_shift, y_shift)
                screen.blit(bg, (0, 0))
                pygame.draw.rect(screen, BLUE, r)
                pygame.display.flip()
    
    pygame.quit()
    return objects_locations

# look again
def define_object(object_dimension, caption):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()


    original_bg = pygame.image.load(PARKING_MAP).convert()
    bg = original_bg.copy()
    r = pygame.Rect((0, 0), object_dimension)
    object_location = None
    screen.blit(bg, (0, 0))
    pygame.draw.rect(screen, BLUE, r)
    pygame.display.flip()

    running = True

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    bg = original_bg.copy()
                    screen.blit(bg, (0, 0))
                    pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    x_shift = pos[0] - r.x
                    y_shift = pos[1] - r.y
                    r.move_ip(x_shift, y_shift)
                    object_location = [r.topleft, r.bottomright]
                    pygame.draw.rect(bg, BLUE, r)
                    pygame.display.flip()
                elif event.button == 3:
                    w = r.width
                    r.width = r.height
                    r.height = w
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                x_shift = pos[0] - r.x
                y_shift = pos[1] - r.y
                r.move_ip(x_shift, y_shift)
                screen.blit(bg, (0, 0))
                pygame.draw.rect(screen, BLUE, r)
                pygame.display.flip()
    return object_location


def mark_region(caption):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))

    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    upper_left, bottom_right = None, None
    bg = pygame.image.load(PARKING_MAP).convert()
    screen.blit(bg, (0, 0))
    pygame.display.flip()
    running = True
    pressing = False    

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                upper_left = event.pos
                pressing = True
            elif pygame.mouse.get_pressed() == (1, 0, 0) and upper_left is not None:
                bottom_right = event.pos
                # draw intermidiate rectangle
                screen.blit(bg, (0, 0))
                w, l = get_dimension((upper_left, bottom_right))
                pygame.draw.rect(screen, BLUE, pygame.Rect(upper_left[0], upper_left[1], w, l))
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONUP and pressing:
                bottom_right = event.pos

                # draw final rectangle
                screen.blit(bg, (0, 0))
                w, l = get_dimension((upper_left, bottom_right))
                pygame.draw.rect(screen, BLUE, pygame.Rect(upper_left[0], upper_left[1], w, l))
                pygame.display.flip()

                pressing = False            

    pygame.quit()
    if upper_left is None or bottom_right is None:
        return None
    return [upper_left, bottom_right]    


def mark_regions(caption):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))

    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    coords = []
    upper_left, bottom_right = None, None
    original_bg = pygame.image.load(PARKING_MAP).convert()
    bg = original_bg.copy()
    screen.blit(bg, (0, 0))
    pygame.display.flip()
    running = True
    pressing = False

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(coords) > 0:
                        coords.pop()
                        bg = original_bg.copy()
                        screen.blit(bg, (0, 0))
                        [pygame.draw.rect(bg, BLUE, pygame.Rect(object[0], get_dimension(object))) for object in coords]
                        pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                upper_left = event.pos
                pressing = True
            elif event.type == pygame.MOUSEBUTTONUP and pressing:
                bottom_right = event.pos
                coords.append([upper_left, bottom_right])
                # draw final rectangle
                screen.blit(bg, (0, 0))
                w, l = get_dimension((upper_left, bottom_right))
                pygame.draw.rect(bg, BLUE, pygame.Rect(upper_left, (w, l)))
                # pygame.display.flip()
                pressing = False    
            if pygame.mouse.get_pressed() == (1, 0, 0) and upper_left is not None:
                bottom_right = event.pos
                # draw intermidiate rectangle
                screen.blit(bg, (0, 0))
                w, l = get_dimension((upper_left, bottom_right))
                pygame.draw.rect(screen, BLUE, pygame.Rect(upper_left[0], upper_left[1], w, l))
                pygame.display.flip()
            
            
    pygame.quit()
    return coords


def fit_figure_inside(domain_coords, figure_coords):
        d_ul, d_br = list(domain_coords[0]), list(domain_coords[1])
        f_ul, f_br = list(figure_coords[0]), list(figure_coords[1])

        if f_ul[0] < d_ul[0]:
            f_ul[0] = d_ul[0]
        if d_br[0] < f_ul[0]:
            return None

        if f_ul[1] < d_ul[1]:
            f_ul[1] = d_ul[1]
        if d_br[1] < f_ul[1]:
            return None
        
        if d_br[0] < f_br[0]:
            f_br[0] = d_br[0]
        if f_br[0] < d_ul[0]:
            return None

        if d_br[1] < f_br[1]:
            f_br[1] = d_br[1]
        if f_br[1] < d_ul[1]:
            return None
        
        return [tuple(f_ul), tuple(f_br)]

          
def fit_figures_inside(domain_coords, figures_coords):
    fitted_figures = []
    for figure in figures_coords:
        fitted_f = fit_figure_inside(domain_coords, figure)
        if fitted_f is not None:
            fitted_figures.append(fitted_f)

    return fitted_figures


def shift_point(coordinate, x_shift, y_shift):
    """returns new coordinates of the given point (x0, y0):  (x0 - x_shift, y0 - y_shift)"""
    return (coordinate[0] - x_shift, coordinate[1] - y_shift)


def shift_coordinate(coodinates, x_shift, y_shift):
    """returns: [(upper_left - (x_shift, y_shift), bottom_right - (x_shift, y_shift))]"""
    return [shift_point(point, x_shift, y_shift) for point in coodinates]
    

def shift_coordinates_array(coordinates_array, x_shift, y_shift):
    return [shift_coordinate(coord, x_shift, y_shift) for coord in coordinates_array]


def set_up_parking():
    # -------- Setting parking object ---------   
    # step 1: define parking size
    parking_location = mark_region("Define parking:")
    if parking_location is None:
        print("Defining of parking failed.")
        return None
    parking_dimension = get_dimension(parking_location)
    
    # step 1.2: define shift coordiantes(x_shift, y_shift)
    x_shift, y_shift = parking_location[0]

    # step 2: define parking slot size
    slot_location = mark_region("Define slot size:")
    if slot_location is None:
        print("Failed to set slot size.")
        return None
    slot_location = fit_figure_inside(parking_location, slot_location)
    if slot_location is None:
        print("Failed to set slot size.")
        return None
    slot_dimnension = get_dimension(slot_location)

    # step 3: define default starting vehicle position
    # starting_vehicle_position = define_object(slot_dimnension, "Define vehicle starting position:")
    # if starting_vehicle_position is None:
    #     print("Failed to set up starting vehicle position.")
    #     return None 
    # starting_vehicle_position = shift_coordinate(starting_vehicle_position, x_shift, y_shift)

    # step 4: place slots location
    slots_locations = define_objects(slot_dimnension, "Define slots locations:")
    slots_locations = fit_figures_inside(parking_location, slots_locations)
    if slots_locations == []:
        print("Failed to set parking slots locations.")
        return None
    slots_locations = shift_coordinates_array(slots_locations, x_shift, y_shift)

    # step 5: define entrance location
    v_entrance_location = mark_region("Define entrance (for vehicles):")
    v_entrance_location = fit_figure_inside(parking_location, v_entrance_location)
    if v_entrance_location is None:
        print("Failed to set vehicles entrance location.")
        return None
    v_entrance_location = shift_coordinate(v_entrance_location, x_shift, y_shift)

    # step 6: define exit location
    v_exit_location = mark_region("Define exit (for vehicles):")
    v_exit_location = fit_figure_inside(parking_location, v_exit_location)
    if v_exit_location is None:
        print("Failed to set vehicles exit location.")
        return None
    v_exit_location = shift_coordinate(v_exit_location, x_shift, y_shift)

    # step 7: define pedestrian exits
    p_exits_locations = mark_regions("Define pedestrian exits locations:")
    p_exits_locations = fit_figures_inside(parking_location, p_exits_locations)
    if p_exits_locations == []:
        print("Failed to set pedestrians exit locations.")
        return None
    p_exits_locations = shift_coordinates_array(p_exits_locations, x_shift, y_shift) 

    # step 8: define walls and other obstacles
    walls_locations = mark_regions("Define walls(obstacles) locations:")
    walls_locations = fit_figures_inside(parking_location, walls_locations)
    walls_locations = shift_coordinates_array(walls_locations, x_shift, y_shift)

    # step 9: define road directions
    arrow_up_char = '\u2191'
    arrow_down_char = '\u2193'
    west_movement_areas = mark_regions("<- To west <-")
    west_movement_areas = fit_figures_inside(parking_location, west_movement_areas)
    east_movement_areas = mark_regions("-> To east ->")
    east_movement_areas = fit_figures_inside(parking_location, east_movement_areas)
    north_movement_areas = mark_regions(f"{arrow_up_char} To north {arrow_up_char}")
    north_movement_areas = fit_figures_inside(parking_location, north_movement_areas)
    south_movement_areas = mark_regions(f"{arrow_down_char} To south {arrow_down_char}")
    south_movement_areas = fit_figures_inside(parking_location, south_movement_areas)
    if east_movement_areas == [] or west_movement_areas == [] or north_movement_areas == [] or south_movement_areas == []:
        print("Failed to set up movements areas.")
    east_movement_areas = shift_coordinates_array(east_movement_areas, x_shift, y_shift)
    west_movement_areas = shift_coordinates_array(west_movement_areas, x_shift, y_shift)
    north_movement_areas = shift_coordinates_array(north_movement_areas, x_shift, y_shift)
    south_movement_areas = shift_coordinates_array(south_movement_areas, x_shift, y_shift)
   
    parking = pf.Parking(parking_dimension,
                         slots_locations,
                         v_entrance_location,
                         v_exit_location,
                         p_exits_locations,
                         walls_locations,
                         west_movement_areas,
                         east_movement_areas,
                         north_movement_areas,
                         south_movement_areas)
    
    parking_data = [parking_dimension,
                    slots_locations,
                    v_entrance_location,
                    v_exit_location,
                    p_exits_locations,
                    walls_locations,
                    west_movement_areas,
                    east_movement_areas,
                    north_movement_areas,
                    south_movement_areas]

    for data, path in list(zip(parking_data, PATHS)):
        with open(path, 'wb') as f:
            pickle.dump(data, f)
    
    return parking
    
    # step: save configured data

    # step 10: initialize parking object with gathered arguments
    # parking = Parking(parking_dimension,
    #                   starting_vehicle_position,
    #                   slots_locations,
    #                   v_entrance_location,
    #                   v_exit_location,
    #                   p_exits_locations,
    #                   walls_locations,
    #                   west_movement_areas,
    #                   east_movement_areas,
    #                   north_movement_areas,
    #                   south_movement_areas)
    # return parking
    # step 9.1: create binary occupancy map

    # step 9.2: create directions map

    # step 9.3: set all slots to be free

    # step 9.4: calculate default (supposing starting vehicle position is at entrance) 
    # optimality coefficients and paths to each parking slot

    # step 10: save parking object


if __name__ == "__main__":
    # parking = set_up_parking()

    with open('parking.dat', 'wb') as f:
        parking = pickle.load(f)
    

    # with open ('parking.dat', 'wb') as f:
    #     pickle.dump(parking, f)
    # configurational_data = []
    # for path in PATHS:
    #     with open(path, 'rb') as f:
    #         configurational_data.append(pickle.load(f))
  
    # parking = pf.Parking(
    #                   configurational_data[0],
    #                   configurational_data[1],
    #                   configurational_data[2],
    #                   configurational_data[3],
    #                   configurational_data[4],
    #                   configurational_data[5],
    #                   configurational_data[6],
    #                   configurational_data[7],
    #                   configurational_data[8],
    #                   configurational_data[9],
    #                   configurational_data[10])

    
    # free_slots = parking.get_free_slots()
    # x_shift, y_shift = -parking.WIDTH, -parking.LENGTH

    # entrance_width, entrance_length = get_dimension(parking.car_entrance.coordinates)
    # entrance_ul = parking.car_entrance.coordinates[0]
    # start_pos = (entrance_ul[0] + round(entrance_width/2), entrance_ul[1] + round(entrance_length/2))

    # path_and_cost = parking.get_trajectory(start_pos, free_slots[0].coordinates)

    # if path_and_cost is not None:
    #     path = [shift_coordinates_array(path_and_cost[0], x_shift, y_shift)]
    #     with Image.open(PARKING_MAP) as im:
    #         drawer = ImageDraw.Draw(im)
    #         for p in path:
    #             drawer.point(p, fill=BLUE)
    #         im.show()
    
    
    
    
    # with open('parking.bat', 'wb') as f:
    #     pickle.dump(parking, f)
        
    # dimension = configurational_data[0]

    # south_area = configurational_data[-1]
    # north_area = configurational_data[-2]
    # east_area = configurational_data[-3]
    # west_area = configurational_data[-4]

    # def within_parking(coords):
    #     return coords[1][0] < dimension[0] and coords[1][1] < dimension[1]

    # print("south:")
    # for s in south_area:
    #     if not within_parking(s):
    #         print(f"Failed. coordinates: {s}, parking actual size: {dimension}")
    # print("north:")
    # for n in north_area:
    #     if not within_parking(n):
    #         print(f"Failed. coordinates: {n}, parking actual size: {dimension}")
    # print("west:")
    # for w in west_area:
    #     if not within_parking(w):
    #         print(f"Failed. coordinates: {w}, parking actual size: {dimension}")
    # print("east:")
    # for e in east_area:
    #     if not within_parking(n):
    #         print(f"Failed. coordinates: {e}, parking actual size: {dimension}")
    

    #                   parking_dimension,
    #                   starting_vehicle_position,
    #                   slots_locations,
    #                   v_entrance_location,
    #                   v_exit_location,
    #                   p_exits_locations,
    #                   walls_locations,
    #                   west_movement_areas,
    #                   east_movement_areas,
    #                   north_movement_areas,
    #                   south_movement_areas)
    # im = Image.new('RGB', configurational_data[0], (255, 255, 255))
    # d = ImageDraw.Draw(im)

    # bi_g = parking.get_bi_grid()

    # for y in range(len(bi_g)):
    #     for x in range(len(bi_g[y])):
    #         if bi_g[y][x] == 1:
    #             d.point((y, x), fill=(0, 0, 0))
    
    # im.show()

    # im = Image.new('RGB', configurational_data[0], (255, 255, 255))
    # d = ImageDraw.Draw(im)

        
