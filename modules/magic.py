import os
import pygame
from modules.settings import *
from modules.support import *
from random import randint

class Magic(pygame.sprite.Sprite):
	def __init__(self, magic_type, pos, groups):
		super().__init__(groups)
		self.magic_type = magic_type
		self.image = self.resize_image(pygame.image.load(fixpath(f"assets/images/magic/{magic_type}/alpha.png")).convert_alpha())
		self.rect = self.image.get_rect(center=pos)

		self.animation_speed = 0.2
		self.animation_index = -7

		self.animation = []

		for i in range(len(next(os.walk(fixpath(f'assets/images/magic/{magic_type}')))[2]) - 1):
			self.animation.append(self.resize_image(pygame.image.load(fixpath(f"assets/images/magic/{magic_type}/{i}.png"))))

		print(len(self.animation))

	def resize_image(self, image):
		if self.magic_type == "heal":
			return image
		if self.magic_type == "earth":
			return pygame.transform.scale2x(image)
		if self.magic_type == "ice":
			return pygame.transform.scale2x(image)
		if self.magic_type == "fire":
			return pygame.transform.scale2x(image)
		if self.magic_type == "lightning":
			return pygame.transform.scale_by(image, 1.5)
		if self.magic_type == "dark":
			return pygame.transform.scale2x(image)



	def animate(self):
		self.animation_index += self.animation_speed
		if self.animation_index < 0:
			return
		if int(self.animation_index) >= len(self.animation):
			self.kill()
		else:
		    self.image = self.animation[int(self.animation_index)]

	def update(self):
		self.animate()


		# self.magic_type = magic_type
		# if magic_type == "heal":
		# 	self.
		# self.animation_player = animation_player
		# self.sounds = {
		# 'heal': pygame.mixer.Sound('../audio/heal.wav'),
		# 'flame':pygame.mixer.Sound('../audio/Fire.wav')
		# }

	# def heal(self,player,strength,cost,groups):
	# 	if player.energy >= cost:
	# 		# self.sounds['heal'].play()
	# 		player.health += strength
	# 		player.energy -= cost
	# 		if player.health >= player.stats['health']:
	# 			player.health = player.stats['health']
	# 		# self.animation_player.create_particles('aura',player.rect.center,groups)
	# 		# self.animation_player.create_particles('heal',player.rect.center,groups)
	#
	# def flame(self,player,cost,groups):
	# 	if player.energy >= cost:
	# 		player.energy -= cost
	# 		self.sounds['flame'].play()
	#
	# 		if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1,0)
	# 		elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1,0)
	# 		elif player.status.split('_')[0] == 'up': direction = pygame.math.Vector2(0,-1)
	# 		else: direction = pygame.math.Vector2(0,1)
	#
	# 		for i in range(1,6):
	# 			if direction.x: #horizontal
	# 				offset_x = (direction.x * i) * TILESIZE
	# 				x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
	# 				y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
	# 				self.animation_player.create_particles('flame',(x,y),groups)
	# 			else: # vertical
	# 				offset_y = (direction.y * i) * TILESIZE
	# 				x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
	# 				y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
	# 				self.animation_player.create_particles('flame',(x,y),groups)