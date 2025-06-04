import time
import threading
import queue
import random
import pygame


# Thread to calculate the next move
class AIThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.daemon = True

    def run(self):
        t_running = True
        while t_running:
            if self.queue.empty():
                time.sleep(0.1)
                print("waiting for prompt...")
                pass
            else:
                print("prompt found!")
                data = self.queue.get()
                if data == "exit":
                    t_running = False
                else:
                    # Assume it's a move command
                    move_history.append(data["move"])
                    print("finding best move... .[5 SECONDS]")

                    time.sleep(5.0)  # determine the best response move

                    print("done finding best move!")
                    print(move_history)

    def run(self):
        while True:
            data = self.queue.get()  # This blocks until data is available
            if data == "exit":
                break
            move_history.append(data["move"])
            print("finding best move... .[5 SECONDS]")
            time.sleep(5.0)
            print("done finding best move!")
            print(move_history)

WIDTH, HEIGHT = 640, 480
FPS = 600000000

move_history = []

# create a queue to send commands from the main thread
the_threading_queue = queue.Queue()
# create and then start the thread
ai_thread = AIThread(the_threading_queue)
ai_thread.start()

pygame.init()
font = pygame.font.SysFont(None, 25)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            the_threading_queue.put("exit")
        if event.type == pygame.MOUSEBUTTONUP:
            move = f"{random.choice("ABCDEFGH")}{random.choice("12345678")}"
            print("Sending Move")
            the_threading_queue.put({"move": move}); """THREADING STARTS HERE"""

    # Clear Screen
    screen.fill("gray")
    # Draw Board
    for i, move in enumerate(move_history):
        if i % 2 == 0:
            color = "white"
        else:
            color = "black"
        text = font.render(move, True, color)
        text_rect = text.get_rect(top=i * 30)
        screen.blit(text, text_rect)



    # Update Screen
    pygame.display.update()
    # Update Title
    pygame.display.set_caption(f"FPS: {clock.get_fps():.1f}")
    clock.tick(FPS)
pygame.quit()