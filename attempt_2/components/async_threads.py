import queue
import time
import threading
class AsyncThread:...
class AsyncThread(threading.Thread):
    thread_id = 0
    def __init__(self, condition: threading.Condition):
        super().__init__(daemon = True)
        self.action_queue: queue.Queue = queue.Queue()
        self.condition: threading.Condition = condition
    
        self.id = AsyncThread.thread_id
        AsyncThread.thread_id += 1

        self.busy_proccessing: bool = False

    def run(self):
        running = True
        while running:       
            # pay attention: this line blocks the loop until there is an item in the queue 
            #   -> optimize, avoid the cpu to loop unecessarily
            action_ticket: dict = self.action_queue.get()

            if action_ticket["function"] == "exit":
                running = False

            else:
                self.busy_proccessing = True

                try:
                    function = action_ticket["function"]
                    args = action_ticket["args"]
                    function(*args)
                except Exception as error:
                    print(f"[THREAD {self.name}] - ({function.__name__}):Unexpected problem occured: {error}")

                with self.condition:
                    self.busy_proccessing = False
                    self.condition.notify_all()
    
    def close(self):
        print(f"[AsyncThread]: Terminating the {self.name} thread ...")
        # end the life time of the run() function
        self.action_queue.put({"function": "exit", "args": ()}) 
        # note self.join(): self.join() does nothing, just waiting for the thread to terminate
        # for this type of custom thread (async_threads), the join() method waits, blocking the main thread until the run() completes its lifetime
        self.join()
    
    @property
    def busy_queueing(self) -> bool:
        return not self.action_queue.empty()

    @property
    def is_busy(self) -> bool:
        return self.busy_proccessing or self.busy_queueing

    @staticmethod 
    def thread_custom_join(threads_list: list[AsyncThread], condition: threading.Condition):
        with condition:
            condition.wait_for(lambda: all(not thread.is_busy for thread in threads_list))
        


            


    