from Environment import *

serfSemaphore = MySemaphore(0, "serfSemaphore")
hackerSemaphore = MySemaphore(0, "hackerSemaphore")
totalMultiplex = MySemaphore(5, "totalMultiplex")

boatBarrier = MyBarrier(4, "boatBarrier")

boatMutex = MyMutex("boatMutex")
initializationMutex = MyMutex("initializationMutex")

serfCount = MyInt(0, "SerfCounter")
hackerCount = MyInt(0, "HackerCounter")
passengerCount = MyInt(0, "PassengerCount")


def BoatThread(my_count: MyInt, other_count: MyInt, my_semaphore: MySemaphore, other_semaphore: MySemaphore):
    while True:
        totalMultiplex.wait()  # Make sure we have at most 1 boat trips (Simplify problem)

        initializationMutex.wait()  # Protect the passenger counts
        my_count.v += 1
        if my_count.v == 4:
            my_semaphore.signal(4)
            my_count.v = 0

        elif my_count.v >= 2 and other_count.v >= 2:
            my_semaphore.signal(2)
            other_semaphore.signal(2)

            my_count.v -= 2
            other_count.v -= 2
        initializationMutex.signal()

        my_semaphore.wait()  # Let only valid people trough

        boatMutex.wait()  # Protect the boat ride. Nobody can embark when there are people leaving it.

        print("Embark")
        passengerCount.v += 1

        if passengerCount.v == 4:
            print("Rowboat")
            passengerCount.v = 0

        boatMutex.signal()

        boatBarrier.wait()  # Leave the boat together
        totalMultiplex.signal()


def setup():
    for i in range(7):
        subscribe_thread(lambda: BoatThread(serfCount, hackerCount, serfSemaphore, hackerSemaphore))

    for i in range(7):
        subscribe_thread(lambda: BoatThread(hackerCount, serfCount, hackerSemaphore, serfSemaphore))
