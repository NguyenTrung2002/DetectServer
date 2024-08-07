#CODE HOÀN THIỆN (LÀM MẪU)
import socket
import sys
import threading
from client_ui import Ui_MainWindow
from PyQt5 import QtWidgets

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        try:
            self.ip = socket.gethostbyname(self.host)
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connected = False
        except:
            raise ValueError

    def start(self):
        try:
            self.socket_client.connect((self.ip, self.port))
            print("Kết nối tới server thành công")
            self.connected = True
        except:
            raise ConnectionRefusedError

    def close(self):
        self.socket_client.close()
        print("Đã ngắt kết nối với server")

    def receive_messages(self, callback):
        while self.connected:
            try:
                data = self.socket_client.recv(1024)
                if data:
                    message = data.decode('utf-8')
                    callback(message)
                else:
                    self.connected = False
            except ConnectionResetError:
                self.connected = False
                break
            except ConnectionAbortedError:
                self.connected = False
                break
            except OSError:
                self.connected = False
                break

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.client = None
        self.setupUi(self)
        self.connectBut.clicked.connect(self.connect_server)
        self.disconnectBut.clicked.connect(self.disconnect_server)
        self.sendBut.clicked.connect(self.send_message)
        self.disconnectBut.setDisabled(True)
        self.sendBut.setDisabled(True)

    def connect_server(self):
        host = self.ipLine.text()
        port = self.portLine.text()
        if host == "" or port == "":
            self.chatTextEdit.append("Chưa nhập IP hoặc PORT")
            return
        try:
            self.client = Client(host, port)
            self.client.start()
            self.connectBut.setDisabled(True)
            self.disconnectBut.setDisabled(False)
            self.sendBut.setDisabled(False)
            self.ipLine.setDisabled(True)
            self.portLine.setDisabled(True)
            self.chatTextEdit.append(f"Client connected: "
                                     f"{self.client.socket_client.getsockname()[0]}:"
                                     f" {self.client.socket_client.getsockname()[1]}")
            self.start_receiving()
        except ValueError:
            self.chatTextEdit.append("Sai địa chỉ IP")
        except ConnectionRefusedError:
            self.chatTextEdit.append("Kết nối tới Server thất bại, kiểm tra lại IP và PORT")

    def disconnect_server(self):
        if self.client:
            self.client.close()
            self.chatTextEdit.append("Client disconnected")
        self.connectBut.setDisabled(False)
        self.disconnectBut.setDisabled(True)
        self.sendBut.setDisabled(True)
        self.ipLine.setDisabled(False)
        self.portLine.setDisabled(False)

    def send_message(self):
        message = self.sendLine.text()
        if message == '':
            self.chatTextEdit.append("Vui lòng nhập tin nhắn")
            return
        data = message.encode('utf-8')
        try:
            self.client.socket_client.sendall(data)
            self.chatTextEdit.append(f"Me: {message}")
            self.sendLine.clear()
        except ConnectionResetError:
            self.chatTextEdit.append("Kết nối đã bị ngắt, không thể gửi tin nhắn")
            self.connectBut.setDisabled(False)
            self.disconnectBut.setDisabled(True)
            self.sendBut.setDisabled(True)
            self.ipLine.setDisabled(False)
            self.portLine.setDisabled(False)

    def start_receiving(self):
        self.receive_thread = threading.Thread(target=self.client.receive_messages, args=(self.show_message,))
        self.receive_thread.start()

    def show_message(self, message):
        self.chatTextEdit.append(f"Server: {message}")

    def get_message(self):
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
