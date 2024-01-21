WIDTH = 1280
HEIGTH = 720
FPS = 60
# TILESIZE = 64
TILESIZE = 32

MAIN_TILE_IMAGES = {}

ID = 0
for y in range(47):
    for x in range(51):
        # print(x, y)
        MAIN_TILE_IMAGES[ID] = (x * TILESIZE, y * TILESIZE)
        # TILE_IMAGES[ID] = (x, y)
        ID += 1

DECORATIVE_TILE_IMAGES = {}

ID = 0
for y in range(29):
    for x in range(13):
        # print(x, y)
        DECORATIVE_TILE_IMAGES[ID] = (x * TILESIZE, y * TILESIZE)
        # TILE_IMAGES[ID] = (x, y)
        ID += 1
