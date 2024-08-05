import socket


class Client:
    def __init__(self):
        self.HOST = socket.gethostname()
        self.IP = socket.gethostbyname(self.HOST)
        self.PORT = 12345
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        self.socket_client.connect((self.IP, self.PORT))
        print("Kết nối tới server thành công")

    def send_message(self, msg):
        data = msg.encode('utf-8')
        self.socket_client.sendall(data)
        print("Đã gửi tin nhắn")

    def send_image(self):
        pass

    def start(self):
        self.connect_to_server()
        while True:
            msg = input("Gửi tin nhắn: ")
            if msg == 'q':
                self.close()
                break
            self.send_message(msg)

    def close(self):
        self.socket_client.close()
        print("Đã ngắt kết nối với server")


if __name__ == '__main__':
    client = Client()
    client.start()
