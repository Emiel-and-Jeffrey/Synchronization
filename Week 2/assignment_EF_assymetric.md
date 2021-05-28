### Initial values:
```
semaphore1 = semaphore(0)
semaphore2 = semaphore(0)
semaphore3 = semaphore(0)
semaphore4 = semaphore(0)

turnstile1 = semaphore(0)
turnstile2 = semaphore(0)
```
---
### Thread 1:
```
while(true)
{
	semaphore1.signal()
	turnstile1.wait()

	//critical section

	semaphore1.signal()
	turnstile2.wait()
}
```
---
### Thread 2:
```
while(true)
{
	semaphore2.signal()
	turnstile1.wait()

	//critical section

	semaphore2.signal()
	turnstile2.wait()
}
```
---
### Thread 3:
```
while(true)
{
	semaphore3.signal()
	turnstile1.wait()

	//critical section

	semaphore3.signal()
	turnstile2.wait()
}

```
---
### Thread 4:
```
while(true)
{
	semaphore4.signal()
	turnstile1.wait()

	//critical section

	semaphore4.signal()
	turnstile2.wait()
}
```
---
### Barrier Thread:
```
while(true)
{
	semaphore1.wait()
	semaphore2.wait()
	semaphore3.wait()
	semaphore4.wait()

	turnstile1.signal(4)

	semaphore1.wait()
	semaphore2.wait()
	semaphore3.wait()
	semaphore4.wait()

	turnstile2.signal(4)
}
```
