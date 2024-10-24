from socket import *
import csv

poems = {}

with open('poems.csv', encoding="utf-8") as f:
    reader = csv.reader(f)
    poem_list = list(reader)

for poem in poem_list:
    poems[poem[0]] = [poem[1], poem[2]]

def create_server():
    serversocket = socket(AF_INET, SOCK_STREAM)
    try:
        serversocket.bind(('localhost', 9000))
        serversocket.listen(5)
        while True:
            (clientsocket, address) = serversocket.accept()

            rd = clientsocket.recv(5000).decode()
            pieces = rd.split("\n")

            # a posição do body muda a depender se fazemos a requisição 
            # com o postman ou com o browser.py
            for element in pieces:
                print(element)
                if "poema" in element:
                    poem = pieces[pieces.index(element)]
            poem = poem.split("=")[1]

            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type: text/html; charset=utf-8\r\n"
            data += "\r\n"
            data += f'<html lang="en"><head><style>h1 {{font-family: "Lucida Sans", "Lucida Sans Regular", "Lucida Grande", "Lucida Sans Unicode", Geneva, Verdana, sans-serif;}}p{{font-family: "Courier New", Courier, monospace;}}</style><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>HUB de poemas!</title></head><body><h1>{poems[poem][0]}</h1><p>{poems[poem][1]}</p></body> </html>'
            clientsocket.sendall(data.encode())
            clientsocket.shutdown(SHUT_WR)
    except KeyboardInterrupt:
        print("\nShutting down...\n")
        serversocket.close()
    except Exception as exc:
        print("Error:\n")
        print(exc)

print('Access http://localhost:9000')
create_server()
