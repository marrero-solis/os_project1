import socket
import sys
import time
from threading import Thread
from random import randint

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)

max_jobs = 4
class edevice(Thread):
    def __init__(self, ID):
        self.ID = ID
        Thread.__init__(self)

    def run(self):
        for i in range(max_jobs):
            # Get random amount of time in the compute server
            job_time = randint(1,10)

            message = "{}:{}".format(self.ID,job_time)
            # Send data
            print("sending {}".format(message))
            sock.sendto(bytes(message, "utf-8"), server_address)

            sleep_time = randint(1,5)
            time.sleep(sleep_time)
            print("Device {} slept for {} seconds".format(self.ID, sleep_time))

def main():
    device_amount = 3
    myDevices = [0] * device_amount

    # Create N threads to fill the buffer and start the threads
    for i in range(device_amount):
        myDevices[i] = edevice(i)
        myDevices[i].start()

    # Make the original thread wait for the created threads.
    for i in range(device_amount):
        myDevices[i].join()


    ### From new source
    print(sys.stderr, 'closing socket')
    sock.close()

if __name__ == "__main__":
    main()