import pygame
import tkinter as tk
from tkinter import *
import os

root = tk.Tk()
root.overrideredirect(True)#移除标题栏
embed = tk.Frame(root, width = 950, height = 750) #creates embed frame for pygame window
embed.grid(columnspan = (950), rowspan = 750) # Adds grid
embed.pack() #packs window to the left
buttonwin = tk.Frame(root, width = 75, height = 500)
buttonwin.pack(side = LEFT)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
screen = pygame.display.set_mode((500,500))
screen.fill(pygame.Color(255,255,255))
pygame.display.init()
pygame.display.update()
def draw():
    pygame.draw.circle(screen, (0,0,0), (250,250), 125)
    pygame.display.update()
    button1 = Button(buttonwin,text = 'Draw',  command=draw)
    button1.pack()
    root.update()

while True:
    pygame.display.update()
    root.update()     