import pygame as pg
import numpy as np
from pygame.locals import *
import time

from network import *
from string_manipulation import *

network = Network()
player_id = int(network.Receive()) - 1
print(f"we ve got the IP, baby: {player_id}")

WIDTH, HEIGHT = 800, 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
FPS = 10000000
# FPS = 10

class Player:
    def __init__(self, x = WIDTH / 2, y = WIDTH / 2):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.w = 100
        self.h = 100
        self.velocity = 200

        self.rect = pg.rect.Rect(self.x, self.y, self.w, self.h)
        
        self.color: tuple[int, int, int] = (0, 0, 255)
    
    def Input(self, dt: float):
        if keys[K_a]:
            self.x -= self.velocity * dt
        if keys[K_d]:
            self.x += self.velocity * dt
        if keys[K_s]:
            self.y += self.velocity * dt
        if keys[K_w]:
            self.y -= self.velocity * dt
    
    def Draw(self, surface: pg.surface.Surface):
        self.rect.x = self.x 
        self.rect.y = self.y
        pg.draw.rect(surface, self.color, self.rect)

running = True

player = Player()
player2 = Player()
players_list: list[Player] = [player, player2]

contact_id = 0 if 1 else 0

previous_time = time.time()
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
    
    print(player_id)
    network.Send(string_the_pos((players_list[player_id].x, players_list[player_id].y)))

    # try:
    #     players_list[contact_id] = int_the_pos(network.Receive())
    # except:
    #     pass
    keys = pg.key.get_pressed()
    player.Input(dt)

    player2.Draw(screen)
    player.Draw(screen)

    clock.tick(FPS)
    pg.display.update()
    pg.display.set_caption(f"{clock.get_fps() // 1}")
