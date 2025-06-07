import queue
import time
import threading
class AsyncThreads: ...
class AsyncThreads(threading.Thread):
    thread_id: int = 0
    def __init__(self, action_queue: queue.Queue, condition: threading.Condition):
        super().__init__(daemon = True)

        self.condition: threading.Condition = condition

        self.queue: queue.Queue = action_queue

        self.id = AsyncThreads.thread_id

        self.busy_processing: bool = False

        # string stop flag
        self.exit_string_flag: str = "exit"
    
    def SetExitStringFlag(self, string: str):
        self.exit_string_flag = string

    def run(self):
        assert self.exit_string_flag != None, "it cant be a None"
        running: bool = True
        while running:
            action_dict: str = self.queue.get()
            if action_dict == self.exit_string_flag:
                print(f"[THREAD: {self.name}]: terminating the thread...")
                running = False
            else: # found the task
                # self.busy_processing = True
                # try:
                #     # expects action_dict being written as: 
                #     # action = {"func": the_function, "args": (...)}
                #     function = action_dict["function"]
                #     args = action_dict["args"]
                #     function(*args)
                # except Exception as error:
                #     print(f"unexpected problems occured: {error}")
                # self.busy_processing = False
                with self.condition:
                    self.busy_processing = True
                try:
                    # expects action_dict being written as: 
                    # action = {"func": the_function, "args": (...)}
                    function = action_dict["function"]
                    args = action_dict["args"]
                    function(*args)
                except Exception as error:
                    print(f"unexpected problems occurred: {error}")
                with self.condition:
                    self.busy_processing = False
                    self.condition.notify_all()  # 

    def close(self):
        self.queue.put("exit")
        self.join()

    @property
    def is_busy(self) -> bool:
        # (idk how to write english without it sounding weird :sob:)
        # if the queue is empty then the thread is not busy, the opposite also true 
        # if the thread is also not process anything then we can know that it is free (not busy)
        return (not self.queue.empty()) or (self.busy_processing)


    @staticmethod
    def find_best_thread(threads_pool: list[AsyncThreads]) -> AsyncThreads:
        # find threads with minimal task
        pass

    # @staticmethod
    # def join_custom(threads_list: list[AsyncThreads]):
    #     """
    #     NOTE: can be extremely slow, since the loop is heavy without time.sleep()

    #     this will be the replicate of the join method (but still maintain its)
    #     it just a wait function, waiting for all threads to finnish all of its task before moving on (peak multi threading)
    #     how it works:
    #         it open the while True loops, that would break if the threads list meets all of the given statement:
    #             - all threads in the list must have it .is_busy = False
    #             - uhm, that is it
    #     """
        
    #     while not all(not t.is_busy for t in threads_list):
    #         pass
    @staticmethod
    def join_custom(threads_list: list[AsyncThreads], condition: threading.Condition):
        with condition:
            condition.wait_for(lambda: all(not t.is_busy for t in threads_list))

            

    


if __name__ == "__main__":
    def DelayedHello(delay: float = 2):
        time.sleep(delay)
        print(f"hello in {delay} seconds")
    
    import pygame as pg
    from pygame.locals import *
    WIDTH, HEIGHT = 640, 480
    FPS = 10




    thread_condition: threading.Condition = threading.Condition()
    the_threading_queue = queue.Queue()
    compute_thread = AsyncThreads(the_threading_queue, thread_condition)
    compute_thread.start()
    

    pg.init()
    font = pg.font.SysFont(None, 25)
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    running = True
    
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
                # compute_thread.close()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    # compute_thread.close()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == BUTTON_LEFT:
                    print("thread started")
                    compute_thread.queue.put({"function": DelayedHello, "args": ()})
                    
        print(compute_thread.is_busy)
        
        screen.fill((0, 0, 0))

        pg.display.update()
        pg.display.set_caption(f"FPS: {clock.get_fps():.1f}")
        clock.tick(FPS)

    pg.quit()
    compute_thread.close()


    

            
    
