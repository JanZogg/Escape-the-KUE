from pgzero import clock
quizzes = {
    "room1_item1": {
        "question": "Wie Gross ist der Inneninkel von Pacmans Mund?",
        "answers": [
            "45°",
            "60°",
            "90°"
        ],
        "correct": 1
    },
    "room2_item1": {
        "question": "Welche Aussage beschreibt die innere Entwicklung des lyrischen Ichs im Gedicht am genauesten?",
        "answers": [
            "Das lyrische Ich erkennt, dass die Suche nach Bedeutung erfolglos ist, und entscheidet sich deshalb, die Vorstellungen der Gesellschaft vollständig zu übernehmen.",
            "Das lyrische Ich besitzt noch keine sichere Antwort, betrachtet aber bereits die fortgesetzte Suche und die Bewahrung der eigenen Identität als etwas Sinnvolles.",
            "Das lyrische Ich hat sein eigentliches Lebensziel bereits gefunden, befürchtet jedoch, dieses durch äussere Erwartungen wieder zu verlieren."
        ],
        "correct": 2
    }
}

opened_quiz = None
game_is_frozen = False
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
    global message

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
        game_freeze()
        clock.schedule_unique(close_quiz, 1.5) # Formel von ChatGPT
        clock.schedule_unique(game_freeze, 1.5)

def game_freeze():
    global game_is_frozen

    game_is_frozen = not game_is_frozen

def draw_quiz(screen, width, height, rect_class, standard_box):
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
        fontsize=26,
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
            fontsize=20,
            lineheight=0.85,
            color="white"
        )
        y += 70
    if message != "":
        screen.draw.text(message, center=(width / 2, box_y + box_height - 25), fontsize=28, color="yellow")
