# QueueUp - A simple and easy queue interface for all of your needs


**QueueUp** -- Is an entirely integrated queue interface over kombu to completely include all settings inside of a single object.

The reason we use `kombu` and AMQP as a whole is to allow for complex objects and delivery guaruntees we normally wouldn't get with much newer platforms.




## Differences from QueueUp and Queue

You'd use the `QueueUp` library in the exact way you'd use the `queue.Queue` library. Let's look at the difference.

**An example for python's `queue`**
```py
import time
import random
import threading
from queue import Queue


# We're starting two threading daemons, 
# 1. one that pushes information into a queue, 
# 2. the other that reads information from the queue then publishes it



def queue_pusher(q):
    while True:
        q.put(random.randint(0, 1000))
        time.sleep(0.05)


def queue_reciever(q):
    while True:
        qitem = q.get(block=True)
        print(f"Printing {item}")
        time.sleep(0.05)

if __name__ == "__main__":
    common_queue = Queue()
    threading.Thread(target=queue_pusher, daemon=True, args=(common_queue,)).start()
    threading.Thread(target=queue_reciever, daemon=True, args=(common_queue,)).start()
    
    # Now the two queues will communicate with each other.
    
    while True:
        time.sleep(5)
```

**An example for `QueueUp`**


```py
import time
import random
import threading
from queueup import Queue


# We're starting two threading daemons, 
# 1. one that pushes information into a queue, 
# 2. the other that reads information from the queue then publishes it



def queue_pusher(q):
    while True:
        q.put(random.randint(0, 1000))
        time.sleep(0.05)


def queue_reciever(q):
    while True:
        qitem = q.get(block=True)
        print(f"Printing {item}")
        time.sleep(0.05)

if __name__ == "__main__":
    common_queue = Queue() # w/o parameters it returns a multiprocessing.Queue()
    threading.Thread(target=queue_pusher, daemon=True, args=(common_queue,)).start()
    threading.Thread(target=queue_reciever, daemon=True, args=(common_queue,)).start()
    
    # Now the two queues will communicate with each other.
    
    while True:
        time.sleep(5)
```