from parking_facilities import Parking
from PIL import Image, ImageDraw
import pygame
from image_resizing import resize_image

MAP_PATH = "parking_plan.jpg"
BLUE = (66, 135, 245)
SCREEN_LENGTH = 800
resize_image(MAP_PATH, SCREEN_LENGTH, MAP_PATH)
with Image.open(MAP_PATH) as im:
    SCREEN_WIDTH = im.size[0]


def get_dimension(ul, br):
    return abs(ul[0] - br[0]), abs(ul[1] - br[1])


def define_objects(object_width, object_length, caption):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()

    bg = pygame.image.load(MAP_PATH).convert()
    r = pygame.Rect(0, 0, object_width, object_length)
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
    return upper_left, bottom_right    


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


def main():
    # -------- Setting parking object ---------   
    # step 1: define parking size
    parking_ul, parking_br = mark_region("Define parking size:")
    if parking_ul is None or parking_br is None:
        print("Defining parking size failed.")
        return None
    parking_width, parking_length = get_dimension(parking_ul, parking_br)

    # step 2: define parking slot size
    slot_ul, slot_br = mark_region("Define slot size:")
    if slot_ul or slot_br is None:
        print("Defining slot size failed.")
        return None
    slot_width, slot_length = get_dimension(slot_ul, slot_br)

    # step 3: place slots location
    slots_locations = define_objects(slot_width, slot_length, "Define slots locations:")

    # step 4: define entrance location
    v_entrance_location = mark_region("Define entrance (for vehicles):")

    # step 5: define exit location
    v_exit_location = mark_region("Define exit (for vehicles):")

    # step 6: define pedestrian exits
    p_exits_locations = mark_regions("Define pedestrian exits locations:")

    # step 7: define walls and other obstacles
    walls_locations = mark_regions("Define walls(obstacles) locations:")

    # step 8: define road directions
    arrow_up_char = '\u2191'
    arrow_down_char = '\u2193'
    # to right
    right_movement = mark_regions("<- To left <-")
    left_movement = mark_regions("-> To right ->")
    up_movement = mark_regions(f"{arrow_up_char} Up {arrow_up_char}")
    down_movement = mark_regions(f"{arrow_down_char} Down {arrow_down_char}")
    
    # step 9: initialize parking object with gathered arguments
    parking = Parking((parking_width, parking_length),
                      (slot_width, slot_length),
                      slots_locations,
                      v_entrance_location,
                      v_exit_location,
                      p_exits_locations,
                      walls_locations,
                      left_movement,
                      right_movement,
                      up_movement,
                      down_movement)

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
    c = define_objects(15, 30, "Define regions")
    [print(coord) for coord in c]
    # main()