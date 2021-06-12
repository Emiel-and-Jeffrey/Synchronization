from Environment import *

#this gets stuck on the second mutex.wait for the writer and im not sure why

mutex = MyMutex("mutex")
cv_reader = MyConditionVariable(mutex,"cv_reader")
cv_writer = MyConditionVariable(mutex,"cv_writer")

nrof_reader_busy = MyInt(0,"reader_busy")
nrof_writer_busy = MyInt(0,"writer_busy")

nrof_reader_wait = MyInt(0,"reader_wait")
nrof_writer_wait = MyInt(0,"writer_wait")

writer_prio = MyBool(True,"writer_prio")

turnstile = MySemaphore(1, "turnstile")

def reader_thread():
	while True:
		
		turnstile.wait()
		turnstile.signal()
		
		mutex.wait()
		
		nrof_reader_wait.v += 1
		
		# and (writer_prio and nrof_writer_wait > 0)
		while nrof_writer_busy.v > 0:
			cv_reader.wait()
		
		nrof_reader_wait.v -= 1
		nrof_reader_busy.v += 1
		
		mutex.signal()
		
		print("reading...")
		
		mutex.wait()
		
		nrof_reader_busy.v -= 1
		
		if writer_prio.v:
			if nr_writer_wait.v > 0:
				turnstile.wait()
				cv_writer.notify()
		
		mutex.signal()	

def writer_thread():
	while True:
	
		mutex.wait()
		
		nrof_writer_wait.v += 1
		
		while nrof_writer_busy.v > 0 and nrof_reader_busy.v > 0:
			cv_writer.wait()
		
		nrof_writer_wait.v -= 1
		nrof_writer_busy.v += 1
		
		mutex.signal()
		
		print("writing...")
		
		mutex.wait()
		
		nrof_writer_busy.v -= 1
		
		if writer_prio.v:
			if nr_writer_wait.v > 0:
				cv_writer.notify()
			else:
				turnstile.signal()
				cv_reader.notify_all()
		else:
			if nr_reader_wait.v > 0:
				cv_reader.notify_all()
			else:
				cv_writer.notify()
		
		mutex.signal()

def setup():
	# subscribe_thread(reader_thread)
	# subscribe_thread(reader_thread)
	# subscribe_thread(reader_thread)
	subscribe_thread(writer_thread)