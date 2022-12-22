from parking_facilities import Parking
from PIL import Image, ImageDraw
import pygame
from image_resizing import resize_image

ORIGINAL_MAP = "parking_plan_original.jpg"
MAP_PATH = "parking_plan_fitted.jpg"
BLUE = (66, 135, 245)
SCREEN_LENGTH = 800
# resize_image(ORIGINAL_MAP, SCREEN_LENGTH, MAP_PATH)
# with Image.open(MAP_PATH) as im:
#     SCREEN_WIDTH = im.size[0]
SCREEN_WIDTH = 1131

def get_dimension(ul, br):
    return (abs(ul[0] - br[0]), abs(ul[1] - br[1]))


def define_objects(object_dimension, caption):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    bg = pygame.image.load(MAP_PATH).convert()
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    objects_locations.append([(pos[0], pos[1]), (pos[0] + r.width, pos[1] + r.height)])
                    pygame.draw.rect(bg, BLUE, r)
                    pygame.display.flip()
                elif event.button == 3:
                    w = r.width
                    r.width = r.height
                    r.height = w
            if event.type == pygame.MOUSEMOTION:
                r.topleft = pygame.mouse.get_pos()
                screen.blit(bg, (0, 0))
                pygame.draw.rect(screen, BLUE, r)
                pygame.display.flip()
    
    pygame.quit()
    return objects_locations

# look again
def place_car(car_width, car_length):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))
    pygame.display.set_caption("Place car at initial position")
    clock = pygame.time.Clock()

    bg = pygame.image.load(MAP_PATH).convert()
    r = pygame.Rect(0, 0, car_width, car_length)

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    r.topleft = pos
                    running = False

                    screen.blit(bg, (0, 0))
                    pygame.draw.rect(screen, BLUE, r)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    break
                elif event.button == 3:
                    w = r.width
                    r.width = r.height
                    r.height = w
        if running:
            r.topleft = pygame.mouse.get_pos()
            screen.blit(bg, (0, 0))
            pygame.draw.rect(screen, BLUE, r)
            pygame.display.flip()
    return [r.topleft, r.bottomright]


def mark_region(caption):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))

    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    upper_left, bottom_right = None, None
    bg = pygame.image.load(MAP_PATH).convert()
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
            elif pygame.mouse.get_pressed() == (1, 0, 0):
                bottom_right = event.pos
                # draw intermidiate rectangle
                screen.blit(bg, (0, 0))
                w, l = get_dimension(upper_left, bottom_right)
                pygame.draw.rect(screen, BLUE, pygame.Rect(upper_left[0], upper_left[1], w, l))
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONUP and pressing:
                bottom_right = event.pos

                # draw final rectangle
                screen.blit(bg, (0, 0))
                w, l = get_dimension(upper_left, bottom_right)
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
    bg = pygame.image.load(MAP_PATH).convert()
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
            elif pygame.mouse.get_pressed() == (1, 0, 0):
                bottom_right = event.pos
                # draw intermidiate rectangle
                screen.blit(bg, (0, 0))
                w, l = get_dimension(upper_left, bottom_right)
                pygame.draw.rect(screen, BLUE, pygame.Rect(upper_left[0], upper_left[1], w, l))
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONUP and pressing:
                bottom_right = event.pos
                coords.append([upper_left, bottom_right])
                # draw final rectangle
                screen.blit(bg, (0, 0))
                w, l = get_dimension(upper_left, bottom_right)
                pygame.draw.rect(bg, BLUE, pygame.Rect(upper_left[0], upper_left[1], w, l))
                # pygame.display.flip()

                pressing = False
    pygame.quit()
    return coords


def fit_figure_inside(domain_coords, figure_coords):
        d_ul, d_br = domain_coords
        f_ul, f_br = figure_coords

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
        
        return [f_ul, f_br]

          
def fit_figures_inside(domain_coords, figures_coords):
    fitted_figures = []
    for figure in figures_coords:
        fitted_f = fit_figure_inside(domain_coords, figure)
        if fitted_f is not None:
            fitted_figures.append(fitted_f)

    return fitted_figures


