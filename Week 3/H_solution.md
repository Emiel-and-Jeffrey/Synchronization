Assume we have at least `1` left-handed philosopher and at least `1` right-handed philosopher.

## Used variables
```python
n = 5
forks = [Semaphore(1) for i in range(n)]
```

## Helper function for forks
```python
def left(i):
    return i

def right(i):
    return (i + 1) % n
```

## Right-handed philosopher code
```python
def right_handed_philosopher(i):
    while True:
        think()

        forks[right(i)].wait()
        forks[left(i)].wait()

        eat()
        
        forks[right(i)].signal()
        forks[left(i)].signal()
```

## Left-handed philosopher code
```python
def left_handed_philosopher(i):
    while True:
        think()

        forks[left(i)].wait()
        forks[right(i)].wait()

        eat()

        forks[left(i)].signal()
        forks[right(i)].signal()
```