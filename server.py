import socket
from threading import Thread, Lock, Semaphore
import time
from operator import itemgetter

buffer_SIZE = 12
buffer = []*buffer_SIZE
mutex = Lock()
empty = Semaphore(buffer_SIZE)
full = Semaphore(0)

job_table = {}
counter = 0

# Connect with server through UDP socket
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

class Producer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        for i in range(buffer_SIZE):
        #while True:
            message, address = sock.recvfrom(4096)
            dec_msg = message.decode("utf-8")
            #device_ID, job_time = dec_msg[0], dec_msg[1]
            print(dec_msg)

            empty.acquire()
            # Enter Critical Region
            mutex.acquire()
            split_dec_msg = dec_msg.split(":")
            print("newly split message: {}".format(split_dec_msg))
            buffer.append(split_dec_msg)
            buffer.sort(key=itemgetter(1), reverse=True)  # Simulate SJF
            mutex.release()
            # Exit Critical Region
            full.release()


class Consumer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        for i in range(buffer_SIZE):
        #while True:
            full.acquire()
            # Enter critical Region
            mutex.acquire()
            print("Next item in the queue: {}".format(buffer[-1]))
            job = buffer.pop()
            mutex.release()
            # Exit Critical Region
            empty.release()

            # Consume Item
            if job[0] not in job_table:
                job_table[job[0]] = int(job[1])
            else:
                job_table[job[0]] += int(job[1])

            time.sleep(int(job[1]))


def main():
    master = Producer()
    worker = Consumer()

    master.start()
    worker.start()

    master.join()
    worker.join()

    print("Final Job Table:")
    print(job_table)

if __name__ == '__main__':
    main()