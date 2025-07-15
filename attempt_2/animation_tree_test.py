from components.animations import *
from components.settings import *
from components.UI import * 

import pygame as pg
import numpy as np
from pygame.locals import * 
import time
pg.init()
font = pg.font.Font(r"attempt_2\assets\font\NewCM08-Book.otf", 15)
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()


Frame1: GraphicFrame = GraphicFrame(
    (0.25, 0.5), 
    0.05, 0.07, 
    (255, 255, 255),
    WIDTH, HEIGHT
)
Frame2: GraphicFrame = GraphicFrame(
    (0.5, 0.5), 
    0.05, 0.07, 
    (255, 255, 255),
    WIDTH, HEIGHT
)
Frame3: GraphicFrame = GraphicFrame(
    (0.75, 0.5), 
    0.05, 0.07, 
    (255, 255, 255),
    WIDTH, HEIGHT
)
Frame4: GraphicFrame = GraphicFrame(
    (0.75, 0.5), 
    0.05, 0.07, 
    (255, 255, 255),
    WIDTH, HEIGHT
)

def what_a_function(animating_object: Graphic, t: float):
    animating_object.TextureSetAlpha(t * 255)

animation_tree = TimelineTree([
    TimelineLeaf(
        CustomAnimation(2), 1, Frame1, what_a_function
    ),
    TimelineLeaf(
        CustomAnimation(2), 1.25, Frame2, what_a_function
    ),
    TimelineLeaf(
        CustomAnimation(2), 1.5, Frame3, what_a_function
    ),
])

Text = GraphicText((0.5, 0.25), 
                   font, f"", True, 
                   (255, 255, 255), 
                   WIDTH, HEIGHT)

Frame1.TextureSetAlpha(0)
Frame2.TextureSetAlpha(0)
Frame3.TextureSetAlpha(0)
Frame4.TextureSetAlpha(0)

FPS = 20000
running = True
local_time = 0
previous_time = time.time()
while running:
    screen.fill((0, 0, 0))
    dt = time.time() - previous_time
    previous_time = time.time()
    
    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    
    # animation_tree.Update(dt)
    animation_tree.UpdateAndRender(dt, screen)
    # Frame1.TextureSetAlpha(animation_tree.get_t(0) * 255)
    # Frame2.TextureSetAlpha(animation_tree.get_t(1) * 255)
    # Frame3.TextureSetAlpha(animation_tree.get_t(2) * 255)

    local_time += dt
    Text.ChangeMessage(f"{local_time:.02f}", WIDTH, HEIGHT)
    Text.Draw(screen)
    
    # Frame1.Draw(screen, WIDTH, HEIGHT)
    # Frame2.Draw(screen, WIDTH, HEIGHT)
    # Frame3.Draw(screen, WIDTH, HEIGHT)

    pg.display.update()
    pg.display.set_caption(f"{clock.get_fps() // 1}")
    clock.tick(FPS)