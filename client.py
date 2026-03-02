# Spring 2026 CSCI 4211: Introduction to Computer Networks

# This program serves as the client of the trivia game application.
# Written in Python v3.

import sys
from socket import *
import json

# The server's information when the clients and server run on the same
# machine.
LOCAL_HOST = gethostname()
LOCAL_PORT = 5001

# The server's information when the server runs in the cloud and the clients
# are remote.
REMOTE_HOST = "52.14.112.108"
REMOTE_PORT = 5001

class Client:
    '''
    Initializes any class variables and data structures.

    Parameters
    ----------
    - server_host : str
        - The IPv4 address or hostname of the server (e.g., "100.50.200.5" or 
          "localhost"). Its value is determined by which command line option
          was used to run the client (i.e., 1 or 2).
    - server_port : int
        - The TCP port number the server will run on (e.g., 5001). Its value 
          is determined by which command line option was used to run the 
          client (i.e., 1 or 2).
    '''
    def __init__(self, server_host, server_port):
        self.LOCAL_HOST = server_host
        self.LOCAL_PORT = server_port
        return
    
    def recv_until_end(self, sock):
        data = ""
        while True:
            chunk = sock.recv(1024).decode()
            if not chunk:
                break
            data += chunk
            if "END" in data:
                return data.split("END")[0]
    
    '''
    Connects to the server and facilitates the trivia game with the server
    based on the general interaction described in Section 2 in the 
    instructions.
    '''    
    def run(self):
        print("=====================================================================")
        print("                    University of Minnesota Trivia                   ")
        print("=====================================================================\n")
            
        print("\n------------------------- GAME INSTRUCTIONS -------------------------")
        print("  • Five random trivia questions about the University of Minnesota")
        print("    will be proposed to you along with possible answers.\n")
        
        print("  • Select your answer by entering the associated number (e.g., '1').\n")
        
        print("  • After all five questions have been answered, you will receive")
        print("    your total score.")

        server = socket()   
        server.connect((self.LOCAL_HOST, self.LOCAL_PORT)) 

        while(1):
        
            print("\nWould you like to start a new game? [y/n]: ")

            # Get the user's response.
            while (1):
                print("Input: ", end = "")
                st = input()
                if ((st != "y") and (st != "Y") and (st != "n") and (st != "N")):
                    continue
                else:
                    server.send(st.encode())
                    break

            # If the input is "n" or "N", then quit the program.
            if ((st == "n") or (st == "N")):
                print("\nClient is exiting...")
                sys.exit(0)

            count = 0
            while(count < 5):
                print (self.recv_until_end(server))

                print("Answer: ", end = "")
                st = input()
                
                server.send(st.encode())
                print(self.recv_until_end(server))
                count+=1
            print(self.recv_until_end(server))
            
            print("\n----------------------------- GAME OVER -----------------------------")
            
            print("\nThanks for playing!")

        server.close()  

'''
This is the main() function that first executes when client.py runs. It
initializes the client instance and then runs it. 

NOTE: Do not modify this function.
'''
if (__name__ == '__main__'):
    # Check if an argument was provided on the command line. If not, then
    # print a usage message and exit the program.
    if (len(sys.argv) != 2):
        print("\nusage: python3 client.py [1 | 2]\n")
        sys.exit(1)

    # Check the value of the provided command line argument and initialize the
    # server instance accordingly. If the value is invalid, then print a usage 
    # message and exit the program.
    option = sys.argv[1]
    if (option == "1"):
        client = Client(LOCAL_HOST, LOCAL_PORT)
    elif (option == "2"):
        client = Client(REMOTE_HOST, REMOTE_PORT)
    else:
        print("\nusage: python3 client.py [1 | 2]\n")
        sys.exit(1)
    
    client.run()