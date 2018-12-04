import pygame
import sys
import traceback
from pygame.locals import *
from Map import *
import player
import bomb

pygame.init()
pygame.mixer.init()

bg_size = bg_width, bg_height = 950, 750  # 整个游戏界面的大小（包括战场和道具栏）
main_size = main_width, main_height = 750, 750  # 战场的大小
element_width, element_height = 50, 50  # 人物的大小
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("泡泡堂")

def main():
    # pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    player1 = player.player(main_size, "images/player1.png", [2, 1])
    player2 = player.player(main_size, "images/player2.png", [13, 13])
    player.player_list.append(player1)
    player.player_list.append(player2)

    # 检测游戏是否还在进行
    running = True

    while running:
        start_game = True
        choose_scene = False
        play_game = False

        while start_game:
            space = pygame.image.load("images/background.jpg").convert_alpha()
            planet = pygame.image.load("images/playgame.png").convert_alpha()
            superman = pygame.image.load("images/information.png").convert_alpha()
            width, height = superman.get_size()
            planet = pygame.transform.smoothscale(planet, (width - 153, height - 41))
            superman = pygame.transform.smoothscale(superman, (width // 2, height // 2))
            screen.blit(space, (0, 0))
            width, height = planet.get_size()
            # 在屏幕的中间绘制地球
            screen.blit(planet, (480 - width / 2, 350 - height / 2))
            width, height = superman.get_size()
            screen.blit(superman, (470 - width / 2, 510 - height / 2))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if y > 296 and y <400  and x > 254 and x < 715:
                        choose_scene = True
                        start_game = False

        while choose_scene:
            space = pygame.image.load("images/scene_choose.jpg").convert_alpha()
            screen.blit(space, (0, 0))
            scene_one = pygame.image.load("images/one.png").convert_alpha()
            scene_two = pygame.image.load("images/two.jpg").convert_alpha()
            scene_three = pygame.image.load("images/three.jpg").convert_alpha()
            scene_four = pygame.image.load("images/four.jpg").convert_alpha()
            scene_five = pygame.image.load("images/five.jpg").convert_alpha()
            scene_six = pygame.image.load("images/six.jpg").convert_alpha()
            scene_seven = pygame.image.load("images/seven.jpg").convert_alpha()
            width, height = scene_two.get_size()
            scene_one = pygame.transform.smoothscale(scene_one, (width - 350, height - 350))
            scene_two = pygame.transform.smoothscale(scene_two, (width - 350, height - 350))
            scene_three = pygame.transform.smoothscale(scene_three, (width - 350, height - 350))
            scene_four = pygame.transform.smoothscale(scene_four, (width - 350, height - 350))
            scene_five = pygame.transform.smoothscale(scene_five, (width - 350, height - 350))
            scene_six = pygame.transform.smoothscale(scene_six, (width - 350, height - 350))
            scene_seven = pygame.transform.smoothscale(scene_seven, (width - 350, height - 350))
            s = pygame.image.load("images/s.png").convert_alpha()
            # s=pygame.transform.smoothscale(s, (width//2, height//2))
            c = pygame.image.load("images/c.png").convert_alpha()
            # =pygame.transform.smoothscale(c, (width//2, height//2))
            e = pygame.image.load("images/e.png").convert_alpha()
            # e=pygame.transform.smoothscale(e, (width//2, height//2))
            n = pygame.image.load("images/n.png").convert_alpha()
            # n=pygame.transform.smoothscale(n, (width//2, height//2))
            e1 = pygame.image.load("images/e.png").convert_alpha()
            # e1=pygame.transform.smoothscale(e1, (width//2, height//2))
            width, height = scene_one.get_size()
            screen.blit(scene_one, (150, 250))
            width, height = scene_two.get_size()
            screen.blit(scene_two, (320, 250))
            width, height = scene_three.get_size()
            screen.blit(scene_three, (490, 250))
            width, height = scene_four.get_size()
            screen.blit(scene_four, (660, 250))
            width, height = scene_five.get_size()
            screen.blit(scene_five, (230, 430))
            width, height = scene_six.get_size()
            screen.blit(scene_six, (400, 430))
            width, height = scene_seven.get_size()
            screen.blit(scene_seven, (570, 430))
            width, height = s.get_size()
            screen.blit(s, (160, 150))
            width, height = c.get_size()
            screen.blit(c, (220, 150))
            width, height = e.get_size()
            screen.blit(e, (280, 150))
            width, height = n.get_size()
            screen.blit(n, (340, 150))
            width, height = e1.get_size()
            screen.blit(e1, (400, 150))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if y >250 and y < 400 and x > 150 and x < 300:
                        play_game = True
                        choose_scene = False
        while play_game:
            background = pygame.image.load("images/bg.png").convert()

            BOMB_EXPLODE = USEREVENT
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == BOMB_EXPLODE:
                    bomb.explode()

            # 取出所有键盘事件
            key_pressed = pygame.key.get_pressed()

            # player1的动作，wasd移动，空格放炸弹
            # 人物一的移动
            if player1.alive:
                if (key_pressed[K_w]):
                    player1.move(1)
                if (key_pressed[K_s]):
                    player1.move(2)
                if (key_pressed[K_a]):
                    player1.move(3)
                if (key_pressed[K_d]):
                    player1.move(4)
                # 放炸弹
                if (key_pressed[K_SPACE]):
                    bomb.add_bomb(player1)

            if player2.alive:
                # 人物二的移动
                if (key_pressed[K_UP]):
                    player2.move(1)
                if (key_pressed[K_DOWN]):
                    player2.move(2)
                if (key_pressed[K_LEFT]):
                    player2.move(3)
                if (key_pressed[K_RIGHT]):
                    player2.move(4)

            bomb.bomb_explode()  # 每次检查是否有炸弹爆炸
            screen.blit(background, (0, 0))
            draw_map()
            for each_player in player.player_list:  # 绘制出所有还存活的玩家
                if each_player.alive:
                    screen.blit(each_player.image, each_player.rect)

            pygame.display.flip()
            clock.tick(60)


def draw_map():
    brick_image = pygame.image.load("images/const_brick.png").convert_alpha()
    wall_image = pygame.image.load("images/wall.png").convert_alpha()
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    fire1_image = pygame.image.load("images/fire1.png").convert_alpha()
    explode_bomb_image = pygame.image.load("images/explode_bomb.png").convert_alpha()
    destoried_wall_image = pygame.image.load("images/destoried_wall.png").convert_alpha()

    for i in range(len(Map)):
        for j in range(len(Map[0])):
            if (Map[i][j] == "#"):  # 固定墙
                screen.blit(brick_image, (j * element_height, i * element_width))
            elif (Map[i][j] == "@"):  # 普通墙
                screen.blit(wall_image, (j * element_height, i * element_width))
            elif (Map[i][j] == "$"):  # 炸弹
                screen.blit(bomb_image, (j * element_height, i * element_width))
            elif (Map[i][j] == "1"):  # 朝上的火焰
                screen.blit(pygame.transform.rotate(fire1_image, -90), (j * element_height, i * element_width))
            elif (Map[i][j] == "2"):  # 朝左的火焰
                screen.blit(fire1_image, (j * element_height, i * element_width))
            elif (Map[i][j] == "3"):  # 朝下的火焰
                screen.blit(pygame.transform.rotate(fire1_image, 90), (j * element_height, i * element_width))
            elif (Map[i][j] == "4"):  # 朝右的火焰
                screen.blit(pygame.transform.rotate(fire1_image, 180), (j * element_height, i * element_width))
            elif (Map[i][j] == "%"):  # 正在爆炸的炸弹
                screen.blit(explode_bomb_image, (j * element_height, i * element_width))
            elif (Map[i][j] == "*"):  # 被炸毁的墙
                screen.blit(destoried_wall_image, (j * element_height, i * element_width))


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
