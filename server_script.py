# YOU THERE, you little piece of shiit......
# dont you dare do anything to any of this files
# this is my beginner's peak , something i will never not be proud for..
# TOUCH THEM AND YOU WILL DIE !!!!!


import socket 
import threading

SERVER_IP = "127.0.0.1"
PORT = 9200

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((SERVER_IP,PORT))

userName = {}
clients = []   

def broadcast_msg(message,*connect):
    if connect:
        for client in clients :
            if client not in connect:
                client.send(message)
    else:
        for client in clients:
            client.send(message)

def handle_client(connect,address):
    broadcast_msg(f"[ {userName[connect]} joined  the chat !! ]".encode('utf-8'))
    connected = True
    while connected:
        msg = connect.recv(1024)
        if "/exit" in msg.decode('utf-8'):
            connected = False
            broadcast_msg(f"[ {userName[connect]} left the chat !! ]".encode('utf-8'))
            connect.close()
            clients.remove(connect)
            userName.pop(connect)
            break
        else:
            broadcast_msg(msg,connect)

def init():
    print(f"\nserver hosted on {SERVER_IP} at {PORT}.......")
    server.listen()
    while True:
        connect,address = server.accept()
        clients.append(connect)
        name = connect.recv(1024).decode('utf-8')
        userName[connect] = name

        handling_thread = threading.Thread(target=handle_client, args=(connect,address))
        print(f"\n[ ACTIVE CONNECTIONS ] : {threading.active_count()}")
        handling_thread.start()

init()