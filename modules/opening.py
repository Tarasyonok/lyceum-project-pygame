import pygame
from settings import *

class Opening:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.story = [
            ("Hello", 500),
            ("world", 500),
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

    def show_story(self):
        self.start_opening()
        for text, delta in self.story:
            self.show_text(text, delta)
        self.end_opening()

    def cooldowns(self):
        curr_time = pygame.time.get_ticks()

        # что-то сравниваем