import pygame
import sys
import traceback
from pygame.locals import *
from Map import *
import player
import bomb
import prop


def main():
    player_num = 4;
    a = game(player_num)
    a.run()


def set_bgm(selection_scene):
    #pygame.mixer.music.load("sound/" + str(selection_scene) + ".wav")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)


class game():
    def __init__(self):
        # 各界面的显示状态
        self.start_game = True
        self.choose_scene = False
        self.play_game = False
        self.show_information = False
        self.end_game = False

        self.bg_size = 950, 750  # 整个游戏界面的大小（包括战场和道具栏）
        self.main_size = 750, 750  # 战场的大小
        self.element_width, self.element_height = 50, 50  # 人物的大小
        self.screen = ''
        self.clock = ''
        self.score_font = pygame.font.Font(None, 24)  # 字体
        self.player_num = 0

        self.bg_image1 = ''
        self.bg_image2 = ''
        self.bg_image3 = ''

        # 初始界面两个按钮
        self.planet_image = ''
        self.info_image = ''
        self.planet_image =''
        self.info_image =''

        self.planet_width, self.planet_height = '',''
        self.info_width, self.info_height = '',''

        # 七个战斗场景
        self.battle_one = ''
        self.battle_two = ''
        self.battle_three = ''
        self.battle_four = ''
        self.battle_five = ''
        self.battle_six = ''
        self.battle_seven = ''

        self.screen_width, self.screen_height = '',''

        self.scene_one = ''
        self.scene_two = ''
        self.scene_three =''
        self.scene_four = ''
        self.scene_five =''
        self.scene_six = ''
        self.scene_seven = ''

        self.battle_scene_one = ''
        self.battle_scene_two = ''
        self.battle_scene_three = ''
        self.battle_scene_four = ''
        self.battle_scene_five = ''
        self.battle_scene_six = ''
        self.battle_scene_seven = ''
        self.battle_scene = self.battle_scene_one

        self.s = ''
        self.c = ''
        self.e = ''
        self.n = ''

        self.brick_image = ''
        self.wall_image = ''
        self.bomb_image = ''
        self.fire1_image = ""
        self.explode_bomb_image = ''
        self.destoried_wall_image = ''
        self.add_bomb_prop_image = ''
        self.add_fire_num_prop_image = ''
        self.speed_up_prop_image = ''

        # 结束游戏背景:
        self.end_game_scene = ''
        self.end_game_scene = ''

        # 返回按钮
        self.return_game = ''
        self.return_game = ''

        # 文本框
        self.frame = ''
        self.frame = ''
        # create_prop()	# 初始化所有道具的位置

        # 人物
        self.Avatar_player1 = ''
        self.Avatar_player2 = ''


    def init(self,player_num):
        self.start_game = True
        self.choose_scene = False
        self.play_game = False
        self.show_information = False
        self.end_game = False

        self.bg_size = 950, 750  # 整个游戏界面的大小（包括战场和道具栏）
        self.main_size = 750, 750  # 战场的大小
        self.element_width, self.element_height = 50, 50  # 人物的大小
        self.screen = pygame.display.set_mode(self.bg_size)
        self.clock = pygame.time.Clock()
        self.score_font = pygame.font.Font(None, 24)  # 字体
        self.player_num = player_num

        self.bg_image1 = pygame.image.load("images/background.jpg").convert()
        self.bg_image2 = pygame.image.load("images/scene_choose.jpg").convert()
        self.bg_image3 = pygame.image.load("images/bg.png").convert()

        # 初始界面两个按钮
        self.planet_image = pygame.image.load("images/playgame.png").convert_alpha()
        self.info_image = pygame.image.load("images/information.png").convert_alpha()
        self.planet_image = pygame.transform.smoothscale(self.planet_image, (500, 132))
        self.info_image = pygame.transform.smoothscale(self.info_image, (326, 86))

        self.planet_width, self.planet_height = self.planet_image.get_size()
        self.info_width, self.info_height = self.info_image.get_size()

        # 七个战斗场景
        self.battle_one = pygame.image.load("images/one.png").convert()
        self.battle_two = pygame.image.load("images/two.jpg").convert()
        self.battle_three = pygame.image.load("images/three.jpg").convert()
        self.battle_four = pygame.image.load("images/four.jpg").convert()
        self.battle_five = pygame.image.load("images/five.jpg").convert()
        self.battle_six = pygame.image.load("images/six.jpg").convert()
        self.battle_seven = pygame.image.load("images/seven.jpg").convert()

        self.screen_width, self.screen_height = self.battle_one.get_size()

        self.scene_one = pygame.transform.smoothscale(self.battle_one,
                                                      (self.screen_width - 350, self.screen_height - 350))
        self.scene_two = pygame.transform.smoothscale(self.battle_two,
                                                      (self.screen_width - 350, self.screen_height - 350))
        self.scene_three = pygame.transform.smoothscale(self.battle_three,
                                                        (self.screen_width - 350, self.screen_height - 350))
        self.scene_four = pygame.transform.smoothscale(self.battle_four,
                                                       (self.screen_width - 350, self.screen_height - 350))
        self.scene_five = pygame.transform.smoothscale(self.battle_five,
                                                       (self.screen_width - 350, self.screen_height - 350))
        self.scene_six = pygame.transform.smoothscale(self.battle_six,
                                                      (self.screen_width - 350, self.screen_height - 350))
        self.scene_seven = pygame.transform.smoothscale(self.battle_seven,
                                                        (self.screen_width - 350, self.screen_height - 350))

        self.battle_scene_one = pygame.transform.smoothscale(self.battle_one, (950, 750))
        self.battle_scene_two = pygame.transform.smoothscale(self.battle_two, (950, 750))
        self.battle_scene_three = pygame.transform.smoothscale(self.battle_three, (950, 750))
        self.battle_scene_four = pygame.transform.smoothscale(self.battle_four, (950, 750))
        self.battle_scene_five = pygame.transform.smoothscale(self.battle_five, (950, 750))
        self.battle_scene_six = pygame.transform.smoothscale(self.battle_six, (950, 750))
        self.battle_scene_seven = pygame.transform.smoothscale(self.battle_seven, (950, 750))
        self.battle_scene = self.battle_scene_one

        self.s = pygame.image.load("images/s.png").convert_alpha()
        self.c = pygame.image.load("images/c.png").convert_alpha()
        self.e = pygame.image.load("images/e.png").convert_alpha()
        self.n = pygame.image.load("images/n.png").convert_alpha()

        self.brick_image = pygame.image.load("images/const_brick.png").convert_alpha()
        self.wall_image = pygame.image.load("images/wall.png").convert_alpha()
        self.bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
        self.fire1_image = pygame.image.load("images/fire.png").convert_alpha()
        self.explode_bomb_image = pygame.image.load("images/explode_bomb.png").convert_alpha()
        self.destoried_wall_image = pygame.image.load("images/destoried_wall.png").convert_alpha()
        self.add_bomb_prop_image = pygame.image.load("images/add_bomb_prop.png").convert_alpha()
        self.add_fire_num_prop_image = pygame.image.load("images/add_fire_num_prop.png").convert_alpha()
        self.speed_up_prop_image = pygame.image.load("images/speed_up_prop.png").convert_alpha()

        # 结束游戏背景:
        self.end_game_scene = pygame.image.load("images/end_game_scene.jpg").convert()
        self.end_game_scene = pygame.transform.smoothscale(self.end_game_scene, (950, 750))

        # 返回按钮
        self.return_game = pygame.image.load("images/return.png").convert_alpha()
        self.return_game = pygame.transform.smoothscale(self.return_game, (700, 700))

        # 文本框
        self.frame = pygame.image.load("images/frame.png").convert_alpha()
        self.frame = pygame.transform.smoothscale(self.frame, (900, 700))
        # create_prop()	# 初始化所有道具的位置

        # 人物
        self.Avatar_player1 = pygame.image.load("images/player1.png").convert_alpha()
        self.Avatar_player2 = pygame.image.load("images/player2.png").convert_alpha()
        self.set_player_pos()

        pygame.display.set_caption("泡泡堂")

        pygame.mixer.music.load("sound/0.wav")
        pygame.mixer.music.set_volume(0.4)

    def freshPlayer(self,pos,flag):
        if flag < 5:
            exec("self.player{pos}.move({id})".format(pos=pos,id=flag))
        elif flag == 5:
            exec("bomb.add_bomb(self.player{pos})".format(pos=pos))
        elif flag == 6:
            exec("self.player{pos}.bomb_num += 1".format(pos=pos))
        elif flag == 7:
            exec("self.player{pos}.fire_num += 1".format(pos=pos))
        elif flag == 8:
            exec("self.player{pos}.speed += .5".format(pos=pos))

    def freshDead(self,pos):
        exec("self.player{pos}.alive = False".format(pos=pos))

    def set_player_pos(self):
        # 加载所有人物
        self.player1 = player.player(self.main_size, "images/player1.png", [1, 1])
        self.player2 = player.player(self.main_size, "images/player2.png", [13, 1])
        player.player_list.append(self.player1)
        player.player_list.append(self.player2)
        if self.player_num >= 3:
            self.player3 = player.player(self.main_size, "images/player3.png", [1, 13])
            player.player_list.append(self.player3)
        if self.player_num >= 4:
            self.player4 = player.player(self.main_size, "images/player4.png", [13, 13])
            player.player_list.append(self.player4)

    def run(self,client):
        pygame.mixer.music.play(-1)

        self.play_game = True
        self.mapchange(1)

        you = ''
        if client.pos == 1:
            you = self.player1
        if client.pos == 2:
            you = self.player2
        if client.pos == 3:
            you = self.player3
        if client.pos == 4:
            you = self.player4
        if client.pos == 5:
            you = self.player5
        if client.pos == 6:
            you = self.player6
        if client.pos == 7:
            you = self.player7
        if client.pos == 8:
            you = self.player8
        while self.play_game:  # 游戏战斗界面
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            # 取出所有键盘事件
            key_pressed = pygame.key.get_pressed()

            # player1的动作，wasd移动，空格放炸弹
            # 人物的移动
            if you.alive:
                if (key_pressed[K_w]):
                    client.gamingSend(1)
                if (key_pressed[K_s]):
                    client.gamingSend(2)
                if (key_pressed[K_a]):
                    client.gamingSend(3)
                if (key_pressed[K_d]):
                    client.gamingSend(4)
                if (key_pressed[K_SPACE]):
                    client.gamingSend(5)
            else:
                if client.sendLiveFlag == 0:
                    client.sendDead()
                    client.sendLiveFlag = 1

            if you.temp:
                client.gamingSend(you.temp)
                you.temp = 0


            fire_num1 = self.player1.get_fire_num()
            bomb_num1 = self.player1.get_bomb_num()
            speed1 = self.player1.get_speed()
            fire_num2 = self.player2.get_fire_num()
            bomb_num2 = self.player2.get_bomb_num()
            speed2 = self.player2.get_speed()

            bomb.bomb_explode()  # 每次检查是否有炸弹爆炸
            self.screen.blit(self.battle_scene, (0, 0))
            self.draw_map()

            # 状态栏人物
            self.screen.blit(self.Avatar_player1, (800, 60))
            self.screen.blit(self.Avatar_player2, (800, 460))
            # 画道具
            self.screen.blit(self.add_fire_num_prop_image, (800, 120))
            self.screen.blit(self.add_bomb_prop_image, (800, 180))
            self.screen.blit(self.speed_up_prop_image, (800, 240))
            self.screen.blit(self.add_fire_num_prop_image, (800, 520))
            self.screen.blit(self.add_bomb_prop_image, (800, 580))
            self.screen.blit(self.speed_up_prop_image, (800, 640))
            # 状态栏渲染
            player1_fire_num = self.score_font.render("Number: %d" % fire_num1, True, (0, 0, 0))
            player1_bomb_num = self.score_font.render("Number: %d" % bomb_num1, True, (0, 0, 0))
            player1_speed = self.score_font.render("Number: %d" % speed1, True, (0, 0, 0))
            player2_fire_num = self.score_font.render("Number: %d" % fire_num2, True, (0, 0, 0))
            player2_bomb_num = self.score_font.render("Number: %d" % bomb_num2, True, (0, 0, 0))
            player2_speed = self.score_font.render("Number: %d" % speed2, True, (0, 0, 0))
            self.screen.blit(player1_fire_num, (860, 140))
            self.screen.blit(player1_bomb_num, (860, 200))
            self.screen.blit(player1_speed, (860, 260))
            self.screen.blit(player2_fire_num, (860, 540))
            self.screen.blit(player2_bomb_num, (860, 600))
            self.screen.blit(player2_speed, (860, 660))

            alive_player_num = 0
            for each_player in player.player_list:  # 绘制出所有还存活的玩家
                if each_player.alive:
                    self.screen.blit(each_player.image, each_player.rect)
                    alive_player_num += 1
            if alive_player_num == 1:
                self.play_game = False
                self.end_game = True

            pygame.display.update()
            self.clock.tick(60)

        while self.end_game:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                else:
                    self.screen.blit(self.end_game_scene, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

    def mapchange(self, choose):
        self.map_choose = choose
        if self.map_choose == 1:
            self.battle_scene = self.battle_scene_one
        elif self.map_choose == 2:
            self.battle_scene = self.battle_scene_two
        elif self.map_choose == 3:
            self.battle_scene = self.battle_scene_three
        elif self.map_choose == 4:
            self.battle_scene = self.battle_scene_four
        elif self.map_choose == 5:
            self.battle_scene = self.battle_scene_five
        elif self.map_choose == 6:
            self.battle_scene = self.battle_scene_six
        elif self.map_choose == 7:
            self.battle_scene = self.battle_scene_seven
        if self.map_choose != -1:
            set_bgm(self.map_choose)
            set_Map(self.map_choose)
            prop.create_prop()


    def draw_map(self):
        for i in range(len(Map)):
            for j in range(len(Map[0])):
                if (Map[i][j] == "#"):  # 固定墙
                    self.screen.blit(self.brick_image, (j * self.element_height, i * self.element_width))
                elif (Map[i][j] == "@"):  # 普通墙
                    self.screen.blit(self.wall_image, (j * self.element_height, i * self.element_width))
                elif (Map[i][j] == "$"):  # 炸弹
                    self.screen.blit(self.bomb_image, (j * self.element_height, i * self.element_width))
                elif (Map[i][j] == "1"):  # 朝上的火焰
                    self.screen.blit(pygame.transform.rotate(self.fire1_image, -90),
                                     (j * self.element_height, i * self.element_width))
                elif (Map[i][j] == "2"):  # 朝左的火焰
                    self.screen.blit(self.fire1_image, (j * self.element_height, i * self.element_width))
                elif (Map[i][j] == "3"):  # 朝下的火焰
                    self.screen.blit(pygame.transform.rotate(self.fire1_image, 90),
                                     (j * self.element_height, i * self.element_width))
                elif (Map[i][j] == "4"):  # 朝右的火焰
                    self.screen.blit(pygame.transform.rotate(self.fire1_image, 180),
                                     (j * self.element_height, i * self.element_width))
                elif (Map[i][j] == "%"):  # 正在爆炸的炸弹
                    self.screen.blit(self.explode_bomb_image, (j * self.element_height, i * self.element_width))
                elif (Map[i][j] == "*"):  # 被炸毁的墙
                    self.screen.blit(self.destoried_wall_image, (j * self.element_height, i * self.element_width))
                elif (Map[i][j] == "a"):  # 加炸弹数的道具
                    self.screen.blit(self.add_bomb_prop_image, (j * self.element_height, i * self.element_width))
                elif (Map[i][j] == "b"):
                    self.screen.blit(self.add_fire_num_prop_image, (j * self.element_height, i * self.element_width))
                elif (Map[i][j] == "c"):  # 加速度的道具
                    self.screen.blit(self.speed_up_prop_image, (j * self.element_height, i * self.element_width))


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()