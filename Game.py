TITLE = "MaturaArbeit"
GAME_WIDTH = 1920
GAME_HEIGHT = 1080
from pygame import Rect
from pgzero import clock
import pgzero.game
import pygame
import time
import quiz as Quiz
from Panorama import PanoramaView, find_hotspot_at_point, draw_hotspot_overlay
from Hotspot import create_hotspots

# KI
pgzero.game.DISPLAY_FLAGS = pygame.FULLSCREEN | pygame.SCALED
pygame.mouse.set_visible(False)

#Variabeln
# ä = \u00e4
# ö = \u00f6
# ü = \u00fc
WIDTH = GAME_WIDTH
HEIGHT = GAME_HEIGHT
panorama_base_speed = 6.4
panorama_max_speed = 12.8
game_started = False
move = True
speed = panorama_base_speed
room_index = 0
mouse_move_pos = (0, 0)
mouse_klick_pos = (0, 0)
item_large_pos = None
current_item_quiz = None
hovered_hotspot = None
timer_duration = 60 * 60
timer_start = None
timer_paused = False
timer_remaining = timer_duration
scaled_transparent_image_cache = {}
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
show_confirm = False
highlighted_room = None
sounds.click.set_volume(0.4)
help_tracker = 0
intro_index = 0
intro_playing = True

# Einstellungen für die Schlüsselanimation.
key_animation_hold_duration = 0.5
key_animation_flight_duration = 0.75
key_hotbar_max_size = (75, 75)

# Einstellung für image_big Grösse
big_image_max_height = 550

#Listen
room = [
    "room1", #Deutsch
    "room2", #Mathematik
    "room3", #Geographie
    "room4", #Chemie
    "room5", #Biologie
    "room6", #Latein
    "escaped"
    ]
room_start_center_x = [
    270,  #Raum 1: Deutsch
    280,  #Raum 2: Mathematik
    210,  #Raum 3: Geographie
    3710, #Raum 4: Chemie
    0,    #Raum 5: Biologie
    260   #Raum 6: Latein
    ]
doors_room = [
    0, #Türe im Raum 0
    1, #Türe im Raum 1
    2, #Türe im Raum 2
    3, #Türe im Raum 3
    4, #Türe im Raum 4
    5, #Türe im Raum 5
    99 #Schlusszeichen
    ]
door_keys = [
    "room1_item2",
    "room2_item1",
    "room3_item4",
    "room4_item1",
    "room5_item1",
    "room6_item1"
    ]
items_room = [
    0, #room1_item1 im Raum 0
    0, #room1_item2 im Raum 0
    1, #room2_item1 im Raum 1
    1, #room2_item2 im Raum 1
    1, #room2_item3 im Raum 1
    2, #room3_item1 im Raum 2
    2, #room3_item2 im Raum 2
    2, #room3_item3 im Raum 2
    2, #room3_item4 im Raum 2
    2, #room3_item5 im Raum 2
    3, #room4_item1 im Raum 3
    3, #room4_item2 im Raum 3
    3, #room4_item3 im Raum 3
    3, #room4_item4 im Raum 3
    3, #room4_item5 im Raum 3
    3, #room4_item6 im Raum 3
    3, #room4_item7 im Raum 3
    4, #room5_item1 im Raum 4
    4, #room5_item2 im Raum 4
    4, #room5_item3 im Raum 4
    4, #room5_item4 im Raum 4
    4, #room5_item5 im Raum 4
    5, #room6_item1 im Raum 5
    5, #room6_item2 im Raum 5
    5, #room6_item3 im Raum 5
    5, #room6_item4 im Raum 5
    5, #room6_item5 im Raum 5
    5, #room6_item6 im Raum 5
    5, #room6_item7 im Raum 5
    5 #room6_item7 im Raum 5
    ]
hotspots = create_hotspots(items_room, doors_room)

