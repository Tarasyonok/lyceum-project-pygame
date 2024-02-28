import pygame
from modules.settings import *


class Comment:
    def __init__(self, pos, text):
        self.pos = pos
        self.text = text

        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.display_surface = pygame.display.get_surface()
        self.size = 0

    def show(self):
        text_surf = self.font.render(self.text, True, TEXT_COLOR)
        # x = self.display_surface.get_size()[0] - 20
        # y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(topleft=self.pos)
        # text_rect.height *= self.size
        # text_rect.width *= self.size

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        # self.display_surface.blit(text_surf, (0, 0), (self.pos[0], self.pos[1], text_surf.get_width(), text_surf.get_height()))
        # self.display_surface.blit(text_surf, (0, 0), text_rect)
        pygame.draw.rect(
            self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3
        )

        self.size += 0.01

    def close(self):
        self.kill()

    # def display(self):
