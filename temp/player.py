import pygame
from Map import *

player_list = []

# 人物大小 50 * 50
class player(pygame.sprite.Sprite):
	def __init__(self, main_size, image_src, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image_src).convert_alpha()
		self.rect = self.image.get_rect()
		self.speed = 10
		self.alive = True
		self.width, self.height = main_size[0], main_size[1]
		self.pos = pos		# 人物在地图数组上的位置，pos[0]是行数， pos[1]是列数
		self.rect.left, self.rect.top = self.pos[1] * 50, self.pos[0] * 50
		self.mask = pygame.mask.from_surface(self.image)
		self.fire_num = 6		# 炸弹火力大小
		self.bomb_num = 5		# 总共能放的炸弹数

	def move(self, key):
		if key == 1:  	# 向上移动
			# 上边是墙壁或炸弹的情况
			# if((Map[self.pos[0] - 1][self.pos[1]] == "@") or (Map[self.pos[0] - 1][self.pos[1]] == "#") or (Map[self.pos[0] - 1][self.pos[1]] == "$")):
			if(Map[self.pos[0] - 1][self.pos[1]] in ["@", "#", "$", "*"]):
				self.rect.top -= self.speed
				if(self.rect.top < self.pos[0] * 50):
					self.rect.top = self.pos[0] * 50
			else:
				# 如果卡在左半边墙
				if(self.pos[1] * 50 - 25 < self.rect.left < self.pos[1] * 50 - self.speed):
					self.rect.left += self.speed
				# 如果卡在右半边墙
				elif(self.pos[1] * 50 + self.speed < self.rect.left < self.pos[1] * 50 + 25):
					self.rect.left -= self.speed
				# 卡在中间，能直接上去
				elif(self.pos[1] * 50 - self.speed <= self.rect.left <= self.pos[1] * 50 + self.speed):
					if self.rect.left != self.pos[1] * 50:
						self.rect.left = self.pos[1] * 50
					else:
						self.rect.top -= self.speed

		elif key == 2:	# 向下移动
			# 下边是墙壁或炸弹的情况
			# if((Map[self.pos[0] + 1][self.pos[1]] == "@") or (Map[self.pos[0] + 1][self.pos[1]] == "#") or (Map[self.pos[0] + 1][self.pos[1]] == "$")):
			if(Map[self.pos[0] + 1][self.pos[1]] in ["@", "#", "$", "*"]):	
				self.rect.top += self.speed
				if(self.rect.top > self.pos[0] * 50):
					self.rect.top = self.pos[0] * 50
			else:
				# 如果卡在左半边墙
				if(self.pos[1] * 50 - 25 < self.rect.left < self.pos[1] * 50 - self.speed):
					self.rect.left += self.speed
				# 如果卡在右半边墙
				elif(self.pos[1] * 50 + self.speed < self.rect.left < self.pos[1] * 50 + 25):
					self.rect.left -= self.speed
				# 卡在中间，能直接上去
				elif(self.pos[1] * 50 - self.speed <= self.rect.left <= self.pos[1] * 50 + self.speed):
					if self.rect.left != self.pos[1] * 50:
						self.rect.left = self.pos[1] * 50
					else:
						self.rect.top += self.speed

		elif key == 3: 	# 向左移动
			# 左边是墙壁或炸弹的情况
			# if((Map[self.pos[0]][self.pos[1] - 1] == "@") or (Map[self.pos[0]][self.pos[1] - 1] == "#") or (Map[self.pos[0]][self.pos[1] - 1] == "$")):
			if(Map[self.pos[0]][self.pos[1] - 1] in ["@", "#", "$", "*"]):
				self.rect.left -= self.speed
				if(self.rect.left < self.pos[1] * 50):
					self.rect.left = self.pos[1] * 50
			else:
				# 如果卡在上半边墙
				if(self.pos[0] * 50 - 25 < self.rect.top < self.pos[0] * 50 - self.speed):
					self.rect.top += self.speed
				# 如果卡在右半边墙
				elif(self.pos[0] * 50 + self.speed < self.rect.top < self.pos[0] * 50 + 25):
					self.rect.top -= self.speed
				# 卡在中间，能直接上去
				elif(self.pos[0] * 50 - self.speed <= self.rect.top <= self.pos[0] * 50 + self.speed):
					if self.rect.top != self.pos[0] * 50:
						self.rect.top = self.pos[0] * 50
					else:
						self.rect.left -= self.speed

		elif key == 4:	# 向右移动
			# 右边是墙壁或炸弹的情况
			# if((Map[self.pos[0]][self.pos[1] + 1] == "@") or (Map[self.pos[0]][self.pos[1] + 1] == "#") or (Map[self.pos[0]][self.pos[1] + 1] == "$")):
			if(Map[self.pos[0]][self.pos[1] + 1] in ["@", "#", "$", "*"]):
				self.rect.left += self.speed
				if(self.rect.left > self.pos[1] * 50):
					self.rect.left = self.pos[1] * 50
			else:
				# 如果卡在上半边墙
				if(self.pos[0] * 50 - 25 < self.rect.top < self.pos[0] * 50 - self.speed):
					self.rect.top += self.speed
				# 如果卡在右半边墙
				elif(self.pos[0] * 50 + self.speed < self.rect.top < self.pos[0] * 50 + 25):
					self.rect.top -= self.speed
				# 卡在中间，能直接上去
				elif(self.pos[0] * 50 - self.speed <= self.rect.top <= self.pos[0] * 50 + self.speed):
					if self.rect.top != self.pos[0] * 50:
						self.rect.top = self.pos[0] * 50
					else:
						self.rect.left += self.speed

		self.pos[0] = (self.rect.top + 25) // 50
		self.pos[1] = (self.rect.left + 25) // 50

		if( Map[self.pos[0]][self.pos[1]] in ["1", "2", "3", "4"]):
			self.alive = False
	
