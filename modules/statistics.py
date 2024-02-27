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

