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
speed = 5
room_index = 0
mouse_move_pos = (0, 0)
mouse_klick_pos = (0, 0)
item_large_pos = None
hovered_hotspot = None
show_hotspot_debug = False
timer_duration = 60 * 60
timer_start = None
quiz_item_index = 1
door_locked_text = False
current_song = None
mute = False

#Item Actors
q_pacman = Actor("pacman", (855, 312)) #r = Rätsel
q_room1_item1 = Actor("room1_item1", (923,315))

#Listen
room = [
    "room1",
    "background"
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
    0, #q_pacman im Raum 0
    0 #q_room1_item1 im Raum 0
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
speaker = Actor("speaker", (1145, 12))
muted_speaker = Actor("speaker_mute", (1145, 12))
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
    )
]

def draw_large_item(screen, item_index):
    large_item = items_large[item_index]
    top_left = (
        int(large_item.x - large_item.width / 2),
        int(large_item.y - large_item.height / 2)
    )
    screen.blit(large_item.image, top_left)

def update():
    global game_started, item_large_pos, move, mouse_klick_pos, mouse_move_pos, speed, room_index, door_locked_text, hovered_hotspot, mute
    print(mute)
    #print(speed)

    if game_started:
        quiz_offen = Quiz.quiz_is_open()
        if keyboard.A and move and not quiz_offen:
            speed = speed * 1.005
            panorama_view.speed = speed
            panorama_view.move_left()
            if speed > 8:
                speed = 8
        elif keyboard.D and move and not quiz_offen:
            panorama_view.speed = speed
            panorama_view.move_right()
            speed = speed * 1.005
            if speed > 8:
                speed = 8
        else:
            speed = 5

        panorama_view.offset %= room_actor._surf.get_width() #ChatGPT hat mir die Formel %= gegebenl, _surf formel von PyGame Zero
        magnifier.pos = mouse_move_pos
        invis_magnifier.pos = mouse_klick_pos
        hovered_hotspot = None

        if invis_magnifier.colliderect(speaker):
            mute = not mute
        if mouse_klick_pos != (0, 0):
            door_locked_text = False
        if move and not quiz_offen:
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

    mouse_move_pos = pos

def on_mouse_down(pos):
    global mouse_klick_pos

    if not Quiz.quiz_is_open():
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
    global game_started, room_index, room, timer_start, mute

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
            if mute:
                screen.blit(muted_speaker.image, (1140, 12))
                sounds.part1.set_volume(0)
                sounds.part2.set_volume(0)
                sounds.part3.set_volume(0)
            else:
                screen.blit(speaker.image, (1140, 12))
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
            screen.blit("roomkey1", (352.5, 602.5))
        Quiz.draw_quiz(screen, GAME_WIDTH, GAME_HEIGHT, Rect, standard_box)

def draw():
    draw_game()
    magnifier.draw()
