# Lucas Garzuze Cordeiro - Resolução do exercício ping - 29/08/2024
# Tomei a liberdade de alterar o nome de algumas variáveis do código original
# Para mim, CamelCase em python é só para nome de classes. #paz
import os
import sys
import time
import select
import struct
import binascii
from socket import *

ICMP_ECHO_REPLY = 0
ICMP_ECHO_REQUEST = 8
ICMP_DEST_UNREACH = 3
ICMP_TTL_EXPIRED = 11

def checksum(data):
    csum = 0
    count_to = (len(data) // 2) * 2
    count = 0

    while count < count_to:
        this_val = (data[count + 1] << 8) + data[count]
        csum = csum + this_val
        csum = csum & 0xffffffff
        count = count + 2

    if count_to < len(data):
        csum = csum + data[len(data) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = (answer >> 8) | ((answer << 8) & 0xff00)

    return answer

def receive_one_ping(my_socket, ID, timeout, dest_addr):
    time_left = timeout

    while True:
        started_select = time.time()
        what_ready = select.select([my_socket], [], [], time_left)
        how_long_in_select = (time.time() - started_select)

        if what_ready[0] == []:  # timeout
            return "Request timed out."

        time_received = time.time()
        rec_packet, _ = my_socket.recvfrom(1024)

        # Extrair cabeçalho ICMP
        icmp_type, code, icmp_checksum, ID, sequence, date_rcvd = struct.unpack("bbHHhd", rec_packet[20:])

        # Extrair TTL
        ttl  = struct.unpack("H", rec_packet[8:10]);

        # Criar header auxiliar para comparar checksum
        header = struct.pack("bbHHhd", icmp_type, code, 0, ID, sequence, date_rcvd)

        time_left = time_left - how_long_in_select
        delay = int(time_left*1000);

        print("<><><><><><><><><><><><><><><><><><>")
        
        if ntohs(icmp_checksum) != checksum(header):
            return "Invalid checksum"
        if icmp_type == ICMP_ECHO_REPLY:
            print(f"> Response from: {str(dest_addr)}")
            print(f"> Type: {str(icmp_type)}")
            print(f"> Code: {str(code)}")
            print(f"> Checksum: {str(icmp_checksum)}")
            print(f"> ID: {str(ID)}")
            print(f"> TTL: {str(ttl[0])}")
            return f"> Delay (ms): {str(delay)}"
        elif icmp_type == ICMP_DEST_UNREACH:
            if code == 0:
                return "Destination network unreachable."
            elif code == 1:
                return "Destination host unreachable."
        elif icmp_type == ICMP_TTL_EXPIRED:
            return "TTL expired in transit."
        elif delay <= 0:
            return "Request timed out."
        

def send_one_ping(my_socket, dest_addr, ID):
    my_checksum = 0

    # Pacote ICMP "Echo request": tipo (8) / codigo (0) / checksum / ID / sequence
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    data = struct.pack("d", time.time())

    my_checksum = checksum(header + data)
    my_checksum = htons(my_checksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    packet = header + data

    my_socket.sendto(packet, (dest_addr, 1))

def do_one_ping(dest_addr, timeout):
    icmp = getprotobyname("icmp")
    my_socket = socket(AF_INET, SOCK_RAW, icmp)

    my_ID = os.getpid() & 0xffff
    send_one_ping(my_socket, dest_addr, my_ID)
    delay = receive_one_ping(my_socket, my_ID, timeout, dest_addr)

    my_socket.close()
    return delay

def ping(host, timeout=1):
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")

    while True:
        delay = do_one_ping(dest, timeout)
        print(delay)
        time.sleep(1)

    return delay

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ping.py <hostname>")
    else:
        ping(sys.argv[1])
