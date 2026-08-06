TITLE = "MaturaArbeit"
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
from pygame import Rect
from pgzero import clock
import pgzero.game
import pygame
import time
import Quiz
from Panorama import Hotspot, PanoramaView, find_hotspot_at_point, draw_hotspot_overlay

# Pygame Zero liest diese Flags nach dem Laden dieses Moduls und erstellt
# damit selbst genau einen Screen mit einer logischen Aufloesung von 1920x1080.
pgzero.game.DISPLAY_FLAGS = pygame.FULLSCREEN | pygame.SCALED
pygame.mouse.set_visible(False)

#Variabeln
# ä = \u00e4
# ö = \u00f6
# ü = \u00fc
WIDTH = GAME_WIDTH
HEIGHT = GAME_HEIGHT
PANORAMA_BASE_SPEED = 6.4
PANORAMA_MAX_SPEED = 12.8
game_started = False
move = True
speed = PANORAMA_BASE_SPEED
room_index = 0
mouse_move_pos = (0, 0)
mouse_klick_pos = (0, 0)
item_large_pos = None
current_item_quiz = None
hovered_hotspot = None
show_hotspot_debug = False
timer_duration = 60 * 60
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
active_key_animation = None

# Einstellungen für die Schlüsselanimation.
KEY_ANIMATION_HOLD_DURATION = 0.5
KEY_ANIMATION_FLIGHT_DURATION = 0.75
KEY_HOTBAR_MAX_SIZE = (77, 77)

#Listen
room = [
    "room1", #Mathematik
    "room2", #Deutsch
    "room3", #Latein
    "room4", #Biologie
    "room5", #Geographie
    "escaped"
    ]
doors_room = [
    0, #Türe im Raum 0
    1, #Türe im Raum 1
    2, #Türe im Raum 2
    3, #Türe im Raum 3
    4, #Türe im Raum 4
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
    Actor("pacman_gross", (WIDTH / 2, HEIGHT / 2)),
    Actor("room1_big1", (WIDTH / 2, HEIGHT / 2)),
    Actor("room2_big1", (WIDTH / 2, HEIGHT / 2))
    ]
quiz_items = {
    1: "room1_item1",
    2: "room2_item1"
    }
key_animation_config = {
    "room1_item1": ("room1_key1", (21, 488)),
    "room2_item1": ("room2_key1", (21, 576)),
    "room3_item1": ("room3_key1", (21, 664)),
    "room4_item1": ("room4_key1", (21, 752)),
    "room5_item1": ("room5_key1", (21, 840))
    }
key_inventory = []

#Actors
room_actor = Actor(room[room_index])
magnifier = Actor("magnifier")
invis_magnifier = Actor("magnifier2")
speaker = Actor("speaker", (1864, 58))
muted_speaker = Actor("speaker_mute", (1864, 58))
start_button = Actor("start_button", (WIDTH / 2, 800))
puzzle_button = Actor("puzzle_button", (WIDTH / 2, 944))
restart_button = Actor("restart_button", (WIDTH / 2, 960))
escaped = Actor("escaped", (WIDTH / 2, HEIGHT / 2))
imprissond = Actor("gameover", (WIDTH / 2, HEIGHT / 2))
panorama_view = PanoramaView(
    room_actor,
    speed,
    slice_width=6,
    focal_length=1120
)