items_large = [
    Actor("room1_big1", (WIDTH / 2, HEIGHT / 2)),
    Actor("room1_big2", (WIDTH / 2, HEIGHT / 2)),
    Actor("room2_big1", (WIDTH / 2, HEIGHT / 2)),
    Actor("room2_big2", (WIDTH / 2, HEIGHT / 2)),
    Actor("room2_big3", (WIDTH / 2, HEIGHT / 2)),
    Actor("room3_big1", (WIDTH / 2, HEIGHT / 2)),
    Actor("room3_big2", (WIDTH / 2, HEIGHT / 2)),
    Actor("room3_big3", (WIDTH / 2, HEIGHT / 2)),
    Actor("room3_big4", (WIDTH / 2, HEIGHT / 2)),
    Actor("room3_big5", (WIDTH / 2, HEIGHT / 2)),
    Actor("room4_big1", (WIDTH / 2, HEIGHT / 2)),
    Actor("room4_big2", (WIDTH / 2, HEIGHT / 2)),
    Actor("room4_big3", (WIDTH / 2, HEIGHT / 2)),
    Actor("room4_big4", (WIDTH / 2, HEIGHT / 2)),
    Actor("room4_big5", (WIDTH / 2, HEIGHT / 2)),
    Actor("room4_big6", (WIDTH / 2, HEIGHT / 2)),
    Actor("room4_big7", (WIDTH / 2, HEIGHT / 2)),
    Actor("room5_big1", (WIDTH / 2, HEIGHT / 2)),
    Actor("room5_big2", (WIDTH / 2, HEIGHT / 2)),
    Actor("room5_big3", (WIDTH / 2, HEIGHT / 2)),
    Actor("room5_big4", (WIDTH / 2, HEIGHT / 2)),
    Actor("room5_big5", (WIDTH / 2, HEIGHT / 2)),
    Actor("room6_big1", (WIDTH / 2, HEIGHT / 2)),
    Actor("room6_big2", (WIDTH / 2, HEIGHT / 2)),
    Actor("room6_big3", (WIDTH / 2, HEIGHT / 2)),
    Actor("room6_big4", (WIDTH / 2, HEIGHT / 2)),
    Actor("room6_big5", (WIDTH / 2, HEIGHT / 2)),
    Actor("room6_big6", (WIDTH / 2, HEIGHT / 2)),
    Actor("room6_big7", (WIDTH / 2, HEIGHT / 2)),
    Actor("room6_big8", (WIDTH / 2, HEIGHT / 2))
    ]
scaled_big_image_cache = {}
quiz_items = {
    1: "room1_item2",
    2: "room2_item1",
    8: "room3_item4",
    10: "room4_item1",
    17: "room5_item1",
    22: "room6_item1"
    }
key_animation_config = {
    "room1_item2": ("room1_key1", (34, 545)),
    "room2_item1": ("room2_key1", (34, 626)),
    "room3_item4": ("room3_key1", (34, 705)),
    "room4_item1": ("room4_key1", (34, 785)),
    "room5_item1": ("room5_key1", (34, 864)),
    "room6_item1": ("room6_key1", (34, 944))
    }
key_inventory = []
intro_images = [
    "intro_black",
    "intro_message",
    "intro_reply",
    "intro_battery",
    "intro_end"
]

#Actors
room_actor = Actor(room[room_index])
magnifier = Actor("magnifier")
help_icon = Actor("lightbulb", (1750, 61))
confirm_button = Actor("yes", (810, 690))
reject_button = Actor("no", (1110, 690))
speaker = Actor("speaker", (1857, 61))
muted_speaker = Actor("speaker_mute", (1857, 61))
start_button = Actor("start_button", (WIDTH / 2, 800))
puzzle_button = Actor("puzzle_button", (WIDTH / 2, 944))
restart_button = Actor("restart_button", (WIDTH / 2, 960))
escaped = Actor("escaped", (WIDTH / 2, HEIGHT / 2))
imprissond = Actor("gameover", (WIDTH / 2, HEIGHT / 2))
x = Actor("close_smth", (1565, 300))
next_button = Actor("next", (1750, 61))
skip_button = Actor("skip", (1857, 61))
panorama_view = PanoramaView(
    room_actor,
    speed,
    slice_width=6,
    focal_length=1120
)

def set_room_with_start_view(new_room_index):
    panorama_view.set_room_image(room[new_room_index])

    if new_room_index < len(room_start_center_x):
        center_x = room_start_center_x[new_room_index]
        panorama_view.offset = center_x - GAME_WIDTH / 2
    else:
        panorama_view.offset = 0

    panorama_view.offset %= room_actor._surf.get_width()

set_room_with_start_view(room_index)

