import socket
import threading
HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 12345
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind((IP, PORT))
socket_server.listen()
def handle_client():
    pass
def start():
    pass
if __name__ == '__main__':
    pass
