import pygame
import sys

from modules.settings import *
from modules.support import *

import sqlite3

class Statistics:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.background = pygame.image.load(fixpath('assets/images/main_menu.jpg')).convert()

        half_width = self.display_surface.get_width() // 2
        height = self.display_surface.get_height()

        self.normal_color = pygame.color.Color((255, 255, 255))
        self.hover_color = pygame.color.Color((210, 210, 210))
        self.active_color = pygame.color.Color((150, 50, 50))

        self.mouse_pressed = False
        self.choosing_level = None
        self.in_settings = False

        self.menu_music = pygame.mixer.Sound(fixpath('assets/sounds/main_theme.mp3'))
        self.menu_music.play(loops=-1)
        self.menu_music.set_volume(0.1)

        # buttons

        self.kills_text = self.font.render("KILLS", True, self.normal_color)
        self.kills_text_rect = self.kills_text.get_rect(center=(half_width, height * 0.5))

        self.deaths_text = self.font.render("DEATHS", True, self.normal_color)
        self.deaths_text_rect = self.deaths_text.get_rect(center=(half_width, height * 0.5 + 60))

        self.kills_num_text = self.font.render("xxx", True, self.normal_color)
        self.kills_num_text_rect = self.kills_num_text.get_rect(center=(half_width, height * 0.5 + 120))

        self.deaths_num_text = self.font.render("xxx", True, self.normal_color)
        self.deaths_num_text_rect = self.deaths_num_text.get_rect(center=(half_width, height * 0.5 + 180))

        self.btn_to_main_menu = self.font.render("xxx", True, self.normal_color)
        self.btn_to_main_menu_rect = self.btn_to_main_menu.get_rect(center=(half_width, height * 0.5 + 180))

    def mouse_check(self, rect, pos):
        x, y = pos
        left, right, top, bottom = rect.left, rect.right, rect.top, rect.bottom
        return top <= y <= bottom and left <= x <= right

    def show(self):
        self.display_surface.blit(self.background, self.background.get_rect(topleft=(-350, 0)))
        self.display_surface.blit(self.kills_text, self.kills_text_rect)
        self.display_surface.blit(self.kills_num_text, self.kills_num_text_rect)
        self.display_surface.blit(self.deaths_text, self.deaths_text_rect)
        self.display_surface.blit(self.deaths_num_text, self.deaths_num_text_rect)
        self.display_surface.blit(self.btn_to_main_menu, self.btn_to_main_menu_rect)