def scale_big_image(image_surface, max_height=big_image_max_height):
    image_width, image_height = image_surface.get_size()

    # Kleine Bilder bleiben in ihrer Originalgrösse.
    if image_height <= max_height:
        return image_surface

    scale_factor = max_height / image_height
    scaled_size = (
        max(1, round(image_width * scale_factor)),
        max_height
    )
    return pygame.transform.smoothscale(image_surface, scaled_size)

def get_scaled_big_image(image_name):
    if image_name not in scaled_big_image_cache:
        # Actor.image ist nur der Bildname. Erst images.<name> liefert die Surface.
        image_surface = getattr(images, image_name)
        scaled_big_image_cache[image_name] = scale_big_image(image_surface)

    return scaled_big_image_cache[image_name]

def draw_large_item(screen, item_index):
    large_item = items_large[item_index]
    scaled_image = get_scaled_big_image(large_item.image)
    image_rect = scaled_image.get_rect(
        center=(round(large_item.x), round(large_item.y))
    )
    screen.surface.blit(scaled_image, image_rect)

def puzzle_button_is_visible():
    return (
        item_large_pos is not None
        and current_item_quiz is not None
        and not Quiz.quiz_is_solved(current_item_quiz)
        and not Quiz.quiz_is_open()
    )

def get_key_hotbar_size(key_image):
    image_width, image_height = key_image.get_size() # Ursprünglihce Bildgrösse
    max_width, max_height = key_hotbar_max_size
    scale = min(max_width / image_width, max_height / image_height) # Berechnet den kleineren Verkleinerungsfaktor, KI
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

def update_key_animation(): # KI
    global active_key_animation

    if active_key_animation is None:
        return

    elapsed = time.time() - active_key_animation["start_time"] # Wie lange Animation schon läuft
    if elapsed <= key_animation_hold_duration:
        return

    flight_elapsed = elapsed - key_animation_hold_duration # Flugzeit
    progress = min(flight_elapsed / key_animation_flight_duration, 1) # Fortschritt

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

def hover_button(button, normal_image, hover_image):
    area = getattr(images, normal_image).get_rect(center=button.center) # Formel von KI die macht, dass trotzvergrösserung des Bildes durch highlight, das normale Bild gilt
    if area.collidepoint(mouse_move_pos):
        button.image = hover_image
    else:
        button.image = normal_image