hotspots = [
    # Die Punkte sind Panorama-Koordinaten, nicht die vom Screen
    Hotspot(
        points=[
            (1379, 501),
            (1418, 501),
            (1418, 541),
            (1379, 541)
        ],
        room_index=items_room[0], #pacman
        hotspot_type="item",
        reference_index=0
    ),
    Hotspot(
        points=[
            (1472, 504),
            (1510, 504),
            (1510, 544),
            (1472, 544)
        ],
        room_index=items_room[1], #room1_item1
        hotspot_type="item",
        reference_index=1
    ),
    Hotspot(
        points=[
            (2101, 438),
            (2192, 438),
            (2192, 688),
            (2101, 688)
        ],
        room_index=doors_room[0],
        hotspot_type="door",
        reference_index=0
    ),
    Hotspot(
        points=[
            (1851, 653),
            (1885, 653),
            (1885, 688),
            (1851, 688)
        ],
        room_index=items_room[2], #room2_item1
        hotspot_type="item",
        reference_index=2
    ),
    Hotspot(
        points=[
            (629, 355),
            (757, 355),
            (757, 630),
            (629, 630)
        ],
        room_index = doors_room[1],
        hotspot_type="door",
        reference_index = 1
    ),
        Hotspot(
        points=[
            (629, 355),
            (757, 355),
            (757, 630),
            (629, 630)
        ],
        room_index = doors_room[2],
        hotspot_type="door",
        reference_index = 2
    ),
    Hotspot(
        points=[
            (629, 355),
            (757, 355),
            (757, 630),
            (629, 630)
        ],
        room_index = doors_room[3],
        hotspot_type="door",
        reference_index = 3
    ),
    Hotspot(
        points=[
            (629, 355),
            (757, 355),
            (757, 630),
            (629, 630)
        ],
        room_index = doors_room[4],
        hotspot_type="door",
        reference_index = 4
    )
]

def draw_large_item(screen, item_index):
    large_item = items_large[item_index]
    top_left = (
        int(large_item.x - large_item.width / 2),
        int(large_item.y - large_item.height / 2)
    )
    screen.blit(large_item.image, top_left)

def puzzle_button_is_visible():
    return (
        item_large_pos is not None
        and current_item_quiz is not None
        and not Quiz.quiz_is_solved(current_item_quiz)
        and not Quiz.quiz_is_open()
    )

def get_key_hotbar_size(key_image):
    image_width, image_height = key_image.get_size() # Ursprünglihce Bildgrösse
    max_width, max_height = KEY_HOTBAR_MAX_SIZE
    scale = min(max_width / image_width, max_height / image_height) # Berechnet den kleineren Verkleinerungsfaktor, ChatGPT
    return (
        max(1, round(image_width * scale)),
        max(1, round(image_height * scale))
    )

def key_is_in_inventory(target_pos):
    return any(key["target_pos"] == target_pos for key in key_inventory)

def start_key_animation(key_image, target_pos):
    global active_key_animation

    # Es kann immer nur ein Schlüssel gleichzeitig animiert werden.
    if active_key_animation is not None or key_is_in_inventory(target_pos):
        return False

    start_size = key_image.get_size()
    final_size = get_key_hotbar_size(key_image)
    # Dictionary mit sämtlichen Infos
    active_key_animation = {
        "image": key_image, # Ursprüngliche Schlüsselbild
        "target_pos": target_pos, # Zielposition
        "start_time": time.time(), # Startzeitpunkt der Animation
        "start_size": start_size, # Anfangsgrösse
        "final_size": final_size, # Endgrösse
        "current_pos": (
            WIDTH / 2 - start_size[0] / 2, # Startposition
            HEIGHT / 2 - start_size[1] / 2
        ),
        "current_size": start_size
    }
    return True

def update_key_animation(): # Codex
    global active_key_animation

    if active_key_animation is None:
        return

    elapsed = time.time() - active_key_animation["start_time"] # Wie lange Animation schon läuft
    if elapsed <= KEY_ANIMATION_HOLD_DURATION:
        return

    flight_elapsed = elapsed - KEY_ANIMATION_HOLD_DURATION # Flugzeit
    progress = min(flight_elapsed / KEY_ANIMATION_FLIGHT_DURATION, 1) # Fortschritt

    # Verkleinerung berechnen
    start_width, start_height = active_key_animation["start_size"]
    final_width, final_height = active_key_animation["final_size"]
    current_width = round(start_width + (final_width - start_width) * progress)
    current_height = round(start_height + (final_height - start_height) * progress)

    # Bewegung berechnen
    start_center = (WIDTH / 2, HEIGHT / 2)
    target_center = (
        active_key_animation["target_pos"][0] + final_width / 2,
        active_key_animation["target_pos"][1] + final_height / 2
    )
    current_center = (
        start_center[0] + (target_center[0] - start_center[0]) * progress,
        start_center[1] + (target_center[1] - start_center[1]) * progress
    )
    active_key_animation["current_size"] = (max(1, current_width), max(1, current_height))
    active_key_animation["current_pos"] = (
        current_center[0] - active_key_animation["current_size"][0] / 2,
        current_center[1] - active_key_animation["current_size"][1] / 2
    )

    if progress == 1: # Animation beenden
        key_inventory.append({
            "image": pygame.transform.smoothscale(
                active_key_animation["image"],
                active_key_animation["final_size"]
            ),
            "target_pos": active_key_animation["target_pos"],
        })
        active_key_animation = None

