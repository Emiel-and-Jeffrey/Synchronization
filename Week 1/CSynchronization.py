from Environment import *

semaphoreA = MySemaphore(1, "semaphoreA")
semaphoreB = MySemaphore(0, "semaphoreB")
semaphoreC = MySemaphore(0, "semaphoreC")
semaphoreD = MySemaphore(0, "semaphoreD")


def threadA():
    while True:
        semaphoreA.wait()
        for i in range(1, 6):
            print(i)
        semaphoreB.signal()


def threadB():
    while True:
        semaphoreB.wait()
        for i in range(2, 7):
            print(i)
        semaphoreC.signal()


def threadC():
    while True:
        semaphoreC.wait()
        for i in range(3, 8):
            print(i)
        semaphoreD.signal()


def threadD():
    while True:
        semaphoreD.wait()
        for i in range(4, 9):
            print(i)
        semaphoreA.signal()


def setup():
    subscribe_thread(threadA)
    subscribe_thread(threadB)
    subscribe_thread(threadC)
    subscribe_thread(threadD)
