import threading
import time

condition = threading.Condition()
resource = None 

local_time = 0
previous_time = time.time()

"""
ABOUT THREADING CONDITION
so basically:
    one condition must be binded in the desired objects (objects that we want to block temporary)
    
    wait and wait for
        wait() will block the whole thread, like (a while True loop with only pass statement)'s natural but more efficient, since it uses thread locks
            NOTE: wait_for() although use imported function, but it still needs to be notificated to check again 
                (you see, the wait_for() just like wait() but rather than wake up instantly when being notified
                    it just have another logic gate to check, would wake up if the logic statement is satified)
                e.g. with condition: condition.wait_for(lambda: func()), the func() return

        notify and notify all(): must be called somewhere else (avoid this condition.wait() .... condition.notify())
            , i mean must not be in the same loop, but in diff funcs, places        
"""

def producer():
    global resource # how the fuck, idk why but it needs global prefix, or else, it wont work >:(
    global local_time
    global previous_time
    dt = time.time() - previous_time
    local_time += dt
    previous_time = time.time()

    print("Producer: Waiting to produce")
    with condition:
        condition.wait()  
        print("hello, customer!")
    print("Producer: Producing")
    resource = "Data"


def consumer():
    global resource
    print("Consumer: Waiting to consume")
    with condition:
        condition.notify() # consumer active, wake up the producer to make food for the customers
        # could be condition.notify_all() since there is only one threads waiting
        condition.wait_for(lambda: not (resource is None)) # Wait until resource is available
    print("Consumer: Consuming", resource)

producer_thread = threading.Thread(target = producer)

consumer_thread = threading.Thread(target = consumer)

producer_thread.start()
consumer_thread.start()
producer_thread.join()
consumer_thread.join()