def update():
    global game_started, item_large_pos, current_item_quiz, move, mouse_klick_pos, mouse_move_pos, speed, room_index
    global door_locked_text, hovered_hotspot, mute, escape, game_over, show_controls, timer_start, winning_sound_playing
    global gameover_sound_playing, show_confirm, timer_remaining, highlighted_room, help_tracker
    global intro_index, intro_playing

    panorama_view.offset %= room_actor._surf.get_width() # KI hat mir die Formel %= gegebenl, _surf formel von PyGame Zero
    hovered_hotspot = None
    magnifier.pos = (mouse_move_pos[0] + 5, mouse_move_pos[1] + 15)
    update_key_animation()

    if not game_started:
        hover_button(start_button, "start_button", "high_start_button")
        if start_button.collidepoint(mouse_klick_pos):
            play_click()
            game_started = True
            clock.schedule_unique(play_message_received, 0.1)
    elif game_over:
        hover_button(restart_button, "restart_button", "high_restart_button")
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
    elif intro_playing:
        hover_button(next_button, "next", "high_next")
        hover_button(skip_button, "skip", "high_skip")
        if skip_button.collidepoint(mouse_klick_pos):
            play_click()
            mouse_klick_pos = (0, 0)
            intro_playing = False
        elif next_button.collidepoint(mouse_klick_pos):
            intro_index += 1
            play_click()
            mouse_klick_pos = (0, 0)
            if intro_index >= len(intro_images):
                intro_playing = False
        if intro_index != 0 or not intro_playing:
            sounds.message_received.stop()
    else:
        hover_button(x, "close_smth", "high_close_smth")
        hover_button(reject_button, "no", "high_no")
        hover_button(confirm_button, "yes", "high_yes")
        hover_button(puzzle_button, "puzzle_button", "high_puzzle_button")
        hover_button(Quiz.check_button, "check_button", "high_check_button")
        hover_button(help_icon, "lightbulb", "high_lightbulb")
        hover_button(speaker, "speaker", "high_speaker")
        hover_button(muted_speaker, "speaker_mute", "high_speaker_mute")
        if speaker.collidepoint(mouse_klick_pos):
            play_click()
            mute = not mute
            mouse_klick_pos = (0, 0)
        if (not show_controls
            and not Quiz.quiz_is_open()
            and item_large_pos is None):
            if (help_icon.collidepoint(mouse_klick_pos) and not show_confirm
                and highlighted_room != room_index):
                play_click()
                show_confirm = True
                mouse_klick_pos = (0, 0)
            if (show_confirm and confirm_button.collidepoint(mouse_klick_pos)
                and highlighted_room != room_index):
                play_click()
                Quiz.deduction_text = True
                clock.schedule_unique(Quiz.set_deduction_on_false, 1.5)
                timer_remaining = max(0, timer_remaining - 120)
                show_confirm = False
                mouse_klick_pos = (0, 0)
                highlighted_room = room_index
                Quiz.game_is_frozen = False
                help_tracker += 1
            elif show_confirm and reject_button.collidepoint(mouse_klick_pos):
                play_click()
                show_confirm = False
                mouse_klick_pos = (0, 0)
                Quiz.game_is_frozen = False
        if not Quiz.game_is_frozen:
            quiz_open = Quiz.quiz_is_open()
            if keyboard.A and move and not quiz_open:
                speed = speed * 1.005
                panorama_view.speed = speed
                panorama_view.move_left()
                if speed > panorama_max_speed:
                    speed = panorama_max_speed
            elif keyboard.D and move and not quiz_open:
                panorama_view.speed = speed
                panorama_view.move_right()
                speed = speed * 1.005
                if speed > panorama_max_speed:
                    speed = panorama_max_speed
            else:
                speed = panorama_base_speed

            if mouse_klick_pos != (0, 0):
                door_locked_text = False
            if move and not quiz_open:
                hovered_hotspot = find_hotspot_at_point(mouse_move_pos, room_index, hotspots, panorama_view, GAME_WIDTH)

                door_clicked = False
                clicked_door_hotspot = None

                if mouse_klick_pos != (0, 0):
                    clicked_door_hotspot = find_hotspot_at_point(mouse_klick_pos, room_index, hotspots, panorama_view, GAME_WIDTH, "door")
                if clicked_door_hotspot is not None:
                    i = clicked_door_hotspot.reference_index
                    if doors_room[i] == room_index:
                        play_click()
                        door_clicked = True
                        if Quiz.quiz_is_solved(door_keys[i]):
                            room_index = room_index + 1
                            set_room_with_start_view(room_index)
                            item_large_pos = None
                            current_item_quiz = None
                            if doors_room[room_index] == 99:
                                pause_timer()
                                game_over = True
                                escape = True
                        else:
                            door_locked_text = True
                if not door_clicked:
                    clicked_item_hotspot = None
                    if mouse_klick_pos != (0, 0):
                        clicked_item_hotspot = find_hotspot_at_point(mouse_klick_pos, room_index, hotspots, panorama_view, GAME_WIDTH, "item")
                    if clicked_item_hotspot is not None:
                        i = clicked_item_hotspot.reference_index
                        if items_room[i] == room_index:
                            play_click()
                            item_large_pos = i
                            current_item_quiz = quiz_items.get(i)

        if (show_controls or item_large_pos is not None) and x.collidepoint(mouse_klick_pos):
            play_click()
            if show_controls:
                show_controls = False
                Quiz.game_is_frozen = False
                timer_start = time.time()
            else:
                item_large_pos = None
                current_item_quiz = None

        mouse_klick_pos = (0, 0)
        if Quiz.quiz_is_open():
            move = False
        elif item_large_pos != None:
            move = False
        elif item_large_pos == None:
            move = True

def on_mouse_move(pos):
    global mouse_move_pos

    mouse_move_pos = pos

def on_mouse_down(pos):
    global mouse_klick_pos, item_large_pos, current_item_quiz

    if game_started and intro_playing:
        mouse_klick_pos = pos
        return

    if game_over and restart_button.collidepoint(pos):
        restart_game()
        play_click()
        return
    if Quiz.quiz_is_open():
        if x.collidepoint(pos):
            close_quiz_with_key_animation()
            play_click()
        else:
            if Quiz.click_quiz(pos, GAME_WIDTH, GAME_HEIGHT):
                play_click()
        return
    if puzzle_button_is_visible() and puzzle_button.collidepoint(pos):
        if Quiz.open_quiz(current_item_quiz):
            play_click()
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
    if key == pygame.K_4 or key == pygame.K_KP4:
        return "4"
    if key == pygame.K_TAB:
        return "tab"
    if key == pygame.K_BACKSPACE:
        return "backspace"
    letter = pygame.key.name(key)
    if len(letter) == 1 and letter.isalpha():
        return letter
    return None

