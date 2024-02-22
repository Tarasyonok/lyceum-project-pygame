import pygame

from modules.settings import *
from modules.support import *

class MainMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.background = pygame.image.load(fixpath('assets/images/main_menu.jpg')).convert()

        # buttons
        self.btn_new_game = ...
        self.btn_continue_game = ...
        self.btn_open_settings = ...
        self.btn_show_statistics = ...
        self.btn_quit_game = ...

    def new_game(self):
        pass

    def continue_game(self):
        pass

    def open_settings(self):
        pass

    def show_statistics(self):
        pass

    def quit_game(self):
        pygame.quit()
        quit()

    def show(self):
        self.display_surface.blit(self.background, self.background.get_rect(topleft=(0, 0)))