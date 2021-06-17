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

heathens = MyInt(0, "heathens")
prudes = MyInt(0, "prudes")

state = MyString("", "state")

def person_thread(
        counter: MyInt, ncounter: MyInt,
        buffer_cv: MyConditionVariable,
        queue_cv: MyConditionVariable, nqueue_cv: MyConditionVariable,
        rule_state: str, nrule_state: str,
        transition_state: str, ntransition_state: str):
    while True:

        mutex.wait()

        #first condition variable: (acts as a transition buffer to prevent newcomers adding to the queue)
        #-heathens get stuck here if state == "transitioning to prudes"
        #-prudes get stuck here if state == "transitioning to heathens"
        while state.v == ntransition_state:
            buffer_cv.wait()

        counter.v += 1

        #if statements:
        #-heathens:
        #   if state == "neutral":
        #       state == "heathens rule"
        #   if state == "prudes rule" && heathens > prudes:
        #       state = "transitioning to heathens"
        #
        #-prudes:
        #   if state == "neutral":
        #       state == "prudes rule"
        #   if state == "heathens rule" && prudes > heathens:
        #       state = "transitioning to prudes"
        if state.v == NEUTRAL:
            state.v == rule_state

        elif state.v == nrule_state and counter.v > ncounter.v:
            state.v == transition_state

        #second condition variable: (acts as the queue for when we cannot enter the field directly)
        #-heathens get stuck here if state == "prudes rule" || "transitioning to heathens"
        #-prudes get stuck here if state == "heathens rule" || "transitioning to prudes"
        while state.v == nrule_state or state.v == transition_state:
            queue_cv.wait()

        mutex.signal()

        print("walking field...")

        mutex.wait()

        counter.v -= 1

        #if statements:
        #-heathens:
        #   if state == "heathens rule" && heathens == 0:
        #       state == "neutral"
        #   if state == "heathens rule" && prudes > heathens:
        #       state == "transitioning to prudes"
        #   
        #-prudes:
        #   if state == "prudes rule" && prudes == 0:
        #       state == "neutral"
        #   if state == "prudes rule" && prudes > heathens:
        #       state == "transitioning to heathens"
        if state.v == rule_state and ncounter.v > counter.v:
            state.v == ntransition_state

        if state.v == ntransition_state and counter.v == 0:
            state.v == nrule_state
            nqueue_cv.notify_all()
            buffer_cv.notify_all()
        
        if state.v == rule_state and counter.v == 0:
            state.v == NEUTRAL

        mutex.signal()

def setup():
	subscribe_thread(lambda: person_thread(heathens, prudes, heathens_buffer_cv, heathens_queue_cv, prudes_queue_cv, HEATHENS_RULE, PRUDES_RULE, HEATHENS_TRANSITION, PRUDES_TRANSITION))
	subscribe_thread(lambda: person_thread(heathens, prudes, heathens_buffer_cv, heathens_queue_cv, prudes_queue_cv, HEATHENS_RULE, PRUDES_RULE, HEATHENS_TRANSITION, PRUDES_TRANSITION))
	subscribe_thread(lambda: person_thread(heathens, prudes, heathens_buffer_cv, heathens_queue_cv, prudes_queue_cv, HEATHENS_RULE, PRUDES_RULE, HEATHENS_TRANSITION, PRUDES_TRANSITION))
