import signal
import socket
import os
from os.path import abspath, dirname
import threading

from cryptography.fernet import Fernet

HOME = '/'.join(abspath(dirname(__file__)).split('/')[:3])

def send_messages():
    """
    Sends input to server which
    sends to other clients
    """
    while True:
        msg = input()
        if msg != "":
            s.send(bytes(msg, "utf-8"))
        print("\033[A                             \033[A")

def receive_messages():
    """
    Constantly reveieves data from
    server and prints to console
    """
    while True:
        data = s.recv(1024)
        print(data.decode("utf-8"))    

if __name__ == "__main__":
    
    os.system("stty -echo") 
    password = input("Password: ")
    os.system("stty echo")
    print() 

    with open(f"{HOME}/.chat-app.key", "rb") as f:
        key = f.read()
    
    fernet = Fernet(key)
    
    # read encrypted message
    with open(f'{HOME}/.chat-app-user-secrets', 'rb') as f:
        encrypted = f.read()

    if password == fernet.decrypt(encrypted).decode("utf-8"):
    
        server = input("server: ")
        port = input("port: ")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, int(port)))
        print("Successfully connected to the server!")   
        
        username = input("username: ")
        s.send(bytes(username, 'utf-8'))    
 
        def signal_handler(sig, frame):
            os._exit(1)
        signal.signal(signal.SIGINT, signal_handler)    

        sm = threading.Thread(target=send_messages)
        rm = threading.Thread(target=receive_messages)
        sm.start()
        rm.start()
    else:
        print('incorrect password')
