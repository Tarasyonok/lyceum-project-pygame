import pygame
from modules.settings import *


class Opening:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.story = [
            ("Kingdom of Elfrieden is the largest in the world.", 2000),
            ("All energy people use is extracting from magical crystals.", 2000),
            ("A lot of magical crystals quarried in the dungeon Aincrad.", 2000),
            ("One day a lot of miners didn't came back from the dungeon.", 2000),
            ("The survivors said, that they was murdered by monsters.", 2000),
            ("No one knew where these creatures came from", 2000),
            ("and none were prepared for there attack.", 2000),
            ("The King is sending you as the strongest warrior to the dungeon.", 2000),
            ("You must kill all monsters!", 2000),
        ]

        self.text_color = pygame.color.Color((255, 255, 255))

        width = self.display_surface.get_width()
        height = self.display_surface.get_height()

        self.background = pygame.surface.Surface((width, height))
        self.background_rect = self.background.get_rect(topleft=(0, 0))
        pygame.draw.rect(
            self.background, pygame.color.Color((0, 0, 0)), self.background_rect
        )

        self.curr_text = self.font.render("", True, self.text_color)
        self.curr_text_rect = self.curr_text.get_rect(
            center=(width * 0.5, height * 0.5)
        )

        self.start_black = pygame.time.get_ticks()
        self.black_time = 1000

        self.start_opening_flag = True
        self.tell_story_flag = False
        self.end_opening_flag = False

        self.text_index = 0

    def start_opening(self):
        curr_time = pygame.time.get_ticks()
        if curr_time < self.start_black + self.black_time:
            self.background.set_alpha(
                255 * ((curr_time - self.start_black) / self.black_time)
            )
        else:
            self.background.set_alpha(255)
            self.start_opening_flag = False
            self.tell_story_flag = True
            self.start_curr_text = pygame.time.get_ticks()
            self.curr_text_delay = self.story[self.text_index][1]
            self.pre_text_delay = 500
            self.end_text_delay = 500

            half_width = self.display_surface.get_width() // 2
            half_height = self.display_surface.get_height() // 2

            self.curr_text = self.font.render(
                self.story[self.text_index][0], True, self.text_color
            )
            self.curr_text_rect = self.curr_text.get_rect(
                center=(half_width, half_height)
            )

            self.curr_text.set_alpha(0)

    def tell_story(self):
        curr_time = pygame.time.get_ticks()
        if curr_time < self.start_curr_text + self.pre_text_delay:
            self.curr_text.set_alpha(
                255 * ((curr_time - self.start_curr_text) / self.pre_text_delay)
            )
        else:
            self.curr_text.set_alpha(255)

        if (
            0
            < curr_time
            - (self.start_curr_text + self.pre_text_delay + self.curr_text_delay)
            < self.end_text_delay
        ):
            self.curr_text.set_alpha(
                255
                - 255
                * (
                    (
                        curr_time
                        - self.start_curr_text
                        - self.pre_text_delay
                        - self.curr_text_delay
                    )
                    / self.end_text_delay
                )
            )
        elif (
            curr_time
            > self.start_curr_text
            + self.pre_text_delay
            + self.curr_text_delay
            + self.end_text_delay
        ):
            self.text_index += 1
            if self.text_index >= len(self.story):
                self.tell_story_flag = False
                self.end_opening_flag = True
                self.start_normal = pygame.time.get_ticks()
                self.normal_time = 1000
                return

            half_width = self.display_surface.get_width() // 2
            half_height = self.display_surface.get_height() // 2

            self.start_curr_text = pygame.time.get_ticks()
            self.curr_text_delay = self.story[self.text_index][1]

            self.curr_text = self.font.render(
                self.story[self.text_index][0], True, self.text_color
            )
            self.curr_text_rect = self.curr_text.get_rect(
                center=(half_width, half_height)
            )

            self.curr_text.set_alpha(0)

    def end_opening(self):
        curr_time = pygame.time.get_ticks()
        if curr_time < self.start_normal + self.normal_time:
            self.background.set_alpha(
                255 - 255 * ((curr_time - self.start_normal) / self.normal_time)
            )
        else:
            self.background.set_alpha(0)
            self.curr_text.set_alpha(0)
            self.end_opening_flag = False

    def display(self):
        if self.start_opening_flag:
            self.start_opening()
        elif self.tell_story_flag:
            self.tell_story()
        elif self.end_opening_flag:
            self.end_opening()
        self.display_surface.blit(self.background, self.background_rect)
        if self.tell_story_flag:
            self.display_surface.blit(self.curr_text, self.curr_text_rect)
