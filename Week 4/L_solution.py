from Environment import *

N = 5
forks = [True for i in range(N)]

mutex = MyMutex()
condition_variables = [MyConditionVariable(mutex) for i in range(N)]

def left(i):
    return i

def right(i):
    return (i + 1) % N

def forks_available(i):
    return forks[left(i)] and forks[right(i)]

def philosopher_thread(i):

    print(i)

    while True:
        print("thinking...")

        mutex.wait()

        print("i am " + str(i) + " and i need forks " + str(left(i)) + " and " + str(right(i)))
        print(forks)

        while not forks_available(i):
            condition_variables[i].wait()
        
        forks[left(i)] = False
        forks[right(i)] = False

        mutex.signal()

        print("eating")

        mutex.wait()

        forks[left(i)] = True
        forks[right(i)] = True

        condition_variables[left(i)].notify()
        condition_variables[right(i)].notify()

        mutex.signal()

def setup():
    subscribe_thread(lambda: philosopher_thread(0))
    subscribe_thread(lambda: philosopher_thread(1))
    subscribe_thread(lambda: philosopher_thread(2))
    subscribe_thread(lambda: philosopher_thread(3))
    subscribe_thread(lambda: philosopher_thread(4))