from Environment import *

mutex = MyMutex("mutex")
cv_reader = MyConditionVariable(mutex, "cv_reader")
cv_writer = MyConditionVariable(mutex, "cv_writer")

readers_waiting = MyInt(0, "readers_waiting")
readers_busy = MyInt(0, "reader_busy")

writers_waiting = MyInt(0, "writers_waiting")
writers_busy = MyInt(0, "writer_busy")

writer_priority = MyBool(True, "writer_priority")


def reader_thread():
    while True:

        mutex.wait()

        readers_waiting.v += 1

        while writers_busy.v > 0 or (writers_waiting.v > 0 and writer_priority.v):
            cv_reader.wait()

        readers_waiting.v -= 1
        readers_busy.v += 1

        mutex.signal()

        print("reading...")

        mutex.wait()

        readers_busy.v -= 1

        if readers_busy.v == 0:
            if writer_priority.v and writers_waiting.v > 0:
                cv_writer.notify()
            elif readers_waiting.v > 0:
                cv_reader.notify_all()

        mutex.signal()


def writer_thread():
    while True:

        mutex.wait()

        writers_waiting.v += 1

        while readers_busy.v > 0 or writers_busy.v > 0 or (readers_waiting.v > 0 and not writer_priority.v):
            cv_writer.wait()

        writers_waiting.v -= 1
        writers_busy.v += 1

        mutex.signal()

        print("writing...")

        mutex.wait()

        writers_busy.v -= 1

        if writer_priority.v and writers_waiting.v > 0:
            cv_writer.notify()
        elif readers_waiting.v > 0:
            cv_reader.notify_all()
        mutex.signal()


def setup():
    for i in range(7):
        subscribe_thread(reader_thread)
    for i in range(1):
        subscribe_thread(writer_thread)
