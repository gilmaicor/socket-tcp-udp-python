import socket
import sys
from myconfig import ACK_KILL_PROCESS
from myconfig import TIMEOUT
from myconfig import TCP_UDP_PROTOCOL

# MARK: Functions
def startTCPClient(ip, port):
    # Get protocol according to TCP_UDP_PROTOCOL value
	protocol = socket.SOCK_STREAM if TCP_UDP_PROTOCOL else socket.SOCK_DGRAM

	try:
		serverConnection = socket.socket(socket.AF_INET, protocol)
	except socket.error as e:
		print("Failed to create socket: %s"%(e))
		sys.exit()

	try:
		serverConnection.connect((ip, port))
	except socket.error as e:
		print("Failed to connect: %s"%(e))
		sys.exit()
	
	stayInTouch = True
	while stayInTouch:
		# Send a message to server
		message = raw_input("Enter a message: ")
		serverConnection.send(message)

		# Receive a response
		response = serverConnection.recv(4096)

		stayInTouch = False if (response == ACK_KILL_PROCESS) else True
		response = response if stayInTouch else "You have just left the connection."

		print ("Server said: %s"%(response))

	# Close connection when server send an ack to a \CLOSE signal
	serverConnection.close()

def startUDPClient(ip, port):
    # Get protocol according to TCP_UDP_PROTOCOL value
	protocol = socket.SOCK_STREAM if TCP_UDP_PROTOCOL else socket.SOCK_DGRAM

	try:
		serverConnection = socket.socket(socket.AF_INET, protocol)
	except socket.error as e:
		print("Failed to create socket: %s"%(e))
		sys.exit()
	
	stayInTouch = True
	while stayInTouch:
		# Send a message to server
		message = raw_input("Enter a message: ")
		serverConnection.sendto(message, (ip, port))

		# Receive a response
		response, server = serverConnection.recvfrom(4096)

		stayInTouch = False if (response == ACK_KILL_PROCESS) else True
		response = response if stayInTouch else "You have just left the connection."

		print ("SERVER SAID: %s"%(response))

	# Close connection when server send an ack to a \CLOSE signal
	serverConnection.close()

def main():
	ip = raw_input("Enter an ip address to connect: Ex.: 'localhost', '127.0.0.1', ''")
	port = int(raw_input("Enter a port: "))
	if TCP_UDP_PROTOCOL:
		startTCPClient(ip, port)
	else:
		startUDPClient(ip, port)

print("\n** Welcome to my socket app! Send a message using TCP/UDP sockets! Change protocol inside myconfig.py **\n\n")
main()
print("** This is the end! **")







