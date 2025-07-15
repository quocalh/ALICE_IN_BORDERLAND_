from components.UI import * 
from components.settings import *

import pygame as pg
from pygame.locals import *


screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
pg.init()
game_font = pg.font.Font(r"attempt_2\assets\font\NewCM08-Book.otf", 15)
image  = GraphicText((0.25, 0.25), game_font, "nigga move", True, (255, 255, 255))
image1 = GraphicText((0.5, 0.25), game_font, "nigga move", True, (255, 255, 255))
image2 = GraphicText((0.75, 0.25), game_font, "nigga move", True, (255, 255, 255))

image3 = GraphicFrame((0.25, 0.75), 0.05, 0.1, (255, 255, 255), WIDTH, HEIGHT)
image4 = GraphicFrame((0.5, 0.75), 0.05, 0.1, (255, 255, 255), WIDTH, HEIGHT)
image5 = GraphicFrame((0.75, 0.75), 0.05, 0.1, (255, 255, 255), WIDTH, HEIGHT)

button = Button([0.5, 0.5], 0.2, 0.1)
text_1 = GraphicText((0.5, 0.5), game_font, "nazi", True)
text_1_original = GraphicText((0.5, 0.5), game_font, "nazi", True)

text_1.pw = 0.2
text_1.ph = 0.2 
text_1.texture = pg.transform.scale(text_1_original.texture, (text_1.pw * WIDTH, 0 * HEIGHT))
text_1.texture = pg.transform.scale(text_1_original.texture, (text_1.pw * WIDTH, text_1.ph * HEIGHT))
# text_1.texture.fill((255, 255, 0))
running = True
while running:
    screen.fill((0, 0, 0))
    mouse_leftclick = False
    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == BUTTON_LEFT:
                button.ClickCheck(pg.mouse.get_pos(), WIDTH, HEIGHT)
                mouse_leftclick = True
    
    
    if button.is_clicked and mouse_leftclick:
        print("clicked")

    button.Draw(screen)
    text_1.Draw(screen)
    

    image.Draw(screen)
    image1.Draw(screen)
    image2.Draw(screen)


    image3.Draw(screen, WIDTH, HEIGHT)
    image4.Draw(screen, WIDTH, HEIGHT)
    image5.Draw(screen, WIDTH, HEIGHT)

    pg.display.flip()
    pg.display.set_caption(f"{clock.get_fps() // 1}")
    clock.tick()
