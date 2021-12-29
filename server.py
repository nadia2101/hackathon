import time
from socket import *
from struct import *
import threading

ip = gethostname()
enough_players = False


def UDPConnection():
    global enough_players
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    udp_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    msg = pack('!IBH', 0xabcddcba, 0x2, 2122)

    print("Server started, listening on IP address ", ip)

    end_time = time.time() + 10
    while time.time() <= end_time and not enough_players:
        udp_socket.sendto(msg, ('<broadcast>', 13117))
        time.sleep(1)
        print('tick')


def TCPConnection():
    global enough_players
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind((ip, 2122))
    tcp_socket.listen()

    socket1, address1 = tcp_socket.accept()
    socket2, address2 = tcp_socket.accept()

    enough_players = True

    msg1 = socket1.recv(1024)
    msg2 = socket2.recv(1024)


# create threads for broadcasting and accepting players
players_conn_thread = threading.Thread(target=TCPConnection, args=())
broadcast_thread = threading.Thread(target=UDPConnection, args=())

players_conn_thread.start()
broadcast_thread.start()

