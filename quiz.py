from pgzero import clock

quizzes = {
    "room1_item2": {
        "question": "Welche Aussage trifft auf das lyrische Ich am meisten zu?",
        "answers": [
            "Das lyrische Ich gibt die Suche nach Bedeutung auf und passt sich der Gesellschaft an.",
            "Das lyrische Ich hat noch keine Antwort, sieht aber in der Suche und der eigenen Identität einen Sinn.",
            "Das lyrische Ich hat sein Lebensziel gefunden, fürchtet aber, es durch äussere Erwartungen zu verlieren."
        ],
        "correct": 2
    },
    "room2_item1": {
        "question": "Was haben die folgenden Figuren gemeinsam?",
        "answers": [
            "Ihre Innenwinkelsumme beträgt 720°",
            "Sie besitzen gleich viele Symmetrieachsen",
            "Ihr Umfang beträgt jeweils 24cm"
        ],
        "correct": 1
    }
}

opened_quiz = None
game_is_frozen = False
deduction = False
deduction_text = False
correct_sound_playing = False
message = ""
solved_quizzes = []

def reset_quiz_state():
    global opened_quiz, game_is_frozen, deduction, deduction_text, correct_sound_playing, message

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

def open_quiz(quiz_name):
    global opened_quiz, message

    if quiz_is_solved(quiz_name):
        return False
    opened_quiz = quiz_name
    message = ""
    return True

def close_quiz():
    global opened_quiz, message

    opened_quiz = None
    message = ""

def quiz_is_open():
    return opened_quiz is not None

def quiz_is_solved(quiz_name):
    return quiz_name in solved_quizzes

def press_key(key):
    global message, deduction, deduction_text, correct_sound_playing

    if opened_quiz is None:
        return
    if key not in ["1", "2", "3"]:
        return

    question = quizzes[opened_quiz]
    chosen_answer = int(key)

    if game_is_frozen:
        return
    elif chosen_answer == question["correct"]:
        message = "Richtig"
        correct_sound_playing = True
        if opened_quiz not in solved_quizzes:
            solved_quizzes.append(opened_quiz)
    else:
        message = "Falsch, versuche es nochmals"
        deduction = True
        deduction_text = True
        game_freeze()
        clock.schedule_unique(close_quiz, 1.5) # Formel von ChatGPT
        clock.schedule_unique(game_freeze, 1.5)
        clock.schedule_unique(set_deduction_on_false, 1.5)

def game_freeze():
    global game_is_frozen

    game_is_frozen = not game_is_frozen

def set_deduction_on_false():
    global deduction_text

    deduction_text = False

def draw_quiz(screen, width, height, standard_box):
    if opened_quiz is None:
        return

    question = quizzes[opened_quiz]
    box_width = 1216
    box_height = 576
    box_x = (width - box_width) // 2
    box_y = (height - box_height) // 2
    standard_box(box_x, box_y, box_width, box_height)
    screen.draw.text(
        question["question"],
        midtop=(width / 2, box_y + 32),
        width=box_width - 160,
        fontsize=48,
        lineheight=0.9,
        align="center",
        color="white"
    )

    y = box_y + 152
    for number, answer in enumerate(question["answers"], start=1):
        text = str(number) + ". " + answer
        screen.draw.text(
            text,
            topleft=(box_x + 112, y),
            width=box_width - 224,
            fontsize=40,
            lineheight=0.85,
            color="white"
        )
        y += 112
    if message != "":
        if message == "Richtig":
            screen.draw.text(message, center=(width / 2, box_y + box_height - 40), fontsize=45, color="green")
        else:
            screen.draw.text(message, center=(width / 2, box_y + box_height - 40), fontsize=45, color="red")
