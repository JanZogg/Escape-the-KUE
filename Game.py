TITLE = "MaturaArbeit"
WIDTH = 1200
HEIGHT = 675

#Variabeln
game_started = False
speed = 5
offset_x = 0
aktueller_zimmer_index = 0

#Listen
zimmer = ["raum1", "background"]

#Actors
zimmer_actor = Actor(zimmer[aktueller_zimmer_index])

#Programm
def update():
    global offset_x, game_started

    if game_started:
        if keyboard.A:
            offset_x -= speed
        if keyboard.D:
            offset_x += speed

        offset_x %= zimmer_actor.width #ChatGPT hat mir die Formel %= gegeben

def on_key_down(key):
    global game_started, aktueller_zimmer_index, zimmer

    if not game_started and key == keys.S:
        game_started = True
    if keyboard.P:
        aktueller_zimmer_index = aktueller_zimmer_index + 1
        zimmer_actor.image = zimmer[aktueller_zimmer_index]

def draw():
    if not game_started:
        screen.blit("titelbild", (0, 0))
    else:
        screen.clear()

        x = -offset_x

        screen.blit(zimmer_actor.image, (x, 0))
        screen.blit(zimmer_actor.image, (x + zimmer_actor.width, 0))





