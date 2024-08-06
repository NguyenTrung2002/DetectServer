import socket
import threading
from client_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys


class Client:
    def __init__(self, host, port):
        self.socket_client = None
        self.host = host
        self.port = port
        self.ip = socket.gethostbyname(self.host)

    def start(self):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((self.ip, self.port))
        print("Kết nối tới server thành công")

    def send_image(self):
        pass

    def send_message(self):
        self.start()
        while True:
            msg = input("Gửi tin nhắn: ")
            if msg == 'q':
                self.close()
                break
            data = msg.encode('utf-8')
            self.socket_client.sendall(data)
            print("Đã gửi tin nhắn")

    def close(self):
        self.socket_client.close()
        print("Đã ngắt kết nối với server")


class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)

    def connect_server(self):
        pass

    def disconnect_server(self):
        pass

    def send_message(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
