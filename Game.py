TITLE = "MaturaArbeit"
WIDTH = 1200
HEIGHT = 675
import pygame
from pygame import Rect
import time
import quiz

pygame.mouse.set_visible(False)

#Variabeln
game_started = False
move = True
speed = 5
offset_x = 0
room_index = 0
mouse_move_pos = (0, 0)
mouse_klick_pos = (0, 0)
item_high_pos = None
item_large_pos = None
timer_duration = 60 * 60
timer_start = None
quiz_item_index = 1
sekunden = ""
minuten = ""
stunden = ""

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

def item_rects(item):
    return [
        Rect((item.x - offset_x, item.y), (item.width, item.height)),
        Rect((item.x - offset_x + room_actor.width, item.y), (item.width, item.height))
    ]

def actor_collides_with_item(item, actor):
    for item_rect in item_rects(item):
        if actor.colliderect(item_rect):
            return True
    return False

#Programm
def update():
    print(magnifier.pos)
    global offset_x, game_started, item_large_pos, item_high_pos, move, mouse_klick_pos, mouse_move_pos, speed

    if game_started:
        quiz_offen = quiz.quiz_is_open()
        if keyboard.A and move and not quiz_offen:
            speed = speed * 1.005
            offset_x -= speed
            if speed > 10:
                speed = 10
        elif keyboard.D and move and not quiz_offen:
            offset_x += speed
            speed = speed * 1.005
            if speed > 10:
                speed = 10
        else:
            speed = 5

        offset_x %= room_actor.width #ChatGPT hat mir die Formel %= gegeben
        magnifier.pos = mouse_move_pos
        invis_magnifier.pos = mouse_klick_pos
        item_high_pos = None

        if move and not quiz_offen:
            for i, item in enumerate(items):
                if items_room[i] != room_index:
                    continue
                if actor_collides_with_item(item, magnifier):
                    item_high_pos = i
                    break
            for i, item in enumerate(items):
                if items_room[i] != room_index:
                    continue
                if actor_collides_with_item(item, invis_magnifier):
                    if i in quiz_items and not quiz.quiz_is_solved(quiz_items[i]):
                        quiz.open_quiz(quiz_items[i])
                        item_large_pos = None
                    else:
                        item_large_pos = i
                    break

        mouse_klick_pos = (0, 0)
        if quiz.quiz_is_open():
            move = False
        elif item_large_pos != None:
            move = False
        elif item_large_pos == None:
            move = True
    if keyboard.ESCAPE:
        if quiz.quiz_is_open():
            quiz.close_quiz()
        else:
            item_large_pos = None

def on_mouse_move(pos):
    global mouse_move_pos

    mouse_move_pos = pos

def on_mouse_down(pos):
    global mouse_klick_pos

    if not quiz.quiz_is_open():
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
    global game_started, room_index, room, timer_start

    if quiz.quiz_is_open():
        quiz_taste = quiz_taste_von_key(key)
        if quiz_taste is not None:
            quiz.press_key(quiz_taste)
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

def draw():
    if not game_started:
        screen.blit("start", (0, 0))
    else:
        screen.clear()
        screen.blit(room_actor.image, (0 - offset_x, 0))
        screen.blit(room_actor.image, (room_actor.width - offset_x, 0))
        if room_index == 0:
            screen.blit(doors[0].image, (doors[0].x - offset_x, doors[0].y))
            screen.blit(doors[0].image, (doors[0].x - offset_x + room_actor.width, doors[0].y))
            screen.blit(q_pacman.image, (q_pacman.x - offset_x, q_pacman.y))
            screen.blit(q_pacman.image, (q_pacman.x - offset_x + room_actor.width, q_pacman.y))
            screen.blit(q_room1_item1.image, (q_room1_item1.x - offset_x,q_room1_item1.y))
            screen.blit(q_room1_item1.image, (q_room1_item1.x - offset_x + room_actor.width,q_room1_item1.y))
        if move:
            if item_high_pos is not None:
                item = items[item_high_pos]
                leucht = items_high[item_high_pos]
                screen.blit(leucht.image, (item.x - offset_x, item.y))
                screen.blit(leucht.image, (item.x - offset_x + room_actor.width, item.y))
        if item_large_pos is not None:
            items_large[item_large_pos].draw()
            if item_large_pos in quiz_items and quiz.quiz_is_solved(quiz_items[item_large_pos]):
                screen.draw.text("Raetsel geloest", center=(600, 590), fontsize=40, color="yellow")
        if not move:
            screen.draw.text("Um fortzufahren, druecken sie ESC", center=(600, 80), fontsize=40, color="white")

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
        if quiz.quiz_is_solved("room1_item1"):
            screen.blit("roomkey1", (352.5, 602.5))
        magnifier.draw()
        quiz.draw_quiz(screen, WIDTH, HEIGHT, Rect, standard_box)
