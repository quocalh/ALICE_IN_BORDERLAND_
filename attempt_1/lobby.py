import pygame as pg
import numpy as np
import time as time
from pygame.locals import *


from components.settings import *

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

running = True
previous_time = time.time()

class Menu:
    def __init__(self):
        pass

while running:
    dt = time.time() - previous_time

    previous_time = time.time()

    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    

    pg.display.flip()
    clock.tick()
    pg.display.set_caption(f"{clock.get_fps() // 1}")