def on_key_down(key):
    global game_started, room_index, mute, item_large_pos, current_item_quiz, game_over, escape

    if Quiz.quiz_is_open():
        quiz_taste = quiz_taste_von_key(key)
        if quiz_taste is not None:
            Quiz.press_key(quiz_taste)
        return
    if game_started and not intro_playing:
        if keyboard.P:
            room_index = room_index + 1
            set_room_with_start_view(room_index)
            item_large_pos = None
            current_item_quiz = None
        if keyboard.M:
            mute = not mute

def draw_image(image_name, x, y, width, height, transparency=0):
    transparency = max(0, min(100, transparency))
    cache_key = (image_name, width, height, transparency)
    if cache_key not in scaled_transparent_image_cache:
        image = getattr(images, image_name) # Formel von KI die macht, dass man das Bild mit dem name image_name aussucht
        image = pygame.transform.smoothscale(image, (width, height))
        image.set_alpha(round(255 * (1 - transparency / 100)))
        scaled_transparent_image_cache[cache_key] = image
    screen.blit(scaled_transparent_image_cache[cache_key], (x, y))

def overlay():
    box_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    box_surface.fill((0, 0, 0, 100))
    screen.surface.blit(box_surface, (0, 0))

def play_click():
    sounds.click.play(0)

def play_message_received():
    global intro_playing, intro_index

    if intro_playing and intro_index == 0:
        sounds.message_received.play(-1)

def set_volume_back():
    global mistake_sound_playing

    sounds.part1.set_volume(1)
    sounds.part2.set_volume(1)
    sounds.part3.set_volume(1)
    mistake_sound_playing = False

def stop_correct_sound():
    global correct_sound_startet

    Quiz.correct_sound_playing = False
    close_quiz_with_key_animation()
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
    global active_key_animation, highlighted_room, show_confirm, help_tracker
    global intro_index, intro_playing

    # Ausstehende Sound-Callbacks des alten Durchlaufs entfernen.
    clock.unschedule(set_volume_back)
    clock.unschedule(stop_correct_sound)
    clock.unschedule(play_message_received)

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
    set_room_with_start_view(room_index)
    speed = panorama_base_speed
    panorama_view.speed = speed

    item_large_pos = None
    current_item_quiz = None
    hovered_hotspot = None
    door_locked_text = False
    move = True
    mouse_move_pos = (0, 0)
    mouse_klick_pos = (0, 0)
    magnifier.pos = mouse_move_pos

    game_over = False
    escape = None
    current_song = None
    mute = False
    mistake_sound_playing = False
    correct_sound_startet = False
    winning_sound_playing = False
    gameover_sound_playing = False
    show_controls = True
    highlighted_room = None
    help_tracker = 0
    show_confirm = False
    active_key_animation = None
    key_inventory.clear()

    timer_start = None
    timer_paused = False
    timer_remaining = timer_duration

    intro_index = 0
    intro_playing = True

    Quiz.reset_quiz_state()

def pause_timer():
    global timer_start, timer_paused, timer_remaining

    if timer_start is not None and not timer_paused:
        vergangen = time.time() - timer_start
        timer_remaining = max(0, timer_remaining - vergangen)
        timer_paused = True
        timer_start = None

def get_remaining_time():
    if timer_paused or timer_start is None:
        verbleibend = timer_remaining
    else:
        vergangen = time.time() - timer_start
        verbleibend = max(0, timer_remaining - vergangen)

    return int(verbleibend)

