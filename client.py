import socket
import sys
import time
from threading import Thread
from random import randint


# Number of edevices
eDEVICE_CNT = 4
# Maximum amount of jobs per edevice
MAX_JOBS = 4
# Range of sleep times
sleep_time = randint(1,4)


# Read server address from command line prompt
address = (sys.argv[1])
# Read server port from command line prompt
port = (sys.argv[2])


# This class will be used to simulate several embedded devices that simultaneously send "job" messages to a server
# through independent sockets for each device.
class Edevice(Thread):
    def __init__(self, ID):
        self.ID = ID
        Thread.__init__(self)

    def run(self):
        # Create a UDP socket for each embedded device to connect with server
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for i in range(MAX_JOBS):
            # Get random amount of time for a job to complete
            job_time = randint(1,8)
            # Prepare message to send
            message = "{}:{}".format(self.ID,job_time)
            # Send data through a socket connection, using the server and port addresses specified during file execution
            print("Device {} sending {}".format(self.ID, message))
            sock.sendto(bytes(message,"utf-8"),(address,int(port)))
            # Pause embedded device between jobs
            time.sleep(sleep_time)
        # Close the socket
        sock.close()


def main():

    my_devices = [0] * eDEVICE_CNT

    # Create embedded device threads
    for i in range(eDEVICE_CNT):
        my_devices[i] = Edevice(i)
        my_devices[i].start()

    # Make the original thread wait for the created threads.
    for i in range(eDEVICE_CNT):
        my_devices[i].join()


if __name__ == "__main__":
    main()