#CODE HOÀN THIỆN (LÀM MẪU)
import socket
import threading
from server_ui import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys

class Server:
    def __init__(self, host, port, update_client_list_callback, show_message_callback):
        self.host = host
        self.port = port
        self.ip = socket.gethostbyname(host)
        self.socket_server = None
        self.count = 0
        self.count_lock = threading.Lock()
        self.client_sockets = []
        self.client_addresses = {}  # Dictionary to map client sockets to addresses
        self.server_thread = None
        self.running = False
        self.update_client_list_callback = update_client_list_callback
        self.show_message_callback = show_message_callback

    def connect_to_client(self):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.ip, self.port))
        self.socket_server.listen()
        print(f"Đang chờ kết nối {self.ip}")

    def handle_client(self, client_socket, client_address):
        if client_socket:
            with self.count_lock:
                self.count += 1
                print(f"Đã kết nối với client {client_address}, hiện đang có {self.count} kết nối")
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
                print(f"{client_address} đã thoát, hiện tại còn {self.count} kết nối")
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
                thread_client = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
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

    def send_message(self, message, target_client=None):
        data = message.encode('utf-8')
        if target_client:
            thread_send = threading.Thread(target=self.send_to_client, args=(target_client, data))
            thread_send.start()
        else:
            thread_send = threading.Thread(target=self.send_to_all_clients, args=(data,))
            thread_send.start()

    def send_to_client(self, client_socket, data):
        try:
            client_socket.sendall(data)
            print(f"Đã gửi tin nhắn tới {client_socket.getpeername()}")
        except socket.error as e:
            print(f"Lỗi khi gửi tin nhắn tới {client_socket.getpeername()}: {e}")

    def send_to_all_clients(self, data):
        for client_socket in self.client_sockets:
            try:
                client_socket.sendall(data)
                print(f"Đã gửi tin nhắn tới {client_socket.getpeername()}")
            except socket.error as e:
                print(f"Lỗi khi gửi tin nhắn tới {client_socket.getpeername()}: {e}")


class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        self.client_model = QStandardItemModel()
        self.connectedList.setModel(self.client_model)
        self.connectedList.clicked.connect(self.on_client_selected)  # Event to handle client selection
        self.selected_client = None
        self.disconnectBut.setDisabled(True)
        self.sendBut.setDisabled(True)
        self.server = Server(host=socket.gethostname(),
                             port=22222,
                             update_client_list_callback=self.update_client_list,
                             show_message_callback=self.get_message)
        self.connectBut.clicked.connect(self.start_server)
        self.disconnectBut.clicked.connect(self.stop_server)
        self.sendBut.clicked.connect(self.send_message)
        self.centralwidget.installEventFilter(self)  # Install event filter to detect click outside QListView

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
            item.setData(client_address)  # Store client address in item data
            self.client_model.appendRow(item)
            self.manaTextEdit.append(f"Client connected: {address_str}")
        else:
            for row in range(self.client_model.rowCount()):
                item = self.client_model.item(row)
                if item.text() == address_str:
                    self.client_model.removeRow(row)
                    break
            self.manaTextEdit.append(f"Client disconnected: {address_str}")

    def on_client_selected(self, index):
        item = self.client_model.itemFromIndex(index)
        client_address = item.data()
        for client_socket, address in self.server.client_addresses.items():
            if address == client_address:
                self.selected_client = client_socket
                break

    def get_message(self, client_address, message):
        address_str = f"{client_address[0]}:{client_address[1]}"
        self.chatTextEdit.append(f"{address_str}: {message}")

    def send_message(self):
        message = self.sendLine.text()
        if message == '':
            self.chatTextEdit.append("Vui lòng nhập tin nhắn muốn gửi")
            return
        if len(self.server.client_sockets) == 0:
            self.chatTextEdit.append("Không có kết nối nên không thể gửi")
            return
        if self.selected_client:
            self.server.send_message(message, target_client=self.selected_client)
            self.chatTextEdit.append(f"Server to {self.selected_client.getpeername()}: {message}")
        else:
            self.server.send_message(message)
            self.chatTextEdit.append(f"Server: {message}")
        self.sendLine.clear()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if source is self.centralwidget:
                if not self.connectedList.geometry().contains(event.pos()):
                    self.connectedList.clearSelection()
                    self.selected_client = None
        return super(MainApp, self).eventFilter(source, event)

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
