TITLE = "MaturaArbeit"
GAME_WIDTH = 1200
GAME_HEIGHT = 675
WIDTH = GAME_WIDTH
HEIGHT = GAME_HEIGHT
LETTERBOX_COLOR = (0, 0, 0)
import pygame
from pygame import Rect
import time
import Quiz
from Panorama import Hotspot, PanoramaView, find_hotspot_at_point, draw_hotspot_overlay

pygame.mouse.set_visible(False)
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

#Variabeln
game_started = False
move = True
speed = 5
room_index = 0
mouse_move_pos = (0, 0)
mouse_klick_pos = (0, 0)
item_high_pos = None
item_large_pos = None
hovered_hotspot = None
show_hotspot_debug = False
timer_duration = 60 * 60
timer_start = None
quiz_item_index = 1
sekunden = ""
minuten = ""
stunden = ""
door_locked_text = False

#Item Actors
q_pacman = Actor("pacman", (855, 312)) #r = Rätsel
q_room1_item1 = Actor("room1_item1", (923,315))

#Listen
room = [
    "room1",
    "background"
    ]
doors = [Actor("room1_door1", (1313,274))
    ]
doors_room = [
    0 #room1_door1 im Raum 0
    ]
door_keys = [
    "room1_item1" #room1_door1 braucht roomkey1
    ]
items = [
    q_pacman,
    q_room1_item1
    ]
items_room = [
    0, #q_pacamn im Raum 0
    0 #q_room1_item1 im Raum 0
    ]
items_high = [
    Actor("pacman_leuchtend"),
    Actor("room1_high1")
    ]
items_large = [
    Actor("pacman_gross", (600, 337.5)),
    Actor("room1_big1", (600, 337.5))
    ]
quiz_items = {
    1: "room1_item1"
    }

#Actors
room_actor = Actor(room[room_index])
magnifier = Actor("magnifier")
invis_magnifier = Actor("magnifier2")

panorama_view = PanoramaView(room_actor, speed)

hotspots = [
    # Adjust these polygon points manually to match the objects painted into
    # the panorama. The points are panorama coordinates, not screen coordinates;
    # PanoramaView.project_polygon() bends them into the current screen view.
    Hotspot(
        points=[
            (855, 312),
            (888, 312),
            (888, 337),
            (855, 337)
        ],
        room_index=items_room[0],
        hotspot_type="item",
        reference_index=0
    ),
    Hotspot(
        points=[
            (923, 315),
            (944, 315),
            (944, 337),
            (923, 337)
        ],
        room_index=items_room[1],
        hotspot_type="item",
        reference_index=1
    ),
    Hotspot(
        points=[
            (1313, 274),
            (1370, 274),
            (1370, 430),
            (1313, 430)
        ],
        room_index=doors_room[0],
        hotspot_type="door",
        reference_index=0
    )
]

def draw_large_item(screen, item_index):
    large_item = items_large[item_index]
    top_left = (
        int(large_item.x - large_item.width / 2),
        int(large_item.y - large_item.height / 2)
    )
    screen.blit(large_item.image, top_left)

#Programm
def update():
    print(magnifier.pos)
    global game_started, item_large_pos, item_high_pos, move, mouse_klick_pos, mouse_move_pos, speed, room_index, door_locked_text, hovered_hotspot

    if game_started:
        quiz_offen = Quiz.quiz_is_open()
        if keyboard.A and move and not quiz_offen:
            speed = speed * 1.005
            panorama_view.speed = speed
            panorama_view.move_left()
            if speed > 10:
                speed = 10
        elif keyboard.D and move and not quiz_offen:
            panorama_view.speed = speed
            panorama_view.move_right()
            speed = speed * 1.005
            if speed > 10:
                speed = 10
        else:
            speed = 5

        panorama_view.offset %= room_actor.width #ChatGPT hat mir die Formel %= gegeben
        magnifier.pos = mouse_move_pos
        invis_magnifier.pos = mouse_klick_pos
        item_high_pos = None
        hovered_hotspot = None
        if mouse_klick_pos != (0, 0):
            door_locked_text = False

        if move and not quiz_offen:
            hovered_hotspot = find_hotspot_at_point(magnifier.pos, room_index, hotspots, panorama_view, GAME_WIDTH)
            if hovered_hotspot is not None and hovered_hotspot.hotspot_type == "item":
                item_high_pos = hovered_hotspot.reference_index

            door_clicked = False
            clicked_door_hotspot = None
            if mouse_klick_pos != (0, 0):
                clicked_door_hotspot = find_hotspot_at_point(invis_magnifier.pos, room_index, hotspots, panorama_view, GAME_WIDTH, "door")
            if clicked_door_hotspot is not None:
                i = clicked_door_hotspot.reference_index
                if doors_room[i] == room_index:
                    door_clicked = True
                    if Quiz.quiz_is_solved(door_keys[i]):
                        room_index = room_index + 1
                        room_actor.image = room[room_index]
                        item_large_pos = None
                    else:
                        door_locked_text = True
            if not door_clicked:
                clicked_item_hotspot = None
                if mouse_klick_pos != (0, 0):
                    clicked_item_hotspot = find_hotspot_at_point(invis_magnifier.pos, room_index, hotspots, panorama_view, GAME_WIDTH, "item")
                if clicked_item_hotspot is not None:
                    i = clicked_item_hotspot.reference_index
                    if items_room[i] == room_index:
                        if i in quiz_items and not Quiz.quiz_is_solved(quiz_items[i]):
                            Quiz.open_quiz(quiz_items[i])
                            item_large_pos = None
                        else:
                            item_large_pos = i

        mouse_klick_pos = (0, 0)
        if Quiz.quiz_is_open():
            move = False
        elif item_large_pos != None:
            move = False
        elif item_large_pos == None:
            move = True
    if keyboard.ESCAPE:
        if Quiz.quiz_is_open():
            Quiz.close_quiz()
        else:
            item_large_pos = None

