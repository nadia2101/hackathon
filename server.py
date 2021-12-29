import time
from socket import *
from struct import *
import random
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


def generate_mul():
    op1 = random.randint(1, 9)
    op2 = random.randint(0, int(9 / op1))
    ans = str(op1 * op2)
    ques = f'{op1} * {op2}'

    return ques, ans


def generate_add():
    op1 = random.randint(0, 9)
    op2 = random.randint(0, 9 - op1)
    ans = str(op1 + op2)
    ques = f'{op1} + {op2}'

    return ques, ans


def generate_div():
    ans = random.randint(1, 9)
    op1 = random.randint(1, 9)
    op2 = ans * op1
    ques = f'{op2} / {op1}'

    return ques, str(ans)


def generate_min():
    op1 = random.randint(0, 9)
    op2 = random.randint(0, 9 + op1)
    ans = str(op1 - op2)
    ques = f'{op1} - {op2}'

    return ques, ans


def generate_question():
    op = random.randint(1, 4)

    if op == 1:
        return generate_add()
    if op == 2:
        return generate_add()
    if op == 3:
        return generate_min()
    if op == 4:
        return generate_div()


def TCPConnection():
    global enough_players
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.bind((ip, 2122))
    tcp_socket.listen()

    socket1, address1 = tcp_socket.accept()
    # socket2, address2 = tcp_socket.accept()

    enough_players = True

    question, answer = generate_question()

    socket1.send(question.encode('utf-8'))
    # socket2.send(question.encode('utf-8'))


# create threads for broadcasting and accepting players
players_conn_thread = threading.Thread(target=TCPConnection, args=())
broadcast_thread = threading.Thread(target=UDPConnection, args=())

players_conn_thread.start()
broadcast_thread.start()
