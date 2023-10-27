
from tkinter import *
import socket 
import threading

def init(event=None):    # initial GUI window to accept Server_ip, port number and username.
    global root            # global variable to access them outside the function
    global ip_entry
    global port_entry
    global name_entry

    root = Tk()                    # GUI window for client login
    root.geometry("330x170")
    root.resizable(False,False)        # restricting window resizing
    root.title("Server Configuration")
    
    lbl_ip = Label(root , text="SERVER IP", font=('B',15), fg='orange').place(x=20, y=15)
    ip_entry = Entry(root, font=("B", 13), justify=CENTER , width= 20)
    ip_entry.place(x=125 , y=15)

    lbl_port = Label(root , text="PORT NO.", font=('B',15), fg='orange').place(x=20, y=45)
    port_entry = Entry(root, font=("B", 13), justify=CENTER , width= 20)
    port_entry.place(x=125 , y=45)

    lbl_name = Label(root , text="USER-NAME", font=('B',15), fg='orange').place(x=20, y=75)
    name_entry = Entry(root, font=("B", 13), justify=CENTER , width= 20)
    name_entry.place(x=125 , y=75)

    btn = Button(root, text= 'Submit', command=chat_win, padx=3).place(x=125, y=115)
    root.mainloop()

def chat_win(event=None):        # chat window
    global SERVER_IP
    global PORT
    global USERNAME
    global chat_win
    global my_message
    global myCanvas
    global msg_Frame
    global client
    global win
    global recieving_thread

    SERVER_IP = ip_entry.get()        # assigning input server_ip, port, and username to a variable to use 
    PORT = int(port_entry.get())
    USERNAME = name_entry.get()

    root.destroy()                # discarding first [initial] login window
    win = Tk()                    # creating new window for chat system
    win.geometry("540x440")
    win.resizable(False,False)    # restricting window resizing
    win.title("Chat Room")
    
    message_frame = LabelFrame(win, height=365)
    myCanvas = Canvas(message_frame)    # creating a canvas within window to display sent/recieved messages

    scrollbar = Scrollbar(message_frame, orient="vertical", command=myCanvas.yview)    #scrollbar
    msg_Frame = LabelFrame(myCanvas)

    msg_Frame.bind('<Configure>', lambda e: myCanvas.configure(scrollregion = myCanvas.bbox('all')))
    myCanvas.create_window((0,0), window=msg_Frame, width=500, anchor='nw')
    myCanvas.configure(yscrollcommand=scrollbar.set)

    message_frame.pack_propagate(0)
    message_frame.pack(fill="x", padx=10, pady=10)
    myCanvas.pack(side=LEFT, fill="both", expand=True)
    scrollbar.pack(side=RIGHT, fill='y')

    my_message = StringVar()
    my_message.set("")

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    # initialising scoket connection
    try:
        client.connect((SERVER_IP,PORT))        # connecting to the server
        client.send(USERNAME.encode('utf-8'))    # sending username to the server

        recieving_thread = threading.Thread(target=recv_msg)    # therading recieve message process to send and recieve messages parallely
        recieving_thread.start()

    except Exception as error_code :            # exception handling on server connection and thread creation
        Label(msg_Frame, text = error_code , bg = "#aaa", fg="#a55", font=16).pack(anchor='center')
        myCanvas.yview_moveto(1)

    msg_entry = Entry(win, textvariable=my_message, width=45, font= 16, fg="green")
    msg_entry.bind("<Return>", send_msg)
    msg_entry.place(x=15, y=390)

    send_btn = Button(win, text="Send", command=send_msg, padx=3)
    send_btn.place(x=445, y=388)

    win.protocol("WM_DELETE_WINDOW", client_closing)    # discarding chat window 
    win.mainloop()

def client_closing():
    my_message.set("/exit")    # close the client connection over sending message "/exit"
    send_msg()
    win.destroy()
    client.close()

def send_msg(event=None):
    message = my_message.get()    # get message from the gui interface
    my_message.set("")
    if len(message)!=0:
        Label(msg_Frame, text=message, bg="lightgreen",fg='black',font=20).pack(anchor='e')
        myCanvas.yview_moveto(1)
        try:
            msg_send = f"[ {USERNAME} ] : {message}".encode('utf-8') # bind username with message to send to server in format - " [username]:message "
            client.send(msg_send)
        except Exception as error_code:            # error handling for message sending
            Label(msg_Frame, text = error_code , bg = "#aaa", fg="#a55", font=16).pack(anchor='center')
            myCanvas.yview_moveto(1)

def recv_msg(event=None):
    while True:
        try:
            msg_recv = client.recv(1024).decode('utf-8')    # message recieve from server
        except Exception as error_code :        # exception handling
            Label(msg_Frame, text = error_code , bg = "#aaa", fg="#a55", font=16).pack(anchor='center')
            myCanvas.yview_moveto(1)

        if msg_recv:        # displaying recieved message
            if msg_recv[0]=="[" and msg_recv[-1]==']':
                Label(msg_Frame, text = msg_recv , bg = "#ddd", fg="#aa4456", font=16).pack(anchor='center')
                myCanvas.yview_moveto(1)
            else:
                Label(msg_Frame, text=msg_recv, bg="#666", fg="#111", font=20).pack(anchor='w')
                myCanvas.yview_moveto(1)
init()
