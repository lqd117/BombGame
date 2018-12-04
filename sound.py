import pygame

pygame.init()
pygame.mixer.init()

pick_up_prop_sound = pygame.mixer.Sound("sound/pick_up_prop.wav")
pick_up_prop_sound.set_volume(0.2)
game_win_sound = pygame.mixer.Sound("sound/game_win.wav")
game_win_sound.set_volume(0.2)
game_over_sound = pygame.mixer.Sound("sound/game_over.wav")
game_over_sound.set_volume(0.2)
bomb_explode_sound = pygame.mixer.Sound("sound/bomb_explode.wav")
bomb_explode_sound.set_volume(0.2)