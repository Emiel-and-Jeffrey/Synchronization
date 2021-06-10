-there are 9 reindeer threads

-there are n elf threads

-santa needs to help _at least_ 3 elves, can be more

-reindeer do **not** have priority

-the elves `getHelp()` must be executed in conjunction with santa's `helpElves()`

-solution must work with **any** number of elves


helping the elves:
after the thirds elf arrives, a semaphore must be switched allowing santa to go to the help section, when there, santa locks the help section for the elves and calls help with all elves that were able to queue in in-time

hitching the reindeer:
aften all 9 reindeer arrive, they signal santa, who will in turn release their barrier, allowing them to enter the critical section. They should then invoke `getHitched()` after santa has invoked `prepareSleigh()`

the santa semaphore indicates that either the reindeer or the elves can be helped. Santa can only help either the elves or the reindeer in one iteration of the loop

## Used variables
```python
elves = 0
reindeer = 0

santaSem = Semaphore(0)

elfMutex1 = Semaphore(1)
elfMutex2 = Semaphore(1)
reindeerMutex = Semaphore(1)

needHelpQueue = Semaphore(0)
helpedQueue = Semaphore(0)
doneHelping = Semaphore(0)

reindeerQueue = semaphore(0)
```

The below solution works only it has the disadvantage of sometimes unnecessarily waking santa
## Santa code
```python
def santa():
    santaSem.wait()
    elfMutex1.wait()
    if elves >= 3:
        needHelpQueue.signal(elves) # <-- can be removed if getHelp() is a blocking function
        helpElves()
        doneHelping.wait()
        helpedQueue.signal(elves)
    elfMutex1.signal()

    reindeerMutex.wait()
    if reindeer == 9:
        prepareSleigh()
        reindeerQueue.signal(9)
        reindeer -= 9
    reindeerMutex.signal()
```

## Elf code
```python
def elf():
    elfMutex1.wait()
    elves += 1
    if elves == 3:
        santaSem.signal()
    elfMutex1.signal()

    needHelpQueue.wait() # <-- can be removed if getHelp() is a blocking function
    getHelp()

    elfMutex2.wait()
    elves -= 1
    if elves == 0:
        doneHelping.signal()
    elfMutex2.wait()

    helpedQueue.wait() # <-- if using weak semaphores, a thread could possibly starve here
```

## Reindeer code
```python
def reindeer():
    reindeerMutex.wait()
    reindeer += 1
    if reindeer == 9:
        santaSem.signal()
    reindeerMutex.signal()

    reindeerQueue.wait()
    getHitched()
```

# Alternative solution
This alternative solution uses a turnstile controlled by the reindeer and santa to block the elves. This is to prevent starvation of the reindeer.

## Used variables
```python
elves = 0
reindeer = 0

santaSem = Semaphore(0)
elfTurnstile = Semaphore(1)

elfMutex1 = Semaphore(1)
elfMutex2 = Semaphore(1)
reindeerMutex = Semaphore(1)

needHelpQueue = Semaphore(0)
helpedQueue = Semaphore(0)
doneHelping = Semaphore(0)

reindeerQueue = semaphore(0)
```

## Santa code
```python
def santa():
    santaSem.wait()
    mutex.wait()
    if elves >= 3:
        needHelpQueue.signal(elves)
        helpElves()
        doneHelping.wait()
        helpedQueue.signal(elves)
    else if reindeer == 9:
        prepareSleigh()
        reindeerQueue.signal(9)
        reindeer -= 9
        elfTurnstile.signal()
    mutex.signal()
```

## Elf code
```python
def elf():
    elfTurnstile.wait()
    elfTurnstile.signal()

    mutex.wait()
    elves += 1
    if elves == 3:
        santaSem.signal()
    mutex.signal()

    needHelpQueue.wait()
    getHelp()

    elfMutex.wait()
    elves -= 1
    if elves == 0:
        doneHelping.signal()
    elfMutex.wait()

    helpedQueue.wait()
```

## Reindeer code
```python
def reindeer():
    mutex.wait()
    reindeer += 1
    if reindeer == 9:
        elfTurnstile.wait()
        santaSem.signal()
    mutex.signal()

    reindeerQueue.wait()
    getHitched()
```