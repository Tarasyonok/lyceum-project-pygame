import pygame
from modules.settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface.convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        if sprite_type == "stop":
            self.hitbox.top += 5
            self.hitbox.height -= 15
        else:
            self.hitbox.top += 10
            self.hitbox.height -= 15
