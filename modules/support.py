'''
Здесь вспомогательные функции
fixpath - чтобы пути работаи для виндовс и линукс одинаково
import_csv_layout - загрузка CSV карты в матрицу
crop_tile - выбирает нужный тайл по индексу
'''

from csv import reader
from os import path, walk
from modules.settings import *
import pygame


def fixpath(p):
    return path.abspath(path.expanduser(p))


def import_csv_layout(path):
    terrain_map = [] # создайм пустой массив
    with open(path) as level_map: # открываем CSV файл
        layout = reader(level_map, delimiter=',') # читаем его
        for row in layout:
            terrain_map.append(list(row)) # построчно завитываем в массив
        return terrain_map # возврат массива

main_tiles = pygame.image.load(fixpath('assets/images/tiles-images/main_tiles.png'))
decorative_tiles = pygame.image.load(fixpath('assets/images/tiles-images/decorative_tiles.png'))


def crop_tile(style, ID):
    if style == 'wall':
        tiles = main_tiles
        tile_posx, tile_posy = MAIN_TILE_IMAGES[ID]
    if style == 'detail' or style == 'object':
        tiles = decorative_tiles
        tile_posx, tile_posy = DECORATIVE_TILE_IMAGES[ID]

    tile_surf = pygame.Surface((TILESIZE, TILESIZE)).convert_alpha()
    tile_surf.fill((0, 0, 0, 0))
    tile_surf.blit(tiles, (0, 0),
                   (tile_posx, tile_posy, TILESIZE, TILESIZE))
    return tile_surf

# def import_enemy_images(monster_name):
#     print(monster_name)
#     d = {'idle': [], 'move': [], 'attack': [], 'hit': [], 'die': []}
#     for p in next(walk(fixpath(f'assets/images/enemies/{monster_name}')))[2]:
#         print(p)
#         for key in d:
#             if key in p:
#                 d[key].append(pygame.image.load(fixpath(f'assets/images/enemies/{monster_name}/{p}')))
#                 break
#     return d

# print(import_enemy_images('slime'))