'''
Здесь вспомогательные функции
fixpath - чтобы пути работаи для виндовс и линукс одинаково
import_csv_layout - загрузка CSV карты в матрицу
crop_tile - выбирает нужный тайл по индексу
'''

from csv import reader
# from os import walk
from os import path
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
