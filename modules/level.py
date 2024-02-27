import pygame
from modules.settings import *
from modules.tile import Tile
from modules.player import Player
from modules.attack import Attack
from modules.debug import debug
from modules.support import *
from modules.ui import UI
from modules.enemy import Enemy
from modules.comment import Comment


class Level:
    def __init__(self, level_name, exit_area):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = CameraGroup(level_name)
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.monsters_left = 0
        self.level_name = level_name
        self.exit_area = exit_area
        self.create_map(level_name)

        # user interface
        self.ui = UI()
        self.comments = []  # [Comment((500, 500), "Hello, world!")]

        # statistics
        self.deaths = 0
        self.kills = 0
        self.game_time = 0


    def create_map(self, level_name):
        layouts = {
            'stop': import_csv_layout(fixpath(f'levels/{level_name}/map_Stop.csv')),
            'detail': import_csv_layout(fixpath(f'levels/{level_name}/map_Details.csv')),
            'wall': import_csv_layout(fixpath(f'levels/{level_name}/map_Walls.csv')),
            'object': import_csv_layout(fixpath(f'levels/{level_name}/map_Objects.csv')),
            'entities': import_csv_layout(fixpath(f'levels/{level_name}/map_Entities.csv')),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    col = int(col)
                    if col != -1:
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'stop':
                            self.create_stop_blocks(col, x, y)
                        if style == 'wall':
                            Tile((x, y), [self.visible_sprites], 'wall', crop_tile(style, col))
                        # if style == 'detail':
                        #     Tile((x, y), [self.visible_sprites], 'detail', crop_tile(style, col))
                        if style == 'object':
                            Tile((x, y), [self.visible_sprites], 'object', crop_tile(style, col))
                        if style == 'entities':
                            if col == 0:
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack
                                )
                            else:
                                if col == 1: monster_name = 'slime'
                                elif col == 2: monster_name = 'cobra'
                                elif col == 8: monster_name = 'golem'
                                else: monster_name = 'slime'
                                self.monsters_left += 1
                                # elif col == 12: monster_name = 'cyclop'
                                # elif col == 13: monster_name = 'minotaur'
                                Enemy(
                                    monster_name,
                                    (x,y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                )
                            


        # 		if col == 'b':
        # 			Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
        # 		if col == 'p':
        # 			self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites)
        
    def create_attack(self, attack_type):
        self.current_attack = Attack(self.player, [self.visible_sprites, self.attack_sprites], attack_type)
        collision_sprites = pygame.sprite.spritecollide(self.current_attack,self.attackable_sprites,False)
        if collision_sprites:
            for target in collision_sprites:
                target.get_damage(self.player, self.current_attack.attack_type)
                if target.health <= 0:
                    self.monsters_left -= 1

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.current_attack:
            collision_sprites = pygame.sprite.spritecollide(self.current_attack, self.attackable_sprites,False)
            if collision_sprites:
                for target_sprite in collision_sprites:
                    target_sprite.get_damage(self.player, 'sword')

    def damage_player(self, amount):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            if 'hit' not in self.player.status:
                self.player.status = self.player.status.split('_')[0] + '_hit'
                self.player.frame_index = 0

    def create_stop_blocks(self, col, x, y):
        positions = []
        if col == 0:
            positions = [
                [x, y],
                [x + 16, y],
                [x, y + 16],
                [x + 16, y + 16]
            ]
        elif col == 1:
            positions = []
        elif col == 2:
            positions = [
                [x + 16, y],
                [x, y + 16]
            ]
        elif col == 3:
            positions = [
                [x, y],
                [x + 16, y + 16]
            ]
        elif col == 4:
            positions = [
                [x + 16, y],
                [x, y + 16],
                [x + 16, y + 16]
            ]
        elif col == 5:
            positions = [
                [x, y],
                [x, y + 16],
                [x + 16, y + 16]
            ]
        elif col == 6:
            positions = [
                [x, y],
                [x + 16, y],
                [x, y + 16],
            ]
        elif col == 7:
            positions = [
                [x, y],
                [x + 16, y],
                [x + 16, y + 16]
            ]
        elif col == 8:
            positions = [
                [x, y]
            ]
        elif col == 9:
            positions = [
                [x + 16, y]
            ]
        elif col == 10:
            positions = [
                [x, y]
            ]
        elif col == 11:
            positions = [
                [x, y + 16]
            ]
        elif col == 12:
            positions = [
                [x, y],
                [x + 16, y]
            ]
        elif col == 13:
            positions = [
                [x, y + 16],
                [x + 16, y + 16]
            ]
        elif col == 14:
            positions = [
                [x, y],
                [x, y + 16]
            ]
        elif col == 15:
            positions = [
                [x + 16, y],
                [x + 16, y + 16]
            ]

        for pos in positions:
            t = Tile(pos, [self.obstacle_sprites, self.visible_sprites], 'stop', pygame.Surface((16, 16), pygame.SRCALPHA, 32))
            # t.image.fill('red')

    def check_level_end(self):
        if self.player.health <= 0:
            return True, 'lose'
        if self.monsters_left == 0 and self.player.rect.colliderect(self.exit_area):
            return True, 'win'

        return False, 'still playing'

    def display_text(self, texts, delta):
        if 'start_time' not in self.__dict__:
            self.start_time = pygame.time.get_ticks()
        if 'counter' not in self.__dict__:
            self.counter = 0
        if self.counter >= len(texts):
            return
        if self.start_time + delta < pygame.time.get_ticks():
            self.counter += 1
            if self.counter >= len(texts):
                return
            self.start_time = pygame.time.get_ticks()

        text = texts[self.counter]
        font = pygame.font.Font('assets/fonts/joystix.ttf', 22)
        x, y = self.display_surface.get_size()

        self.text = font.render(text, False, TEXT_COLOR)
        self.rect = self.text.get_rect(bottomleft=((x - self.text.get_rect().width) // 2, y - 50))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.rect.inflate(20, 20))
        self.display_surface.blit(self.text, self.rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.rect.inflate(20, 20), 3)

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.display_text(['WELCOME, DMITRY SERGEEVICH!', '[W][A][S][D] IS YOUR MOVEMENT', '[SPACE] IS YOUR ATTACK'], 3000)
        self.ui.display(self.player)
        for comment in self.comments:
            comment.show()
        # print(self.check_level_end(), self.player.rect, self.exit_area, self.player.rect.colliderect(self.exit_area))


class CameraGroup(pygame.sprite.Group):
    def __init__(self, level_name):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = [0, 0]

        self.floor_surf = pygame.image.load(fixpath(f'levels/{level_name}/Floor.png')).convert()
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
