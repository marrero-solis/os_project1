import socket
import sys
import time
from threading import Thread
from random import randint

# Create a UDP socket to connect with server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Read server address from command line prompt
address = (sys.argv[1])
# Read server port from command line prompt
port = (sys.argv[2])

# Number of edevices to send jobs to the sever
eDEVICE_CNT = 3
# Maximum amount of jobs per edevice
MAX_JOBS = 3

# This class will be used to simulate several embedded devices that simultaneously send "job" messages to a server.
class Edevice(Thread):
    def __init__(self, ID):
        self.ID = ID
        Thread.__init__(self)

    def run(self):
        for i in range(MAX_JOBS):
            # Get random amount of time for a job to complete
            job_time = randint(1,10)
            # Prepare message to send
            message = "{}:{}".format(self.ID,job_time)
            # Send data through a socket connection, using the server and port addresses specified during file execution
            print("Client sending {}".format(message))
            sock.sendto(bytes(message,"utf-8"),(address,int(port)))
            # Define pause length and simulate a job execution
            sleep_time = randint(1,4)
            time.sleep(sleep_time)

def main():
    my_devices = [0] * eDEVICE_CNT

    # Create embedded device threads
    for i in range(eDEVICE_CNT):
        my_devices[i] = Edevice(i)
        my_devices[i].start()

    # Make the original thread wait for the created threads.
    for i in range(eDEVICE_CNT):
        my_devices[i].join()

    # Close the socket
    sock.close()

if __name__ == "__main__":
    main()