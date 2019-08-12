import socket
import threading
import datetime
import sys
from myconfig import ACK_KILL_PROCESS
from myconfig import UPTIME
from myconfig import REQNUM
from myconfig import CLOSE
from myconfig import TIMEOUT
from myconfig import TCP_UDP_PROTOCOL

# MARK: Global variables
requestsReceived = 0
serverStartedSince = datetime.datetime.now()

# MARK: Classes definitions
class ThreadedServer(object):
    # MARK: Constructor
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        # Get protocol according to TCP_UDP_PROTOCOL value
        protocol = socket.SOCK_STREAM if TCP_UDP_PROTOCOL else socket.SOCK_DGRAM

        try:
            self.serverSocket = socket.socket(socket.AF_INET, protocol)
            # [Errno 98] Address already in use
            # the SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, 
            # without waiting for its natural timeout to expire.
            self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error as e:
            print("Failed to create socket: %s"%(e))
            sys.exit()

        try:
            self.serverSocket.bind((self.ip, self.port))
            # Server's up
            mode = "TCP" if TCP_UDP_PROTOCOL else "UDP"
            print("Server is up and ready to receive connections in **%s MODE (change it inside myconfig.py file)**! IP %s and PORT %s"%(mode, self.ip, self.port))
        except socket.error as e:
            print("Failed to bind: %s"%(e))
            sys.exit()

    # MARK: Methods
    def startTCPServer(self):
        # Listen for connections made to the socket. The backlog argument specifies the maximum number of 
        # queued connections and should be at least 0; the maximum value is system-dependent (usually 5), 
        # the minimum value is forced to 0.
        self.serverSocket.listen(5)

        while True:
            # Wait until a client connects
            clientConnection, clientAddress = self.serverSocket.accept()
            clientConnection.settimeout(60)

            # Throw a thread in order to handle simultaneous clients
            threading.Thread(target = self.handleTCPClientConnection,args = (clientConnection, clientAddress)).start()

    def startUDPServer(self):
        self.handleUDPClientConnection(self.serverSocket)

    def handleTCPClientConnection(self, clientConnection, clientAddress):
        print("Client connected from IP %s"%(clientAddress[0]))

        # Stay in touch to client until he/she leaves
        stayInTouch = True

        while stayInTouch:
            # Get client's message
            messageFromClient = clientConnection.recv(4096)
            if messageFromClient:
                print("MESSAGE FROM IP %s: %s"%(clientAddress[0], messageFromClient))

                try:
                    # Handle the message according to received signal and send a response to client
                    response = handleMessageAndGetResponse(messageFromClient)
                except:
                    response = ACK_KILL_PROCESS
                    stayInTouch = False

                # Reply client
                clientConnection.send(response)

        # Close connection when user sends a CLOSE signal
        clientConnection.close()
        print("Client disconnected from IP %s"%(clientAddress[0]))

    def handleUDPClientConnection(self, serverSocket):
        while True:
            # Get client's message
            messageFromClient, clientAddress = serverSocket.recvfrom(4096)
            if messageFromClient:
                print("MESSAGE FROM IP %s: %s"%(clientAddress[0], messageFromClient))

                try:
                    # Handle the message according to received signal and send a response to client
                    response = handleMessageAndGetResponse(messageFromClient)
                except:
                    response = ACK_KILL_PROCESS

                # Reply client
                serverSocket.sendto(response, clientAddress)

        print("Client disconnected from IP %s"%(clientAddress[0]))

# MARK: Functions
def incrementNumberOfConnections():
    # Increment number of received connections
    global requestsReceived
    requestsReceived += 1

def handleMessageAndGetResponse(message):
    incrementNumberOfConnections()

    if message == "\\CLOSE":
        raise Exception("User's just closed connection.")

    handler = {
        UPTIME: "The server is running since %s. Total time up: %s"%(serverStartedSince, datetime.datetime.now() - serverStartedSince),
        REQNUM: "Number of requests received, including this one: %s"%(requestsReceived)
    }
    return handler.get(message, "Invalid message: try '%s', '%s' or '%s"%(UPTIME, REQNUM, CLOSE))

# MARK: Init main()
def main():
    while True:
        try:
            ip = raw_input("Enter an ip address to this server(Ex.: 'localhost', '127.0.0.1', ''): ")
            port = int(raw_input("Enter a port: "))
            ip = str(ip)
            port = int(port)
            if TCP_UDP_PROTOCOL:
                ThreadedServer(ip ,port).startTCPServer()
            else:
                ThreadedServer(ip ,port).startUDPServer()
            break
        except ValueError:
            pass

print("\n** Welcome to my socket app! Send a message using TCP/UDP sockets! Change protocol inside myconfig.py file **\n\n")
main()
print("** This is the end! **")










