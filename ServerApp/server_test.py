# CODE TEST
import socket
import threading
from server_ui import Ui_MainWindow
from PyQt5 import QtWidgets
# from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys
from PyQt5.QtCore import Qt, QModelIndex


class Server:
    def __init__(self, host, port,
                 update_client_list_callback,
                 show_message_callback):
        self.host = host
        self.port = port
        self.ip = socket.gethostbyname(host)
        self.socket_server = None
        self.count = 0
        self.count_lock = threading.Lock()
        self.client_sockets = []
        self.client_addresses = {}
        self.server_thread = None
        self.running = False
        self.update_client_list_callback = update_client_list_callback
        self.show_message_callback = show_message_callback

    def connect_to_client(self):
        self.socket_server = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM)
        self.socket_server.bind((self.ip, self.port))
        self.socket_server.listen()
        print(f"Đang chờ kết nối {self.ip}")

    def handle_client(self, client_socket, client_address):
        if client_socket:
            with self.count_lock:
                self.count += 1
                print(f"Đã kết nối với client"
                      f" {client_address},"
                      f" hiện đang có {self.count} kết nối")
                self.update_client_list_callback(client_address, True)
            self.client_sockets.append(client_socket)
            self.client_addresses[client_socket] = client_address
            while self.running:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    string = data.decode('utf-8', 'backslashreplace')
                    self.show_message_callback(client_address, string)
                    print(f"{client_address}: {string}")
                except (ConnectionResetError, ConnectionAbortedError, OSError):
                    break
            with self.count_lock:
                self.count -= 1
                print(f"{client_address} đã thoát,"
                      f" hiện tại còn {self.count} kết nối")
                self.client_sockets.remove(client_socket)
                del self.client_addresses[client_socket]
                self.update_client_list_callback(client_address, False)
            client_socket.close()

    def start_server(self):
        self.running = True
        self.connect_to_client()
        while self.running:
            try:
                client_socket, client_address = self.socket_server.accept()
                thread_client = threading.Thread(target=self.handle_client,
                                                 args=(client_socket,
                                                       client_address))
                thread_client.start()
            except OSError:
                break

    def start(self):
        if not self.running:
            self.server_thread = threading.Thread(target=self.start_server)
            self.server_thread.start()

    def stop(self):
        self.running = False
        for client_socket in self.client_sockets:
            client_socket.close()
        if self.socket_server:
            self.socket_server.close()
        if self.server_thread:
            self.server_thread.join()
        self.socket_server = None
        print("\nĐã ngắt kết nối")


class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.selected_client_address = None
        self.setupUi(self)
        self.client_model = QStandardItemModel()
        self.connectedList.setModel(self.client_model)
        self.disconnectBut.setDisabled(True)
        self.sendBut.setDisabled(True)
        self.server = Server(host=socket.gethostname(),
                             port=22222,
                             update_client_list_callback=self.update_client_list,
                             show_message_callback=self.get_message)
        self.connectBut.clicked.connect(self.start_server)
        self.disconnectBut.clicked.connect(self.stop_server)
        self.sendBut.clicked.connect(self.send_message)
        self.connectedList.setEditTriggers(QListView.NoEditTriggers)
        self.connectedList.clicked.connect(self.item_clicked)

    def start_server(self):
        self.server.start()
        self.manaTextEdit.append("Server started...")
        self.connectBut.setDisabled(True)
        self.disconnectBut.setDisabled(False)
        self.sendBut.setDisabled(False)

    def stop_server(self):
        self.server.stop()
        self.manaTextEdit.append("Server stopped...")
        self.connectBut.setDisabled(False)
        self.disconnectBut.setDisabled(True)
        self.sendBut.setDisabled(True)

    def update_client_list(self, client_address, connected):
        address_str = f"{client_address[0]}:{client_address[1]}"
        if connected:
            item = QStandardItem(address_str)
            self.client_model.appendRow(item)
            self.manaTextEdit.append(f"Client connected:"
                                     f" {address_str}")
        else:
            for row in range(self.client_model.rowCount()):
                item = self.client_model.item(row)
                if item.text() == address_str:
                    self.client_model.removeRow(row)
                    break
            self.manaTextEdit.append(f"Client disconnected: "
                                     f"{address_str}")

    def get_message(self, client_address, message):
        address_str = f"{client_address[0]}:{client_address[1]}"
        self.chatTextEdit.append(f"{address_str}: {message}")

    def send_message(self):
        message = self.sendLine.text()
        data = message.encode('utf-8')
        if message == '':
            self.chatTextEdit.append("Vui lòng nhập tin nhắn muốn gửi")
            return
        if len(self.server.client_sockets) == 0:
            self.chatTextEdit.append("Không có kết nối nên không thể gửi")
            return
        if self.selected_client_address is None:
            for client_socket in self.server.client_sockets:
                client_socket.sendall(data)
            self.chatTextEdit.append(f"Server: {message}")
            self.sendLine.clear()
        else:
            for client_socket, client_address in self.server.client_addresses.items():
                if client_address == self.selected_client_address:
                    client_socket.sendall(data)
                    self.chatTextEdit.append(f"Server{self.selected_client_address}: {message}")
                    self.sendLine.clear()

    def item_clicked(self,  index: QModelIndex):
        self.selected_client_address = self.client_model.data(index, Qt.DisplayRole)
        self.selected_client_address = tuple(self.selected_client_address.split(':'))
        self.selected_client_address = (self.selected_client_address[0], int(self.selected_client_address[1]))
        print(f'You clicked on: {self.selected_client_address}')

    def mousePressEvent(self, event):
        if not self.connectedList.geometry().contains(event.pos()):
            self.connectedList.clearSelection()
        super().mousePressEvent(event)
        self.selected_client_address = None

    def get_image(self):
        pass

    def set_image(self):
        pass

    def handle_image(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
