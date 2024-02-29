import pygame
from modules.settings import *
from modules.entity import Entity
from modules.support import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player):

        # general setup
        super().__init__(groups)
        self.sprite_type = "enemy"

        # graphics setup
        self.import_graphics(monster_name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.hitbox.top += 10
        self.hitbox.height -= 10
        # if monster_name == 'cyclop':
        #     self.hitbox.top -= 30
        #     self.hitbox.height += 300

        self.obstacle_sprites = obstacle_sprites

        self.animation_move_speed = 0.15
        self.animation_idle_speed = 0.05
        self.animation_attack_speed = 0.3
        self.animation_hit_speed = 0.2
        self.animation_die_speed = 0.15

        self.save_direction = self.direction

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info["health"]
        self.exp = monster_info["exp"]
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["damage"]
        self.resistance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
        self.attack_type = monster_info["attack_type"]

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.stop_flag = False
        self.died = False

        self.vulnerable = True
        self.hit_time = 0
        self.vulnerability_duration = 600

        self.damage_player = damage_player

        self.sounds = {}

        sound_names = ['idle', 'move', 'attack', 'hit', 'die']
        for name in sound_names:
            try:
                self.sounds[name] = pygame.mixer.Sound(fixpath(f'assets/sounds/{self.monster_name}/{name}.mp3'))
                self.sounds[name].set_volume(0.2)
            except FileNotFoundError:
                pass

    def import_graphics(self, name):
        # print(fixpath(f'assets/images/enemies/{name}'))
        self.animations = {"idle": [], "move": [], "attack": [], "hit": [], "die": []}
        for p in next(walk(fixpath(f"assets/images/enemies/{name}")))[2]:
            for key in self.animations:
                if key in p:
                    self.animations[key].append(
                        pygame.image.load(fixpath(f"assets/images/enemies/{name}/{p}"))
                    )
                    break

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(
            (player.rect.center[0], player.rect.center[1] + 10)
        )
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        if self.status in ["hit", "die"]:
            return

        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"
            self.stop_flag = True
        elif distance <= self.notice_radius:
            self.status = "move"
            self.stop_flag = False

        else:
            self.status = "idle"

    def actions(self, player):
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage)
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1]
            self.save_direction = self.direction
        else:
            self.direction = pygame.math.Vector2()

    def get_damage(self, player, attack_type):
        if not self.vulnerable:
            return
        if self.status == "hit" or self.status == "die":
            return
        self.direction = self.get_player_distance_direction(player)[1]
        if attack_type == "sword":
            self.health -= player.stats["attack"]
        else:
            pass
        # print(self.health)
        if self.health <= 0:
            self.status = "die"
        else:
            self.status = "hit"
            self.hit_time = pygame.time.get_ticks()
        self.vulnerable = False
        self.frame_index = 0

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction = self.save_direction * (-self.resistance)
            # print(self.direction)
            # self.direction *= -500

    def play_sounds(self):
        if self.frame_index == 0:
            try:
                self.sound = self.sounds[self.status]
                self.sound.play()
            except KeyError:
                pass

    def animate(self):
        animation = self.animations[self.status]

        try:
            self.image = animation[int(self.frame_index)]
            if self.save_direction.x < 0:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.rect = self.image.get_rect(center=self.hitbox.center)
        except:
            print(int(self.frame_index), len(animation), self.status)

        if self.status == "idle":
            self.frame_index += self.animation_idle_speed
        elif self.status == "move":
            self.frame_index += self.animation_move_speed
        elif self.status == "attack":
            self.frame_index += self.animation_attack_speed
        elif self.status == "hit":
            self.frame_index += self.animation_hit_speed
        elif self.status == "die":
            self.frame_index += self.animation_die_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.status == "attack":
                self.can_attack = False
            if self.status == "hit":
                self.status = "move"
            if self.status == "die":
                self.died = True

        if self.died:
            self.kill()

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.vulnerability_duration:
                self.vulnerable = True

    def update(self):
        self.hit_reaction()
        # if not self.stop_flag:
        self.move(self.speed)
        self.play_sounds()
        self.animate()
        self.cooldown()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
