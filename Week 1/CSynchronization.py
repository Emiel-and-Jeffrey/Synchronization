from Environment import *

semaphoreA = MySemaphore(1, "semaphoreA")
semaphoreB = MySemaphore(0, "semaphoreB")
semaphoreC = MySemaphore(0, "semaphoreC")
semaphoreD = MySemaphore(0, "semaphoreD")

def threadA():
    while True:
        semaphoreA.wait()
        print(1)
        semaphoreB.signal()
        semaphoreA.wait()
        print(5)
        semaphoreB.signal()

def threadB():
    while True:
        semaphoreB.wait()
        print(2)
        semaphoreC.signal()
        semaphoreB.wait()
        print(6)
        semaphoreC.signal()

def threadC():
    while True:
        semaphoreC.wait()
        print(3)
        semaphoreD.signal()
        semaphoreC.wait()
        print(7)
        semaphoreD.signal()

def threadD():
    while True:
        semaphoreD.wait()
        print(4)
        semaphoreA.signal()
        semaphoreD.wait()
        print(8)
        semaphoreA.signal()

def setup():
    subscribe_thread(threadA)
    subscribe_thread(threadB)
    subscribe_thread(threadC)
    subscribe_thread(threadD)
