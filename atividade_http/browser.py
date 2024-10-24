import socket
import csv

poem_ids = []
with open('poems.csv', encoding="utf-8") as f:
    reader = csv.reader(f)
    for line in reader:
        poem_ids.append(line[0])

print("Seja bem vindo ao HUB de poemas!\nTemos os seguintes poemas disponíveis:")
for poem_id in poem_ids:
    print(poem_id)

param = input("Digite o poema que quer ver:\n")
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect( ('localhost', 9000) )
cmd = f'POST / HTTP/1.1\nHost: localhost:9000\nContent-Length: 15\npoema={str(param)}'.encode()
mysock.send(cmd)

while True:
    data = mysock.recv(512)
    if len(data) <1 :
        break
    print(data.decode(),end='')

mysock.close()