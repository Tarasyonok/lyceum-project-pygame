WIDTH = 1280
HEIGTH = 720
FPS = 60
# TILESIZE = 64
TILESIZE = 32

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = "assets/fonts/icekingdom.ttf"
UI_FONT_SIZE = 40

# general colors
WATER_COLOR = "#71ddee"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

# ui colors
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

monster_data = {
    "slime": {
        "health": 30,
        "exp": 20,
        "damage": 10,
        "attack_type": None,
        "attack_sound": None,
        "speed": 1,
        "resistance": 10,
        "attack_radius": 30,
        "notice_radius": 300,
    },
    "cobra": {
        "health": 50,
        "exp": 20,
        "damage": 15,
        "attack_type": None,
        "attack_sound": None,
        "speed": 1,
        "resistance": 10,
        "attack_radius": 30,
        "notice_radius": 300,
    },
    "golem": {
        "health": 150,
        "exp": 100,
        "damage": 25,
        "attack_type": None,
        "attack_sound": None,
        "speed": 2,
        "resistance": 1,
        "attack_radius": 35,
        "notice_radius": 400,
    },
    "cyclop": {
        "health": 200,
        "exp": 2000,
        "damage": 75,
        "attack_type": None,
        "attack_sound": None,
        "speed": 0,
        "resistance": 2,
        "attack_radius": 50,
        "notice_radius": 500,
    },
    "minotaur": {
        "health": 500,
        "exp": 2000,
        "damage": 50,
        "attack_type": None,
        "attack_sound": None,
        "speed": 1,
        "resistance": 0,
        "attack_radius": 80,
        "notice_radius": 500,
    },
}

magic_data = {
	'heal' : {'strength': 20,'cost': 10},
    'earth': {'strength': 20,'cost': 10},
    'ice': {'strength': 30,'cost': 15},
    'fire': {'strength': 40,'cost': 20},
    'lightning': {'strength': 60,'cost': 30},
    'dark': {'strength': 100,'cost': 40},
}


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
