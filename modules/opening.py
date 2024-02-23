import pygame
from settings *

class Opening:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.story = [
            "Hello",
            "world",
        ]

    def start_opening(self):
        # Замемняем экран до чёрного цвета
        pass

    def show_text(self, text, delta):
        # Показывает текст text на экране на пормежуток времени delta
        pass

    def end_opening(self):
        # Убираем чёрное затемнение
        pass