import socket
import sys
import time
from threading import Thread
from random import randint

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)

device_count = 4
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
            print("Client sending {}".format(message))
            sock.sendto(bytes(message, "utf-8"), server_address)

            sleep_time = randint(1,4)
            time.sleep(sleep_time)
            print("Device {} slept for {} seconds".format(self.ID, sleep_time))

def main():
    myDevices = [0] * device_count

    # Create device threads
    for i in range(device_count):
        myDevices[i] = edevice(i)
        myDevices[i].start()

    # Make the original thread wait for the created threads.
    for i in range(device_count):
        myDevices[i].join()

    # Close the socket
    sock.close()

if __name__ == "__main__":
    main()