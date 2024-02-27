import pygame
import sys

from modules.settings import *
from modules.support import *

import sqlite3

class MainMenu:
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
        self.choosing_level = False
        self.in_settings = False

        self.menu_music = pygame.mixer.Sound(fixpath('assets/sounds/main_theme.mp3'))
        self.menu_music.play(loops=-1)
        self.menu_music.set_volume(0.1)


        # buttons

        self.btn_play = self.font.render("PLAY", True, self.normal_color)
        self.btn_play_rect = self.btn_play.get_rect(center=(half_width, height * 0.5))

        self.btn_open_settings = self.font.render("OPEN SETTINGS", True, self.normal_color)
        self.btn_open_settings_rect = self.btn_open_settings.get_rect(center=(half_width, height * 0.5 + 60))

        self.btn_show_statistics = self.font.render("SHOW STATISTICS", True, self.normal_color)
        self.btn_show_statistics_rect = self.btn_show_statistics.get_rect(center=(half_width, height * 0.5 + 120))

        self.btn_quit_game = self.font.render("QUIT", True, self.normal_color)
        self.btn_quit_game_rect = self.btn_quit_game.get_rect(center=(half_width, height * 0.5 + 180))

        self.FLAG = False

        self.create_settings_interface()

    def show_choose_level(self):
        con = sqlite3.connect(fixpath("data/database.sqlite"))
        cur = con.cursor()

        # titles = cur.execute("""SELECT title FROM categories""").fetchall()
        # cur.execute("""DELETE FROM categories WHERE title = ?""", (title,))

        games = cur.execute(f"""SELECT level FROM Games""").fetchall()

        con.close()


        width = self.display_surface.get_width()
        height = self.display_surface.get_height()

        self.place1 = pygame.image.load(fixpath('assets/images/new_game.png')).convert()
        self.place1_rect = self.place1.get_rect(center=(width * 0.25, height * 0.65))
        if games[0][0] == 0:
            text = "NEW GAME"
        else:
            text = "CONTINUE"
        self.place1_text = self.font.render(text, True, self.normal_color)
        self.place1_text_rect = self.place1_text.get_rect(center=(width * 0.25, height * 0.52))
        pygame.draw.rect(self.place1, self.normal_color, (0, 0, self.place1_rect.width, self.place1_rect.height), 4)

        self.place2 = pygame.image.load(fixpath('assets/images/new_game.png')).convert()
        self.place2_rect = self.place2.get_rect(center=(width * 0.5, height * 0.65))

        self.place3 = pygame.image.load(fixpath('assets/images/new_game.png')).convert()
        self.place3_rect = self.place3.get_rect(center=(width * 0.75, height * 0.65))

    def new_game(self):
        con = sqlite3.connect(fixpath("data/database.sqlite"))
        cur = con.cursor()

        # titles = cur.execute("""SELECT title FROM categories""").fetchall()
        # cur.execute("""DELETE FROM categories WHERE title = ?""", (title,))

        cur.execute(f"""
        UPDATE Games SET level = 1, kills = 0, deaths = 0, time = 0
        WHERE id = 1
        """)

        con.close()


    def continue_game(self):
        con = sqlite3.connect(fixpath("data/database.sqlite"))
        cur = con.cursor()

        # titles = cur.execute("""SELECT title FROM categories""").fetchall()
        # cur.execute("""DELETE FROM categories WHERE title = ?""", (title,))

        level = cur.execute(f"""
        SELECT level FROM Games
        WHERE id = 1
        """).fetchone()[0]

        con.close()

        return level, 1

    def open_settings(self):
        pass

    def show_statistics(self):
        pass

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def mouse_hover(self, pos):
        x, y = pos
        left1, right1, top1, bottom1 = self.btn_play_rect.left, self.btn_play_rect.right, self.btn_play_rect.top, self.btn_play_rect.bottom
        left2, right2, top2, bottom2 = self.btn_open_settings_rect.left, self.btn_open_settings_rect.right, self.btn_open_settings_rect.top, self.btn_open_settings_rect.bottom
        left3, right3, top3, bottom3 = self.btn_show_statistics_rect.left, self.btn_show_statistics_rect.right, self.btn_show_statistics_rect.top, self.btn_show_statistics_rect.bottom
        left4, right4, top4, bottom4 = self.btn_quit_game_rect.left, self.btn_quit_game_rect.right, self.btn_quit_game_rect.top, self.btn_quit_game_rect.bottom

        if self.mouse_pressed:
            color = self.active_color
        else:
            color = self.hover_color

        if top1 <= y <= bottom1 and left1 <= x <= right1:
            self.btn_play = self.font.render("PLAY", True, color)
        else:
            self.btn_play = self.font.render("PLAY", True, self.normal_color)
        if top2 <= y <= bottom2 and left2 <= x <= right2:
            self.btn_open_settings = self.font.render("OPEN SETTINGS", True, color)
        else:
            self.btn_open_settings = self.font.render("OPEN SETTINGS", True, self.normal_color)
        if top3 <= y <= bottom3 and left3 <= x <= right3:
            self.btn_show_statistics = self.font.render("SHOW STATISTICS", True, color)
        else:
            self.btn_show_statistics = self.font.render("SHOW STATISTICS", True, self.normal_color)
        if top4 <= y <= bottom4 and left4 <= x <= right4:
            self.btn_quit_game = self.font.render("QUIT", True, color)
        else:
            self.btn_quit_game = self.font.render("QUIT", True, self.normal_color)


    def mouse_press(self, pos):
        self.mouse_pressed = True
        self.mouse_hover(pos)

    def mouse_check(self, rect, pos):
        x, y = pos
        left, right, top, bottom = rect.left, rect.right, rect.top, rect.bottom
        return top <= y <= bottom and left <= x <= right

    def mouse_click(self, pos):
        self.mouse_pressed = False

        x, y = pos
        left1, right1, top1, bottom1 = self.btn_play_rect.left, self.btn_play_rect.right, self.btn_play_rect.top, self.btn_play_rect.bottom
        left2, right2, top2, bottom2 = self.btn_open_settings_rect.left, self.btn_open_settings_rect.right, self.btn_open_settings_rect.top, self.btn_open_settings_rect.bottom
        left3, right3, top3, bottom3 = self.btn_show_statistics_rect.left, self.btn_show_statistics_rect.right, self.btn_show_statistics_rect.top, self.btn_show_statistics_rect.bottom
        left4, right4, top4, bottom4 = self.btn_quit_game_rect.left, self.btn_quit_game_rect.right, self.btn_quit_game_rect.top, self.btn_quit_game_rect.bottom

        if self.mouse_pressed:
            color = self.active_color
        else:
            color = self.hover_color

        if top1 <= y <= bottom1 and left1 <= x <= right1:
            self.show_choose_level()
            self.choosing_level = True
        if top2 <= y <= bottom2 and left2 <= x <= right2:
            self.btn_open_settings = self.font.render("OPEN SETTINGS", True, color)
            self.FLAG = True
        if top3 <= y <= bottom3 and left3 <= x <= right3:
            self.btn_show_statistics = self.font.render("SHOW STATISTICS", True, color)
        if top4 <= y <= bottom4 and left4 <= x <= right4:
            self.quit_game()

    def create_settings_interface(self):
        x, y = self.display_surface.get_size()
        self.volume = self.font.render("Will be added soon", True, 'white')
        self.volume_rect = self.volume.get_rect(bottomleft=((x - self.volume.get_rect().width) // 2, y // 2))


    def show(self):
        self.display_surface.blit(self.background, self.background.get_rect(topleft=(-350, 0)))

        if self.FLAG:
            self.display_surface.blit(self.volume, self.volume_rect)
        else:
            if self.choosing_level:
                self.display_surface.blit(self.place1, self.place1_rect)
                self.display_surface.blit(self.place1_text, self.place1_text_rect)
                self.display_surface.blit(self.place2, self.place2_rect)
                self.display_surface.blit(self.place3, self.place3_rect)
            elif self.in_settings:
                pass
            else:
                self.display_surface.blit(self.btn_play, self.btn_play_rect)
                self.display_surface.blit(self.btn_open_settings, self.btn_open_settings_rect)
                self.display_surface.blit(self.btn_show_statistics, self.btn_show_statistics_rect)
                self.display_surface.blit(self.btn_quit_game, self.btn_quit_game_rect)

