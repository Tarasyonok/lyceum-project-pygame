import pygame
from modules.settings import *
from modules.tile import Tile
from modules.player import Player
from modules.debug import debug
from modules.support import *


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        layouts = {
            'stop': import_csv_layout(fixpath('levels/level0/map_FloorBlocks.csv')),
            'detail': import_csv_layout(fixpath('levels/level0/map_Details.csv')),
            'wall': import_csv_layout(fixpath('levels/level0/map_Walls.csv')),
            'object': import_csv_layout(fixpath('levels/level0/map_Objects.csv')),
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
        # 		if col == 'b':
        # 			Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
        # 		if col == 'p':
        # 			self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites)
        self.player = Player((400, 300), [self.visible_sprites], self.obstacle_sprites)
        pygame.display.flip()

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


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
