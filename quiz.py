from pgzero import clock
from pygame import Rect
from pgzero.actor import Actor

check_button = Actor("check_button")

quizzes = {
    "room1_item2": {
        "question": "Welche Aussage trifft auf das lyrische Ich am meisten zu?",
        "answers": [
            "Das lyrische Ich gibt die Suche nach Bedeutung auf und passt sich der Gesellschaft an.",
            "Das lyrische Ich hat noch keine Antwort, sieht aber in der Suche und der eigenen Identität einen Sinn.",
            "Das lyrische Ich hat sein Lebensziel gefunden, fürchtet aber, es durch äussere Erwartungen zu verlieren.",
            "Das lyrische Ich gibt die Suche noch nicht auf aber ist kurz davor aufzugeben."
        ],
        "correct": 2,
        "rätsel_type": "multiplechoice"
    },
    "room2_item1": {
        "question": "Was haben die folgenden Figuren gemeinsam?",
        "answers": [
            "Ihre Innenwinkelsumme beträgt 720°",
            "Sie besitzen gleich viele Symmetrieachsen",
            "Ihr Umfang beträgt jeweils 24cm",
            "Nichts der oberen angaben"
        ],
        "correct": 4,
        "rätsel_type": "multiplechoice"
    },
    "room3_item4": {
        "question": "a) 5. Buchstabe | b) 1. Buchstabe | c) 3. Buchstabe = ?",
        "correct": ["C", "P", "H"],
        "max_length": 1,
        "rätsel_type": "eingabe"
    },
    "room4_item1": {
        "question": "Welche Elementkette ist im Raum versteckt? Die Antwort muss alphabetische geordnet sein!",
        "correct": ["B", "Ca", "S", "W"],
        "max_length": 2,
        "rätsel_type": "eingabe"
    },
    "room5_item1": {
        "question": "Wie Alt wurde dieser Büffel?",
        "answers": [
            "32",
            "28",
            "24",
            "20"
        ],
        "correct": 4,
        "rätsel_type": "multiplechoice"
    },
    "room6_item1": {
        "question": "Finde das versteckte Wort?",
        "correct": ["F", "I", "N"],
        "max_length": 1,
        "rätsel_type": "eingabe"
    }
}

opened_quiz = None
game_is_frozen = False
deduction = False
deduction_text = False
correct_sound_playing = False
message = ""
solved_quizzes = []
# Lehre dictionaries die nachher mit einerseits mit den richtigen antworten und dem "Status" gespeichert werden (True oder False)
input_answers = {} # [""],[""],[""]
correct_fields = {} # [False],[False],[False]
active_input_field = 0

def reset_quiz_state():
    global opened_quiz, game_is_frozen, deduction, deduction_text, correct_sound_playing, message
    global active_input_field

    # Alte Quiz-Callbacks dürfen keinen neuen Spieldurchlauf verändern.
    clock.unschedule(close_quiz)
    clock.unschedule(game_freeze)
    clock.unschedule(set_deduction_on_false)

    opened_quiz = None
    game_is_frozen = False
    deduction = False
    deduction_text = False
    correct_sound_playing = False
    message = ""
    solved_quizzes.clear()
    input_answers.clear()
    correct_fields.clear()
    active_input_field = 0

def open_quiz(quiz_name):
    global opened_quiz, message

    if game_is_frozen or quiz_is_solved(quiz_name):
        return False
    opened_quiz = quiz_name
    message = ""
    if quizzes[quiz_name]["rätsel_type"] == "eingabe":
        if quiz_name not in input_answers:
            field_count = len(quizzes[quiz_name]["correct"]) # Anzahl der lehren Felder die nacher erstellt werden müssen
            input_answers[quiz_name] = [""] * field_count
            correct_fields[quiz_name] = [False] * field_count
        select_first_unsolved_field()
    return True

def close_quiz():
    global opened_quiz, message, active_input_field

    opened_quiz = None
    message = ""
    active_input_field = 0

def quiz_is_open():
    return opened_quiz is not None

def quiz_is_solved(quiz_name):
    return quiz_name in solved_quizzes

def press_key(key):
    global active_input_field, message

    if opened_quiz is None or game_is_frozen or quiz_is_solved(opened_quiz):
        return

    question = quizzes[opened_quiz]
    if question["rätsel_type"] == "eingabe":
        answers = input_answers[opened_quiz]
        confirmed = correct_fields[opened_quiz]
        if key == "tab": # Codex verwendet für tab Funktion
            # Bereits richtige Felder werden beim Wechsel übersprungen.
            for step in range(1, len(answers) + 1):
                next_field = (active_input_field + step) % len(answers)
                if not confirmed[next_field]:
                    active_input_field = next_field
                    break
        elif not confirmed[active_input_field]:
            if key == "backspace": # Codex verwendet für backspace Funktion
                answers[active_input_field] = answers[active_input_field][:-1]
                message = ""
            elif len(key) == 1 and key.isalpha(): # isalpha() von ChatGPT und prüft ob es ein Buchstabe ist
                if len(answers[active_input_field]) < question["max_length"]:
                    answers[active_input_field] += key.upper() # .upper() von ChatGPT und macht, dass angehängte Buchstabe gross ist
                    message = ""
        return

    if key not in ["1", "2", "3", "4"]:
        return
    chosen_answer = int(key)
    if not 1 <= chosen_answer <= len(question["answers"]):
        return

    check_answer(chosen_answer == question["correct"])

