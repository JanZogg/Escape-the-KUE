TITLE = "MaturaArbeit"
GAME_WIDTH = 1200
GAME_HEIGHT = 675
from pygame import Rect
import pygame
import time
import Quiz
from Panorama import Hotspot, PanoramaView, find_hotspot_at_point, draw_hotspot_overlay
pygame.mouse.set_visible(False)

#Variabeln
WIDTH = GAME_WIDTH
HEIGHT = GAME_HEIGHT
game_started = False
move = True
speed = 4
room_index = 0
mouse_move_pos = (0, 0)
mouse_klick_pos = (0, 0)
item_large_pos = None
current_item_quiz = None
hovered_hotspot = None
show_hotspot_debug = False
timer_duration = 60 * 60
timer_start = None
quiz_item_index = 1
door_locked_text = False
current_song = None
mute = False

#Item Actors
q_pacman = Actor("pacman", (855, 312)) #q = Rätsel
q_room1_item1 = Actor("room1_item1", (923,315))
q_room2_item1 = Actor("room2_item1", (1000, 500))

#Listen
room = [
    "room1",
    "room2"
    ]
doors_room = [
    0 #Türe im Raum 0
    ]
door_keys = [
    "room1_item1", #room1_door1 braucht roomkey1
    "room2_item1"
    ]
items = [
    q_pacman,
    q_room1_item1,
    q_room2_item1
    ]
items_room = [
    0, #q_pacman im Raum 0
    0, #q_room1_item1 im Raum 0
    1 #q_room2_item1 im Raum 1
    ]
items_large = [
    Actor("pacman_gross", (600, 337.5)),
    Actor("room1_big1", (600, 337.5)),
    Actor("room2_big1", (600, 337.5))
    ]
quiz_items = {
    1: "room1_item1",
    2: "room2_item1"
    }

#Actors
room_actor = Actor(room[room_index])
magnifier = Actor("magnifier")
invis_magnifier = Actor("magnifier2")
speaker = Actor("speaker", (1165, 36))
muted_speaker = Actor("speaker_mute", (1165, 36))
start_button = Actor("start_button", (600, 500))
quiz_button = Actor("quiz_button", (GAME_WIDTH / 2, 570))
panorama_view = PanoramaView(room_actor, speed)

hotspots = [
    # Die Punkte sind Panorama-Koordinaten, nicht die vom Screen
    Hotspot(
        points=[
            (862, 313),
            (886, 313),
            (886, 338),
            (862, 338)
        ],
        room_index=items_room[0], # q_pacman
        hotspot_type="item",
        reference_index=0
    ),
    Hotspot(
        points=[
            (920, 315),
            (944, 315),
            (944, 340),
            (920, 340)
        ],
        room_index=items_room[1], # q_room1_item1
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
    ),
    Hotspot(
        points=[
            (1157, 408),
            (1178, 408),
            (1178, 430),
            (1157, 430)
        ],
        room_index=items_room[2],
        hotspot_type="item",
        reference_index=2
    )
]

def draw_large_item(screen, item_index):
    large_item = items_large[item_index]
    top_left = (
        int(large_item.x - large_item.width / 2),
        int(large_item.y - large_item.height / 2)
    )
    screen.blit(large_item.image, top_left)

def quiz_button_is_visible():
    return (
        item_large_pos is not None
        and current_item_quiz is not None
        and not Quiz.quiz_is_solved(current_item_quiz)
        and not Quiz.quiz_is_open()
    )

def update():
    global game_started, item_large_pos, current_item_quiz, move, mouse_klick_pos, mouse_move_pos, speed, room_index, door_locked_text, hovered_hotspot, mute
    print(mute)

    panorama_view.offset %= room_actor._surf.get_width() #ChatGPT hat mir die Formel %= gegebenl, _surf formel von PyGame Zero
    invis_magnifier.pos = mouse_klick_pos
    hovered_hotspot = None
    magnifier.pos = mouse_move_pos

    if not game_started:
        if start_button.collidepoint(mouse_klick_pos):
            game_started = True
    if game_started and not Quiz.game_is_frozen:
        quiz_open = Quiz.quiz_is_open()
        if keyboard.A and move and not quiz_open:
            speed = speed * 1.005
            panorama_view.speed = speed
            panorama_view.move_left()
            if speed > 8:
                speed = 8
        elif keyboard.D and move and not quiz_open:
            panorama_view.speed = speed
            panorama_view.move_right()
            speed = speed * 1.005
            if speed > 8:
                speed = 8
        else:
            speed = 4

        if mouse_klick_pos != (0, 0):
            if speaker.collidepoint(mouse_klick_pos):
                mute = not mute
            door_locked_text = False
        if move and not quiz_open:
            hovered_hotspot = find_hotspot_at_point(magnifier.pos, room_index, hotspots, panorama_view, GAME_WIDTH)

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
                        panorama_view.offset = 0
                        room_actor.image = room[room_index]
                        item_large_pos = None
                        current_item_quiz = None
                    else:
                        door_locked_text = True
            if not door_clicked:
                clicked_item_hotspot = None
                if mouse_klick_pos != (0, 0):
                    clicked_item_hotspot = find_hotspot_at_point(invis_magnifier.pos, room_index, hotspots, panorama_view, GAME_WIDTH, "item")
                if clicked_item_hotspot is not None:
                    i = clicked_item_hotspot.reference_index
                    if items_room[i] == room_index:
                        item_large_pos = i
                        current_item_quiz = quiz_items.get(i)

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
            current_item_quiz = None

