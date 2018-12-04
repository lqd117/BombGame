import pygame
import player
from prop import create_prop

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()

bg_size = bg_width, bg_height = 950, 750  		# 整个游戏界面的大小（包括战场和道具栏）
main_size = main_width, main_height = 750, 750  # 战场的大小
element_width, element_height = 50, 50  		# 人物的大小
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("泡泡堂")
#绘制状态栏：

# 加载所有人物
player1 = player.player(main_size, "images/player1.png", [2, 1])
player2 = player.player(main_size, "images/player2.png", [13, 13])
player.player_list.append(player1)
player.player_list.append(player2)

#人物：
Avatar_player1=pygame.image.load("images/player1.png").convert_alpha()
Avatar_player2=pygame.image.load("images/player2.png").convert_alpha()

bg_image1 = pygame.image.load("images/background.jpg").convert()
bg_image2 = pygame.image.load("images/scene_choose.jpg").convert()
bg_image3 = pygame.image.load("images/bg.png").convert()

# 初始界面两个按钮
planet_image = pygame.image.load("images/playgame.png").convert_alpha()
info_image = pygame.image.load("images/information.png").convert_alpha()
planet_image = pygame.transform.smoothscale(planet_image, (500, 132))
info_image = pygame.transform.smoothscale(info_image, (326, 86))

planet_width, planet_height = planet_image.get_size()
info_width, info_height = info_image.get_size()

# 选择界面的所有场景图片
battle_one = pygame.image.load("images/one.png").convert()
battle_two = pygame.image.load("images/two.jpg").convert()
battle_three = pygame.image.load("images/three.jpg").convert()
battle_four = pygame.image.load("images/four.jpg").convert()
battle_five = pygame.image.load("images/five.jpg").convert()
battle_six = pygame.image.load("images/six.jpg").convert()
battle_seven = pygame.image.load("images/seven.jpg").convert()

screen_width, screen_height = battle_one.get_size()

scene_one = pygame.transform.smoothscale(battle_one, (screen_width - 350, screen_height - 350))
scene_two = pygame.transform.smoothscale(battle_two, (screen_width - 350, screen_height - 350))
scene_three = pygame.transform.smoothscale(battle_three, (screen_width - 350, screen_height - 350))
scene_four = pygame.transform.smoothscale(battle_four, (screen_width - 350, screen_height - 350))
scene_five = pygame.transform.smoothscale(battle_five, (screen_width - 350, screen_height - 350))
scene_six = pygame.transform.smoothscale(battle_six, (screen_width - 350, screen_height - 350))
scene_seven = pygame.transform.smoothscale(battle_seven, (screen_width - 350, screen_height - 350))

battle_scene_one = pygame.transform.smoothscale(battle_one, (950,750))
battle_scene_two = pygame.transform.smoothscale(battle_two, (950,750))
battle_scene_three = pygame.transform.smoothscale(battle_three,(950,750))
battle_scene_four = pygame.transform.smoothscale(battle_four,(950,750))
battle_scene_five = pygame.transform.smoothscale(battle_five,(950,750))
battle_scene_six = pygame.transform.smoothscale(battle_six, (950,750))
battle_scene_seven = pygame.transform.smoothscale(battle_seven,(950,750))

s = pygame.image.load("images/s.png").convert_alpha()
c = pygame.image.load("images/c.png").convert_alpha()
e = pygame.image.load("images/e.png").convert_alpha()
n = pygame.image.load("images/n.png").convert_alpha()

brick_image = pygame.image.load("images/const_brick.png").convert_alpha()
wall_image = pygame.image.load("images/wall.png").convert_alpha()
bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
fire1_image = pygame.image.load("images/fire.png").convert_alpha()
explode_bomb_image = pygame.image.load("images/explode_bomb.png").convert_alpha()
destoried_wall_image = pygame.image.load("images/destoried_wall.png").convert_alpha()
add_bomb_prop_image = pygame.image.load("images/add_bomb_prop.png").convert_alpha()
add_fire_num_prop_image = pygame.image.load("images/add_fire_num_prop.png").convert_alpha()
speed_up_prop_image = pygame.image.load("images/speed_up_prop.png").convert_alpha()
score_font = pygame.font.Font(None, 16)

#结束游戏背景:
end_game_scene= pygame.image.load("images/end_game_scene.jpg").convert()
end_game_scene= pygame.transform.smoothscale(end_game_scene, (950,750))

create_prop()	# 初始化所有道具的位置