import pygame
from modules.settings import *
from modules.tile import Tile
from modules.player import Player
from modules.attack import Attack
from modules.debug import debug
from modules.support import *
from modules.ui import UI
from modules.enemy import Enemy


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self):
        layouts = {
            'stop': import_csv_layout(fixpath('levels/level0/map_FloorBlocks.csv')),
            'detail': import_csv_layout(fixpath('levels/level0/map_Details.csv')),
            'wall': import_csv_layout(fixpath('levels/level0/map_Walls.csv')),
            'object': import_csv_layout(fixpath('levels/level0/map_Objects.csv')),
            'entities': import_csv_layout(fixpath('levels/level0/map_Entities.csv')),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    col = int(col)
                    if col != -1:
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'stop':
                            Tile((x, y), [self.obstacle_sprites], 'stop')
                        if style == 'wall':
                            Tile((x, y), [self.visible_sprites], 'wall', crop_tile(style, col))
                        # if style == 'detail':
                        #     Tile((x, y), [self.visible_sprites], 'detail', crop_tile(style, col))
                        if style == 'object':
                            Tile((x, y), [self.visible_sprites], 'object', crop_tile(style, col))
                        if style == 'entities':
                            if col == 0:
                                self.player = Player(
                                    (400, 300),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack
                                )
                            else:
                                if col == 1: monster_name = 'slime'
                                elif col == 2: monster_name = 'cobra'
                                Enemy(
                                    monster_name,
                                    (x,y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites
                                )
                            


        # 		if col == 'b':
        # 			Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
        # 		if col == 'p':
        # 			self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites)
        
    def create_attack(self):
        self.current_attack = Attack(self.player, [self.visible_sprites, self.attack_sprites])
        collision_sprites = pygame.sprite.spritecollide(self.current_attack,self.attackable_sprites,False)
        if collision_sprites:
            for target in collision_sprites:
                target.get_damage()


    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            pass


    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)

        self.ui.display(self.player)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = [0, 0]

        self.floor_surf = pygame.image.load(fixpath('levels/level0/Floor.png')).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset[0] = player.rect.centerx - self.half_width
        self.offset[1] = player.rect.centery - self.half_height

        floor_offset_pos = [self.floor_rect.left - self.offset[0], self.floor_rect.top - self.offset[1]]
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = [sprite.rect.left - self.offset[0], sprite.rect.top - self.offset[1]]
            self.display_surface.blit(sprite.image, offset_pos)


    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for spite in enemy_sprites:
            spite.enemy_update(player)
