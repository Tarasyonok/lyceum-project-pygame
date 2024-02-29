import pygame
import sys

from modules.settings import *
from modules.support import *

import sqlite3


class MainMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.background = pygame.image.load(
            fixpath("assets/images/main_menu.jpg")
        ).convert()

        half_width = self.display_surface.get_width() // 2
        height = self.display_surface.get_height()

        self.logo_text = pygame.image.load(
            fixpath("assets/images/logo_text.png")
        ).convert_alpha()
        self.logo_text_rect = self.logo_text.get_rect(
            center=(half_width, height * 0.25)
        )

        self.normal_color = pygame.color.Color((255, 255, 255))
        self.hover_color = pygame.color.Color((180, 180, 180))
        self.active_color = pygame.color.Color((150, 100, 100))

        self.mouse_pressed = False
        self.choosing_level = None
        self.in_settings = False

        self.menu_music = pygame.mixer.Sound(fixpath("assets/sounds/main_theme.mp3"))
        self.menu_music.play(loops=-1)
        self.menu_music.set_volume(0.1)

        # buttons

        self.btn_play = self.font.render("PLAY", True, self.normal_color)
        self.btn_play_rect = self.btn_play.get_rect(center=(half_width, height * 0.6))

        self.btn_open_settings = self.font.render(
            "OPEN SETTINGS", True, self.normal_color
        )
        self.btn_open_settings_rect = self.btn_open_settings.get_rect(
            center=(half_width, height * 0.6 + 60)
        )
        self.btn_quit_game = self.font.render("QUIT", True, self.normal_color)
        self.btn_quit_game_rect = self.btn_quit_game.get_rect(
            center=(half_width, height * 0.6 + 120)
        )

        self.create_settings_interface()

    def show_choose_level(self):
        con = sqlite3.connect(fixpath("data/database.sqlite"))
        cur = con.cursor()

        # titles = cur.execute("""SELECT title FROM categories""").fetchall()
        # cur.execute("""DELETE FROM categories WHERE title = ?""", (title,))

        games = cur.execute(f"""SELECT level FROM Games""").fetchall()
        print(games)

        con.close()

        width = self.display_surface.get_width()
        height = self.display_surface.get_height()

        self.place1 = pygame.image.load(fixpath("assets/images/new_game.png")).convert()
        self.place1_rect = self.place1.get_rect(center=(width * 0.25, height * 0.65))
        if games[0][0] == 0:
            self.text = "NEW GAME"
        else:
            self.text = "CONTINUE"
        self.place1_text = self.font.render(self.text, True, self.normal_color)
        self.place1_text_rect = self.place1_text.get_rect(
            center=(width * 0.25, height * 0.52)
        )
        pygame.draw.rect(
            self.place1,
            self.normal_color,
            (0, 0, self.place1_rect.width, self.place1_rect.height),
            4,
        )

        self.place2 = pygame.image.load(fixpath("assets/images/new_game.png")).convert()
        self.place2_rect = self.place2.get_rect(center=(width * 0.5, height * 0.65))
        if games[1][0] == 0:
            self.text2 = "NEW GAME"
        else:
            self.text2 = "CONTINUE"
        self.place2_text = self.font.render(self.text2, True, self.normal_color)
        self.place2_text_rect = self.place2_text.get_rect(
            center=(width * 0.5, height * 0.52)
        )
        pygame.draw.rect(
            self.place2,
            self.normal_color,
            (0, 0, self.place2_rect.width, self.place2_rect.height),
            4,
        )

        self.place3 = pygame.image.load(fixpath("assets/images/new_game.png")).convert()
        self.place3_rect = self.place3.get_rect(center=(width * 0.75, height * 0.65))
        if games[2][0] == 0:
            self.text3 = "NEW GAME"
        else:
            self.text3 = "CONTINUE"
        self.place3_text = self.font.render(self.text3, True, self.normal_color)
        self.place3_text_rect = self.place3_text.get_rect(
            center=(width * 0.75, height * 0.52)
        )
        pygame.draw.rect(
            self.place3,
            self.normal_color,
            (0, 0, self.place3_rect.width, self.place3_rect.height),
            4,
        )

    def new_game(self, id):
        con = sqlite3.connect(fixpath("data/database.sqlite"))
        cur = con.cursor()

        # titles = cur.execute("""SELECT title FROM categories""").fetchall()
        # cur.execute("""DELETE FROM categories WHERE title = ?""", (title,))

        cur.execute(
            f"""
        UPDATE Games SET level = 1, kills = 0, deaths = 0, time = 0
        WHERE id = {id}
        """
        )

        con.close()

        self.choosing_level = False
        return 0

    def continue_game(self, id):
        con = sqlite3.connect(fixpath("data/database.sqlite"))
        cur = con.cursor()

        # titles = cur.execute("""SELECT title FROM categories""").fetchall()
        # cur.execute("""DELETE FROM categories WHERE title = ?""", (title,))

        level = cur.execute(
            f"""
        SELECT level FROM Games
        WHERE id = {id}
        """
        ).fetchone()[0]

        con.close()

        self.choosing_level = False
        return level

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def mouse_hover(self, pos):
        x, y = pos
        if self.mouse_pressed:
            color = self.active_color
        else:
            color = self.hover_color

        is_btn_hovered = False
        if self.mouse_check(self.btn_play_rect, pos):
            self.btn_play = self.font.render("PLAY", True, color)
            is_btn_hovered = True
        else:
            self.btn_play = self.font.render("PLAY", True, self.normal_color)
        if self.mouse_check(self.btn_open_settings_rect, pos):
            self.btn_open_settings = self.font.render("OPEN SETTINGS", True, color)
            is_btn_hovered = True
        else:
            self.btn_open_settings = self.font.render(
                "OPEN SETTINGS", True, self.normal_color
            )
        if self.mouse_check(self.btn_quit_game_rect, pos):
            self.btn_quit_game = self.font.render("QUIT", True, color)
            is_btn_hovered = True
        else:
            self.btn_quit_game = self.font.render("QUIT", True, self.normal_color)


    def mouse_press(self, pos):
        self.mouse_pressed = True
        self.choose_btn_sound.play()
        self.mouse_hover(pos)

    def mouse_check(self, rect, pos):
        x, y = pos
        left, right, top, bottom = rect.left, rect.right, rect.top, rect.bottom
        return top <= y <= bottom and left <= x <= right

    def mouse_click(self, pos):
        self.mouse_pressed = False

        if self.mouse_pressed:
            color = self.active_color
        else:
            color = self.hover_color

        if self.choosing_level is None:
            if self.mouse_check(self.btn_play_rect, pos):
                self.show_choose_level()
                self.choosing_level = True
            if self.mouse_check(self.btn_open_settings_rect, pos):
                self.btn_open_settings = self.font.render("OPEN SETTINGS", True, color)
                self.in_settings = True
            if self.mouse_check(self.btn_quit_game_rect, pos):
                self.quit_game()

    def mouse_choosing_click(self, pos):
        if self.mouse_check(self.place1_rect, pos):
            return 1, self.text
        if self.mouse_check(self.place2_rect, pos):
            return 2, self.text2
        if self.mouse_check(self.place3_rect, pos):
            return 3, self.text3

    def create_settings_interface(self):
        width, height = self.display_surface.get_size()
        self.volume = self.font.render("Will be added soon", True, "white")
        self.volume_rect = self.volume.get_rect(
            center=(width * 0.5, height * 0.6)
        )

    def show(self):
        self.display_surface.blit(
            self.background, self.background.get_rect(topleft=(-350, 0))
        )
        self.display_surface.blit(self.logo_text, self.logo_text_rect)

        if self.in_settings:
            self.display_surface.blit(self.volume, self.volume_rect)
        elif self.choosing_level:
            self.display_surface.blit(self.place1, self.place1_rect)
            self.display_surface.blit(self.place1_text, self.place1_text_rect)
            self.display_surface.blit(self.place2, self.place2_rect)
            self.display_surface.blit(self.place2_text, self.place2_text_rect)
            self.display_surface.blit(self.place3, self.place3_rect)
            self.display_surface.blit(self.place3_text, self.place3_text_rect)
        else:
            self.display_surface.blit(self.btn_play, self.btn_play_rect)
            self.display_surface.blit(
                self.btn_open_settings, self.btn_open_settings_rect
            )
            self.display_surface.blit(self.btn_quit_game, self.btn_quit_game_rect)
