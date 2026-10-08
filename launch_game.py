"""Standalone entry point for the Pygame Zero game and packaged smoke test."""
import os
import sys
from pathlib import Path
from types import ModuleType


def main():
    self_test = "--self-test" in sys.argv
    if self_test:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

    import pygame
    from pgzero.runner import prepare_mod, run_mod

    root = Path(__file__).resolve().parent
    game_path = root / "Game.py"
    mod = ModuleType("escape_the_kue_game")
    mod.__file__ = str(game_path)
    sys.modules[mod.__name__] = mod
    prepare_mod(mod)
    exec(compile(game_path.read_text(encoding="utf-8"), str(game_path), "exec"), mod.__dict__)

    if self_test:
        from packaging_smoke import run
        run(mod, root)
        pygame.quit()
    else:
        run_mod(mod)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        import traceback
        import tempfile
        log_path = Path(tempfile.gettempdir()) / "Escape-the-KUE-error.log"
        log_path.write_text(traceback.format_exc(), encoding="utf-8")
        if "--self-test" not in sys.argv and getattr(sys, "frozen", False) and sys.platform == "win32":
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                None,
                "Das Spiel konnte nicht gestartet werden.\nFehlerbericht: " + str(log_path),
                "Escape the KUE", 0x10,
            )
        raise
