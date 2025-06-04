from pygame.locals import *
import pygame as pg

import numpy as np
import numba as nb

from components.host_table import *
from components.settings import *
from components.cards import *
# from components.host import *
from components.UI import *


screen = pg.display.set_mode((WIDTH, HEIGHT))

pg.init()

clock = pg.time.Clock()

card3 = Cards(0.3, np.array([0.5, 0.5], dtype = np.float64))
card4 = Cards(12.3, np.array([0.25, 0.5], dtype = np.float64))
card4.hidden = True
card3.hidden = True
card_deck = CardDeck()

GraphFont = GraphicText((0.5, 0.5), default_font, "im vincing it, soo good!", True)
# GraphFont = GraphicText((0.5, 0.5), default_font, "im vincing it, soo good!", 0.5, 0.15, True)
GraphFont.Transfrom()

gameloop = GameLoopBlackJack()
gameloop.player.DrawCardFromDeck(gameloop.card_deck)
gameloop.player.DrawCardFromDeck(gameloop.card_deck)
gameloop.host.DrawCardFromDeck(gameloop.card_deck)
gameloop.host.DrawCardFromDeck(gameloop.card_deck)

running = True
mouse_clicked = False

while running:
    screen.fill((0, 0, 0))

    mouse_clicked = False
    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == BUTTON_LEFT:
                mouse_clicked = True
    
    keys = pg.key.get_pressed()
    mouse = pg.mouse.get_pressed()

    MousePosition = pg.mouse.get_pos()

    gameloop.Loop()

    gameloop.Draw(screen, MousePosition, WIDTH, HEIGHT)

    # GraphFont.Draw(screen)
    
    gameloop.HandleButtonCheck(mouse_clicked, MousePosition)
    

    pg.display.flip()
    pg.display.set_caption(f"{clock.get_fps() // 1}")
    clock.tick(FPS)


