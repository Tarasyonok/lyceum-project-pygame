import pygame
from modules.settings import *
from modules.support import *
from modules.debug import debug
from modules.entity import Entity

class Player(Entity):
    def __init__(self,pos,groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load(fixpath("assets/images/red-wizard/downidle1.png"))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.copy()
        self.hitbox.top += 13
        self.hitbox.height -= 13

        self.import_player_assets()

        self.status = 'down'

        self.animation_move_speed = 0.15
        self.animation_idle_speed = 0.05
        self.animation_attack_speed = 0.1

        self.direction = pygame.math.Vector2()
        self.save_direction = self.direction

        self.attacking = False
        self.attack_cooldown = 500
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'speed': 4}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

    def import_player_assets(self):
        self.pathes = {
            'up': ['upmove1', 'upmove2'],
            'down': ['downmove1', 'downmove2'],
            'left': ['leftmove1', 'leftmove2'],
            'right': ['rightmove1', 'rightmove2'],

            'downright': ['downrightmove1', 'downrightmove2'],
            'upright': ['uprightmove1', 'uprightmove2'],
            'upleft': ['upleftmove1', 'upleftmove2'],
            'downleft': ['downleftmove1', 'downleftmove2'],

            'up_idle': ['upidle1', 'upidle2'],
            'down_idle': ['downidle1', 'downidle2'],
            'left_idle': ['leftidle1', 'leftidle2'],
            'right_idle': ['rightidle1', 'rightidle2'],

            'downright_idle': ['downrightidle1', 'downrightidle2'],
            'upright_idle': ['uprightidle1', 'uprightidle2'],
            'upleft_idle': ['upleftidle1', 'upleftidle2'],
            'downleft_idle': ['downleftidle1', 'downleftidle2'],

            'up_attack': ['upsword1', 'upsword2', 'upsword3', 'upsword4'],
            'down_attack': ['downsword1', 'downsword2', 'downsword3', 'downsword4'],
            'left_attack': ['leftsword1', 'leftsword2', 'leftsword3', 'leftsword4'],
            'right_attack': ['rightsword1', 'rightsword2', 'rightsword3', 'rightsword4'],

            'downright_attack': ['downrightsword1', 'downrightsword2', 'downrightsword3', 'downrightsword4'],
            'upright_attack': ['uprightsword1', 'uprightsword2', 'uprightsword3', 'uprightsword4'],
            'upleft_attack': ['upleftsword1', 'upleftsword2', 'upleftsword3', 'upleftsword4'],
            'downleft_attack': ['downleftsword1', 'downleftsword2', 'downleftsword3', 'downleftsword4'],
        }

        self.animations = {}

        for s in self.pathes:
            self.animations[s] = []
            for p in self.pathes[s]:
                self.animations[s].append(pygame.image.load(fixpath(f'assets/images/red-wizard/{p}.png')))

    def input(self):
        if self.attacking:
            return
        keys = pygame.key.get_pressed()

        part2 = ''
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction[0] = 1
            part2 = 'right'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction[0] = -1
            part2 = 'left'
        else:
            self.direction[0] = 0

        part1 = ''
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction[1] = 1
            part1 = 'down'
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction[1] = -1
            part1 = 'up'
        else:
            self.direction[1] = 0

        if self.direction != [0, 0]:
            self.save_direction = self.direction[:]

        if part1 + part2 != '':
            self.status = part1 + part2

        if keys[pygame.K_SPACE]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack('sword')
            # attack

        if keys[pygame.K_1]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack('magic')
            # magic

    def get_status(self):
        if self.direction[0] == 0 and self.direction[1] == 0:
            if 'idle' not in self.status and 'attack' not in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction = pygame.math.Vector2()
            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')


    def cooldowns(self):
        curr_time = pygame.time.get_ticks()

        if self.attacking:
            if curr_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        if 'idle' in self.status:
            animation_speed = self.animation_idle_speed
        elif 'attack' in self.status:
            animation_speed = self.animation_attack_speed
        else:
            animation_speed = self.animation_move_speed
        self.frame_index += animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if 'attack' in self.status:
                self.attacking = False
                return
                # self.status.replace()

        # self.the image
        self.image = animation[int(self.frame_index)]
        if 'attack' in self.status and int(self.frame_index) == 3:
            self.destroy_attack()
        self.rect = self.image.get_rect(center=self.hitbox.center)



    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
