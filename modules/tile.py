import pygame
from modules.settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        # self.image = pygame.image.load('bush.png').convert_alpha()
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.hitbox.top += 10
        self.hitbox.height -= 15
