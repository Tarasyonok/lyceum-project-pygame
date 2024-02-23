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

        half_width = self.display_surface.get_width()
        height = self.display_surface.get_height()

        self.background = pygame.surface.Surface((half_width, height))
        self.background_rect = self.background.get_rect(topleft=(0, 0))

        self.start_black = pygame.time.get_ticks()
        self.black_time = 1000

        self.start_opening_flag = True
        self.tell_story_flag = False
        self.end_opening_flag = False


    def start_opening(self):
        curr_time = pygame.time.get_ticks()
        if curr_time < self.start_black + self.black_time:
            self.background.set_alpha(self.black_time / curr_time * 255)
        else:
            self.background.set_alpha(255)
            self.start_opening_flag = False


    def show_text(self, text, delta):
        half_width = self.display_surface.get_width() // 2
        half_height = self.display_surface.get_height() // 2

        self.curr_text = self.font.render("SOMETHING", True, self.normal_color)
        self.curr_text_rect = self.curr_text.get_rect(center=(half_width, half_height))

    def end_opening(self):
        pass

    def tell_story(self):
        pass


    def display(self):
        if self.start_opening_flag:
            self.start_opening()
        elif self.tell_story_flag:
            self.tell_story()
        elif self.end_opening_flag:
            self.end_opening()
        self.display_surface.blit(self.background, self.background_rect)
        self.display_surface.blit(self.curr_text, self.curr_text_rect)