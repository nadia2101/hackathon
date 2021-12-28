import struct
import time
from socket import *
from struct import *


def udpConnection() :
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    udp_socket.bind(('', 13117))
    msg, address= udp_socket.recvfrom(1024)
    magic_cookies , msg_type , port = struct.unpack('!IBH',msg)
    print("Client started, listening for offer requests...")
    if magic_cookies == 0xabcddcba and msg_type == 0x2 :
        address_server=address[0]
        print("Received offer from ",address_server,",attempting to connect...")
    return port,address_server

def tcpConnection(port,address_server):
    tcp_socket=socket(AF_INET, SOCK_STREAM)
    time.sleep(10)
    print(port , address_server)
    tcp_socket.connect((address_server, port))
    tcp_socket.send("nadia\n".encode('utf-8'))





port,address_server =udpConnection()
tcpConnection(port,address_server)