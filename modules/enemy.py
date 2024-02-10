import pygame
from modules.settings import *
from modules.entity import Entity
from modules.support import *

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.copy()
        self.hitbox.top += 10
        self.hitbox.height -= 10
        self.obstacle_sprites = obstacle_sprites

        self.animation_move_speed = 0.15
        self.animation_idle_speed = 0.05
        self.animation_attack_speed = 1

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.stop_flag = False
        self.died = False

    def import_graphics(self,name):
        print(fixpath(f'assets/images/enemies/{name}'))
        self.animations = {'idle': [], 'move': [], 'attack': [], 'hit': [], 'die': []}
        for p in next(walk(fixpath(f'assets/images/enemies/{name}')))[2]:
            for key in self.animations:
                if key in p:
                    self.animations[key].append(pygame.image.load(fixpath(f'assets/images/enemies/{name}/{p}')))
                    break

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)

    def get_status(self, player):
        if self.status in ["hit", "die"]:
            return

        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
            self.stop_flag = True
        elif distance <= self.notice_radius:
            self.status = 'move'
            self.stop_flag = False

        else:
            self.status = 'idle'

    def actions(self,player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def get_damage(self,player):
        self.health -= 10
        if self.health <= 0:
            self.status = "die"
        else:
            self.status = "hit"

    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_idle_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        if self.status == "hit" and int(self.frame_index) == len(animation) - 1:
            self.status = "move"
        if self.status == "die" and int(self.frame_index) == len(animation) - 1:
            self.died = True
        if self.died:
            self.frame_index = len(animation) - 1
        self.image = animation[int(self.frame_index)]
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def cooldown(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    def update(self):
        if not self.stop_flag:
            self.move(self.speed)
        self.animate()
        self.cooldown()

    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)