import struct
import time
from socket import *
from struct import *


def udpConnection():
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
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
    tcp_socket.send("nadia\n".encode('utf-8'))


port, address_server = udpConnection()
tcpConnection(port, address_server)
