import pygame
from modules.settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface.convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        if sprite_type == 'stop':
            self.hitbox.top += HITBOX_OFFSET['stop'][0]
            self.hitbox.height -= HITBOX_OFFSET['stop'][1]
            pass
        else:
            self.hitbox.top += HITBOX_OFFSET[sprite_type][0]
            self.hitbox.height -= HITBOX_OFFSET[sprite_type][1]
