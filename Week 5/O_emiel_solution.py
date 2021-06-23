from Environment import *

EMPTY = 'rope empty'
RIGHT_CROSSING = 'righties crossing'
LEFT_CROSSING = 'lefties crossing'

state = MyString(EMPTY, 'state')

multiplex = MySemaphore(5, 'multiplex')

mutex = MyMutex('mutex')

lefties_cv = MyConditionVariable(mutex, 'lefties_cv')
righties_cv = MyConditionVariable(mutex, 'righties_cv')

lefties_waiting = MyInt(0, 'lefties_waiting')
righties_waiting = MyInt(0, 'righties_waiting')

lefties_crossing = MyInt(0, 'lefties_crossing')
righties_crossing = MyInt(0, 'righties_crossing')

def baboon_thread(
    waiting_counter: MyInt, nwaiting_counter: MyInt,
    crossing_counter: MyInt, ncrossing_counter: MyInt,
    crossing_state: str, ncrossing_state: str,
    cv: MyConditionVariable, ncv: MyConditionVariable):

    while True:
        mutex.wait()

        waiting_counter.v += 1

        if state.v == EMPTY:
            state.v = crossing_state

        while state.v == ncrossing_state or ncrossing_counter.v > 0:
            cv.wait()
        
        waiting_counter.v -= 1
        crossing_counter.v += 1

        mutex.signal()

        multiplex.wait()

        print('crossing...')

        multiplex.signal()

        mutex.wait()

        crossing_counter.v -= 1

        if state.v == crossing_state and nwaiting_counter.v > 0:
            state.v = ncrossing_state
            ncv.notify_all()

        if state.v == ncrossing_state and crossing_counter.v == 0:
            ncv.notify_all()

        if state.v == crossing_state and crossing_counter.v == 0:
            state.v = EMPTY

        mutex.signal()

def setup():
	subscribe_thread(lambda: baboon_thread(lefties_waiting, righties_waiting, lefties_crossing, righties_crossing, LEFT_CROSSING, RIGHT_CROSSING, lefties_cv, righties_cv))
	subscribe_thread(lambda: baboon_thread(lefties_waiting, righties_waiting, lefties_crossing, righties_crossing, LEFT_CROSSING, RIGHT_CROSSING, lefties_cv, righties_cv))
	subscribe_thread(lambda: baboon_thread(lefties_waiting, righties_waiting, lefties_crossing, righties_crossing, LEFT_CROSSING, RIGHT_CROSSING, lefties_cv, righties_cv))
	subscribe_thread(lambda: baboon_thread(lefties_waiting, righties_waiting, lefties_crossing, righties_crossing, LEFT_CROSSING, RIGHT_CROSSING, lefties_cv, righties_cv))
	subscribe_thread(lambda: baboon_thread(lefties_waiting, righties_waiting, lefties_crossing, righties_crossing, LEFT_CROSSING, RIGHT_CROSSING, lefties_cv, righties_cv))
	subscribe_thread(lambda: baboon_thread(lefties_waiting, righties_waiting, lefties_crossing, righties_crossing, LEFT_CROSSING, RIGHT_CROSSING, lefties_cv, righties_cv))
	subscribe_thread(lambda: baboon_thread(lefties_waiting, righties_waiting, lefties_crossing, righties_crossing, LEFT_CROSSING, RIGHT_CROSSING, lefties_cv, righties_cv))
	subscribe_thread(lambda: baboon_thread(lefties_waiting, righties_waiting, lefties_crossing, righties_crossing, LEFT_CROSSING, RIGHT_CROSSING, lefties_cv, righties_cv))

	subscribe_thread(lambda: baboon_thread(righties_waiting, lefties_waiting, righties_crossing, lefties_crossing, RIGHT_CROSSING, LEFT_CROSSING, righties_cv, lefties_cv))
	subscribe_thread(lambda: baboon_thread(righties_waiting, lefties_waiting, righties_crossing, lefties_crossing, RIGHT_CROSSING, LEFT_CROSSING, righties_cv, lefties_cv))