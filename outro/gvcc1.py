import random
from socket import *

AF_INET = 'IPV4'
SOCK_DGRAM = 'UDP'

server_socket = (('localhost', 1200)) # 127.0.0.1, porta 12000

while True:
	rand = random.randint(0, 10)
	data, address= server_socket.recvfrom(1024)
	message = str(data)
	message = message.upper()
	response = str.encode(message)
	if rand < 4:
		continue
	server_socket.sendto(response, address)
