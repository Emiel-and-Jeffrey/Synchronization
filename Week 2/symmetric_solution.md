### Symmetric solution using variables
```
semaphore1 = semaphore(0)
mutex1 = semaphore(1)

semaphore2 = semaphore(0)
mutex2 = semaphore(1)

toggle1 = false
toggle2 = true
```

```
function Barrier()
{
    while(true)
    {
        semaphore1.signal()

        mutex1.wait()
        if(!toggle1)
        {
            semaphore1.wait()
            semaphore1.wait()
            semaphore1.wait()
            semaphore1.wait()

            toggle1 = true
            toggle2 = false
        }
        mutex1.signal()

        //critical section

        semaphore2.signal()

        mutex2.wait()
        if(!toggle2)
        {
            semaphore2.wait()
            semaphore2.wait()
            semaphore2.wait()
            semaphore2.wait()

            toggle2 = true
            toggle1 = false
        }
        mutex2.signal()
    }
}
```

### Symmetric solution using only semaphores
```
semaphore1 = semaphore(0)
mutex1 = semaphore(1)

semaphore2 = semaphore(4)
mutex2 = semaphore(1)

semaphore3 = semaphore(4)
mutex3 = semaphore(1)
```

```
function Barrier()
{
    while(true)
    {
        semaphore1.signal()
        semaphore2.wait()

        mutex1.wait()
        semaphore1.wait()
        semaphore1.wait()
        semaphore1.wait()
        semaphore1.wait()
        semaphore1.signal(4)
        mutex1.signal()

        //critical section

        semaphore2.signal()
        semaphore3.wait()

        mutex2.wait()
        semaphore2.wait()
        semaphore2.wait()
        semaphore2.wait()
        semaphore2.wait()
        semaphore2.signal(4)
        mutex2.signal()

        semaphore3.signal()
        semaphore1.wait()

        mutex3.wait()
        semaphore3.wait()
        semaphore3.wait()
        semaphore3.wait()
        semaphore3.wait()
        semaphore3.signal(4)
        mutex3.signal()
    }
}
```