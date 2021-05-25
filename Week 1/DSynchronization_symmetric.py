from Environment import *

semaphore1 = MySemaphore(1, "semaphore1")
semaphore2 = MySemaphore(1, "semaphore2")
semaphore3 = MySemaphore(1, "semaphore3")

def thread():
    while True:
        semaphore1.wait()
        semaphore2.wait()
        semaphore1.signal()

        semaphore3.wait()
        semaphore2.signal()
        semaphore3.signal()

        semaphore2.wait()
        semaphore1.wait()
        semaphore2.signal()

        semaphore3.wait()
        semaphore1.signal()
        semaphore3.signal()

def setup():
    subscribe_thread(thread)
    subscribe_thread(thread)
    subscribe_thread(thread)
