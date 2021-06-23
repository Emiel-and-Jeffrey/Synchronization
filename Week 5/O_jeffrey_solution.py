from enum import Enum

from Environment import *


class States(str, Enum):
    RopeEmpty = "Rope empty"
    SouthCrossing = "South crossing"
    NorthCrossing = "North crossing"
    Queued = "Queued"


class Side:
    climb_count: MyInt
    queue_count: MyInt
    semaphore: MySemaphore
    active_state: States

    def __init__(self, count: MyInt, queue: MyInt, semaphore: MySemaphore, active_state: States):
        self.climb_count = count
        self.queue_count = queue
        self.semaphore = semaphore
        self.active_state = active_state


active_state = MyString(States.RopeEmpty, "state")
mutex = MyMutex("state mutex")
capacity = MySemaphore(5, "capacity")

northSide = Side(MyInt(0, "north crossing count"), MyInt(0, "north enqueued count"),
                 MySemaphore(0, "northern semaphore"), States.NorthCrossing)
southSide = Side(MyInt(0, "southern crossing count"), MyInt(0, "southern enqueued count"),
                 MySemaphore(0, "southern semaphore"), States.SouthCrossing)


def baboon_thread(my_side: Side, other_side: Side):
    while True:
        mutex.wait()
        my_side.queue_count.v += 1
        if active_state.v == States.RopeEmpty or active_state.v == my_side.active_state:
            change_state(my_side.active_state)
            singal_side(1, my_side)
        elif active_state.v == other_side.active_state:
            change_state(States.Queued)

        mutex.signal()

        # Wait for rope
        my_side.semaphore.wait()

        capacity.wait()
        # cross stuff
        capacity.signal()

        mutex.wait()
        my_side.climb_count.v -= 1
        # Rope empty
        if my_side.climb_count.v == 0:
            if active_state.v == States.Queued:
                change_state(other_side.active_state)
                singal_side(other_side.queue_count.v, other_side)
            else:
                change_state(States.RopeEmpty)

        mutex.signal()


def singal_side(amount: int, side: Side):
    side.semaphore.signal(amount)
    side.climb_count.v += amount
    side.queue_count.v -= amount


def change_state(new_state: States):
    active_state.v = new_state


def setup():
    for i in range(7):
        subscribe_thread(lambda: baboon_thread(northSide, southSide))
    for i in range(7):
        subscribe_thread(lambda: baboon_thread(southSide, northSide))
