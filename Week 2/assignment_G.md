## Used variables
```python
pipet1 = semaphore(1)
pipet2 = semaphore(1)

rendevouz1 = semaphore(0)
rendevouz2 = semaphore(0) 
```

```python
def Leader_thread():
    pipet1.wait()

    rendevouz2.signal()
    rendevouz1.wait()

    # critical section

    pipet1.signal()
```

```python
def Follower_thread():
    pipet2.wait()

    rendevouz1.signal()
    rendevouz2.wait()

    # critical section

    pipet2.signal()
```
