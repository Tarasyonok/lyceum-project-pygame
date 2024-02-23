import pygame
from modules.settings import *

class Opening:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.story = [
            "Hello",
            "world",
        ]

    def start_opening(self):
        pass

    def show_text(self, text, delta):
        half_width = self.display_surface.get_width() // 2
        half_height = self.display_surface.get_height() // 2

        self.curr_text = self.font.render("SOMETHING", True, self.normal_color)
        self.curr_text_rect = self.curr_text.get_rect(center=(half_width, half_height))

    def end_opening(self):
        # Убираем чёрное затемнение
        pass

    def display(self):
        self.display_surface.blit(self.curr_text, self.curr_text_rect)