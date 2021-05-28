from Environment import *


def thread_a(semaphore: MySemaphore, all_semaphores: list):
    while True:

        # study
        barrier(semaphore, all_semaphores)

        # bar
        barrier(semaphore, all_semaphores)


def barrier(semaphore: MySemaphore, all_semaphores: list):
    for signaler in all_semaphores:
        signaler.signal()

    for i in range(len(all_semaphores)):
        semaphore.wait()


def create_semaphores(n: int) -> list:
    values = []
    for i in range(n):
        values.append(MySemaphore(0, "Semaphore" + str(i)))
    return values


def setup():
    semaphores = create_semaphores(4)
    
    subscribe_thread(lambda: thread_a(semaphores[0], semaphores))
    subscribe_thread(lambda: thread_a(semaphores[1], semaphores))
    subscribe_thread(lambda: thread_a(semaphores[2], semaphores))
    subscribe_thread(lambda: thread_a(semaphores[3], semaphores))