import pygame
from Map import *
from prop import prop_list
from sound import *

player_list = []

# 人物大小 50 * 50
class player(pygame.sprite.Sprite):
	def __init__(self, main_size, image_src, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image_src).convert_alpha()
		self.rect = self.image.get_rect()
		self.speed = 3
		self.alive = True
		self.width, self.height = main_size[0], main_size[1]
		self.pos = pos		# 人物在地图数组上的位置，pos[0]是行数， pos[1]是列数
		self.rect.left, self.rect.top = self.pos[1] * 50, self.pos[0] * 50
		self.mask = pygame.mask.from_surface(self.image)
		self.fire_num = 1		# 炸弹火力大小
		self.bomb_num = 1		# 总共能放的炸弹数
		self.temp = 0 # 判断是否需要发送拾取道具信息


	def move(self, key):
		if key == 1:  	# 向上移动
			# 上边是墙壁或炸弹的情况，向上走不动
			if(Map[self.pos[0] - 1][self.pos[1]] in ["@", "#", "$", "*"]):
				self.rect.top -= self.speed
				if(self.rect.top < self.pos[0] * 50):
					self.rect.top = self.pos[0] * 50
			else:
				# 如果卡在左半边墙,向右移动
				if((self.pos[1] * 50 - 25 < self.rect.left < self.pos[1] * 50) and (Map[self.pos[0] - 1][self.pos[1] - 1] in ["@", "#", "$", "*"]) and (self.rect.top - self.speed <= self.pos[0] * 50)):
					self.rect.left = self.rect.left + self.speed if (self.rect.left < self.pos[1] * 50 - self.speed) else self.pos[1] * 50
					self.top = self.pos[0] * 50
				# 如果卡在右半边墙，向左走
				elif((self.pos[1] * 50 < self.rect.left < self.pos[1] * 50 + 25) and (Map[self.pos[0] - 1][self.pos[1] + 1] in ["@", "#", "$", "*"]) and (self.rect.top - self.speed <= self.pos[0] * 50)):
					self.rect.left = self.rect.left - self.speed if (self.rect.left > self.pos[1] * 50 + self.speed) else self.pos[1] * 50
					self.top = self.pos[0] * 50
				else: # 向上走
					self.rect.top -= self.speed

		elif key == 2:	# 向下移动
			# 下边是墙壁或炸弹的情况，向下走不动
			if(Map[self.pos[0] + 1][self.pos[1]] in ["@", "#", "$", "*"]):
				self.rect.top += self.speed
				if(self.rect.top > self.pos[0] * 50):
					self.rect.top = self.pos[0] * 50
			else:
				# 如果卡在左半边墙,向右移动
				if((self.pos[1] * 50 - 25 < self.rect.left < self.pos[1] * 50) and (Map[self.pos[0] + 1][self.pos[1] - 1] in ["@", "#", "$", "*"]) and (self.rect.top + self.speed >= self.pos[0] * 50)):
					self.rect.left = self.rect.left + self.speed if (self.rect.left < self.pos[1] * 50 - self.speed) else self.pos[1] * 50
					self.top = self.pos[0] * 50
				# 如果卡在右半边墙,向左走
				elif((self.pos[1] * 50 < self.rect.left < self.pos[1] * 50 + 25) and (Map[self.pos[0] + 1][self.pos[1] + 1] in ["@", "#", "$", "*"]) and (self.rect.top + self.speed >= self.pos[0] * 50)):
					self.rect.left = self.rect.left - self.speed if (self.rect.left > self.pos[1] * 50 + self.speed) else self.pos[1] * 50
					self.top = self.pos[0] * 50
				else:	# 向下走
					self.rect.top += self.speed
					
		elif key == 3: 	# 向左移动
			# 左边是墙壁或炸弹的情况，向左走不动
			if(Map[self.pos[0]][self.pos[1] - 1] in ["@", "#", "$", "*"]):
				self.rect.left -= self.speed
				if(self.rect.left < self.pos[1] * 50):
					self.rect.left = self.pos[1] * 50
			else:
				# 如果卡在上半边墙,向下移动
				if((self.pos[0] * 50 - 25 < self.rect.top < self.pos[0] * 50) and (Map[self.pos[0] - 1][self.pos[1] - 1] in ["@", "#", "$", "*"]) and (self.rect.left - self.speed <= self.pos[1] * 50)):
					self.rect.top = self.rect.top + self.speed if (self.rect.top < self.pos[0] * 50 - self.speed) else self.pos[0] * 50
					self.left = self.pos[1] * 50
				# 如果卡在下半边墙，向上走
				elif((self.pos[0] * 50 < self.rect.top < self.pos[0] * 50 + 25) and (Map[self.pos[0] + 1][self.pos[1] - 1] in ["@", "#", "$", "*"]) and (self.rect.left - self.speed <= self.pos[1] * 50)):
					self.rect.top = self.rect.top - self.speed if (self.rect.top > self.pos[0] * 50 + self.speed) else self.pos[0] * 50
					self.left = self.pos[1] * 50
				else: # 向左走
					self.rect.left -= self.speed

		elif key == 4:	# 向右移动
			# 右边是墙壁或炸弹的情况，向左走不动
			if(Map[self.pos[0]][self.pos[1] + 1] in ["@", "#", "$", "*"]):
				self.rect.left += self.speed
				if(self.rect.left > self.pos[1] * 50):
					self.rect.left = self.pos[1] * 50
			else:
				# 如果卡在上半边墙,向下移动
				if((self.pos[0] * 50 - 25 < self.rect.top < self.pos[0] * 50) and (Map[self.pos[0] - 1][self.pos[1] + 1] in ["@", "#", "$", "*"]) and (self.rect.left + self.speed >= self.pos[1] * 50)):
					self.rect.top = self.rect.top + self.speed if (self.rect.top < self.pos[0] * 50 - self.speed) else self.pos[0] * 50
					self.left = self.pos[1] * 50
				# 如果卡在下半边墙，向上走
				elif((self.pos[0] * 50 < self.rect.top < self.pos[0] * 50 + 25) and (Map[self.pos[0] + 1][self.pos[1] - 1] in ["@", "#", "$", "*"]) and (self.rect.left + self.speed >= self.pos[1] * 50)):
					self.rect.top = self.rect.top - self.speed if (self.rect.top > self.pos[0] * 50 + self.speed) else self.pos[0] * 50
					self.left = self.pos[1] * 50
				else: # 向右走
					self.rect.left += self.speed

		self.pos[0] = (self.rect.top + 25) // 50
		self.pos[1] = (self.rect.left + 25) // 50

		if( Map[self.pos[0]][self.pos[1]] in ["1", "2", "3", "4", "%"]):	# 玩家碰到火焰和爆炸的炸弹则死亡
			self.alive = False

		self.pick_up_prop()
		
	def pick_up_prop(self):		# 检查人是否拾取了道具
		if(Map[self.pos[0]][self.pos[1]] in ["a", "b", "c"]):
			if(Map[self.pos[0]][self.pos[1]] == "a"):
				#self.bomb_num += 1
				self.temp = 6
			elif(Map[self.pos[0]][self.pos[1]] == "b"):
				#self.fire_num += 1
				self.temp = 7
			elif(Map[self.pos[0]][self.pos[1]] == "c"):
				#self.speed += .5
				self.temp = 8

			pick_up_prop_sound.play()
			change_map(self.pos, " ")

	def get_fire_num(self):
		return self.fire_num

	def get_bomb_num(self):
		return self.bomb_num

	def get_speed(self):
		return self.speed