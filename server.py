import socket
import sys
from threading import Thread, Lock, Semaphore
import time
from operator import itemgetter
import collections

buffer_SIZE = 9
buffer = [] * buffer_SIZE
mutex = Lock()    # Mutex will protect the producer and consumer critical regions
empty = Semaphore(buffer_SIZE)   # Semaphores protect the buffer from producer and consumer accessing it at the same
full = Semaphore(0)              # time, and therefore creating race conditions.

job_table = {}   # Dictionary to be used by the consumer to accumulate the job times of each embedded device.

# Read server address from command line prompt
address = (sys.argv[1])
# Read server port from command line prompt
port = (sys.argv[2])

# Create a UDP socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# With UDP, the server needs to use bind() to create a association between its socket and the port to be used.
sock.bind((address,int(port)))

# This class simulates a producer that waits for job-time messages to be sent by embedded devices
# through a socket connection.
class Producer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # Producer will read messages until the client is done sending jobs.
        for i in range(buffer_SIZE):
            # RECEIVING AND PREPARING THE MESSAGE FOR THE BUFFER QUEUE:
            # Receive message from embedded device through a socket
            message = sock.recv(buffer_SIZE)
            # Decode message
            dec_msg = message.decode("utf-8")
            # Split message to prepare it to be inserted in 2 different spaces in the buffer queue.
            split_dec_msg = dec_msg.split(":")
            # Type cast the job time string of the message so it is ready to be ordered in the "Shortest Job First" queue
            int_time = int(split_dec_msg[1])
            # Message now ready for the queue
            buffer_message = [split_dec_msg[0],int_time]

            # Subtract an empty space that will now be filled with a job
            empty.acquire()

            # ENTER CRITICAL REGION
            mutex.acquire()
            # Insert job in the buffer queue
            buffer.append(buffer_message)
            # Keep job ordered before exiting critical region. If this step is not included in the critical region, the
            # consumer could pop the last inserted item before it was moved to its SJF place in the buffer.
            buffer.sort(key=itemgetter(1))  # Keep buffer queue organized in ascending order to simulate SJF
            mutex.release()
            # EXITED CRITICAL REGION

            # After inserting job in the buffer, increase number of available jobs to consume.
            full.release()

# This class simulates a consumer that takes out jobs from a buffer queue, keeps a table of the total amount of time that
# each embedded device spent in the cpu, and consumes each job by going to sleep the amount of time indicated by the
# popped device message.
class Consumer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # Consumer will consume the amount of job messages stored in the buffer queue.
        for i in range(buffer_SIZE):
            # Decrease the amount of available jobs to consume because the consumer is about to pop one from the buffer.
            full.acquire()

            # ENTER CRITICAL REGION
            mutex.acquire()     # Only the consumer is now allowed to access the buffer
            # Only the popping action is part of the critical for the consumer because it is the only time it shares
            # resources with the producer.
            job = buffer.pop(0)
            mutex.release()     # Now consumer lets producer use the buffer
            # EXITED CRITICAL REGION

            # Increase the amount of spaces available in th buffer because the consumer just took a message out of it.
            empty.release()

            # Consume Job
            # When an embedded device has no jobs stored in the table, this first condition will hold true.
            if job[0] not in job_table:
                job_table[job[0]] = job[1]
            # Accumulate a job's total time in the cpu.
            else:
                job_table[job[0]] += job[1]
            # Simulate executing a job
            time.sleep(job[1])

def main():

    print("Ready to receive and schedule jobs . . .")

    # Create producer and consumer threads
    master = Producer()
    worker = Consumer()

    # Start running threads
    master.start()
    worker.start()

    # Make main thread wait for producer and consumer threads to be done.
    master.join()
    worker.join()

    # When the consumer reads the Nth job from the buffer, finishes accumulating job times, and consumes those times, it
    # prints out a summary table for the total amount of the cpu time each embedded device consumed.
    ordered_table = collections.OrderedDict(sorted(job_table.items()))
    print()
    for job in ordered_table.keys():
        print("Device {} consumed {} seconds of the CPU time.".format(int(job), ordered_table[job]))

if __name__ == '__main__':
    main()