import pygame

class Attack(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        dir_x, dir_y = player.save_direction

        # pl_h = player.image.height
        # print(pl_h)

        # self.image = pygame.Surface((200, 200))
        # self.image.fill((255, 0, 0))
        # self.rect = self.image.get_rect(left=0, top=0)
        if dir_x > 0 and dir_y == 0:
            self.image = pygame.Surface((35, player.rect.height))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(left=player.hitbox.center[0], top=player.rect.top)
        elif dir_x < 0 and dir_y == 0:
            self.image = pygame.Surface((35, player.rect.height))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(right=player.hitbox.center[0], top=player.rect.top)
        elif dir_x == 0 and dir_y < 0:
            self.image = pygame.Surface((28, player.rect.height))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(right=player.rect.right, bottom=player.hitbox.center[1])
        elif dir_x == 0 and dir_y > 0:
            self.image = pygame.Surface((28, player.rect.height))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(right=player.rect.right, top=player.hitbox.center[1])
        elif dir_x > 0 and dir_y > 0:
            self.image = pygame.Surface((player.rect.width, player.rect.width))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(left=player.hitbox.center[0], top=player.hitbox.center[1])
        elif dir_x > 0 and dir_y < 0:
            self.image = pygame.Surface((player.rect.width, player.rect.width))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(left=player.hitbox.center[0], bottom=player.hitbox.center[1])
        elif dir_x < 0 and dir_y < 0:
            self.image = pygame.Surface((player.rect.width, player.rect.width))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(right=player.hitbox.center[0], bottom=player.hitbox.center[1])
        elif dir_x < 0 and dir_y > 0:
            self.image = pygame.Surface((player.rect.width, player.rect.width))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(right=player.hitbox.center[0], top=player.hitbox.center[1])