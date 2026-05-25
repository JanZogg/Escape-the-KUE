TITLE = "MaturaArbeit"
WIDTH = 1200
HEIGHT = 675
import pygame
from pygame import Rect
import time

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
TIMER_DURATION = 60 * 60
timer_start = None

#Item Actors
r_pacman = Actor("pacman", (855, 312)) #r = Rätsel
r_raum1_item1 = Actor("room1_item1", (923,315))

#Listen
room = [
    "room1",
    "background"
    ]
#door = [Actor("...", (0,0))]
items = [
    r_pacman,
    r_raum1_item1
    ]
items_high = [
    Actor("pacman_leuchtend"),
    Actor("room1_high1")
    ]
items_large = [
    Actor("pacman_gross", (600, 337.5)),
    Actor("room1_big1", (600, 337.5))
    ]

#Actors
room_actor = Actor(room[room_index])
magnifier = Actor("magnifier")
invis_magnifier = Actor("magnifier2")

#Programm
def update():
    global offset_x, game_started, mouse_move_pos, item_large_pos, item_high_pos, move, mouse_klick_pos, mouse_move_pos, speed

    if game_started:
        if keyboard.A and move:
            speed = speed * 1.005
            offset_x -= speed
            if speed > 10:
                speed = 10
        elif keyboard.D and move:
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
        if move:
            for i, item in enumerate(items):

                #ChatGPT
                item_rect1 = Rect(
                    (item.x - offset_x, item.y),
                    (item.width, item.height)
                )
                item_rect2 = Rect(
                    (item.x - offset_x + room_actor.width, item.y),
                    (item.width, item.height)
                )
                #bis hier
                if magnifier.colliderect(item_rect1) or magnifier.colliderect(item_rect2):
                    item_high_pos = i
                    break
            for i, item in enumerate(items):

                item_rect1 = Rect((item.x - offset_x, item.y),(item.width, item.height))
                item_rect2 = Rect((item.x - offset_x + room_actor.width, item.y),(item.width, item.height))

                if invis_magnifier.colliderect(item_rect1) or invis_magnifier.colliderect(item_rect2):
                    item_large_pos = i
                    break
        mouse_klick_pos = (0, 0)
        if item_large_pos != None:
            move = False
        elif item_large_pos == None:
            move = True
    if keyboard.ESCAPE:
        item_large_pos = None

def on_mouse_move(pos):
    global mouse_move_pos

    mouse_move_pos = pos

def on_mouse_down(pos):
    global mouse_klick_pos

    mouse_klick_pos = pos

def on_key_down(key):
    global game_started, room_index, room, timer_start

    if not game_started and keyboard.s:
        game_started = True
        timer_start = time.time()

    if game_started:
        if keyboard.P:
            room_index = room_index + 1
            room_actor.image = room[room_index]

def draw():
    if not game_started:
        screen.blit("start", (0, 0))
    else:
        screen.clear()

        screen.blit(room_actor.image, (0 - offset_x, 0))
        screen.blit(room_actor.image, (room_actor.width - offset_x, 0))
        screen.blit(r_pacman.image, (r_pacman.x - offset_x, r_pacman.y))
        screen.blit(r_pacman.image, (r_pacman.x - offset_x + room_actor.width, r_pacman.y))
        screen.blit(r_raum1_item1.image, (r_raum1_item1.x - offset_x,r_raum1_item1.y))
        screen.blit(r_raum1_item1.image, (r_raum1_item1.x - offset_x + room_actor.width,r_raum1_item1.y))
        if move:
            if item_high_pos is not None:
                item = items[item_high_pos]
                leucht = items_high[item_high_pos]
                screen.blit(leucht.image, (item.x - offset_x, item.y))
                screen.blit(leucht.image, (item.x - offset_x + room_actor.width, item.y))
        if item_large_pos is not None:
            items_large[item_large_pos].draw()
        if not move:
            screen.draw.text("Um fortzufahren, druecken sie ESC", center=(600, 80), fontsize=40, color="white")

        #ChatGPT
        if timer_start is not None:
            verbleibend = max(0, TIMER_DURATION - int(time.time() - timer_start))
        else:
            verbleibend = TIMER_DURATION
        stunden = verbleibend // 3600
        minuten = (verbleibend % 3600) // 60
        sekunden = verbleibend % 60
        timer_text = f"{stunden:02}:{minuten:02}:{sekunden:02}"
        screen.draw.text(timer_text, topleft=(20, 20), fontsize=40, color="white", fontname="clock")

        magnifier.draw()
