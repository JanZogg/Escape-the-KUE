TITLE = "MaturaArbeit"
GAME_WIDTH = 1200
GAME_HEIGHT = 675
from pygame import Rect
from pgzero import clock
import pygame
import time
import Quiz
from Panorama import Hotspot, PanoramaView, find_hotspot_at_point, draw_hotspot_overlay
pygame.mouse.set_visible(False)

#Variabeln
# ä = \u00e4
# ö = \u00f6
# ü = \u00fc
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
timer_duration = 60
timer_start = None
timer_paused = False
timer_remaining = timer_duration
door_locked_text = False
current_song = None
mute = False
escape = None
game_over = False
correct_sound_startet = False
winning_sound_playing = False
gameover_sound_playing = False
mistake_sound_playing = False
show_controls = True

#Listen
room = [
    "room1",
    "room2",
    "escaped"
    ]
doors_room = [
    0, #Türe im Raum 0
    1, #Türe im Raum 1
    99 #Schlusszeichen
    ]
door_keys = [
    "room1_item1",
    "room2_item1"
    ]
items_room = [
    0, #pacman im Raum 0
    0, #room1_item1 im Raum 0
    1 #room2_item1 im Raum 1
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
quiz_button = Actor("quiz_button", (600, 590))
restart_button = Actor("restart_button", (600, 620))
escaped = Actor("escaped", (WIDTH / 2, HEIGHT / 2))
imprissond = Actor("gameover", (WIDTH / 2, HEIGHT / 2))
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
        room_index=items_room[0], # pacman
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
        room_index=items_room[1], # room1_item1
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
        room_index=items_room[2], # room2_item1
        hotspot_type="item",
        reference_index=2
    ),
    Hotspot(
        points=[
            (393, 222),
            (473, 222),
            (473, 394),
            (393, 394)
        ],
        room_index = doors_room[1],
        hotspot_type="door",
        reference_index = 1
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
    global game_started, item_large_pos, current_item_quiz, move, mouse_klick_pos, mouse_move_pos, speed, room_index, door_locked_text
    global hovered_hotspot, mute, escape, game_over, show_controls, timer_start, winning_sound_playing
    global gameover_sound_playing
    print(Quiz.deduction_text)

    panorama_view.offset %= room_actor._surf.get_width() #ChatGPT hat mir die Formel %= gegebenl, _surf formel von PyGame Zero
    invis_magnifier.pos = mouse_klick_pos
    hovered_hotspot = None
    magnifier.pos = mouse_move_pos

    if not game_started:
        if start_button.collidepoint(mouse_klick_pos):
            game_started = True
    elif game_over:
        if escape:
            pause_timer()
            if not winning_sound_playing:
                sounds.winning.set_volume(0.5)
                sounds.winning.play(-1)
                sounds.part1.stop()
                sounds.part2.stop()
                sounds.part3.stop()
                winning_sound_playing = True
        else:
            if not gameover_sound_playing:
                sounds.gameover.set_volume(0.7)
                sounds.gameover.play(-1)
                sounds.part1.stop()
                sounds.part2.stop()
                sounds.part3.stop()
                gameover_sound_playing = True
    elif not Quiz.game_is_frozen:
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
                        if doors_room[room_index] == 99:
                            game_over = True
                            escape = True
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
        if show_controls:
            show_controls = False
            Quiz.game_is_frozen = False
            timer_start = time.time()
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

    if game_over and restart_button.collidepoint(pos):
        restart_game()
        return
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
    global game_started, room_index, room, mute, item_large_pos, current_item_quiz, escape, game_over

    if Quiz.quiz_is_open():
        quiz_taste = quiz_taste_von_key(key)
        if quiz_taste is not None:
            Quiz.press_key(quiz_taste)
        return
    if not game_started and keyboard.s:
        game_started = True
    if game_started:
        if keyboard.P:
            room_index = room_index + 1
            panorama_view.offset = 0
            room_actor.image = room[room_index]
            item_large_pos = None
            current_item_quiz = None
        if keyboard.M:
            mute = not mute
        if keyboard.N:
            escape = True
            game_over = True

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

def set_volume_back():
    global mistake_sound_playing

    sounds.part1.set_volume(1)
    sounds.part2.set_volume(1)
    sounds.part3.set_volume(1)
    mistake_sound_playing = False

def stop_correct_sound():
    global correct_sound_startet

    Quiz.correct_sound_playing = False
    correct_sound_startet = False

    if not mute:
        sounds.part1.set_volume(1)
        sounds.part2.set_volume(1)
        sounds.part3.set_volume(1)

def restart_game():
    global game_started, room_index, item_large_pos, current_item_quiz
    global hovered_hotspot, door_locked_text, move, speed
    global mouse_move_pos, mouse_klick_pos
    global timer_start, timer_paused, timer_remaining
    global game_over, escape, current_song, mute, show_controls
    global mistake_sound_playing, correct_sound_startet
    global winning_sound_playing, gameover_sound_playing

    # Auch noch ausstehende Sound-Callbacks des alten Durchlaufs entfernen.
    clock.unschedule(set_volume_back)
    clock.unschedule(stop_correct_sound)

    sounds.winning.stop()
    sounds.gameover.stop()
    sounds.correct_answer.stop()
    sounds.mistake.stop()
    sounds.part1.stop()
    sounds.part2.stop()
    sounds.part3.stop()

    sounds.winning.set_volume(0.5)
    sounds.gameover.set_volume(0.7)
    sounds.correct_answer.set_volume(0.5)
    sounds.mistake.set_volume(1)
    sounds.part1.set_volume(1)
    sounds.part2.set_volume(1)
    sounds.part3.set_volume(1)

    game_started = False
    room_index = 0
    room_actor.image = room[room_index]
    panorama_view.offset = 0
    speed = 4
    panorama_view.speed = speed

    item_large_pos = None
    current_item_quiz = None
    hovered_hotspot = None
    door_locked_text = False
    move = True
    mouse_move_pos = (0, 0)
    mouse_klick_pos = (0, 0)
    magnifier.pos = mouse_move_pos
    invis_magnifier.pos = mouse_klick_pos

    timer_start = None
    timer_paused = False
    timer_remaining = timer_duration

    game_over = False
    escape = None
    current_song = None
    mute = False
    mistake_sound_playing = False
    correct_sound_startet = False
    winning_sound_playing = False
    gameover_sound_playing = False
    show_controls = True

    Quiz.reset_quiz_state()

def pause_timer():
    global timer_start, timer_paused, timer_remaining

    if timer_start is not None and not timer_paused:
        vergangen = time.time() - timer_start
        timer_remaining = max(0, timer_remaining - vergangen)
        timer_paused = True
        timer_start = None

def resume_timer():
    global timer_start, timer_paused

    if timer_paused and timer_remaining > 0:
        timer_start = time.time()
        timer_paused = False

def get_remaining_time():
    if timer_paused or timer_start is None:
        verbleibend = timer_remaining
    else:
        vergangen = time.time() - timer_start
        verbleibend = max(0, timer_remaining - vergangen)

    return int(verbleibend)

def draw_game():
    global current_song, mute, game_over, escape, mistake_sound_playing, show_controls, timer_remaining
    global correct_sound_startet

    screen.clear()
    panorama_view.draw(screen)
    draw_hotspot_overlay(screen, room_index, hovered_hotspot, show_hotspot_debug, hotspots, panorama_view)
    if item_large_pos is not None:
        draw_large_item(screen, item_large_pos)
        if item_large_pos in quiz_items and Quiz.quiz_is_solved(quiz_items[item_large_pos]):
            screen.draw.text("R\u00e4tsel gel\u00f6st", center=(600, 590), fontsize=40, color="yellow")
        elif quiz_button_is_visible():
            quiz_button.draw()
    if not move:
        screen.draw.text("Zum schliessen, dr\u00fccken sie ESC", center=(600, 110), fontsize=40, color="yellow")
    if door_locked_text:
        screen.draw.text("T\u00fcre ist verschlossen", center=(600, 540), fontsize=40, color="yellow")

    #Timer erstellt mit ChatGPT
    if Quiz.deduction:
        timer_remaining = max(0, timer_remaining - 60)
        mistake_sound_playing = True
        sounds.part1.set_volume(0)
        sounds.part2.set_volume(0)
        sounds.part3.set_volume(0)
        sounds.mistake.play()
        clock.schedule_unique(set_volume_back, 1.1)
        Quiz.deduction = False
    if Quiz.deduction_text:
        screen.draw.text("-1 Minute", topleft=(10, 70), fontsize=30, color="red")
    if Quiz.correct_sound_playing and not correct_sound_startet:
        correct_sound_startet = True
        sounds.part1.set_volume(0)
        sounds.part2.set_volume(0)
        sounds.part3.set_volume(0)
        sounds.correct_answer.set_volume(0.5)
        sounds.correct_answer.play()
        clock.schedule_unique(stop_correct_sound, 0.7)

    verbleibend = get_remaining_time()
    hours = verbleibend // 3600
    minutes = (verbleibend % 3600) // 60
    seconds = verbleibend % 60
    timer_text = f"{hours:02}:{minutes:02}:{seconds:02}"
    standard_box(10, 12, 275, 55)
    screen.draw.text(timer_text, topleft=(20, 20), fontsize=40, color="white", fontname="clock")

    if verbleibend == 0:
        game_over = True
        escape = False

    #Musik
    standard_box (1140, 12, 55, 50)
    if mute:
        muted_speaker.draw()
        sounds.part1.set_volume(0)
        sounds.part2.set_volume(0)
        sounds.part3.set_volume(0)
    else:
        speaker.draw()
        if not mistake_sound_playing and not Quiz.correct_sound_playing:
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
    standard_box(10, 300, 55, 350)
    if Quiz.quiz_is_solved("room1_item1"):
        screen.blit("room1_key1", (13, 305))
    if Quiz.quiz_is_solved("room2_item1"):
        screen.blit("room2_key1", (13, 360))
    Quiz.draw_quiz(screen, GAME_WIDTH, GAME_HEIGHT, standard_box)

    #Steuerung
    if show_controls:
        Quiz.game_is_frozen = True
        box_width = 760
        box_height = 360
        box_x = (WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2
        standard_box(box_x, box_y, box_width, box_height)
        screen.draw.text("Steuerung", center=(box_x + box_width/2, box_y + 25), bold=True, fontsize=50, color="white")
        screen.draw.text("A und D:", topleft=(box_x + 5, box_y + 70), bold=True, fontsize=25, color="white")
        screen.draw.text("Bewege dich nach links oder rechts durch den Raum.", topleft=(box_x + 5, box_y + 90), fontsize=25, color="white")
        screen.draw.text("Maus bewegen", topleft=(box_x + 5, box_y + 130), bold=True, fontsize=25, color="white")
        screen.draw.text("Untersuche auff\u00e4llige Gegenst\u00e4nde.", topleft=(box_x + 5, box_y + 150), fontsize=25, color="white")
        screen.draw.text("Linksklick", topleft=(box_x + 5, box_y + 190), bold=True, fontsize=25, color="white")
        screen.draw.text("Sieh dir Gegenst\u00e4nde genauer an oder \u00f6ffne ein Quiz.", topleft=(box_x + 5, box_y + 210), fontsize=25, color="white")
        screen.draw.text("ESC", topleft=(box_x + 5, box_y + 250), bold=True, fontsize=25, color="white")
        screen.draw.text("Schliesse Bilder, Quizfragen und dieses Fenster", topleft=(box_x + 5, box_y + 270), fontsize=25, color="white")
        screen.draw.text("Untersuche die R\u00e4ume aufmerksam, merke dir wichtige Hinweise und l\u00f6se die Quizfragen.", topleft=(box_x + 5, box_y + 310), fontsize=25, color="white")
        screen.draw.text("Bei falscher Antwort gib es Abzug!", topleft=(box_x + 5, box_y + 330), fontsize=25, color="white")

def draw():
    if not game_started:
        screen.blit("start", (0, 0))
        start_button.draw()
    elif game_over:
        if escape:
            escaped.draw()
            restart_button.draw()
            verbleibend = get_remaining_time()
            hours = verbleibend // 3600
            minutes = (verbleibend % 3600) // 60
            seconds = verbleibend % 60
            timer_text = f"{hours:02}:{minutes:02}:{seconds:02}"
            screen.draw.text("Verbleibende Zeit", center=(WIDTH / 2, 490), fontsize=35, color="white")
            screen.draw.text(timer_text, center=(WIDTH/2, 540), fontsize=50, color="white", fontname="clock")
        else:
            imprissond.draw()
            restart_button.draw()
    else:
        draw_game()
    magnifier.draw()
