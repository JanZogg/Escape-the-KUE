"""Exercise packaged resources and main game screens without a desktop window."""
import json
import sys
from pathlib import Path


def run(game, root):
    import pygame
    import pgzero.game
    from pgzero.game import PGZeroGame
    from pgzero.loaders import images, sounds, fonts

    counts = {}
    for folder, loader in (("images", images), ("sounds", sounds)):
        files = sorted((root / folder).iterdir())
        for file in files:
            getattr(loader, file.stem)
        counts[folder] = len(files)
    font_files = sorted((root / "fonts").glob("*.ttf"))
    for file in font_files:
        fonts.load(file.stem, 32)
    counts["fonts"] = len(font_files)

    pgzero.game.DISPLAY_FLAGS = 0
    runtime = PGZeroGame(game)
    runtime.reinit_screen()
    game.draw()
    game.game_started = True
    for i in range(len(game.intro_images)):
        game.intro_index = i
        game.draw()
    game.intro_playing = False
    game.timer_start = game.time.time()
    for room_index in range(6):
        game.room_index = room_index
        game.set_room_with_start_view(room_index)
        game.update()
        game.show_controls = True
        game.draw()
        game.show_controls = False
        game.draw()
    for i in range(len(game.items_large)):
        game.draw_large_item(game.screen, i)
    for quiz_name in game.Quiz.quizzes:
        game.Quiz.open_quiz(quiz_name)
        game.Quiz.draw_quiz(game.screen, game.WIDTH, game.HEIGHT, game.draw_image)
        game.Quiz.check_answer(True)
        game.Quiz.draw_quiz(game.screen, game.WIDTH, game.HEIGHT, game.draw_image)
        game.close_quiz_with_key_animation()
        game.active_key_animation = None
    game.game_over = True
    for escaped in (True, False):
        game.escape = escaped
        game.draw()
    report = {
        "passed": True,
        "frozen": bool(getattr(sys, "frozen", False)),
        "resources": counts,
        "rooms": 6,
        "quizzes": len(game.Quiz.quizzes),
        "screens": ["start", "intro", "controls", "rooms", "items", "quizzes", "win", "gameover"],
    }
    output_index = sys.argv.index("--self-test-output") if "--self-test-output" in sys.argv else None
    if output_index is not None:
        Path(sys.argv[output_index + 1]).write_text(json.dumps(report, indent=2), encoding="utf-8")
    if sys.stdout is not None:
        print(json.dumps(report, indent=2))
