#Einfaches Quiz-Modul fuer Raetselgegenstaende
fragen = {
    "room1_item1": {
        "frage": "Welche Antwort ist richtig?",
        "antworten": [
            "Antwort 1",
            "Antwort 2",
            "Antwort 3"
        ],
        "richtig": 2
    }
}

offenes_quiz = None
meldung = ""
geloeste_quizzes = []


def oeffnen(quiz_name):
    global offenes_quiz, meldung

    if ist_geloest(quiz_name):
        return False

    offenes_quiz = quiz_name
    meldung = ""
    return True


def schliessen():
    global offenes_quiz, meldung

    offenes_quiz = None
    meldung = ""


def ist_offen():
    return offenes_quiz is not None


def ist_geloest(quiz_name):
    return quiz_name in geloeste_quizzes


def taste_druecken(taste):
    global meldung

    if taste == "escape":
        schliessen()
        return

    if offenes_quiz is None:
        return

    if taste not in ["1", "2", "3"]:
        return

    frage = fragen[offenes_quiz]
    gewaehlte_antwort = int(taste)

    if gewaehlte_antwort == frage["richtig"]:
        meldung = "Richtig"
        if offenes_quiz not in geloeste_quizzes:
            geloeste_quizzes.append(offenes_quiz)
    else:
        meldung = "Falsch, versuche es nochmals"


def zeichnen(screen, breite, hoehe, rect_klasse):
    if offenes_quiz is None:
        return

    frage = fragen[offenes_quiz]
    box_breite = 760
    box_hoehe = 360
    box_x = (breite - box_breite) // 2
    box_y = (hoehe - box_hoehe) // 2

    #Pygame Zero braucht hier ein echtes Rect-Objekt.
    quiz_box = rect_klasse((box_x, box_y), (box_breite, box_hoehe))
    screen.draw.filled_rect(quiz_box, (20, 20, 20))
    screen.draw.rect(quiz_box, "white")
    screen.draw.text(frage["frage"], center=(breite / 2, box_y + 55), fontsize=42, color="white")

    y = box_y + 120
    for nummer, antwort in enumerate(frage["antworten"], start=1):
        text = str(nummer) + ". " + antwort
        screen.draw.text(text, topleft=(box_x + 70, y), fontsize=34, color="white")
        y += 55

    if meldung != "":
        screen.draw.text(meldung, center=(breite / 2, box_y + box_hoehe - 65), fontsize=34, color="yellow")

    screen.draw.text("ESC: schliessen", center=(breite / 2, box_y + box_hoehe - 25), fontsize=24, color="white")
