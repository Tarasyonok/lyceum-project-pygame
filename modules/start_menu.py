import pygame

from modules.settings import *
from modules.support import *

class MainMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.background = pygame.image.load(fixpath('assets/images/main_menu.jpg')).convert()

        self.button_area = ...

        # buttons
        self.btn_new_game = self.font.render("NEW GAME", True, TEXT_COLOR)
        self.btn_new_game_rect = self.btn_new_game.get_rect(topleft=(30, 150))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.btn_new_game_rect, 3)

        self.btn_continue_game = self.font.render("CONTINUE GAME", True, TEXT_COLOR)
        self.btn_continue_game_rect = self.btn_continue_game.get_rect(topleft=(30, 200))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.btn_continue_game_rect, 3)

        self.btn_open_settings = self.font.render("OPEN SETTINGS", True, TEXT_COLOR)
        self.btn_open_settings_rect = self.btn_open_settings.get_rect(topleft=(30, 250))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.btn_open_settings_rect, 3)

        self.btn_show_statistics = self.font.render("SHOW STATISTICS", True, TEXT_COLOR)
        self.btn_show_statistics_rect = self.btn_show_statistics.get_rect(topleft=(30, 300))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.btn_show_statistics_rect, 3)

        self.btn_quit_game = self.font.render("QUIT", True, TEXT_COLOR)
        self.btn_quit_game_rect = self.btn_quit_game.get_rect(topleft=(30, 350))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.btn_quit_game_rect, 3)

    def mouse_move(self, pos):
        x, y = pos
        left1, right1, top1, bottom1 = self.btn_new_game_rect.left, self.btn_new_game_rect.right, self.btn_new_game_rect.top, self.btn_new_game_rect.bottom
        left2, right2, top2, bottom2 = self.btn_continue_game_rect.left, self.btn_continue_game_rect.right, self.btn_continue_game_rect.top, self.btn_continue_game_rect.bottom
        left3, right3, top3, bottom3 = self.btn_open_settings_rect.left, self.btn_open_settings_rect.right, self.btn_open_settings_rect.top, self.btn_open_settings_rect.bottom
        left4, right4, top4, bottom4 = self.btn_show_statistics_rect.left, self.btn_show_statistics_rect.right, self.btn_show_statistics_rect.top, self.btn_show_statistics_rect.bottom
        left5, right5, top5, bottom5 = self.btn_quit_game_rect.left, self.btn_quit_game_rect.right, self.btn_quit_game_rect.top, self.btn_quit_game_rect.bottom

        if top1 <= y <= bottom1 and left1 <= x <= right1:
            print("NEW GAME")
        elif top2 <= y <= bottom2 and left2 <= x <= right2:
            print("CONTINUE GAME")
        elif top3 <= y <= bottom3 and left3 <= x <= right3:
            print("OPEN SETTINGS")
        elif top4 <= y <= bottom4 and left4 <= x <= right4:
            print("SHOW STATISTICS")
        elif top5 <= y <= bottom5 and left5 <= x <= right5:
            print("QUIT")


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

        surf_alpha = pygame.Surface((325, 270))
        pygame.draw.rect(surf_alpha, (0, 0, 0), (20, 140, 325, 270))
        surf_alpha.set_alpha(128)
        self.display_surface.blit(surf_alpha, surf_alpha.get_rect(topleft=(20, 140)))
        self.display_surface.blit(self.btn_new_game, self.btn_new_game_rect)
        self.display_surface.blit(self.btn_continue_game, self.btn_continue_game_rect)
        self.display_surface.blit(self.btn_open_settings, self.btn_open_settings_rect)
        self.display_surface.blit(self.btn_show_statistics, self.btn_show_statistics_rect)
        self.display_surface.blit(self.btn_quit_game, self.btn_quit_game_rect)