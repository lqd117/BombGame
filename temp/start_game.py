import sys, random, math, pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((950, 750))
pygame.display.set_caption("开始游戏")
space = pygame.image.load("images/background.jpg").convert_alpha()
planet = pygame.image.load("images/playgame.png").convert_alpha()
superman = pygame.image.load("images/information.png").convert_alpha()
width, height = superman.get_size()
planet=pygame.transform.smoothscale(planet, (width-153, height-41))
superman = pygame.transform.smoothscale(superman, (width // 2, height // 2))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()

    screen.blit(space, (0, 0))
    # 获取位图的宽和高
    width, height = planet.get_size()
    # 在屏幕的中间绘制地球
    screen.blit(planet, (480 - width / 2, 350 - height / 2))
    width, height = superman.get_size()
    screen.blit(superman, (470 - width / 2, 510 - height / 2))
    pygame.display.update()