def on_mouse_move(pos):
    global mouse_move_pos

    mouse_move_pos = window_pos_to_game_pos(pos)

def on_mouse_down(pos):
    global mouse_klick_pos

    if not Quiz.quiz_is_open():
        mouse_klick_pos = window_pos_to_game_pos(pos)

def quiz_taste_von_key(key):
    if key == pygame.K_1 or key == pygame.K_KP1:
        return "1"
    if key == pygame.K_2 or key == pygame.K_KP2:
        return "2"
    if key == pygame.K_3 or key == pygame.K_KP3:
        return "3"
    if key == pygame.K_ESCAPE:
        return "escape"
    return None

def on_key_down(key):
    global game_started, room_index, room, timer_start

    if Quiz.quiz_is_open():
        quiz_taste = quiz_taste_von_key(key)
        if quiz_taste is not None:
            Quiz.press_key(quiz_taste)
        return
    if not game_started and keyboard.s:
        game_started = True
        timer_start = time.time()
    if game_started:
        if keyboard.P:
            room_index = room_index + 1
            room_actor.image = room[room_index]

def standard_box(x, y, width, height):
    box = Rect(x, y, width, height)
    box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    box_surface.fill((150,150,150,170))
    screen.surface.blit(box_surface, (x, y))

    pygame.draw.rect(
        screen.surface,
        (120, 120, 120),
        box,
        width=2
    )
    return box

def set_screen_surface(target_surface):
    screen.surface = target_surface
    if hasattr(screen, "draw"):
        for surface_attribute in ["surface", "_surface", "_surf", "surf"]:
            if hasattr(screen.draw, surface_attribute):
                try:
                    setattr(screen.draw, surface_attribute, target_surface)
                except AttributeError:
                    pass

def get_game_scale(target_surface):
    window_width = target_surface.get_width()
    window_height = target_surface.get_height()

    # Use the smaller scale so the whole 16:9 game image fits into the
    # current window. This keeps the game proportional instead of stretching it.
    scale_factor = min(window_width / GAME_WIDTH, window_height / GAME_HEIGHT)
    scaled_width = int(GAME_WIDTH * scale_factor)
    scaled_height = int(GAME_HEIGHT * scale_factor)

    # Center the scaled game image. If the window is not 16:9, the unused
    # space remains black and becomes the letterbox/pillarbox border.
    draw_offset_x = (window_width - scaled_width) // 2
    draw_offset_y = (window_height - scaled_height) // 2
    return scale_factor, scaled_width, scaled_height, draw_offset_x, draw_offset_y

def window_pos_to_game_pos(pos):
    scale_factor, scaled_width, scaled_height, draw_offset_x, draw_offset_y = get_game_scale(screen.surface)
    x, y = pos
    game_x = (x - draw_offset_x) / scale_factor
    game_y = (y - draw_offset_y) / scale_factor
    return game_x, game_y

def draw_scaled_game_surface(target_surface):
    scale_factor, scaled_width, scaled_height, draw_offset_x, draw_offset_y = get_game_scale(target_surface)

    target_surface.fill(LETTERBOX_COLOR)
    scaled_surface = pygame.transform.smoothscale(game_surface, (scaled_width, scaled_height))
    target_surface.blit(scaled_surface, (draw_offset_x, draw_offset_y))

def draw_game():
    if not game_started:
        screen.blit("start", (0, 0))
    else:
        screen.clear()
        panorama_view.draw(screen)
        draw_hotspot_overlay(screen, room_index, hovered_hotspot, show_hotspot_debug, hotspots, panorama_view)
        if item_large_pos is not None:
            draw_large_item(screen, item_large_pos)
            if item_large_pos in quiz_items and Quiz.quiz_is_solved(quiz_items[item_large_pos]):
                screen.draw.text("Raetsel geloest", center=(600, 590), fontsize=40, color="yellow")
        if not move:
            screen.draw.text("Um fortzufahren, druecken sie ESC", center=(600, 80), fontsize=40, color="white")
        if door_locked_text:
            screen.draw.text("Tuere ist verschlossen", center=(600, 540), fontsize=40, color="white")

        #Timer erstellt mit ChatGPT
        if timer_start is not None:
            verbleibend = max(0, timer_duration - int(time.time() - timer_start))
        else:
            verbleibend = timer_duration
        stunden = verbleibend // 3600
        minuten = (verbleibend % 3600) // 60
        sekunden = verbleibend % 60
        timer_text = f"{stunden:02}:{minuten:02}:{sekunden:02}"
        standard_box(10, 12, 275, 55)
        screen.draw.text(timer_text, topleft=(20, 20), fontsize=40, color="white", fontname="clock")

        #Hotbar
        standard_box(350, 600, 500, 55)
        if Quiz.quiz_is_solved("room1_item1"):
            screen.blit("roomkey1", (352.5, 602.5))
        Quiz.draw_quiz(screen, GAME_WIDTH, GAME_HEIGHT, Rect, standard_box)

def draw():
    window_surface = screen.surface
    game_surface.fill(LETTERBOX_COLOR)
    set_screen_surface(game_surface)
    try:
        draw_game()
    finally:
        set_screen_surface(window_surface)
    draw_scaled_game_surface(window_surface)
    magnifier.draw()
