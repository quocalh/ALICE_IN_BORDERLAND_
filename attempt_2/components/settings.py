import os

WIDTH, HEIGHT = 600, 600
FPS = 10000
# FPS = 60

PLAYER_NAME = "Duy Khang"

GAMEPLAY_MINIMUM_VITALITY: int = -5

CARD_PROPORTION_X, CARD_PROPORTION_Y = 125 / WIDTH, 200 / HEIGHT


BACKGROUND_TEXTURE_PATH: str = r"assets\background\back.jpg"



ipV4: str = "192.168.1.3"
port = 5555

MAX_CLIENT: int = 5

CLIENT_MAX_CPU_CORE_USE = 2


CLIENT_MAX_CPU_CORE_USE = min(CLIENT_MAX_CPU_CORE_USE, os.cpu_count() - 4)
print(f"This program uses {CLIENT_MAX_CPU_CORE_USE} threads")
assert CLIENT_MAX_CPU_CORE_USE >= 0, Exception("[SETUP]: dawg, get a better CPU!")


PLAYER_FRAME_PWIDTH: float = 1/8
PLAYER_FRAME_PHEIGHT: float = 1/6
