# Spring 2026 CSCI 4211: Introduction to Computer Networks

# This program serves as the server of the trivia game application.
# Written in Python v3.

import sys, os
from socket import *
import time
import json
import random
import signal
import threading

# The server's information when the clients and server run on the same
# machine.
LOCAL_HOST = gethostname()
LOCAL_PORT = 5001

# The server's information when the server runs in the cloud and the clients
# are remote.
REMOTE_HOST = "0.0.0.0"
REMOTE_PORT = 5001

class Server:
    '''
    Initializes any class variables and data structures and reads necessary
    files.

    Parameters
    ----------
    - server_host : str
        - The IPv4 address or hostname of the server (e.g., "100.50.200.5" or 
          "localhost"). Its value is determined by which command line option
          was used to run the server (i.e., 1 or 2).
    - server_port : int
        - The TCP port number the server will run on (e.g., 5001). Its value 
          is determined by which command line option was used to run the 
          server (i.e., 1 or 2).
    '''
    def __init__(self, server_host, server_port):
        self.LOCAL_HOST = server_host
        self.LOCAL_PORT = server_port
        return

    '''
    Configures the server socket and waits to receive a new client connection.
    Once a client connection is accepted, the server handles the client and 
    facilitates a trivia game with it.
    '''
    def run(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.LOCAL_HOST, self.LOCAL_PORT))
        print ("server binded to %s" %(self.LOCAL_PORT))

        s.listen(5)
        print ("server is listening") 

        while True:
            client, addr = s.accept()
            print('Got connection from', addr)

            try:
                th = threading.Thread(target=self.trivia_game, args=(client, addr))
                th.start()
            except:
                client.close()
        return

    '''
    The server facilitates the trivia game with the client based on the
    general interaction described in Section 2 in the instructions.

    Parameters
    ----------
    - connection_socket : socket
        - The open socket connected to the client that wants to play the
          trivia game.
    - client_address : (), tuple
        - Identifying information about the client connection (i.e., the 
          host and port number). There's no requirement for this parameter to
          be used in this function. However, it's useful when printing 
          debugging information to the server's terminal to differentiate
          between multiple clients.
    '''
    def trivia_game(self, connection_socket, client_address):
        while(1):
            answer = connection_socket.recv(1024).decode()
            if(answer == "n") or (answer == "N"):
                connection_socket.close()
                break

            with open('trivia_questions.json', 'r') as file:
                questions = json.load(file)
            count = 0
            score = 0
            while(count < 5):
                idx = random.randrange(10) + 1
                question = "\n"+questions[str(idx)][0]
                question += "\n----------------------------------------\n"

                num = 1
                for element in questions[str(idx)][1]:
                    question += (str(num)+") ")
                    question += element
                    question += "\n"
                    num += 1

                connection_socket.send(question.encode())

                answer = connection_socket.recv(1024).decode()
                if(answer == questions[str(idx)][2]):
                    connection_socket.send("Correct! +1 point".encode())
                    score += 1
                else:
                    expected_idx = int(questions[str(idx)][2]) - 1
                    connection_socket.send(("Wrong. Answer: " + questions[str(idx)][1][expected_idx]).encode())

                count+=1
            connection_socket.send(("score: " + str(score) + "/5\n").encode())
        print("Shutting down connection")
        return

    '''
    The server's signal handler. If Ctrl+C is pressed while the server is
    running, then the server will shutdown gracefully. This will allow you to
    immediately restart the server using the same port and a provide an easier
    testing process.

    NOTE: Do not modify this function beyond the listed TODO statement below.
    '''
    def signal_handler(self, sig, frame):
        print('\nReceived signal: ', sig)
        print('Performing cleanup...')
        # TODO: Add your cleanup code here (e.g., closing files, releasing 
        # resources, etc.).
        
        print('Exiting gracefully.')
        sys.exit(0)

'''
This is the main() function that first executes when server.py runs. It
initializes the server instance and then runs it. 

NOTE: Do not modify this function.
'''
if (__name__ == '__main__'):
    # Check if an argument was provided on the command line. If not, then
    # print a usage message and exit the program.
    if (len(sys.argv) != 2):
        print("\nusage: python3 server.py [1 | 2]\n")
        sys.exit(1)

    # Check the value of the provided command line argument and initialize the
    # server instance accordingly. If the value is invalid, then print a usage 
    # message and exit the program.
    option = sys.argv[1]
    if (option == "1"):
        server = Server(LOCAL_HOST, LOCAL_PORT)
    elif (option == "2"):
        server = Server(REMOTE_HOST, REMOTE_PORT)
    else:
        print("\nusage: python3 server.py [1 | 2]\n")
        sys.exit(1)
    
    # Configure the server's signal handler to handle when Ctrl+C is pressed.
    signal.signal(signal.SIGINT, server.signal_handler)
    server.run()