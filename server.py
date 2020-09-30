import socket
from threading import Thread, Lock, Semaphore
import time
from operator import itemgetter

buffer_SIZE = 100
buffer = [] * buffer_SIZE
mutex = Lock()
empty = Semaphore(buffer_SIZE)
full = Semaphore(0)

job_table = {}

# Connect with server through UDP socket
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
sock.bind(server_address)

class Producer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        for i in range(buffer_SIZE):
            message, address = sock.recvfrom(4096)
            dec_msg = message.decode("utf-8")
            split_dec_msg = dec_msg.split(":")
            int_time = int(split_dec_msg[1])
            buffer_message = [split_dec_msg[0],int_time]
            empty.acquire()

            # Enter Critical Region
            mutex.acquire()
            buffer.append(buffer_message)
            print("appending message {}".format(buffer_message))
            print(buffer)
            buffer.sort(key=itemgetter(1), reverse=True)  # Simulate SJF
            print(buffer)
            mutex.release()
            # Exit Critical Region

            full.release()


class Consumer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        for i in range(buffer_SIZE):
            full.acquire()

            # Enter critical Region
            mutex.acquire()
            print(buffer)
            job = buffer.pop()
            print(buffer)
            mutex.release()
            # Exit Critical Region

            empty.release()

            # Consume Job
            if job[0] not in job_table:
                job_table[job[0]] = job[1]
            else:
                job_table[job[0]] += job[1]
            time.sleep(job[1])

def main():
    master = Producer()
    worker = Consumer()

    master.start()
    worker.start()

    master.join()
    worker.join()

    print()
    for job in job_table.keys():
        print("Device {} consumed {} seconds of the CPU time.".format(int(job), job_table[job]))


if __name__ == '__main__':
    main()