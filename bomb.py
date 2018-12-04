from Map import *
from time import perf_counter
from player import player_list
from prop import prop_list
from sound import *

bomb_list = []
explode_bomb_list = []
EXPLODE_LASTING_TIME_IN_SECOND = 3  # 炸弹爆炸秒数
EXPLODE_DURATION_FPS = 60			# 持续120帧，即2秒
FIRE_SPREAD_FPS = 5 				# 火焰每10帧向外扩展一格

class bomb():
	def __init__(self, master):
		self.pos = master.pos.copy()
		self.fire_num = master.fire_num
		self.begin_time = perf_counter()
		self.master = master
		self.duration_fps = 0		# 炸弹爆炸动画已经持续的的帧数


def add_bomb(master):
	# 只有该位置为空地时才可以投放炸弹
	if(Map[master.pos[0]][master.pos[1]] == " " and master.bomb_num > 0):
		change_map(master.pos, "$")
		new_bomb = bomb(master)
		bomb_list.append(new_bomb)
		master.bomb_num -= 1


def bomb_explode():
	# 有炸弹将要爆炸
	if len(bomb_list):
		# 如果有新的炸弹爆炸那么一定是第一个炸弹爆炸
		first_bomb = bomb_list[0]
		if(perf_counter() - first_bomb.begin_time > EXPLODE_LASTING_TIME_IN_SECOND):
			explode_bomb_list.append(first_bomb)
			change_map(first_bomb.pos, "%")
			first_bomb.master.bomb_num += 1
			del bomb_list[0]
			bomb_explode_sound.play()

	# 有炸弹正在爆炸
	if len(explode_bomb_list):
		for bomb in explode_bomb_list:
			# 从内到外添加爆炸产生火焰并造成爆炸效果
			if((bomb.duration_fps < bomb.fire_num * FIRE_SPREAD_FPS) and (bomb.duration_fps % FIRE_SPREAD_FPS == 0)):
				fire_spread(bomb)
			
			if(bomb.duration_fps > EXPLODE_DURATION_FPS):	# 爆炸结束，炸弹火焰消失，炸弹本身消失
				explode_end(bomb)
			bomb.duration_fps += 1
			
def fire_spread(bomb):
	for player in player_list:		# 炸弹中心炸到人物则人物死亡 
		if(player.pos == bomb.pos):
			player.alive = False

	for i in range(1, 5):	# 四个方向
		present_fire_num = bomb.duration_fps // FIRE_SPREAD_FPS + 1
		if(present_fire_num > bomb.fire_num):
			break
		for j in range(1, present_fire_num + 1):
			pos_x = bomb.pos[0] + j * (i % 2) * (i - 2)			# 下一个检查点的横坐标
			pos_y = bomb.pos[1] + j * ((i + 1) % 2) * (i - 3)	# 下一个检查点的纵坐标
			if(Map[pos_x][pos_y] in ["#", "*", "%"]):	# 固定墙或炸毁或爆炸的炸弹的墙则整排火焰消失
				break

			elif(Map[pos_x][pos_y] in ["a", "b", "c"]):	# 遇到道具则跳过道具
				continue

			elif(Map[pos_x][pos_y] == "@"):		# 普通墙则炸开
				Map[pos_x] = Map[pos_x][:pos_y] + "*" + Map[pos_x][pos_y + 1:]

			elif(Map[pos_x][pos_y] in [" ", "1", "2", "3", "4"]):		# 空地和其他方向的火焰则释放火焰
				change_map([pos_x, pos_y], str(i))
				for player in player_list:		# 炸到人物则人物死亡 
					if(player.pos[0] == pos_x and player.pos[1] == pos_y):
						player.alive = False

			elif(Map[pos_x][pos_y] == "$"):		# 炸到未爆炸的炸弹则进行引爆
				for each in range(len(bomb_list)):
					if(bomb_list[each].pos == [pos_x, pos_y]):
						explode_bomb_list.append(bomb_list[each])
						change_map(bomb_list[each].pos, "%")
						bomb_list[each].master.bomb_num += 1
						bomb_explode_sound.play()
						del bomb_list[each]
						break


def explode_end(bomb):
	explode_bomb_list.remove(bomb)
	# 爆炸完成，四个方向的火焰消失
	for i in range(1, 5):	# 四个方向
		for j in range(1, bomb.fire_num + 1):
			pos_x = bomb.pos[0] + j * (i % 2) * (i - 2)			# 下一个检查点的横坐标
			pos_y = bomb.pos[1] + j * ((i + 1) % 2) * (i - 3)	# 下一个检查点的纵坐标
			if(Map[pos_x][pos_y] in ["1", "2", "3", "4"]):		# 如果是火焰或炸毁的墙则收掉
				change_map([pos_x, pos_y], " ")

			elif(Map[pos_x][pos_y] == "*"):		# 如果是被毁的墙则查看是否有道具
				pos_xy = pos_x * 100 + pos_y
				for each_prop in prop_list:
					if each_prop.pos == pos_xy:
						change_map([pos_x, pos_y], each_prop.kind)
				if Map[pos_x][pos_y] == "*":
					change_map([pos_x, pos_y], " ")

			elif(Map[pos_x][pos_y] == "#" or Map[pos_x][pos_y] == "%"):		# 遇到墙则不再考虑此方向
				break

	change_map(bomb.pos, " ")	# 修改地面
	for other_bomb in explode_bomb_list:	# 再绘制一遍其他炸弹的火焰，防止出现火焰空缺
		fire_spread(other_bomb)