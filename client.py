import struct
import sys
import time
from socket import *
from struct import *
from msvcrt import *
import threading


def udpConnection():
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    udp_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    udp_socket.bind(('', 13117))
    msg, address = udp_socket.recvfrom(1024)
    magic_cookies, msg_type, c_port = struct.unpack('!IBH', msg)
    print("Client started, listening for offer requests...")
    if magic_cookies == 0xabcddcba and msg_type == 0x2:
        server_address = address[0]
        print("Received offer from ", server_address, ",attempting to connect...")
        return c_port, server_address


def tcpConnection(c_port, server_address):
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    # time.sleep(10)
    print(c_port, server_address)
    tcp_socket.connect((server_address, c_port))
    return tcp_socket


port, address_server = udpConnection()
c_socket = tcpConnection(port, address_server)

# wait for the server to start the game
print(c_socket.recv(1024).decode('utf-8'))


def send_ans():
    ans = getch()
    c_socket.send(chr(ans[0]).encode('utf-8'))


def rec_result():
    result = c_socket.recv(1024).decode('utf-8')
    print(result)


th1 = threading.Thread(target=send_ans, args=())
th2 = threading.Thread(target=rec_result, args=())

th1.start()
th2.start()

th1.join()
th2.join()
