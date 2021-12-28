import time
from socket import *
from struct import *

ip = gethostname()

def udpConnection():

    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    msg = pack('!IBH',0xabcddcba , 0x2 , 2122)
    timenow = time.time()
    print("Server started, listening on IP address ", ip)
    while time.time() <= timenow + 10:
        udp_socket.sendto(msg, ('<broadcast>', 13117))
        time.sleep(1)
        print(time.time())

def tcpconnection():
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind((ip, 2122))
    tcp_socket.listen()
    socket1, address1 = tcp_socket.accept()
    socket2, address2 = tcp_socket.accept()
    msg1 = socket1.recv(1024)
    msg2 = socket2.recv(1024)
    # msg, address = tcp_socket.accept()
    print(msg1.decode())
    print(msg2.decode())


udpConnection()
tcpconnection()