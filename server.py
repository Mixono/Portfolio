import socket
import threading
import time
from colorama import *

Port = 5050
IPServer = socket.gethostbyname(socket.gethostname())
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Address = (IPServer, Port)
Server.bind(Address)

def handle_client(conn, Address):
    print(Fore.CYAN + '[Micro Server] ' + Fore.BLUE + 'New Connection: ' + Fore.GREEN + Address)
    
def start():
    Server.listen()
    print(Fore.CYAN + '[Micro Server] ' + Fore.BLUE + 'Waiting for New Connections...')
    while True:
        conn, Address = Server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, Address))
        thread.start()
        print(Fore.CYAN + '[Micro Server] ' + Fore.BLUE + 'Active Connections: ' + Fore.GREEN + threading.activeCount() - 1)

print(Fore.CYAN + '[Micro Server] ' + Fore.BLUE + 'Starting Server...')
start()


