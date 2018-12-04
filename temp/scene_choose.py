import sys, random, math, pygame
from pygame.locals import *
radius = 250
angle = 0.0

pygame.init()
screen = pygame.display.set_mode((950, 750))
pygame.display.set_caption("场景选择")
font = pygame.font.Font(None, 18)

space = pygame.image.load("images/scene_choose.jpg").convert_alpha()
scene_one = pygame.image.load("images/one.png").convert_alpha()
scene_two = pygame.image.load("images/two.jpg").convert_alpha()
scene_three = pygame.image.load("images/three.jpg").convert_alpha()
scene_four = pygame.image.load("images/four.jpg").convert_alpha()
scene_five = pygame.image.load("images/five.jpg").convert_alpha()
scene_six = pygame.image.load("images/six.jpg").convert_alpha()
scene_seven = pygame.image.load("images/seven.jpg").convert_alpha()
width, height = scene_two.get_size()
scene_one=pygame.transform.smoothscale(scene_one, (width-350, height-350))
scene_two = pygame.transform.smoothscale(scene_two, (width-350, height-350))
scene_three=pygame.transform.smoothscale(scene_three, (width-350, height-350))
scene_four=pygame.transform.smoothscale(scene_four, (width-350, height-350))
scene_five=pygame.transform.smoothscale(scene_five, (width-350, height-350))
scene_six=pygame.transform.smoothscale(scene_six, (width-350, height-350))
scene_seven=pygame.transform.smoothscale(scene_seven, (width-350, height-350))
s = pygame.image.load("images/s.png").convert_alpha()
#s=pygame.transform.smoothscale(s, (width//2, height//2))
c = pygame.image.load("images/c.png").convert_alpha()
#=pygame.transform.smoothscale(c, (width//2, height//2))
e = pygame.image.load("images/e.png").convert_alpha()
#e=pygame.transform.smoothscale(e, (width//2, height//2))
n = pygame.image.load("images/n.png").convert_alpha()
#n=pygame.transform.smoothscale(n, (width//2, height//2))
e1 = pygame.image.load("images/e.png").convert_alpha()
#e1=pygame.transform.smoothscale(e1, (width//2, height//2))
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
    screen.blit(scene_six, (400 ,430))
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
    pygame.display.update()