def on_mouse_move(pos):
    global mouse_move_pos

    mouse_move_pos = pos

def on_mouse_down(pos):
    global mouse_klick_pos, item_large_pos, current_item_quiz

    if Quiz.quiz_is_open():
        return
    if quiz_button_is_visible() and quiz_button.collidepoint(pos):
        if Quiz.open_quiz(current_item_quiz):
            item_large_pos = None
            current_item_quiz = None
        return
    mouse_klick_pos = pos

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
    global game_started, room_index, room, timer_start, mute, item_large_pos, current_item_quiz

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
            panorama_view.offset = 0
            room_actor.image = room[room_index]
            item_large_pos = None
            current_item_quiz = None
        if keyboard.M:
            mute = not mute

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

def draw_game():
    global current_song, mute

    screen.clear()
    panorama_view.draw(screen)
    draw_hotspot_overlay(screen, room_index, hovered_hotspot, show_hotspot_debug, hotspots, panorama_view)
    if item_large_pos is not None:
        draw_large_item(screen, item_large_pos)
        if item_large_pos in quiz_items and Quiz.quiz_is_solved(quiz_items[item_large_pos]):
            screen.draw.text("Raetsel geloest", center=(600, 590), fontsize=40, color="yellow")
        elif quiz_button_is_visible():
            quiz_button.draw()
    if not move:
        screen.draw.text("Zum schliessen, druecken sie ESC", center=(600, 80), fontsize=40, color="white")
    if door_locked_text:
        screen.draw.text("Tuere ist verschlossen", center=(600, 540), fontsize=40, color="white")

    #Timer erstellt mit ChatGPT
    if timer_start is not None:
        verbleibend = max(0, timer_duration - int(time.time() - timer_start))
    else:
        verbleibend = timer_duration
    hours = verbleibend // 3600
    minutes = (verbleibend % 3600) // 60
    seconds = verbleibend % 60
    timer_text = f"{hours:02}:{minutes:02}:{seconds:02}"
    standard_box(10, 12, 275, 55)
    screen.draw.text(timer_text, topleft=(20, 20), fontsize=40, color="white", fontname="clock")

    #Musik
    if game_started:
        standard_box (1140, 12, 55, 50)
        if mute:
            muted_speaker.draw()
            sounds.part1.set_volume(0)
            sounds.part2.set_volume(0)
            sounds.part3.set_volume(0)
        else:
            speaker.draw()
            sounds.part1.set_volume(1)
            sounds.part2.set_volume(1)
            sounds.part3.set_volume(1)
        if minutes < 20 and hours < 1:
            new_song = 3
        elif minutes < 40 and hours < 1:
            new_song = 2
        else:
            new_song = 1
        if new_song != current_song:
            sounds.part1.stop()
            sounds.part2.stop()
            sounds.part3.stop()
            if new_song == 1:
                sounds.part1.play(-1)
            elif new_song == 2:
                sounds.part2.play(-1)
            else:
                sounds.part3.play(-1)
            current_song = new_song

    #Hotbar
    standard_box(350, 600, 500, 55)
    if Quiz.quiz_is_solved("room1_item1"):
        screen.blit("room1_key1", (353, 603))
    if Quiz.quiz_is_solved("room2_item1"):
        screen.blit("room2_key1", (408, 603))
    Quiz.draw_quiz(screen, GAME_WIDTH, GAME_HEIGHT, Rect, standard_box)

def draw():
    if not game_started:
        screen.blit("start", (0, 0))
        start_button.draw()
    else:
        draw_game()
    magnifier.draw()