def draw_game():
    global current_song, mute, game_over, escape, mistake_sound_playing, show_controls, timer_remaining
    global correct_sound_startet, room_index, show_confirm, mouse_klick_pos

    screen.clear()
    panorama_view.draw(screen)
    draw_hotspot_overlay(
        screen, room_index, hovered_hotspot, hotspots, panorama_view,
        show_item_help=(highlighted_room == room_index)
    )
    if not move and Quiz.opened_quiz is None:
        overlay()
        box_width = 1368
        box_height = 648
        box_x = (WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2
        draw_image("background_items", box_x, box_y, box_width, box_height, transparency=15)
        x.draw()
    if item_large_pos is not None:
        draw_large_item(screen, item_large_pos)
        if item_large_pos in quiz_items and Quiz.quiz_is_solved(quiz_items[item_large_pos]):
            screen.draw.text("R\u00e4tsel gel\u00f6st", center=(WIDTH / 2, 944), fontsize=64, color="yellow", fontname="text_bold")
        elif puzzle_button_is_visible():
            puzzle_button.draw()

    if door_locked_text:
        screen.draw.text("T\u00fcre ist verschlossen", center=(WIDTH / 2, 864), fontsize=64, color="yellow", fontname="text_bold")

    #Steuerung
    if show_controls:
        overlay()
        Quiz.game_is_frozen = True
        box_width = 1368
        box_height = 648
        box_x = (WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2
        draw_image("background_controls", box_x, box_y, box_width, box_height, transparency=15)
        screen.draw.text("Steuerung", center=(box_x + box_width // 2, box_y + 80), fontsize=64, color="white", fontname="text_bold")
        screen.draw.text("A und D:", topleft=(box_x + 110, box_y + 150), fontsize=30, color="white", fontname="text_bold")
        screen.draw.text("Bewege dich nach links oder rechts durch den Raum.", topleft=(box_x + 110, box_y + 180), fontsize=30, color="white", fontname="text_regular")
        screen.draw.text("Raum untersuchen", topleft=(box_x + 110, box_y + 225), fontname="text_bold", fontsize=30, color="white")
        screen.draw.text("Bewege die Maus \u00fcber auff\u00e4llige Gegenst\u00e4nde und Hinweise.", topleft=(box_x + 110, box_y + 255), fontsize=30, color="white", fontname="text_regular")
        screen.draw.text("Linksklick", topleft=(box_x + 110, box_y + 300), fontname="text_bold", fontsize=30, color="white")
        screen.draw.text("Sieh dir Gegenst\u00e4nde genauer an oder \u00f6ffne ein R\u00e4tsel.", topleft=(box_x + 110, box_y + 330), fontsize=30, color="white", fontname="text_regular")
        screen.draw.text("R\u00e4tsel l\u00f6sen.", fontname="text_bold", topleft=(box_x + 110, box_y + 375), fontsize=30, color="white")
        screen.draw.text("W\u00e4hle mit 1 bis 4 oder f\u00fclle die Felder aus und klicke auf Pr\u00fcfen.", topleft=(box_x + 110, box_y + 405), fontsize=30, color="white", fontname="text_regular")
        screen.draw.text("Ziel", topleft=(box_x + 110, box_y + 450), fontname="text_bold", fontsize=30, color="white")
        screen.draw.text("Untersuche jeden Raum aufmerksam, merke dir wichtige Hinweise und l\u00f6se die R\u00e4tsel.", topleft=(box_x + 110, box_y + 480), fontsize=30, color="white", fontname="text_regular")
        #screen.draw.text("Achtung: Falsche Antworten kosten Zeit!", center=(box_x + box_width // 2, box_y + 570), fontname="text_bold", fontsize=30, color="red")
        screen.draw.text("Achtung:", topleft=(box_x + 110, box_y + 525), fontname="text_bold", fontsize=30, color="white")
        screen.draw.text("Falsche Antworten kosten Zeit!", topleft=(box_x + 225, box_y + 525), fontsize=30, color="white", fontname="text_regular")
        x.draw()

    #Nachfrage für Help
    if show_confirm:
        overlay()
        Quiz.game_is_frozen = True
        box_width = 800
        box_height = 500
        box_x = (WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2
        draw_image("background_confirm", box_x, box_y, box_width, box_height, transparency=15)
        screen.draw.text("Brauchst du Hilfe?", center=(box_x + box_width // 2, box_y + 80), fontname="text_bold", fontsize=50, color="white")
        screen.draw.text("Klicke auf das H\u00e4ckchen um alle Objekte", center=(box_x + box_width // 2, box_y + 140), fontsize=28, color="white", fontname="text_regular")
        screen.draw.text("im diesem Raum anzuzeigen.", center=(box_x + box_width // 2, box_y + 170), fontsize=28, color="white", fontname="text_regular")
        screen.draw.text("Achtung!", center=(box_x + box_width // 2, box_y + 250), fontname="text_bold", fontsize=28, color="white")
        screen.draw.text("Es werden dir aber 2 Minuten abgezogen!", center=(box_x + box_width // 2, box_y + 280), fontsize=28, color="white", fontname="text_regular")
        confirm_button.draw()
        reject_button.draw()

    #Abdunklung und Quiz zeichnen inkl. Kreuz zum schliesen
    if Quiz.opened_quiz is not None:
        overlay()
        Quiz.draw_quiz(screen, GAME_WIDTH, GAME_HEIGHT, draw_image)
        if Quiz.quiz_is_open():
            x.draw()

    #Timer
    if Quiz.deduction:
        timer_remaining = max(0, timer_remaining - 120)
        mistake_sound_playing = True
        sounds.part1.set_volume(0)
        sounds.part2.set_volume(0)
        sounds.part3.set_volume(0)
        sounds.mistake.play()
        clock.schedule_unique(set_volume_back, 1)
        Quiz.deduction = False
    if Quiz.deduction_text:
        screen.draw.text("-2 Minuten", center=(229.5, 140), fontsize=40, color="red", fontname="text_bold")
    if Quiz.correct_sound_playing and not correct_sound_startet:
        correct_sound_startet = True
        sounds.part1.set_volume(0)
        sounds.part2.set_volume(0)
        sounds.part3.set_volume(0)
        sounds.correct_answer.set_volume(0.5)
        sounds.correct_answer.play()
        clock.schedule_unique(stop_correct_sound, 1)

    #KI
    verbleibend = get_remaining_time()
    hours = verbleibend // 3600
    minutes = (verbleibend % 3600) // 60
    seconds = verbleibend % 60
    timer_text = f"{hours:02}:{minutes:02}:{seconds:02}"
    draw_image("background_timer", 19, 19, 440, 88, transparency=15)
    screen.draw.text(timer_text, topleft=(65, 36), fontsize=54, color="white", fontname="clock")

    if verbleibend == 0:
        game_over = True
        escape = False

    #Raumanzeige
    draw_image("background_roomdisplay", (WIDTH - 330) // 2, 19, 330, 66, transparency=15)
    screen.draw.text(f"Zimmer {room_index + 1} von 6", center=((WIDTH // 2), 52), fontsize=30, color="white", fontname="text_bold")

    #Musik
    draw_image("background_audio", 1813, 19, 88, 88, transparency=15)
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

    #Helpbutton
    draw_image("background_help", 1706, 19, 88, 88, transparency=15)
    help_icon.draw()

    #Hotbar
    draw_image("background_hotbar", 19, 501, 88, 560, transparency=5)
    draw_key_inventory()

def draw():
    if not game_started:
        screen.blit("start", (0, 0))
        start_button.draw()
    elif intro_playing:
        screen.blit(intro_images[intro_index], (0, 0))
        draw_image("background_next", 1706, 19, 88, 88, transparency=15)
        draw_image("background_skip", 1813, 19, 88, 88, transparency=15)
        next_button.draw()
        skip_button.draw()
    elif game_over:
        if escape:
            escaped.draw()
            restart_button.draw()
            verbleibend = get_remaining_time()
            hours = verbleibend // 3600
            minutes = (verbleibend % 3600) // 60
            seconds = verbleibend % 60
            remaining_time_text = f"{hours:02}:{minutes:02}:{seconds:02}"
            result_text = (f"Verbleibende Zeit: {remaining_time_text} | Fehler: {Quiz.mistake_tracker} | Hilfen: {help_tracker}")
            screen.draw.text(result_text, center=(WIDTH / 2, 790), fontsize=36, color="white", fontname="text_regular")
        else:
            imprissond.draw()
            restart_button.draw()
            result_text = (f"Gel\u00f6ste R\u00e4ume: {room_index}/6 | Fehler: {Quiz.mistake_tracker} | Hilfen: {help_tracker}")
            screen.draw.text(result_text, center=(WIDTH / 2, 790), fontsize=36, color="white", fontname="text_regular")
    else:
        draw_game()
    draw_key_animation()
    magnifier.draw()
