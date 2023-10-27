
import socket 
import threading

SERVER_IP = "127.0.0.1"        # server IP adderss
PORT = 9200                    # Port number

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    # initializing server socket
server.bind((SERVER_IP,PORT))                # binding server to given IP and Port 

userName = {}            # Store client username in key:value pair    [connect(socket object) : username]
clients = []               # store socket object

def broadcast_msg(message,*connect):    # sending message with optional argument connect(client object)
    if connect:        # if client object ,i.e, message from client-to-client, brodcast message to all other client connected the server
        for client in clients :
            if client not in connect:
                client.send(message)
    else:            # if client object not present , i.e, message from server (Warning, Notification, Error) , brodcasting message to all the clients connected to server
        for client in clients:
            client.send(message)

def handle_client(connect,address):
    broadcast_msg(f"[ {userName[connect]} joined  the chat !! ]".encode('utf-8'))    # sending notification about new client connection (with username) to all the clients present 
    connected = True
    while connected:
        msg = connect.recv(1024)            # listening for the incoming messages
        if "/exit" in msg.decode('utf-8'):    # if recieved message == "/exit" , teminating connection for the client and notifying all the connection about it
            connected = False
            broadcast_msg(f"[ {userName[connect]} left the chat !! ]".encode('utf-8'))
            connect.close()
            clients.remove(connect)
            userName.pop(connect)
            break
        else:
            broadcast_msg(msg,connect)        # broadcating messages from the client-to-client

def init():
    print(f"\nserver hosted on {SERVER_IP} at {PORT}.......")
    server.listen()                        # waiting for the client connection
    while True:
        connect,address = server.accept()    # if client connected , accepting client object and client address
        clients.append(connect)
        name = connect.recv(1024).decode('utf-8')
        userName[connect] = name

        handling_thread = threading.Thread(target=handle_client, args=(connect,address))    # defining a thread specific to the client
        print(f"\n[ ACTIVE CONNECTIONS ] : {threading.active_count()}")
        handling_thread.start()            # initializing the thread

init()
