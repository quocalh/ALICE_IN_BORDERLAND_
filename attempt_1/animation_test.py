from pygame.locals import *
import pygame as pg

import numpy as np
import numba as nb

import time

pg.init()

from components.debug_kit import *
from components.host_table import *
from components.settings import *
# from components.host import *
from components.UI import *



"""
COME FORTH, CHILD OF MAN
"""
class AnimationLoop:
    # show two card
    # press button => card move to another card
    # press r => reset postion | teleport back to 505
    def __init__(self):
        self.background = pg.image.load(BACKGROUND_TEXTURE_PATH).convert_alpha()
        self.background = GraphicTextureNotOptimizedYet((0.5, 0.5), self.background, 1, 1)

        self.animate_button = Buttons((0.5, 0.8), 0.3, 0.1)
        
        self.animating_text = GraphicText((0.5, 0.8), default_font,"animating", True)

        self.animation_registry = AnimationRegistry()

        self.card1 = Cards(0.3, np.array([0.75, 0.5], dtype = np.float64))
        self.card2 = Cards(12.3, np.array([0.75, 0.5], dtype = np.float64))

        self.root_node = UI_Nodes([self.animate_button], None, occupation = "i drop nukes :)")
        self.focused_node = self.root_node

    def GameLoop(self):
        if self.root_node == self.focused_node:
            if self.animate_button.is_clicked == True:
                if self.card1.pposition[0] == self.card2.pposition[0]:
                    animation: RigidAnimation = RigidAnimation(300, self.card1, (0.25, 0.5))
                    self.animation_registry.rigid_animation = animation
                    # self.animation_registry.animation_queue.append(FadeIn(300, self.card1.texture))
                else:
                    animation: RigidAnimation = RigidAnimation(300, self.card1, self.card2.pposition)
                    self.animation_registry.rigid_animation = animation
                    # self.animation_registry.animation_queue.append(FadeOut(300, self.card1.texture))
        else:
            pass

    def Draw(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        self.background.Draw(surface, WIDTH, HEIGHT)
        self.animate_button.Draw(surface, WIDTH, HEIGHT)
        self.card1.Draw(surface, WIDTH, HEIGHT)
        self.card2.Draw(surface, WIDTH, HEIGHT)
        self.animating_text.Draw(surface, WIDTH, HEIGHT)
        
    def ButtonEventCheck(self, MouseClicked: bool, MousePosition: list[int, int], WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        if self.animation_registry.CutsceneInProcess(): MouseClicked = False
        for button in self.root_node.buttons:
            button: Buttons = button
            button.is_clicked = MouseClicked
            if MouseClicked:
                button.ClickCheck(MousePosition, WIDTH, HEIGHT)
        # only one to check no need to create queue system

                


screen = pg.display.set_mode((WIDTH, HEIGHT))

pg.init()

clock = pg.time.Clock()


icon = pg.image.load(r"assets\icon\King_of_Diamonds.png").convert_alpha()
pg.display.set_icon(icon)

GraphFont = GraphicText((0.5, 0.5), default_font, "im vincing it, soo good!", True)
GraphFont.Transfrom()

gameloop = GameLoopBlackJack()
gameloop.player.DrawCardFromDeck(gameloop.card_deck)
gameloop.player.DrawCardFromDeck(gameloop.card_deck)
gameloop.host.DrawCardFromDeck(gameloop.card_deck)
gameloop.host.DrawCardFromDeck(gameloop.card_deck)

animation_loop = AnimationLoop()

running = True
mouse_clicked = False

previous_time = time.time()
while running:
    dt = time.time() - previous_time
    previous_time = time.time()

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


    # gameloop.Loop()
    # gameloop.Draw(screen, MousePosition, WIDTH, HEIGHT)    
    # gameloop.HandleButtonCheck(mouse_clicked, MousePosition)
    
    animation_loop.GameLoop()
    if animation_loop.animation_registry.CutsceneInProcess(): mouse_clicked = False
    animation_loop.ButtonEventCheck(mouse_clicked, MousePosition, WIDTH, HEIGHT)

    animation_loop.Draw(screen, WIDTH, HEIGHT)
    animation_loop.animation_registry.Animating(dt)

    # inspecting_texts.ManualLog("nigger", screen, (50, 50))

    # DebugKitDraw([inspecting_lines, inspecting_points, inspecting_texts], screen)
    # DebugKitClear([inspecting_lines, inspecting_points, inspecting_texts])

    pg.display.flip()
    pg.display.set_caption(f"{clock.get_fps() // 1}")
    clock.tick(FPS)


