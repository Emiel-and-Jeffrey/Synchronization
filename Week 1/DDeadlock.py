from Environment import *

semaphoreA = MySemaphore(1, "semaphoreA")
semaphoreB = MySemaphore(1, "semaphoreB")
semaphoreC = MySemaphore(1, "semaphoreC")


def threadA():
    while True:
        semaphoreA.wait()

        # Resource 1
        semaphoreC.wait()
        # Resource 3
        semaphoreC.signal()

        semaphoreA.signal()


def threadB():
    while True:
        semaphoreB.wait()

        # Resource 2
        semaphoreA.wait()
        # Resource 1
        semaphoreA.signal()

        semaphoreB.signal()


def threadC():
    while True:
        semaphoreC.wait()

        # Resource 3
        semaphoreB.wait()
        # Resource 2
        semaphoreB.signal()

        semaphoreC.signal()


def setup():
    subscribe_thread(threadA)
    subscribe_thread(threadB)
    subscribe_thread(threadC)
