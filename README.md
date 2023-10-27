GUI Chat System

This project implements a simple GUI-based chat system using Python. The chat system consists of a server and client components. The server is responsible for handling connections between clients, while the client provides a graphical user interface for users to send and receive messages.

Server Side :

Prerequisites -
  Python 3.x
  
Usage -
  Run the server script by executing the following command in the terminal:
    $ python server_script.py
  
  Replace python with python3 if necessary.
  The server will start listening for incoming connections on the specified IP address and port.

Client Side :

Prerequisites
  Python 3.x
  Tkinter library (usually included with Python)

Usage -
  Run the client script by executing the following command in the terminal:
    $ python client_script.py
    
  Replace python with python3 if necessary.

Enter the server's IP address, port number, and your desired username in the GUI window.
Click the "Submit" button to connect to the server and open the chat window.

Enter your messages in the input field at the bottom of the chat window and press "Enter" or click the "Send" button to send messages.

To exit the chat, type /exit in the input field and press "Enter" or click the "Send" button.
Notes

Make sure to adjust the server's IP address and port in the client script to match the server configuration.
The GUI is created using the Tkinter library, and the communication between the server and client is 
established through sockets.
