"""Keep scaled fullscreen usable when SDL cannot create a GPU renderer."""
import os

import pygame
import pgzero.game
from pgzero.game import PGZeroGame


class CompatibleGame(PGZeroGame):
    software_fallback = False

    def reinit_screen(self):
        try:
            return super().reinit_screen()
        except pygame.error as error:
            if (self.software_fallback
                    or not pgzero.game.DISPLAY_FLAGS & pygame.SCALED
                    or "renderer" not in str(error).lower()):
                raise

            # Recreate the display before retrying the same logical dimensions
            # and scaled mouse coordinates with SDL's software renderer.
            cursor_visible = pygame.mouse.get_visible()
            pygame.display.quit()
            os.environ["SDL_RENDER_DRIVER"] = "software"
            pygame.display.init()
            self.width = self.height = self.icon = self.title = None
            self.software_fallback = True
            changed = super().reinit_screen()
            pygame.mouse.set_visible(cursor_visible)
            return changed
