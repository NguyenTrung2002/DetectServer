import socket
import threading


class Server:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.IP = socket.gethostbyname(HOST)
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.count = 0
        self.count_lock = threading.Lock()

    def connect_to_client(self):
        self.socket_server.bind((self.IP, self.PORT))
        self.socket_server.listen()
        print("Đang chờ kết nối")

    def handle_client(self, client_socket, client_address):
        if client_socket:
            with self.count_lock:
                self.count = self.count + 1
                print(f"Đã kết nối với client {client_address}, hiện đang có {self.count} kết nối")
            while True:
                data = client_socket.recv(4096)
                if not data:
                    with self.count_lock:
                        self.count = self.count - 1
                        print(f"{client_address} đã thoát, hiện tại còn {self.count} kết nối")
                        break
                string = data.decode('utf-8')
                print(f"{client_address}: {string}")

    def handle_image(self):
        pass

    def send_message(self, msg):
        data = msg.encode('utf-8')
        self.socket_server.sendall(data)
        print("Đã gửi tin nhắn")

    def start(self):
        self.connect_to_client()
        while True:
            client_socket, client_address = self.socket_server.accept()
            thread_client = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            thread_client.start()

    def close(self):
        self.socket_server.close()
        print("Đã ngắt kết nối")

