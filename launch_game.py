"""Standalone entry point for the Pygame Zero game and packaged smoke test."""
import os
import sys
from pathlib import Path
from types import ModuleType


def main():
    self_test = "--self-test" in sys.argv
    startup_test = "--startup-test" in sys.argv
    if self_test:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
    if self_test or startup_test:
        os.environ["SDL_AUDIODRIVER"] = "dummy"
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

    import pygame
    from pgzero import runner
    from display_compat import CompatibleGame

    if startup_test:
        runner.DISPLAY_FLAGS |= pygame.HIDDEN

    root = Path(__file__).resolve().parent
    game_path = root / "Game.py"
    mod = ModuleType("escape_the_kue_game")
    mod.__file__ = str(game_path)
    sys.modules[mod.__name__] = mod
    runner.prepare_mod(mod)
    exec(compile(game_path.read_text(encoding="utf-8"), str(game_path), "exec"), mod.__dict__)

    if self_test:
        from packaging_smoke import run
        run(mod, root)
        pygame.quit()
    elif startup_test:
        import json
        import pgzero.game

        pgzero.game.DISPLAY_FLAGS |= pygame.HIDDEN
        runtime = CompatibleGame(mod)
        try:
            runtime.reinit_screen()
            runtime.load_handlers()
            mod.draw()
            pygame.display.flip()
            pygame.event.pump()
            report = {
                "passed": True,
                "frozen": bool(getattr(sys, "frozen", False)),
                "display_driver": pygame.display.get_driver(),
                "logical_size": list(runtime.screen.get_size()),
                "fullscreen": bool(pgzero.game.DISPLAY_FLAGS & pygame.FULLSCREEN),
                "scaled": bool(pgzero.game.DISPLAY_FLAGS & pygame.SCALED),
                "software_fallback": runtime.software_fallback,
            }
            output_index = sys.argv.index("--startup-test-output")
            Path(sys.argv[output_index + 1]).write_text(json.dumps(report, indent=2), encoding="utf-8")
            if sys.stdout is not None:
                print(json.dumps(report, indent=2))
        finally:
            pygame.quit()
    else:
        CompatibleGame(mod).run()


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
        if not any(flag in sys.argv for flag in ("--self-test", "--startup-test")) and getattr(sys, "frozen", False) and sys.platform == "win32":
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                None,
                "Das Spiel konnte nicht gestartet werden.\nFehlerbericht: " + str(log_path),
                "Escape the KUE", 0x10,
            )
        raise