def main():
    # -------- Setting parking object ---------   
    # step 1: define parking size
    parking_location = mark_region("Define parking size:")
    if parking_location is None:
        print("Defining parking size failed.")
        return None
   
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

    # step 3: place slots location
    slots_locations = define_objects(slot_dimnension, "Define slots locations:")
    slots_locations = fit_figures_inside(parking_location, slots_locations)
    if slots_locations == []:
        print("Failed to set parking slots locations.")
        return None

    # step 4: define entrance location
    v_entrance_location = mark_region("Define entrance (for vehicles):")
    v_entrance_location = fit_figure_inside(parking_location, v_entrance_location)
    if v_entrance_location is None:
        print("Failed to set vehicles entrance location.")
        return None

    # step 5: define exit location
    v_exit_location = mark_region("Define exit (for vehicles):")
    v_exit_location = fit_figure_inside(parking_location, v_exit_location)
    if v_exit_location is None:
        print("Failed to set vehicles exit location.")
        return None

    # step 6: define pedestrian exits
    p_exits_locations = mark_regions("Define pedestrian exits locations:")
    p_exits_locations = fit_figures_inside(parking_location, p_exits_locations)
    if p_exits_locations == []:
        print("Failed to set pedestrians exit locations.")
        return None

    # step 7: define walls and other obstacles
    walls_locations = mark_regions("Define walls(obstacles) locations:")
    walls_locations = fit_figures_inside(parking_location, walls_locations)

    # step 8: define road directions
    arrow_up_char = '\u2191'
    arrow_down_char = '\u2193'
    right_movement_areas = mark_regions("<- To right <-")
    right_movement_areas = fit_figures_inside(parking_location, right_movement_areas)
    left_movement_areas = mark_regions("-> To left ->")
    left_movement_areas = fit_figures_inside(parking_location, left_movement_areas)
    up_movement_areas = mark_regions(f"{arrow_up_char} Up {arrow_up_char}")
    up_movement_areas = fit_figures_inside(parking_location, up_movement_areas)
    down_movement_areas = mark_regions(f"{arrow_down_char} Down {arrow_down_char}")
    down_movement_areas = fit_figures_inside(parking_location, down_movement_areas)
    if right_movement_areas == [] or left_movement_areas == [] or up_movement_areas == [] or down_movement_areas == []:
        print("Failed to set up movements areas.")
    
    # step 9: initialize parking object with gathered arguments
    parking = Parking(parking_location,
                      slot_dimnension,
                      slots_locations,
                      v_entrance_location,
                      v_exit_location,
                      p_exits_locations,
                      walls_locations,
                      left_movement_areas,
                      right_movement_areas,
                      up_movement_areas,
                      down_movement_areas)

    # step 9.1: create binary occupancy map

    # step 9.2: create directions map

    # step 9.3: set all slots to be free

    # step 9.4: calculate default (supposing starting vehicle position is at entrance) 
    # optimality coefficients and paths to each parking slot

    # step 10: save parking object



# test: put car at initial position
# initial_pos = place_car(10, 30)

# with Image.open(MAP_PATH) as im:
#     drawer = ImageDraw.Draw(im)
#     drawer.point(initial_pos[0], fill=BLUE)
#     im.show()



# directions_map = parking.directions_map

# # Left
# canvas1 = Image.new('RGB', (parking.parking_width, parking.parking_length))
# drawer1 = ImageDraw.Draw(canvas1)
# for row in range(len(directions_map)):
#     for col in range(len(row)):
#         if 'Left' in directions_map[row][col]:
#             drawer1.point(col, row, fill = BLUE)
# canvas1.save('Left.png')
# # Right
# canvas2 = Image.new('RGB', (parking.parking_width, parking.parking_length))
# drawer2 = ImageDraw.Draw(canvas2)
# for row in range(len(directions_map)):
#     for col in range(len(row)):
#         if 'Right' in directions_map[row][col]:
#             drawer2.point(col, row, fill = BLUE)
# canvas2.save('Right.png')
# # Up
# canvas3 = Image.new('RGB', (parking.parking_width, parking.parking_length))
# drawer3 = ImageDraw.Draw(canvas3)
# for row in range(len(directions_map)):
#     for col in range(len(row)):
#         if 'Up' in directions_map[row][col]:
#             drawer3.point(col, row, fill = BLUE)
# canvas3.save('Up.png')
# # Down
# canvas4 = Image.new('RGB', (parking.parking_width, parking.parking_length))
# drawer4 = ImageDraw.Draw(canvas4)
# for row in range(len(directions_map)):
#     for col in range(len(row)):
#         if 'Down' in directions_map[row][col]:
#             drawer4.point(col, row, fill = BLUE)
# canvas4.save('Down.png')


if __name__ == "__main__":
    main()