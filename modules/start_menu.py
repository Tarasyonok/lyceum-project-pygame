import pygame
import sys

from modules.settings import *
from modules.support import *

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


        # buttons

        self.btn_new_game = self.font.render("NEW GAME", True, self.normal_color)
        self.btn_new_game_rect = self.btn_new_game.get_rect(center=(half_width, height * 0.5))

        self.btn_continue_game = self.font.render("CONTINUE GAME", True, self.normal_color)
        self.btn_continue_game_rect = self.btn_continue_game.get_rect(center=(half_width, height * 0.5 + 60))

        self.btn_open_settings = self.font.render("OPEN SETTINGS", True, self.normal_color)
        self.btn_open_settings_rect = self.btn_open_settings.get_rect(center=(half_width, height * 0.5 + 120))

        self.btn_show_statistics = self.font.render("SHOW STATISTICS", True, self.normal_color)
        self.btn_show_statistics_rect = self.btn_show_statistics.get_rect(center=(half_width, height * 0.5 + 180))

        self.btn_quit_game = self.font.render("QUIT", True, self.normal_color)
        self.btn_quit_game_rect = self.btn_quit_game.get_rect(center=(half_width, height * 0.5 + 240))


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
        sys.exit()

    def mouse_hover(self, pos):
        x, y = pos
        left1, right1, top1, bottom1 = self.btn_new_game_rect.left, self.btn_new_game_rect.right, self.btn_new_game_rect.top, self.btn_new_game_rect.bottom
        left2, right2, top2, bottom2 = self.btn_continue_game_rect.left, self.btn_continue_game_rect.right, self.btn_continue_game_rect.top, self.btn_continue_game_rect.bottom
        left3, right3, top3, bottom3 = self.btn_open_settings_rect.left, self.btn_open_settings_rect.right, self.btn_open_settings_rect.top, self.btn_open_settings_rect.bottom
        left4, right4, top4, bottom4 = self.btn_show_statistics_rect.left, self.btn_show_statistics_rect.right, self.btn_show_statistics_rect.top, self.btn_show_statistics_rect.bottom
        left5, right5, top5, bottom5 = self.btn_quit_game_rect.left, self.btn_quit_game_rect.right, self.btn_quit_game_rect.top, self.btn_quit_game_rect.bottom

        if self.mouse_pressed:
            color = self.active_color
        else:
            color = self.hover_color

        if top1 <= y <= bottom1 and left1 <= x <= right1:
            self.btn_new_game = self.font.render("NEW GAME", True, color)
        else:
            self.btn_new_game = self.font.render("NEW GAME", True, self.normal_color)
        if top2 <= y <= bottom2 and left2 <= x <= right2:
            self.btn_continue_game = self.font.render("CONTINUE GAME", True, color)
        else:
            self.btn_continue_game = self.font.render("CONTINUE GAME", True, self.normal_color)
        if top3 <= y <= bottom3 and left3 <= x <= right3:
            self.btn_open_settings = self.font.render("OPEN SETTINGS", True, color)
        else:
            self.btn_open_settings = self.font.render("OPEN SETTINGS", True, self.normal_color)
        if top4 <= y <= bottom4 and left4 <= x <= right4:
            self.btn_show_statistics = self.font.render("SHOW STATISTICS", True, color)
        else:
            self.btn_show_statistics = self.font.render("SHOW STATISTICS", True, self.normal_color)
        if top5 <= y <= bottom5 and left5 <= x <= right5:
            self.btn_quit_game = self.font.render("QUIT", True, color)
        else:
            self.btn_quit_game = self.font.render("QUIT", True, self.normal_color)


    def mouse_press(self, pos):
        self.mouse_pressed = True
        self.mouse_hover(pos)

    def mouse_click(self, pos):
        pass

    def show(self):
        self.display_surface.blit(self.background, self.background.get_rect(topleft=(-350, 0)))
        self.display_surface.blit(self.btn_new_game, self.btn_new_game_rect)
        self.display_surface.blit(self.btn_continue_game, self.btn_continue_game_rect)
        self.display_surface.blit(self.btn_open_settings, self.btn_open_settings_rect)
        self.display_surface.blit(self.btn_show_statistics, self.btn_show_statistics_rect)
        self.display_surface.blit(self.btn_quit_game, self.btn_quit_game_rect)

