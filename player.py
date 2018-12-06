import pygame
from Map import *
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
        self.score=0			# 游戏得分 由拾取的加分果和杀死敌人的个数决定
        self.kill_enemies_num=0	# 杀死敌人的数目
        self.add_point_tool=0
        self.direction=1 #1:up 2:down 3:left 4:right
        self.dirextion_status=0
        self.temp = 0  # 判断是否需要发送拾取道具信息

    def move(self, key):
        if key == 1:  	# 向上移动
            # 上边是墙壁或炸弹的情况
            # if((Map[self.pos[0] - 1][self.pos[1]] == "@") or (Map[self.pos[0] - 1][self.pos[1]] == "#") or (Map[self.pos[0] - 1][self.pos[1]] == "$")):
            self.direction=4
            if(Map[self.pos[0] - 1][self.pos[1]] in ["@", "#", "$", "*"]):
                self.rect.top -= self.speed
                # self.image=self.image.subsurface((5,6),(50,70))
                if(self.rect.top < self.pos[0] * 50):
                    self.rect.top = self.pos[0] * 50
            #self.player1 = player.player(self.main_size, "images/player2.png", [self.pos[0], self.pos[1]])
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
            self.direction = 1
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
            self.direction = 2
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
            self.direction = 3
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
                #self.speed += 1
                self.temp = 8

            pick_up_prop_sound.play()
            change_map(self.pos, " ")

    def get_fire_num(self):
        return self.fire_num

    def get_bomb_num(self):
        return self.bomb_num

    def get_speed(self):
        return self.speed

    def get_tools(self):
        return (self.get_fire_num(),self.get_bomb_num(),self.get_speed())

    def get_score(self):
        self.score = (self.fire_num-1)* 20+(self.speed-3)*30
        return self.score

    def get_add_point_num(self):
        return self.add_point_tool

    def get_direction(self):
        return self.direction

    def set_fire_num(self,num):
        self.fire_num=num

    def set_bomb_num(self,num):
        self.bomb_num=num

    def set_speed(self,num):
        self.speed=num

    def set_tools(self,fire_num,bomb_num,speed_num):
        self.fire_num=fire_num
        self.bomb_num=bomb_num
        self.speed_num=speed_num





