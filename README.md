# Project No.1: Interprocess Communication

Lilliana Marrero Solís 
CCOM4017 Operating Systems
Prof. J.R. Ortíz Ubarri
University of Puerto Rico, Río Piedras


This project consists of two files that communicate through sockets to simulate a server-client scenario. 
The client file has multiple embedded devices that simultaneously send jobs to execute to a server. In the server file 
a producer schedules the embedded device's jobs, and a consumer accumulates the total amount of time each 
device spends in the cpu, and then prints a summary of each device's activity in the cpu.

To achieve these, multiple threads have to be running at the same time in both files. The threads created in the client 
file will not cause any race conditions because they don't share any resources. On the other hand, the producer thread
and the consumer thread will create race conditions because they share the buffer where job messages are stored.
To deal with this problem, I used mutexes and semaphores. A mutex lock is used to protect the critical regions because 
it can only be used by one thread. To protect access to the buffer, I used semaphores because these can be used by
multiple threads at the same time.

The configuration variables are set the following way: 
    - In the client file, there are T device threads that run K jobs
    - In the server file, the buffer (N) will have a maximum amount of messages of T*K
      In other words, N = T*K

To execute the server file from the command line, use:
> python server.py <server address> <server port>

To execute the client file from the command line, use:
> python client.py <server address> <server port>


This program was created using Python, version 3.7


REFERENCES:

Semaphore examples from: 
https://stackoverflow.com/questions/31508574/semaphores-on-python

Learned how to read arguments from the command line from:
https://www.tutorialspoint.com/python/python_command_line_arguments.htm

Producer-Consumer foundational concepts reviewed from CCOM4017 class module: 
https://www.youtube.com/watch?v=9Amx0e0qebA&list=PL4KOaah3haN6m7ERw8IO6wJtWVO-CvJLI&index=7&ab_channel=JoseR.OrtizUbarri

Client/Server communication and sockets reference from:
https://docs.python.org/3/library/socket.html#functions 

UDP reference from:
https://pymotw.com/2/socket/udp.html





