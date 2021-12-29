import time
from socket import *
from struct import *
import random
import threading

ip = gethostname()
enough_players = False
got_ans = False
lock = threading.Lock()


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
    ans = str(op2 - op1)
    ques = f'{op2} - {op1}'

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
    socket2, address2 = tcp_socket.accept()

    enough_players = True

    question, answer = generate_question()
    question = 'How much is ' + question + ' ?'

    socket1.send(question.encode('utf-8'))
    socket2.send(question.encode('utf-8'))

    th1 = threading.Thread(target=play, args=(socket1, socket2, answer))
    th2 = threading.Thread(target=play, args=(socket2, socket1, answer))

    th1.start()
    th2.start()


def play(c_socket, others_socket, answer):
    global got_ans
    global lock
    # wait for an answer
    c_socket.settimeout(10)
    try:
        ans = c_socket.recv(1024)
        print(ans.decode('utf-8'))
    except timeout:
        print('timeout')
        got_ans = True
        try:
            c_socket.send('It\'s a draw'.encode('utf-8'))
            others_socket.send('It\'s a draw'.encode('utf-8'))
        except timeout:
            return
        return

    # lock - this player answered first
    lock.acquire()
    if got_ans:
        return

    got_ans = True
    # check for correctness
    print(answer)
    print(chr(ans[0]))
    if chr(ans[0]) == answer[0]:
        c_socket.send('You have won!'.encode('utf-8'))
        others_socket.send('You have lost :('.encode('utf-8'))
    else:
        others_socket.send('You have won!'.encode('utf-8'))
        c_socket.send('You have lost :('.encode('utf-8'))


# create threads for broadcasting and accepting players
players_conn_thread = threading.Thread(target=TCPConnection, args=())
broadcast_thread = threading.Thread(target=UDPConnection, args=())

players_conn_thread.start()
broadcast_thread.start()
