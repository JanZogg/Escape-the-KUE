TITLE = "MaturaArbeit"
WIDTH = 1200
HEIGHT = 675
import pygame
from pygame import Rect
import time

pygame.mouse.set_visible(False)

#Variabeln
game_started = False
bewegen = True
speed = 5
offset_x = 0
aktueller_zimmer_index = 0
mouse_move_pos = (0, 0)
mouse_klick_pos = (0, 0)
item_leuchtend_pos = None
item_gross_pos = None
TIMER_DAUER = 60 * 60
timer_start = time.time()

#Item Actors
r_pacman = Actor("pacman", (855, 312)) #r = Rätsel
r_raum1_item1 = Actor("raum1_item1", (923,315))

#Listen
zimmer = ["raum1", "background"]
items = [r_pacman, r_raum1_item1]
items_leuchtend = [Actor("pacman_leuchtend"), Actor("raum1_high1")]
items_gross = [
    Actor("pacman_gross", (600, 337.5)),
    Actor("raum1_big1", (600, 337.5))
    ]

#Actors
zimmer_actor = Actor(zimmer[aktueller_zimmer_index])
lupe = Actor("lupe")
invis_lupe = Actor("lupe2")

#Programm
def update():
    global offset_x, game_started, mouse_move_pos, item_gross_pos, item_leuchtend_pos, bewegen, mouse_klick_pos, mouse_move_pos

    if game_started:
        if keyboard.A and bewegen:
            offset_x -= speed
        if keyboard.D and bewegen:
            offset_x += speed
        offset_x %= zimmer_actor.width #ChatGPT hat mir die Formel %= gegeben
        lupe.pos = mouse_move_pos
        invis_lupe.pos = mouse_klick_pos
        item_leuchtend_pos = None
        for i, item in enumerate(items):

            #ChatGPT
            item_rect1 = Rect(
                (item.x - offset_x, item.y),
                (item.width, item.height)
            )
            item_rect2 = Rect(
                (item.x - offset_x + zimmer_actor.width, item.y),
                (item.width, item.height)
            )
            #bis hier
            if lupe.colliderect(item_rect1) or lupe.colliderect(item_rect2):
                item_leuchtend_pos = i
                break
        for i, item in enumerate(items):

            item_rect1 = Rect((item.x - offset_x, item.y),(item.width, item.height))
            item_rect2 = Rect((item.x - offset_x + zimmer_actor.width, item.y),(item.width, item.height))

            if invis_lupe.colliderect(item_rect1) or invis_lupe.colliderect(item_rect2):
                item_gross_pos = i
                break
        mouse_klick_pos = (0, 0)
        if item_gross_pos != None:
            bewegen = False
        elif item_gross_pos == None:
            bewegen = True
    if keyboard.ESCAPE:
        item_gross_pos = None

def on_mouse_move(pos):
    global mouse_move_pos

    mouse_move_pos = pos

def on_mouse_down(pos):
    global mouse_klick_pos

    mouse_klick_pos = pos

def on_key_down(key):
    global game_started, aktueller_zimmer_index, zimmer

    if not game_started and keyboard.s:
        game_started = True
    if game_started:
        if keyboard.P:
            aktueller_zimmer_index = aktueller_zimmer_index + 1
            zimmer_actor.image = zimmer[aktueller_zimmer_index]

def draw():
    if not game_started:
        screen.blit("titelbild", (0, 0))
    else:
        screen.clear()

        screen.blit(zimmer_actor.image, (0 - offset_x, 0))
        screen.blit(zimmer_actor.image, (zimmer_actor.width - offset_x, 0))
        screen.blit(r_pacman.image, (r_pacman.x - offset_x, r_pacman.y))
        screen.blit(r_pacman.image, (r_pacman.x - offset_x + zimmer_actor.width, r_pacman.y))
        screen.blit(r_raum1_item1.image, (r_raum1_item1.x - offset_x,r_raum1_item1.y))
        screen.blit(r_raum1_item1.image, (r_raum1_item1.x - offset_x + zimmer_actor.width,r_raum1_item1.y))
        if bewegen:
            if item_leuchtend_pos is not None:
                item = items[item_leuchtend_pos]
                leucht = items_leuchtend[item_leuchtend_pos]
                screen.blit(leucht.image, (item.x - offset_x, item.y))
                screen.blit(leucht.image, (item.x - offset_x + zimmer_actor.width, item.y))
        if item_gross_pos is not None:
            items_gross[item_gross_pos].draw()
        if not bewegen:
            screen.draw.text("Um fortzufahren, druecken sie ESC", center=(600, 80), fontsize=40, color="white")

        #ChatGPT
        verbleibend = max(0, TIMER_DAUER - int(time.time() - timer_start))
        stunden = verbleibend // 3600
        minuten = (verbleibend % 3600) // 60
        sekunden = verbleibend % 60
        timer_text = f"{stunden:02}:{minuten:02}:{sekunden:02}"
        screen.draw.text(timer_text, topleft=(20, 20), fontsize=40, color="white", fontname="clock")

        lupe.draw()
