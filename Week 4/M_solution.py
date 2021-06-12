from Environment import *

# these are constants, do not touch
CARNIVORE = 0
VEGETARIAN = 1

NR_O_SERVINGS = 5

#simplify problem by making sure cooks can always add servings to pot regardless of type
servings = MyBag(size=NR_O_SERVINGS*2)

mutex = MyMutex()
empty_pot = [MySemaphore(1), MySemaphore(1)]
condition_variables = [MyConditionVariable(mutex), MyConditionVariable(mutex)]

def food_left(savage_type):
    if savage_type == CARNIVORE:
        return servings.contains("meat")
    else:
        return servings.contains("vegetable")

def get_food(savage_type):
    if savage_type == CARNIVORE:
        servings.get("meat")
        return "meat"
    else:
        servings.get("vegetable")
        return "vegetable"

def put_food(savage_type):
    if savage_type == CARNIVORE:
        for i in range(NR_O_SERVINGS):
            servings.put("meat")
    else:
        for i in range(NR_O_SERVINGS):
            servings.put("vegetable")

def cook_thread(savage_type):
    while True:
        empty_pot[savage_type].wait()

        mutex.wait()

        put_food(savage_type)

        condition_variables[savage_type].notify()

        mutex.signal()

def savage_thread(savage_type):
    while True:
        mutex.wait()

        while not food_left(savage_type):
            condition_variables[savage_type].wait()
        
        food = get_food(savage_type)
        if not food_left(savage_type):
            empty_pot[savage_type].signal()

        mutex.signal()

        print("eating " + food)

def setup():
    subscribe_thread(lambda: cook_thread(CARNIVORE))
    subscribe_thread(lambda: cook_thread(VEGETARIAN))

    subscribe_thread(lambda: savage_thread(CARNIVORE))
    subscribe_thread(lambda: savage_thread(CARNIVORE))
    subscribe_thread(lambda: savage_thread(VEGETARIAN))
    subscribe_thread(lambda: savage_thread(VEGETARIAN))