def select_first_unsolved_field(): # Codex verwendet für Auswahl des ersten Feldes welches noch nicht gelöst wurde
    global active_input_field

    active_input_field = 0
    for number, confirmed in enumerate(correct_fields[opened_quiz]):
        if not confirmed:
            active_input_field = number
            break

def check_input():
    global message

    if opened_quiz is None or game_is_frozen or quiz_is_solved(opened_quiz):
        return
    question = quizzes[opened_quiz]
    if question["rätsel_type"] != "eingabe":
        return

    answers = input_answers[opened_quiz]
    confirmed = correct_fields[opened_quiz]
    if "" in answers:
        message = "Bitte fülle zuerst alle Felder aus."
        return

    for number, correct_answer in enumerate(question["correct"]): # enumerate gibt gleichzetig Position und Eintrag
        # Gross- und Kleinschreibung spielen beim Vergleich keine Rolle.
        if answers[number].upper() == correct_answer.upper():
            confirmed[number] = True
            answers[number] = correct_answer
        else:
            answers[number] = ""

    select_first_unsolved_field()
    # Ein Fehlversuch kostet einmal Zeit, unabhängig von der Zahl falscher Felder.
    check_answer(all(confirmed))

def check_answer(is_correct):
    global message, deduction, deduction_text, correct_sound_playing

    if is_correct:
        message = "Richtig"
        correct_sound_playing = True
        if opened_quiz not in solved_quizzes:
            solved_quizzes.append(opened_quiz)
    else:
        message = "Falsch, versuche es nochmals"
        deduction = True
        deduction_text = True
        game_freeze()
        if quizzes[opened_quiz]["rätsel_type"] == "multiplechoice":
            clock.schedule_unique(close_quiz, 1.5) # Formel von ChatGPT
        clock.schedule_unique(game_freeze, 1.5)
        clock.schedule_unique(set_deduction_on_false, 1.5)

def input_field_rects(width, height): # Mit hilfe von Codex erstellt
    # Drei oder vier Felder werden mit den gleichen Abständen zentriert.
    field_count = len(quizzes[opened_quiz]["correct"])
    field_width = 160
    gap = 60
    total_width = field_count * field_width + (field_count - 1) * gap
    start_x = (width - total_width) // 2
    field_y = (height - 576) // 2 + 220
    return [Rect(start_x + number * (field_width + gap), field_y, field_width, 90)
            for number in range(field_count)] # Erstellt für jede Feldnummer ein Rechteck

def click_quiz(pos, width, height):
    global active_input_field

    if opened_quiz is None or game_is_frozen or quiz_is_solved(opened_quiz):
        return
    if quizzes[opened_quiz]["rätsel_type"] != "eingabe":
        return

    for number, field in enumerate(input_field_rects(width, height)):
        if field.collidepoint(pos) and not correct_fields[opened_quiz][number]:
            active_input_field = number
            return True
    if check_button.collidepoint(pos):
        check_input()
        return True

def game_freeze():
    global game_is_frozen

    game_is_frozen = not game_is_frozen

def set_deduction_on_false():
    global deduction_text

    deduction_text = False

def draw_quiz(screen, width, height, draw_image):
    if opened_quiz is None:
        return

    question = quizzes[opened_quiz]
    box_width = 1368
    box_height = 648
    box_x = (width - box_width) // 2
    box_y = (height - box_height) // 2
    draw_image("background_quiz", box_x, box_y, box_width, box_height, transparency=15)
    screen.draw.text(
        question["question"],
        midtop=(width / 2, box_y + 64),
        width=box_width - 160,
        fontname="text_bold",
        fontsize=40,
        lineheight=0.9,
        align="center",
        color="white"
    )
    y = box_y + 152

    if question["rätsel_type"] == "multiplechoice":
        for number, answer in enumerate(question["answers"], start=1):
            text = str(number) + ". " + answer
            screen.draw.text(
                text,
                topleft=(box_x + 90, y),
                width=box_width - 224,
                fontname="text_regular",
                fontsize=32,
                lineheight=0.85,
                color="white"
            )
            y += 90
    elif question["rätsel_type"] == "eingabe":
        fields = input_field_rects(width, height)
        for number, field in enumerate(fields):
            if correct_fields[opened_quiz][number]:
                field_color = "green"
                background_color = (25, 65, 35) # Grüngrau
            elif number == active_input_field:
                field_color = "yellow"
                background_color = (55, 55, 55) # Hellgrau
            else:
                field_color = "white"
                background_color = (35, 35, 35) # Dunkelgrau
            screen.draw.filled_rect(field, background_color)
            screen.draw.rect(field, field_color)
            screen.draw.text(
                input_answers[opened_quiz][number],
                center=field.center,
                fontname="text_regular",
                fontsize=48,
                color="white"
            )
            if number < len(fields) - 1: # nach jedem Feld ausser dem letzten kommt noch ein Bindestrich
                screen.draw.text("-", center=(field.right + 30, field.centery), fontsize=48, color="white", fontname="text_regular")

        screen.draw.text(
            "Tab oder Mausklick: Feld wechseln   |   Backspace: löschen",
            center=(width / 2, box_y + 400),
            fontname="text_regular",
            fontsize=28,
            color="white"
        )
        check_button.pos = (width / 2, box_y + 520)
        check_button.draw()
    if message != "":
        if message == "Richtig":
            screen.draw.text(message, center=(width / 2, box_y + box_height - 50), fontsize=45, color="green", fontname="text_bold")
        else:
            screen.draw.text(message, center=(width / 2, box_y + box_height - 50), fontsize=45, color="red", fontname="text_bold")
