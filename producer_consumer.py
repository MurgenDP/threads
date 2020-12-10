from time import sleep
from threading import Condition, Thread
import threading
from random import random, randint

def printc(text, c1, c2):
    return print(c1+text+c2)

class Buffer:
    def __init__(self):
        self.buffer = []
        self.size_limit = 20

    def push(self, val):
        if len(self.buffer) >= self.size_limit:
            raise ValueError('Buffer is full')
        self.buffer.append(val)

    def pop(self):
        return self.buffer.pop(0)

    def is_empty(self):
        return not len(self.buffer)

    def is_full(self):
        return len(self.buffer) == self.size_limit

    def __repr__(self):
        return repr(self.buffer)


cv = Condition()
q = Buffer()
threads = []

def worker_producer(cv, sleeptime=0.5, name=""):
    # while True:
    global q
    threads.append(name)
    for _ in range(100):
        with cv:
            # Wait while buffer is full
            while q.is_full():
                printc(f"{name}: --> FULL", '\033[91m', '\033[0m')
                if len(threads) == 1:
                    break
                cv.wait()
            try:
                q.push(randint(1, 10))
                print(f"{name}: --> {q}")
                cv.notify_all()
            except:
                cv.notify_all()
        sleep(sleeptime)
    print(f"{name}: --> EXIT")
    threads.remove(name)


def worker_consumer(cv, sleeptime=0.3, name=""):
    global q
    threads.append(name)
    # while True:
    for _ in range(100):
        with cv:
            while q.is_empty():
                printc(f"{name}: --> EMPTY", '\033[92m', '\033[0m')
                if len(threads) == 1:
                    break
                cv.wait()
            try:
                q.pop()
                print(f"{name}: --> {q}")
                cv.notify_all()
            except:
                cv.notify_all()
        sleep(sleeptime)
    print(f"{name}: --> EXIT")
    threads.remove(name)


# if __name__ == '__main__':
Thread(target=worker_producer, name='worker_producer_1', args=(cv, 0.1, "Producer 1",)).start()
Thread(target=worker_producer, name='worker_producer_2', args=(cv, 0.3, "Producer 2",)).start()
Thread(target=worker_producer, name='worker_producer_3', args=(cv, 0.2, "Producer 3",)).start()

Thread(target=worker_consumer, name='worker_consumer_1', args=(cv, 0.25, "Consumer 1",)).start()
Thread(target=worker_consumer, name='worker_consumer_2', args=(cv, 0.3, "Consumer 2",)).start()
Thread(target=worker_consumer, name='worker_consumer_3', args=(cv, 0.1, "Consumer 3",)).start()

for thread in threading.enumerate():
    print("Имя потока %s." % thread.getName())

