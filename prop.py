from Map import *
import random
prop_list = []

# 种类a, b, c分别代表加炸弹数, 加火力, 加炸弹数三种道具
class prop():
	def __init__(self, kind, pos):
		self.kind = kind
		self.pos = pos


def create_prop(seed):		# 初始化道具种类及位置
	random.seed(seed)
	for i in range(len(Map)):
		for j in range(len(Map[0])):
			if Map[i][j] == "@":
				r = random.randint(1, 10)
				if 1 <= r <= 3:
					if r == 1:
						new_prop = prop("a", i * 100 + j)
					elif r == 2:
						new_prop = prop("b", i * 100 + j)
					elif r == 3:
						new_prop = prop("c", i * 100 + j)
					prop_list.append(new_prop)
