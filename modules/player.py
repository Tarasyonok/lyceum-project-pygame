import pygame
from modules.settings import *
from modules.support import *
from modules.debug import debug
from modules.entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load(
            fixpath("assets/images/red-wizard/downidle1.png")
        )
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.hitbox.top += 17
        self.hitbox.height -= 10

        self.import_player_assets()

        self.status = "up_idle"
        self.prev_status = "up_idle"

        self.animation_move_speed = 0.15
        self.animation_idle_speed = 0.05
        self.animation_attack_speed = 0.1
        self.animation_magic_speed = 0.1
        self.animation_hit_speed = 0.1
        self.animation_die_speed = 0.2

        self.direction = pygame.math.Vector2()
        self.save_direction = [0, 1]

        self.attacking = False
        self.attack_cooldown = 500
        self.attack_time = None

        self.doing_magic = False
        self.magic_cooldown = 500
        self.magic_time = None

        self.obstacle_sprites = obstacle_sprites

        self.stats = {"health": 200, "attack": 20, "energy": 100, "magic": 6, "speed": 4}
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.speed = self.stats["speed"]

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.create_magic = create_magic

        self.vulnerable = True
        self.hurt_time = None
        self.vulnerability_duration = 700

        self.sounds = {
            # 'idle': pygame.mixer.Sound(fixpath(f'assets/sounds/player/idle.mp3')),
            "move": pygame.mixer.Sound(fixpath(f"assets/sounds/player/move.mp3")),
            "attack": pygame.mixer.Sound(fixpath(f"assets/sounds/player/attack.mp3")),
            "hit": pygame.mixer.Sound(fixpath(f"assets/sounds/player/hit.mp3")),
            # 'die': pygame.mixer.Sound(fixpath(f'assets/sounds/player/die.mp3')),
        }

        self.play_sound = False
        self.block_keybord = False

        self.is_died = False

    def import_player_assets(self):
        self.pathes = {
            "up": ["upmove1", "upmove2"],
            "down": ["downmove1", "downmove2"],
            "left": ["leftmove1", "leftmove2"],
            "right": ["rightmove1", "rightmove2"],
            "downright": ["downrightmove1", "downrightmove2"],
            "upright": ["uprightmove1", "uprightmove2"],
            "upleft": ["upleftmove1", "upleftmove2"],
            "downleft": ["downleftmove1", "downleftmove2"],
            "up_idle": ["upidle1", "upidle2"],
            "down_idle": ["downidle1", "downidle2"],
            "left_idle": ["leftidle1", "leftidle2"],
            "right_idle": ["rightidle1", "rightidle2"],
            "downright_idle": ["downrightidle1", "downrightidle2"],
            "upright_idle": ["uprightidle1", "uprightidle2"],
            "upleft_idle": ["upleftidle1", "upleftidle2"],
            "downleft_idle": ["downleftidle1", "downleftidle2"],
            "up_attack": ["upsword1", "upsword2", "upsword3", "upsword4"],
            "down_attack": ["downsword1", "downsword2", "downsword3", "downsword4"],
            "left_attack": ["leftsword1", "leftsword2", "leftsword3", "leftsword4"],
            "right_attack": [
                "rightsword1",
                "rightsword2",
                "rightsword3",
                "rightsword4",
            ],
            "downright_attack": [
                "downrightsword1",
                "downrightsword2",
                "downrightsword3",
                "downrightsword4",
            ],
            "upright_attack": [
                "uprightsword1",
                "uprightsword2",
                "uprightsword3",
                "uprightsword4",
            ],
            "upleft_attack": [
                "upleftsword1",
                "upleftsword2",
                "upleftsword3",
                "upleftsword4",
            ],
            "downleft_attack": [
                "downleftsword1",
                "downleftsword2",
                "downleftsword3",
                "downleftsword4",
            ],

            "up_magic": ["upmagic1", "upmagic2", "upmagic3", "upmagic4"],
            "down_magic": ["downmagic1", "downmagic2", "downmagic3", "downmagic4"],
            "left_magic": ["leftmagic1", "leftmagic2", "leftmagic3", "leftmagic4"],
            "right_magic": [
                "rightmagic1",
                "rightmagic2",
                "rightmagic3",
                "rightmagic4",
            ],
            "downright_magic": [
                "downrightmagic1",
                "downrightmagic2",
                "downrightmagic3",
                "downrightmagic4",
            ],
            "upright_magic": [
                "uprightmagic1",
                "uprightmagic2",
                "uprightmagic3",
                "uprightmagic4",
            ],
            "upleft_magic": [
                "upleftmagic1",
                "upleftmagic2",
                "upleftmagic3",
                "upleftmagic4",
            ],
            "downleft_magic": [
                "downleftmagic1",
                "downleftmagic2",
                "downleftmagic3",
                "downleftmagic4",
            ],

            "up_hit": ["uphit1", "uphit2"],
            "down_hit": ["downhit1", "downhit2"],
            "left_hit": ["lefthit1", "lefthit2"],
            "right_hit": ["righthit1", "righthit2"],
            "downright_hit": ["downrighthit1", "downrighthit2"],
            "upright_hit": ["uprighthit1", "uprighthit2"],
            "upleft_hit": ["uplefthit1", "uplefthit2"],
            "downleft_hit": ["downlefthit1", "downlefthit2"],
        }

        self.animations = {}

        for s in self.pathes:
            self.animations[s] = []
            for p in self.pathes[s]:
                self.animations[s].append(
                    pygame.image.load(fixpath(f"assets/images/red-wizard/{p}.png"))
                )

    def input(self):
        if self.block_keybord:
            return
        if self.attacking or self.doing_magic:
            return
        if self.status == "hit" or self.status == "die":
            return
        keys = pygame.key.get_pressed()

        part2 = ""
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction[0] = 1
            part2 = "right"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction[0] = -1
            part2 = "left"
        else:
            self.direction[0] = 0

        part1 = ""
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction[1] = 1
            part1 = "down"
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction[1] = -1
            part1 = "up"
        else:
            self.direction[1] = 0

        if self.direction != [0, 0]:
            self.save_direction = self.direction[:]

        if part1 + part2 != "":
            self.prev_status = self.status
            self.status = part1 + part2

        if keys[pygame.K_SPACE]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack("sword")
            # attack

        if keys[pygame.K_1]:
            self.doing_magic = True
            self.magic_time = pygame.time.get_ticks()
            self.create_magic("heal")
            self.health += magic_data["heal"]["strength"]
            if self.health > self.stats["health"]:
                self.health = self.stats["health"]

        if keys[pygame.K_2]:
            self.doing_magic = True
            self.magic_time = pygame.time.get_ticks()
            self.create_magic("earth")

        if keys[pygame.K_3]:
            self.doing_magic = True
            self.magic_time = pygame.time.get_ticks()
            self.create_magic("ice")

        if keys[pygame.K_4]:
            self.doing_magic = True
            self.magic_time = pygame.time.get_ticks()
            self.create_magic("fire")

        if keys[pygame.K_5]:
            self.doing_magic = True
            self.magic_time = pygame.time.get_ticks()
            self.create_magic("lightning")

        if keys[pygame.K_6]:
            self.doing_magic = True
            self.magic_time = pygame.time.get_ticks()
            self.create_magic("dark")



        # if keys[pygame.K_F1]:
        #     self.stats = {'health': 10000, 'energy': 10000, 'attack': 10000, 'speed': 4}
        #     self.health = self.stats['health']
        #     self.energy = self.stats['energy']
        #     self.exp = 10000
        #     self.speed = self.stats['speed']

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def get_status(self):
        self.prev_status = self.status
        if "hit" in self.status:
            return
        if self.direction[0] == 0 and self.direction[1] == 0:
            if "idle" not in self.status and "attack" not in self.status and "magic" not in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
            self.status = self.status.replace("_magic", "")
            self.direction = pygame.math.Vector2()
            if "attack" not in self.status:
                self.frame_index = 0
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

        if self.doing_magic and not self.attacking:
            self.status = self.status.replace("_attack", "")
            self.direction = pygame.math.Vector2()
            if "magic" not in self.status:
                self.frame_index = 0
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_magic")
                else:
                    self.status = self.status + "_magic"
        else:
            if "magic" in self.status:
                self.status = self.status.replace("_magic", "")

        if self.prev_status != self.status:
            self.frame_index = 0

    def cooldowns(self):
        curr_time = pygame.time.get_ticks()

        if self.attacking:
            if curr_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if self.doing_magic:
            if curr_time - self.magic_time >= self.magic_cooldown:
                self.doing_magic = False

        if not self.vulnerable:
            if curr_time - self.hurt_time >= self.vulnerability_duration:
                self.vulnerable = True

    def play_sounds(self):
        if self.frame_index == 0:
            try:
                if "idle" in self.status:
                    sound_name = "idle"
                elif "attack" in self.status:
                    sound_name = "attack"
                elif "magic" in self.status:
                    sound_name = "magic"
                elif "hit" in self.status:
                    sound_name = "hit"
                elif "die" in self.status:
                    sound_name = "die"
                else:  # move
                    sound_name = "move"
                if self.play_sound:
                    self.sound.stop()
                self.sound = self.sounds[sound_name]
                self.sound.play()
                self.play_sound = True
            except KeyError:
                pass

    def animate(self):
        # loop over frame index
        animation = self.animations[self.status]

        if self.prev_status != self.status:
            self.frame_index == 0
        # print(int(self.frame_index))
        try:
            self.image = animation[int(self.frame_index)]
            if "magic" in self.status:
                self.rect = self.image.get_rect(topleft=self.hitbox.topleft )
            else:
                self.rect = self.image.get_rect(center=self.hitbox.center)
        except:
            print(int(self.frame_index), len(animation), self.status)

        if "idle" in self.status:
            self.frame_index += self.animation_idle_speed
        elif "attack" in self.status:
            self.frame_index += self.animation_attack_speed
        elif "magic" in self.status:
            self.frame_index += self.animation_magic_speed
        elif "hit" in self.status:
            self.frame_index += self.animation_hit_speed
        elif "die" in self.status:
            self.frame_index += self.animation_die_speed
        else:  # move
            self.frame_index += self.animation_move_speed

        if int(self.frame_index) >= len(animation):
            self.frame_index = 0
            if "attack" in self.status:
                self.attacking = False
                self.destroy_attack()
            if "magic" in self.status:
                self.doing_magic = False
            if "hit" in self.status:
                self.status = self.status.replace("_hit", "")

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.play_sounds()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()
