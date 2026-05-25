import math
import pygame


class NumberCombinationQuiz:
    def __init__(self, width, height, code="374"):
        self.code = code
        self.input_text = ""
        self.solved = False
        self.message = "Gib den 3-stelligen Code ein."

        self.overlay_rect = pygame.Rect(
            width * 0.1,
            height * 0.1,
            width * 0.8,
            height * 0.8,
        )

        button_width = self.overlay_rect.width * 0.28
        button_height = self.overlay_rect.height * 0.16
        self.button_rect = pygame.Rect(
            self.overlay_rect.centerx - button_width / 2,
            self.overlay_rect.bottom - button_height - 40,
            button_width,
            button_height,
        )

        self._wrong_sound = self._create_wrong_sound()

    def _create_wrong_sound(self):
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=1)
            except pygame.error:
                return None

        sample_rate = 22050
        duration = 0.22
        frequency = 220
        samples = int(sample_rate * duration)
        data = bytearray()

        for i in range(samples):
            t = i / sample_rate
            envelope = 1.0 - (i / samples)
            value = int(16000 * envelope * math.sin(2 * math.pi * frequency * t))
            data.extend(int(value).to_bytes(2, byteorder="little", signed=True))

        try:
            return pygame.mixer.Sound(buffer=bytes(data))
        except pygame.error:
            return None

    def _play_wrong_sound(self):
        if self._wrong_sound is not None:
            self._wrong_sound.play()

    def handle_key_down(self, key):
        key_name = ""
        if isinstance(key, int):
            key_name = pygame.key.name(key)
        else:
            key_name = str(key).lower().replace("keys.", "")

        if key_name in ["backspace"]:
            self.input_text = self.input_text[:-1]
            return

        normalized = key_name.replace("kp", "")
        if normalized.isdigit() and len(normalized) == 1:
            if len(self.input_text) < 3:
                self.input_text += normalized

    def handle_mouse_down(self, pos):
        if self.button_rect.collidepoint(pos):
            if self.input_text == self.code:
                self.solved = True
                self.message = "Richtig! Der Mechanismus ist geoeffnet."
            else:
                self.solved = False
                self.message = "Falsch! Bitte erneut versuchen."
                self._play_wrong_sound()

    def draw(self, screen):
        screen.draw.filled_rect(pygame.Rect(0, 0, screen.width, screen.height), (0, 0, 0, 170))
        screen.draw.filled_rect(self.overlay_rect, (25, 25, 40))
        screen.draw.rect(self.overlay_rect, "white")

        screen.draw.text(
            "Zahlenkombinationsschluss",
            center=(self.overlay_rect.centerx, self.overlay_rect.top + 60),
            fontsize=48,
            color="white",
        )

        screen.draw.text(
            self.message,
            center=(self.overlay_rect.centerx, self.overlay_rect.top + 120),
            fontsize=34,
            color="white",
        )

        code_display = (self.input_text + "___")[:3]
        screen.draw.text(
            "Code: " + " ".join(code_display),
            center=(self.overlay_rect.centerx, self.overlay_rect.centery - 20),
            fontsize=72,
            color="yellow",
        )

        button_color = (0, 180, 0) if self.solved else (120, 20, 20)
        screen.draw.filled_rect(self.button_rect, button_color)
        screen.draw.rect(self.button_rect, "white")
        screen.draw.text(
            "OEFFNEN",
            center=self.button_rect.center,
            fontsize=46,
            color="white",
        )
