import socket
import sys
from client_ui import Ui_MainWindow
from PyQt5 import QtWidgets
# from PyQt5 import QtCore, QtGui
# from PyQt5.QtGui import QStandardItemModel, QStandardItem
# import threading


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.ip = socket.gethostbyname(self.host)
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
    def start(self):
        self.connected = True
        self.socket_client.connect((self.ip, self.port))
        print("Kết nối tới server thành công")

    def send_image(self):
        pass

    def send_message(self):
        # while self.connected
        # self.start()
        # while True:
        #     msg = input("Gửi tin nhắn: ")
        #     if msg == 'q':
        #         self.close()
        #         break
        #     data = msg.encode('utf-8')
        #     self.socket_client.sendall(data)
        #     print("Đã gửi tin nhắn")
        pass
    def close(self):
        self.socket_client.close()
        print("Đã ngắt kết nối với server")


class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.client = None
        self.setupUi(self)
        self.disconnectBut.setDisabled(False)
        self.sendBut.setDisabled(True)
        self.connectBut.clicked.connect(self.connect_server)
        self.disconnectBut.clicked.connect(self.disconnect_server)
        self.sendBut.clicked.connect(self.send_message)
    def connect_server(self):
        self.client = Client(host=self.ipLine.text(),
                             port=self.portLine.text())
        self.client.start()
        self.connectBut.setDisabled(True)
        self.disconnectBut.setDisabled(False)
        self.sendBut.setDisabled(False)
        self.chatTextEdit.append(f"Client connected: "
                                 f"{self.client.socket_client.getsockname()[0]}:"
                                 f" {self.client.socket_client.getsockname()[1]}"
                                 )

    def disconnect_server(self):
        self.client.socket_client.close()
        self.chatTextEdit.append(f"Client disconnect...")
        self.connectBut.setDisabled(False)
        self.disconnectBut.setDisabled(True)
        self.sendBut.setDisabled(True)
    def send_message(self):
        data = self.sendLine.text().encode('utf-8')
        self.client.socket_client.sendall(data)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
