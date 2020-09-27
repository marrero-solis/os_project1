import socket
import sys
import time
from threading import Thread
from random import randint


# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Read edevice ID from run command
deviceID = sys.argv[1]
# Initialize <server address> and <server port>
HOST, PORT = "localhost", 4017
#data = " ".join(sys.argv[1:])
max_jobs = 4

class edevice(Thread):
    def __init__(self, ID):
        self.ID = ID
        Thread.__init__(self)

    def run(self):
        # Get random amount of time in the compute server
        job_time = randint(1,10)
        # Send message to server
        message = "{}:{}".format(self.ID,job_time)
        sock.sendto(bytes(message, "utf-8"), (HOST, PORT))

        # Format of the socket object: socket.recv(buffersize[,flags])
        received = str(sock.recv(1024), "utf-8")

        print("Sent:     {}".format(message))
        print("Received: {}".format(received))
        sleep_time = randint(1,5)
        time.sleep(sleep_time)
        print("I'm done, slept for {} seconds".format(sleep_time))

def main():
    # Create edevice Thread object
    myDevice = edevice(deviceID)
    # Start running the device thread
    myDevice.start()
    # Wait for thread to be done
    myDevice.join()

if __name__ == "__main__":
    main()