'''
Я сделал комментарии в файлах, чтобы понимать, что где происходит
main.py запускает игру

Здесь всё понятно, импортируем нужные библиотеки, и создаём класс Game
Можно было бы просто запускить игру в коде но для баллов за модульность оставим так

У класса Game есть __init__ и run
В ините настраиваем игру.
В методе run запускаем главный цикл отлавливаем выход и запускаем уровень

Здесь обьяснение, на всякий
https://proproprogs.ru/modules/chto-takoe-pygame-karkas-prilozheniya-fps
'''

import pygame, sys
from modules.settings import *
from modules.level import Level
from modules.start_menu import MainMenu
from modules.opening import Opening
from modules.debug import debug


class Game:
    def __init__(self):

        # general setup
        pygame.init()  # инициализируем pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))  # создаём экран
        pygame.display.set_caption('Dungeon runner')  # задаём заголовок

        # -------------------------------------
        # Вот тебе задание: выбери и отобрази иконку на окне игры
        # -------------------------------------

        self.clock = pygame.time.Clock()  # создаём инструмент тиков
        # 'prod2', exit_area
        # self.level = Level('prod2', exit_area) # заггружаем уровень (Потом будем менять, т. к. уровней много. Здесь будет заставка)
        self.main_menu = MainMenu()

        self.levels = [
            ('level0', pygame.rect.Rect(0, 0, 10000, 10000)),
            ('prod2', pygame.rect.Rect(0, 0, 10000, 10000)),
        ]
        self.level_index = 0

        self.curr_level = Level(*self.levels[self.level_index])

        self.start_game = True
        self.start_opening = False

    def run(self):
        while True: # Главный цикл
            # Здесь выход по нажатию крестика
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    if not self.start_opening:
                        self.main_menu.mouse_hover(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.main_menu.mouse_press(event.pos)
                # if event.type == pygame.MOUSEBUTTONUP:
                #     if event.button == 1:
                #         self.main_menu.mouse_click(event.pos)
                #         self.opening = Opening()
                #         self.start_opening = True
                #         pygame.mouse.set_visible(False)
                        # self.start_game = True

            # self.screen.fill((200, 200, 200)) # цвет фона


            if self.start_game:
                self.screen.fill((10, 9, 9)) # цвет фона
                self.curr_level.run() # запускаем уровень
                game_result = self.curr_level.check_level_end()
                if game_result[0] == True:
                    if game_result[1] == 'win':
                        self.level_index += 1
                    self.curr_level = Level(*self.levels[self.level_index])
            else:
                self.main_menu.show()

            if self.start_opening:
                self.opening.display()
                if (not self.opening.start_opening_flag
                        and not self.opening.tell_story_flag):
                    self.start_game = True
                if (not self.opening.start_opening_flag
                        and not self.opening.tell_story_flag
                        and not self.opening.end_opening_flag):
                    self.start_opening = False
                    pygame.mouse.set_visible(True)


            pygame.display.update() # обновляем экран, а то просто чёрное всё будет
            self.clock.tick(FPS) # параметр 60 указывает выполнять цикл while 60 раз в секунду


if __name__ == '__main__':
    game = Game() # Создаём игру
    game.run() # Запускаем её
