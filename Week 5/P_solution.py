from Environment import *

NEUTRAL = "neutral"
HEATHENS_RULE = "heathens rule"
PRUDES_RULE = "prudes rule"
HEATHENS_TRANSITION = "transitioning to heathens"
PRUDES_TRANSITION = "transitioning to prudes"

mutex = MyMutex("mutex")

heathens_buffer_cv = MyConditionVariable(mutex, "heathens_buffer")
heathens_queue_cv = MyConditionVariable(mutex, "heathens_queue")

prudes_buffer_cv = MyConditionVariable(mutex, "prudes_buffer")
prudes_queue_cv = MyConditionVariable(mutex, "prudes_queue")

heathens_in_buffer = MyInt(0, "heathens_in_buffer")
prudes_in_buffer = MyInt(0, "prudes_in_buffer")

heathens_in_queue = MyInt(0, "heathens_in_queue")
prudes_in_queue = MyInt(0, "prudes_in_queue")

state = MyString(NEUTRAL, "state")

def person_thread(
        buffer_counter: MyInt,
        queue_counter: MyInt, nqueue_counter: MyInt,
        buffer_cv: MyConditionVariable,
        queue_cv: MyConditionVariable, nqueue_cv: MyConditionVariable,
        rule_state: str, nrule_state: str,
        transition_state: str, ntransition_state: str):
    while True:

        mutex.wait()

        buffer_counter.v += 1

        while state.v == ntransition_state:
            buffer_cv.wait()
        
        buffer_counter.v -= 1

        queue_counter.v += 1

        if state.v == NEUTRAL:
            state.v = rule_state

        elif state.v == nrule_state and queue_counter.v > nqueue_counter.v:
            state.v = transition_state

        while state.v == nrule_state or state.v == transition_state:
            queue_cv.wait()

        mutex.signal()

        print("walking field...")

        mutex.wait()

        queue_counter.v -= 1

        if state.v == rule_state and nqueue_counter.v > queue_counter.v:
            state.v = ntransition_state

        if state.v == ntransition_state and queue_counter.v == 0:
            state.v = nrule_state
            if nqueue_counter.v > 0:
                nqueue_cv.notify_all()
            if buffer_counter.v > 0:
                buffer_cv.notify_all()
        
        if state.v == rule_state and queue_counter.v == 0:
            state.v = NEUTRAL

        mutex.signal()

def setup():
	subscribe_thread(lambda: person_thread(heathens_in_buffer, heathens_in_queue, prudes_in_queue, heathens_buffer_cv, heathens_queue_cv, prudes_queue_cv, HEATHENS_RULE, PRUDES_RULE, HEATHENS_TRANSITION, PRUDES_TRANSITION))
	subscribe_thread(lambda: person_thread(heathens_in_buffer, heathens_in_queue, prudes_in_queue, heathens_buffer_cv, heathens_queue_cv, prudes_queue_cv, HEATHENS_RULE, PRUDES_RULE, HEATHENS_TRANSITION, PRUDES_TRANSITION))
	subscribe_thread(lambda: person_thread(heathens_in_buffer, heathens_in_queue, prudes_in_queue, heathens_buffer_cv, heathens_queue_cv, prudes_queue_cv, HEATHENS_RULE, PRUDES_RULE, HEATHENS_TRANSITION, PRUDES_TRANSITION))
	subscribe_thread(lambda: person_thread(heathens_in_buffer, heathens_in_queue, prudes_in_queue, heathens_buffer_cv, heathens_queue_cv, prudes_queue_cv, HEATHENS_RULE, PRUDES_RULE, HEATHENS_TRANSITION, PRUDES_TRANSITION))

	subscribe_thread(lambda: person_thread(prudes_in_buffer, prudes_in_queue, heathens_in_queue, prudes_buffer_cv, prudes_queue_cv, heathens_queue_cv, PRUDES_RULE, HEATHENS_RULE, PRUDES_TRANSITION, HEATHENS_TRANSITION))
	subscribe_thread(lambda: person_thread(prudes_in_buffer, prudes_in_queue, heathens_in_queue, prudes_buffer_cv, prudes_queue_cv, heathens_queue_cv, PRUDES_RULE, HEATHENS_RULE, PRUDES_TRANSITION, HEATHENS_TRANSITION))
	subscribe_thread(lambda: person_thread(prudes_in_buffer, prudes_in_queue, heathens_in_queue, prudes_buffer_cv, prudes_queue_cv, heathens_queue_cv, PRUDES_RULE, HEATHENS_RULE, PRUDES_TRANSITION, HEATHENS_TRANSITION))
