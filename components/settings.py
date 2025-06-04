import os

WIDTH, HEIGHT = 800, 800
# WIDTH, HEIGHT = 400, 400
FPS = 10_000
# FPS = 60


GAMEPLAY_MAX_LIFE: int = 5

CARD_WIDTH_TEMP = 125; "these two var are only use for direct variant"
CARD_HEIGHT_TEMP = 200; "these two var are only use for direct variant"
CARD_PROPORTION_X = CARD_WIDTH_TEMP / 800
CARD_PROPORTION_Y = CARD_HEIGHT_TEMP / 800

CARD_PWIDTH_INTERVAL = 0.1 / 2

CARD_DECK_WIDTH = 1 / 50

# BACKGROUND_TEXTURE_PATH = r"assets\background\blue_background.jpg"
# BACKGROUND_TEXTURE_PATH = r"assets\background\ril_back.png"
BACKGROUND_TEXTURE_PATH = r"assets\background\back.jpg"


ipV4: str = "192.168.1.3"
port = 5555

MAX_CLIENT: int = 5


MAX_CPU_CORE = 4 
MAX_CPU_CORE = min(MAX_CPU_CORE, os.cpu_count() - 4) 
print(f"This program uses {MAX_CPU_CORE} threads")

