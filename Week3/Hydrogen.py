from Environment import *

oxygenPipet = MyMutex("oxygenPipet")
hydrogenSemaphore = MySemaphore(0, "hydrogenSemaphore")
creationBarrier = MyBarrier(3, "creationBarrier")


def OxygenThread():
    while True:
        oxygenPipet.wait()

        hydrogenSemaphore.signal(2)
        creationBarrier.wait()
        # Create water
        oxygenPipet.signal()


def HydrogenThread():
    while True:
        hydrogenSemaphore.wait()

        creationBarrier.wait()
        # Create water


def setup():
    for i in range(4):
        subscribe_thread(HydrogenThread)

    for i in range(8):
        subscribe_thread(OxygenThread)
