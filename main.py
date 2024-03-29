"""
Я сделал комментарии в файлах, чтобы понимать, что где происходит
main.py запускает игру

Здесь всё понятно, импортируем нужные библиотеки, и создаём класс Game
Можно было бы просто запускить игру в коде но для баллов за модульность оставим так

У класса Game есть __init__ и run
В ините настраиваем игру.
В методе run запускаем главный цикл отлавливаем выход и запускаем уровень

Здесь обьяснение, на всякий
https://proproprogs.ru/modules/chto-takoe-pygame-karkas-prilozheniya-fps
"""

import pygame, sys
from modules.settings import *
from modules.level import Level
from modules.start_menu import MainMenu
from modules.opening import Opening
from modules.debug import debug
from modules.support import *
from modules.statistics import Statistics
import sqlite3


class Game:
    def __init__(self):

        # general setup
        pygame.init()  # инициализируем pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))  # создаём экран
        pygame.display.set_caption("Dungeon runner")  # задаём заголовок
        pygame.display.set_icon(pygame.image.load(fixpath("assets/images/red-wizard/downmagic1.png")).convert_alpha())

        # -------------------------------------
        # Вот тебе задание: выбери и отобрази иконку на окне игры
        # -------------------------------------

        self.clock = pygame.time.Clock()  # создаём инструмент тиков
        # 'prod2', exit_area
        # self.level = Level('prod2', exit_area) # заггружаем уровень (Потом будем менять, т. к. уровней много. Здесь будет заставка)
        self.main_menu = MainMenu()

        self.levels = [
            ("prod_levels/level1", pygame.rect.Rect(1888, 1088, 160, 64)),
            ("prod_levels/level2", pygame.rect.Rect(416, 96, 160, 64)),
            ("prod_levels/level3", pygame.rect.Rect(416, 96, 160, 64)),
            ("prod_levels/level4", pygame.rect.Rect(416, 96, 160, 64)),
            ("prod_levels/level5", pygame.rect.Rect(2912, 192, 160, 64)),
        ]

        self.curr_level = None

        self.swith_to_new_level = False

        self.status = "mainmenu"
        # statuses: mainmenu, opening, playing, statistics, choosing, settings

        self.display_surface = pygame.display.get_surface()
        self.set_black_overlay()
        self.set_back_to_main_menu()
        self.set_cursor()

        self.menu_music = pygame.mixer.Sound(fixpath("assets/sounds/main_theme.mp3"))
        self.menu_music.set_volume(0.3)

        self.main_level_sound = pygame.mixer.Sound(fixpath(f'assets/sounds/main_level.mp3'))
        self.main_level_sound.set_volume(0.3)

        self.boss_level_sound = pygame.mixer.Sound(fixpath(f'assets/sounds/boss_level.mp3'))
        self.boss_level_sound.set_volume(0.3)

        self.curr_sound = self.menu_music
        self.curr_sound.play(loops=-1)

    def set_cursor(self):
        pygame.mouse.set_visible(False)
        self.normal_cursor = pygame.image.load(
            fixpath("assets/images/cursor/normal.png")
        ).convert_alpha()
        self.active_cursor = pygame.image.load(
            fixpath("assets/images/cursor/active.png")
        ).convert_alpha()
        self.game_normal_cursor = pygame.image.load(
            fixpath("assets/images/cursor/game_normal.png")
        ).convert_alpha()
        self.game_active_cursor = pygame.image.load(
            fixpath("assets/images/cursor/game_active.png")
        ).convert_alpha()
        self.cursor = self.normal_cursor
        self.cursor_rect = None
        self.show_cursor = True
        self.click_sound = pygame.mixer.Sound(fixpath(f'assets/sounds/interface/hover.mp3'))
        self.click_sound.set_volume(0.3)

    def set_back_to_main_menu(self):
        width = self.display_surface.get_width()
        height = self.display_surface.get_height()

        font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.btn_back_to_main_menu = font.render("back", True, self.normal_color)
        self.btn_back_to_main_menu_rect = self.btn_back_to_main_menu.get_rect(
            bottomleft=(50, height - 30)
        )

    def mouse_check(self, rect, pos):
        x, y = pos
        left, right, top, bottom = rect.left, rect.right, rect.top, rect.bottom
        return top <= y <= bottom and left <= x <= right

    def set_black_overlay(self):
        width = self.display_surface.get_width()
        height = self.display_surface.get_height()

        self.black_time = 500
        self.normal_time = 500
        self.black_overlay = pygame.surface.Surface((width, height))
        self.black_overlay_rect = self.black_overlay.get_rect(topleft=(0, 0))
        pygame.draw.rect(
            self.black_overlay, pygame.color.Color((0, 0, 0)), self.black_overlay_rect
        )
        self.black_overlay.set_alpha(0)

        self.start_normal = None
        self.start_black = None
        # self.start_normal = pygame.time.get_ticks()
        # self.start_black = pygame.time.get_ticks()

        self.normal_color = pygame.color.Color((255, 255, 255))
        self.hover_color = pygame.color.Color((210, 210, 210))
        self.active_color = pygame.color.Color((150, 50, 50))

    def start_black_overlay(self):
        curr_time = pygame.time.get_ticks()
        if curr_time < self.start_black + self.black_time:
            self.black_overlay.set_alpha(
                255 * ((curr_time - self.start_black) / self.black_time)
            )
        else:
            self.black_overlay.set_alpha(255)
            self.start_black = None
            self.swith_to_new_level = True

            self.status = self.want_status
            if self.status == "playing":
                self.level_index = self.main_menu.continue_game(self.game_id)
                self.curr_level = Level(*self.levels[self.level_index])
                self.status = "playing"

            self.start_normal = pygame.time.get_ticks()

    def end_black_overlay(self):
        curr_time = pygame.time.get_ticks()
        if curr_time < self.start_normal + self.normal_time:
            self.black_overlay.set_alpha(
                255 - 255 * ((curr_time - self.start_normal) / self.normal_time)
            )
        else:
            self.black_overlay.set_alpha(0)
            self.start_normal = None

    def save_game(self, is_win, add_kills, is_died, time):
        con = sqlite3.connect(fixpath("data/database.sqlite"))
        cur = con.cursor()

        level, kills, deaths = cur.execute(
            f"""
        SELECT level, kills, deaths from Games
        WHERE id = {self.curr_player}
        """
        ).fetchone()

        level += is_win
        kills += add_kills
        deaths += is_died

        cur.execute(
            f"""
        UPDATE Games SET level={level}, kills={kills}, deaths={deaths}, time={time}
        WHERE id = {self.curr_player}
        """
        )

        con.commit()

        con.close()

    def run(self):
        while True:  # Главный цикл
            # Здесь выход по нажатию крестика
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    if not pygame.mouse.get_focused():
                        self.cursor_rect = None
                    else:
                        if self.cursor == self.game_active_cursor:
                            self.cursor_rect = self.cursor.get_rect(center=(event.pos))
                        else:
                            self.cursor_rect = self.cursor.get_rect(topleft=(event.pos))
                    if self.status == "mainmenu":
                        self.main_menu.mouse_hover(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)
                    if self.status == "opening":
                        continue
                    if event.button == 1 and self.show_cursor and self.cursor != self.game_active_cursor:
                        self.cursor = self.active_cursor
                        self.click_sound.play()

                if event.type == pygame.MOUSEBUTTONUP:

                    if self.cursor != self.game_active_cursor:
                        self.cursor = self.normal_cursor
                    if self.curr_level and self.curr_level.show_pause_menu:
                        if self.mouse_check(self.curr_level.back_to_game_rect, event.pos):
                            self.curr_level.show_pause_menu = False
                            self.curr_level.player.block_keybord = False
                            # self.show_cursor = False
                            self.cursor = self.game_active_cursor
                        elif self.mouse_check(self.curr_level.return_to_menu_rect, event.pos):
                            kills = self.curr_level.can_kill - len(self.curr_level.attackable_sprites)
                            self.save_game(
                                0, kills, 0, "time"
                            )
                            self.curr_level = None
                            self.status = "mainmenu"
                            self.main_menu.choosing_level = None
                            self.curr_sound.stop()
                            self.curr_sound = self.menu_music
                            self.curr_sound.play(loops=-1)
                        continue
                    if self.mouse_check(self.btn_back_to_main_menu_rect, event.pos):
                        self.status = "mainmenu"
                        self.main_menu.choosing_level = None
                        self.main_menu.in_settings = None
                        # self.show_cursor = True
                    if event.button == 1:
                        if self.main_menu.choosing_level:
                            click_info = self.main_menu.mouse_choosing_click(event.pos)
                            if click_info:
                                # self.show_cursor = False
                                self.cursor = self.game_active_cursor
                                self.game_id, text = click_info
                                self.curr_player = self.game_id
                                if text == "NEW GAME":
                                    self.level_index = self.main_menu.new_game(self.game_id) - 1
                                    self.curr_level = Level(
                                        *self.levels[self.level_index]
                                    )
                                    self.opening = Opening()
                                    self.status = "opening"
                                elif text == "CONTINUE":
                                    # self.start_black = pygame.time.get_ticks()
                                    self.status = "playing"
                                    self.level_index = self.main_menu.continue_game(self.game_id)
                                    self.curr_level = Level(*self.levels[self.level_index])
                                self.curr_sound.stop()
                                if self.level_index == len(self.levels) - 1:
                                    self.curr_sound = self.boss_level_sound
                                else:
                                    self.curr_sound = self.main_level_sound
                                self.curr_sound.play(loops=-1)
                        else:
                            self.main_menu.mouse_click(event.pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.status == "opening":
                            self.status = "playing"
                        elif self.curr_level:
                            self.curr_level.show_pause_menu = True
                            self.curr_level.player.block_keybord = True
                            self.show_cursor = True
                            self.cursor = self.normal_cursor
                            self.curr_level.pause_overlay.set_alpha(200)
                            self.curr_level.show_pause_menu = True
                        else:
                            self.status = "mainmenu"
                            self.main_menu.choosing_level = None
                            self.main_menu.in_settings = None

            if self.status == "mainmenu":
                self.main_menu.show()
            elif self.status == "opening":
                self.show_cursor = False
                self.opening.display()
                if (
                    not self.opening.start_opening_flag
                    and not self.opening.tell_story_flag
                ):
                    self.playing_game = True
                if (
                    not self.opening.start_opening_flag
                    and not self.opening.tell_story_flag
                    and not self.opening.end_opening_flag
                ):
                    self.status = "playing"
                    self.start_normal = pygame.time.get_ticks()
                    self.black_overlay.set_alpha(0)
                    self.end_black_overlay()
                    self.show_cursor = True
                    self.cursor = self.game_active_cursor
            elif self.status == "playing":
                self.show_cursor = True
                self.screen.fill((10, 9, 9))  # цвет фона
                self.curr_level.run()  # запускаем уровень
                game_result = self.curr_level.check_level_end()
                if game_result[0] == True:
                    # self.start_black = pygame.time.get_ticks() and not self.swith_to_new_level
                    print("kills", self.curr_level.kills)
                    self.save_game(
                        game_result[1] == "win", self.curr_level.kills, game_result[1] == "lose", "time"
                    )
                    if game_result[1] == "win":
                        self.level_index += 1
                    if self.level_index >= len(self.levels):
                        self.show_cursor = True
                        self.status = "statistics"
                        self.statistics = Statistics(self.curr_player)
                        self.curr_level = None
                    else:
                        self.curr_level = Level(*self.levels[self.level_index])

                    if self.level_index == len(self.levels) - 1 and self.curr_sound != self.boss_level_sound:
                        self.curr_sound.stop()
                        self.curr_sound = self.boss_level_sound
                        self.curr_sound.play(loops=-1)

            elif self.status == "statistics":
                self.cursor = self.normal_cursor
                self.statistics.show()
                self.display_surface.blit(
                    self.btn_back_to_main_menu, self.btn_back_to_main_menu_rect
                )

            if self.main_menu.choosing_level or self.main_menu.in_settings:
                self.display_surface.blit(
                    self.btn_back_to_main_menu, self.btn_back_to_main_menu_rect
                )

            if self.start_black:
                self.start_black_overlay()
            if self.start_normal:
                self.end_black_overlay()
            self.display_surface.blit(self.black_overlay, self.black_overlay_rect)
            if self.cursor_rect and self.show_cursor:
                self.display_surface.blit(self.cursor, self.cursor_rect)

            pygame.display.update()  # обновляем экран, а то просто чёрное всё будет
            self.clock.tick(
                FPS
            )  # параметр 60 указывает выполнять цикл while 60 раз в секунду


if __name__ == "__main__":
    game = Game()  # Создаём игру
    game.run()  # Запускаем её
