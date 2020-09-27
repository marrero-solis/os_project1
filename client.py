import socket
import sys
import time
from threading import Thread
from random import randint


# Connect with server through UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Read edevice ID from run command
#deviceID = sys.argv[1]
# Initialize <server address> and <server port>
HOST, PORT = "localhost", 4017
#data = " ".join(sys.argv[1:])
max_jobs = 4

class edevice(Thread):
    def __init__(self, ID):
        self.ID = ID
        Thread.__init__(self)

    def run(self):
        for i in range(max_jobs):
            # Get random amount of time in the compute server
            job_time = randint(1,10)

            # Send message to server
            message = "{}:{}".format(self.ID,job_time)
            sock.sendto(bytes(message, "utf-8"), (HOST, PORT))

            # Format of the socket object: socket.recv(buffersize[,flags])
            #received = str(sock.recv(1024), "utf-8")

            print("Sent: {}".format(message))
            #print("Received: {}".format(received))
            sleep_time = randint(1,5)
            time.sleep(sleep_time)
            print("Device {} slept for {} seconds".format(self.ID, sleep_time))

def main():
    device_amount = 10
    myDevices = [0] * device_amount

    # Create N threads to fill the buffer and start the threads
    for i in range(device_amount):
        myDevices[i] = edevice(i)
        myDevices[i].start()

    # Make the original thread wait for the created threads.
    for i in range(device_amount):
        myDevices[i].join()

if __name__ == "__main__":
    main()