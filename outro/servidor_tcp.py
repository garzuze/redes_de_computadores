#!/usr/bin/env python3

import socket


TCP_IP = '10.21.80.117'
TCP_PORT = 6969
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen()

conn, addr = s.accept()
print('Connection address:', addr)
while 1:
    data = conn.recv(BUFFER_SIZE)
    data = data.title()
    if not data: break
    print("received data:", data.decode())
    conn.send(data)  # echo
conn.close()
