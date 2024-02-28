import pygame
import sys

from modules.settings import *
from modules.support import *

import sqlite3


class Statistics:
    def __init__(self, player_id):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.background = pygame.image.load(
            fixpath("assets/images/main_menu.jpg")
        ).convert()

        width = self.display_surface.get_width()
        height = self.display_surface.get_height()

        self.normal_color = pygame.color.Color((255, 255, 255))
        self.hover_color = pygame.color.Color((210, 210, 210))
        self.active_color = pygame.color.Color((150, 50, 50))

        # buttons
        con = sqlite3.connect("data/database.sqlite")
        cur = con.cursor()

        kills, deaths = cur.execute(
        f"""
        SELECT kills, deaths FROM Games WHERE
        id = {player_id}
        """
        ).fetchone()

        self.kills_text = self.font.render("KILLS: " + str(kills), True, self.normal_color)
        self.kills_text_rect = self.kills_text.get_rect(
            center=(width * 0.5, height * 0.4)
        )

        self.deaths_text = self.font.render("DEATHS: " + str(deaths), True, self.normal_color)
        self.deaths_text_rect = self.deaths_text.get_rect(
            center=(width * 0.5, height * 0.5)
        )
        cur = con.cursor()
        cur.execute(
            f"""
                                                                UPDATE Games SET level=0, kills=0, deaths=0, time=0
                                                                WHERE id = {player_id}
                                                                """
        )
        con.commit()
        con.close()

        # self.kills_num_text = self.font.render(str(kills), True, self.normal_color)
        # self.kills_num_text_rect = self.kills_num_text.get_rect(
        #     center=(width * 0.6, height * 0.4)
        # )
        #
        # self.deaths_num_text = self.font.render(str(deaths), True, self.normal_color)
        # self.deaths_num_text_rect = self.deaths_num_text.get_rect(
        #     center=(width * 0.6, height * 0.7)
        # )

    def mouse_check(self, rect, pos):
        x, y = pos
        left, right, top, bottom = rect.left, rect.right, rect.top, rect.bottom
        return top <= y <= bottom and left <= x <= right

    def show(self):
        self.display_surface.blit(
            self.background, self.background.get_rect(topleft=(-350, 0))
        )
        self.display_surface.blit(self.kills_text, self.kills_text_rect)
        # self.display_surface.blit(self.kills_num_text, self.kills_num_text_rect)
        self.display_surface.blit(self.deaths_text, self.deaths_text_rect)
        # self.display_surface.blit(self.deaths_num_text, self.deaths_num_text_rect)
