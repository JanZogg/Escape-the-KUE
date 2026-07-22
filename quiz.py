from pgzero import clock
quizzes = {
    "room1_item1": {
        "question": "Wie Gross ist der Inneninkel von Pacmans Mund?",
        "answers": [
            "45°",
            "60°",
            "75°"
        ],
        "correct": 3
    },
    "room2_item1": {
        "question": "Welche Aussage trifft auf das lyrischen Ichs am meisten zu?",
        "answers": [
            "Das lyrische Ich gibt die Suche nach Bedeutung auf und passt sich der Gesellschaft an.",
            "Das lyrische Ich hat noch keine Antwort, sieht aber in der Suche und der eigenen Identität einen Sinn.",
            "Das lyrische Ich hat sein Lebensziel gefunden, fürchtet aber, es durch äussere Erwartungen zu verlieren."
        ],
        "correct": 2
    }
}

opened_quiz = None
game_is_frozen = False
deduction = False
deduction_text = False
message = ""
solved_quizzes = []

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
    global message, deduction, deduction_text

    if key == "escape":
        close_quiz()
        return
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
    box_width = 760
    box_height = 360
    box_x = (width - box_width) // 2
    box_y = (height - box_height) // 2
    standard_box(box_x, box_y, box_width, box_height)
    screen.draw.text(
        question["question"],
        midtop=(width / 2, box_y + 20),
        width=box_width - 100,
        fontsize=30,
        lineheight=0.9,
        align="center",
        color="white"
    )

    y = box_y + 95
    for number, answer in enumerate(question["answers"], start=1):
        text = str(number) + ". " + answer
        screen.draw.text(
            text,
            topleft=(box_x + 70, y),
            width=box_width - 140,
            fontsize=25,
            lineheight=0.85,
            color="white"
        )
        y += 70
    if message != "":
        if message == "Richtig":
            screen.draw.text(message, center=(width / 2, box_y + box_height - 25), fontsize=28, color="green")
        else:
            screen.draw.text(message, center=(width / 2, box_y + box_height - 25), fontsize=28, color="red")
