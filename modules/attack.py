import pygame

class Attack(pygame.sprite.Sprite):
    def __init__(self, player, groups, attack_type):
        super().__init__(groups)
        self.attack_type = attack_type
        dir_x, dir_y = player.save_direction

        if dir_x > 0 and dir_y == 0:
            self.image = pygame.Surface((35, player.rect.height))
            self.rect = self.image.get_rect(left=player.hitbox.center[0], top=player.rect.top)
        elif dir_x < 0 and dir_y == 0:
            self.image = pygame.Surface((35, player.rect.height))
            self.rect = self.image.get_rect(right=player.hitbox.center[0], top=player.rect.top)
        elif dir_x == 0 and dir_y < 0:
            self.image = pygame.Surface((28, player.rect.height))
            self.rect = self.image.get_rect(right=player.rect.right, bottom=player.hitbox.center[1])
        elif dir_x == 0 and dir_y > 0:
            self.image = pygame.Surface((28, player.rect.height))
            self.rect = self.image.get_rect(right=player.rect.right, top=player.hitbox.center[1])
        elif dir_x > 0 and dir_y > 0:
            self.image = pygame.Surface((player.rect.width, player.rect.width))
            self.rect = self.image.get_rect(left=player.hitbox.center[0], top=player.hitbox.center[1])
        elif dir_x > 0 and dir_y < 0:
            self.image = pygame.Surface((player.rect.width, player.rect.width))
            self.rect = self.image.get_rect(left=player.hitbox.center[0], bottom=player.hitbox.center[1])
        elif dir_x < 0 and dir_y < 0:
            self.image = pygame.Surface((player.rect.width, player.rect.width))
            self.rect = self.image.get_rect(right=player.hitbox.center[0], bottom=player.hitbox.center[1])
        elif dir_x < 0 and dir_y > 0:
            self.image = pygame.Surface((player.rect.width, player.rect.width))
            self.rect = self.image.get_rect(right=player.hitbox.center[0], top=player.hitbox.center[1])

        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))