def draw_key_animation():
    if active_key_animation is None:
        return

    # Smoothscale erzeugt einen neuen Surface, so dass die PNG-Datei unverändert bleibt
    scaled_image = pygame.transform.smoothscale(
        active_key_animation["image"],
        active_key_animation["current_size"]
    )
    draw_pos = (
        round(active_key_animation["current_pos"][0]),
        round(active_key_animation["current_pos"][1])
    )
    screen.surface.blit(scaled_image, draw_pos)

def draw_key_inventory():
    for key in key_inventory:
        screen.surface.blit(key["image"], key["target_pos"])

def close_quiz_with_key_animation():
    quiz_name = Quiz.opened_quiz
    if quiz_name is None:
        return True

    if Quiz.quiz_is_solved(quiz_name) and quiz_name in key_animation_config:
        image_name, target_pos = key_animation_config[quiz_name]
        if not key_is_in_inventory(target_pos):
            if active_key_animation is not None:
                return False
            start_key_animation(getattr(images, image_name), target_pos)

    Quiz.close_quiz()
    return True

def update():
    global game_started, item_large_pos, current_item_quiz, move, mouse_klick_pos, mouse_move_pos, speed, room_index, door_locked_text
    global hovered_hotspot, mute, escape, game_over, show_controls, timer_start, winning_sound_playing, gameover_sound_playing
    # print(Quiz.deduction_text)

    panorama_view.offset %= room_actor._surf.get_width() # ChatGPT hat mir die Formel %= gegebenl, _surf formel von PyGame Zero
    invis_magnifier.pos = mouse_klick_pos
    hovered_hotspot = None
    magnifier.pos = mouse_move_pos
    update_key_animation()

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
                sounds.gameover.set_volume(1.3)
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
            if speed > PANORAMA_MAX_SPEED:
                speed = PANORAMA_MAX_SPEED
        elif keyboard.D and move and not quiz_open:
            panorama_view.speed = speed
            panorama_view.move_right()
            speed = speed * 1.005
            if speed > PANORAMA_MAX_SPEED:
                speed = PANORAMA_MAX_SPEED
        else:
            speed = PANORAMA_BASE_SPEED

        if mouse_klick_pos != (0, 0):
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
                        panorama_view.set_room_image(room[room_index])
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
            close_quiz_with_key_animation()
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
    if puzzle_button_is_visible() and puzzle_button.collidepoint(pos):
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
            if quiz_taste == "escape":
                close_quiz_with_key_animation()
            else:
                Quiz.press_key(quiz_taste)
        return
    if not game_started and keyboard.s:
        game_started = True
    if game_started:
        if keyboard.P:
            room_index = room_index + 1
            panorama_view.offset = 0
            panorama_view.set_room_image(room[room_index])
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
        width=3
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
    global game_started, room_index, item_large_pos, current_item_quiz, hovered_hotspot
    global door_locked_text, move, speed, game_over, escape, current_song, gameover_sound_playing
    global mouse_move_pos, mouse_klick_pos, timer_start, timer_paused, timer_remaining, mute
    global show_controls, mistake_sound_playing, correct_sound_startet, winning_sound_playing
    global active_key_animation

    # Ausstehende Sound-Callbacks des alten Durchlaufs entfernen.
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
    panorama_view.set_room_image(room[room_index])
    panorama_view.offset = 0
    speed = PANORAMA_BASE_SPEED
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

    game_over = False
    escape = None
    current_song = None
    mute = False
    mistake_sound_playing = False
    correct_sound_startet = False
    winning_sound_playing = False
    gameover_sound_playing = False
    show_controls = True
    active_key_animation = None
    key_inventory.clear()

    timer_start = None
    timer_paused = False
    timer_remaining = timer_duration

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
            screen.draw.text("R\u00e4tsel gel\u00f6st", center=(WIDTH / 2, 944), fontsize=64, color="yellow")
        elif puzzle_button_is_visible():
            puzzle_button.draw()
    if not move:
        screen.draw.text("Zum schliessen, dr\u00fccken sie ESC", center=(WIDTH / 2, 176), fontsize=64, color="yellow")
    if door_locked_text:
        screen.draw.text("T\u00fcre ist verschlossen", center=(WIDTH / 2, 864), fontsize=64, color="yellow")

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
        screen.draw.text("-1 Minute", topleft=(16, 112), fontsize=48, color="red")
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
    standard_box(16, 19, 440, 88)
    screen.draw.text(timer_text, topleft=(32, 32), fontsize=64, color="white", fontname="clock")

    if verbleibend == 0:
        game_over = True
        escape = False

    #Musik
    standard_box(1824, 19, 88, 80)
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
    standard_box(16, 480, 88, 560)
    draw_key_inventory()

    Quiz.draw_quiz(screen, GAME_WIDTH, GAME_HEIGHT, standard_box)

    #Steuerung
    if show_controls:
        Quiz.game_is_frozen = True
        box_width = 1216
        box_height = 576
        box_x = (WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2
        standard_box(box_x, box_y, box_width, box_height)
        screen.draw.text("Steuerung", center=(box_x + box_width / 2, box_y + 40), bold=True, fontsize=80, color="white")
        screen.draw.text("A und D:", topleft=(box_x + 8, box_y + 112), bold=True, fontsize=40, color="white")
        screen.draw.text("Bewege dich nach links oder rechts durch den Raum.", topleft=(box_x + 8, box_y + 144), fontsize=40, color="white")
        screen.draw.text("Maus bewegen", topleft=(box_x + 8, box_y + 208), bold=True, fontsize=40, color="white")
        screen.draw.text("Untersuche auff\u00e4llige Gegenst\u00e4nde.", topleft=(box_x + 8, box_y + 240), fontsize=40, color="white")
        screen.draw.text("Linksklick", topleft=(box_x + 8, box_y + 304), bold=True, fontsize=40, color="white")
        screen.draw.text("Sieh dir Gegenst\u00e4nde genauer an oder \u00f6ffne ein Quiz.", topleft=(box_x + 8, box_y + 336), fontsize=40, color="white")
        screen.draw.text("ESC", topleft=(box_x + 8, box_y + 400), bold=True, fontsize=40, color="white")
        screen.draw.text("Schliesse Bilder, Quizfragen und dieses Fenster", topleft=(box_x + 8, box_y + 432), fontsize=40, color="white")
        screen.draw.text("Untersuche die R\u00e4ume aufmerksam, merke dir wichtige Hinweise und l\u00f6se die Quizfragen.", topleft=(box_x + 8, box_y + 496), fontsize=40, color="white")
        screen.draw.text("Bei falscher Antwort gib es Abzug!", topleft=(box_x + 8, box_y + 528), fontsize=40, color="white")

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
            screen.draw.text("Verbleibende Zeit", center=(WIDTH / 2, 752), fontsize=56, color="white")
            screen.draw.text(timer_text, center=(WIDTH / 2, 824), fontsize=80, color="white", fontname="clock")
        else:
            imprissond.draw()
            restart_button.draw()
    else:
        draw_game()
    draw_key_animation()
    magnifier.draw()
