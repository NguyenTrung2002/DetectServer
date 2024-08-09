# CODE TEST
import socket
import sys
import threading
import cv2
# from PyQt5.QtCore import Qt
from ultralytics import YOLO
from client_ui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QImage


# from PyQt5 import QtCore, QtGui
# from PyQt5.QtGui import QStandardItemModel, QStandardItem
# import threading


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        try:
            self.ip = socket.gethostbyname(self.host)
            self.socket_client = socket.socket(socket.AF_INET,
                                               socket.SOCK_STREAM)
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

    def handle_server(self, callback):
        while self.connected:
            try:
                data = self.socket_client.recv(4096)
                if data:
                    string = data.decode('utf-8')
                    callback(string)
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
        self.image_raw = None
        self.qimage_raw = None
        self.qimage_handle = None
        self.receiving_thread = None
        self.client = None
        self.setupUi(self)
        self.connectBut.clicked.connect(self.connect_server)
        self.disconnectBut.clicked.connect(self.disconnect_server)
        self.sendBut.clicked.connect(self.send_message)
        self.handleImageBut.clicked.connect(self.handle_image)
        self.loadImageBut.clicked.connect(self.load_image)
        self.disconnectBut.setDisabled(True)
        self.sendBut.setDisabled(True)
        self.loadImageBut.setDisabled(True)
        self.handleImageBut.setDisabled(True)

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
            self.loadImageBut.setDisabled(False)
            self.chatTextEdit.append(f"Client connected: "
                                     f"{self.client.socket_client.getsockname()[0]}:"
                                     f" {self.client.socket_client.getsockname()[1]}"
                                     )
            self.receiving()
        except ValueError:
            self.chatTextEdit.append("Sai địa chỉ IP")
        except ConnectionRefusedError:
            self.chatTextEdit.append("Kết nối tới Server thất bại"
                                     ", kiểm tra lại IP và PORT")

    def disconnect_server(self):
        self.client.socket_client.close()
        self.chatTextEdit.append(f"Client disconnect...")
        self.connectBut.setDisabled(False)
        self.disconnectBut.setDisabled(True)
        self.sendBut.setDisabled(True)
        self.ipLine.setDisabled(False)
        self.portLine.setDisabled(False)
        self.loadImageBut.setDisabled(True)
        self.handleImageBut.setDisabled(True)
        self.imageRawLab.clear()
        self.imageDetectLab.clear()

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
            self.chatTextEdit.append("Kết nối đã bị ngắt, "
                                     "không thể gửi tin nhắn")
            self.connectBut.setDisabled(False)
            self.disconnectBut.setDisabled(True)
            self.sendBut.setDisabled(True)
            self.ipLine.setDisabled(False)
            self.portLine.setDisabled(False)
            self.loadImageBut.setDisabled(True)
            self.handleImageBut.setDisabled(True)
            self.imageRawLab.clear()
            self.imageDetectLab.clear()

    def receiving(self):
        self.receiving_thread = threading.Thread(target=self.client.handle_server, args=(self.get_message,))
        self.receiving_thread.start()

    def get_message(self, string):
        self.chatTextEdit.append(f"Server: {string}")

    def load_image(self):
        # Mở hộp thoại chọn tệp để tải ảnh
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Open Image File",
                                                   "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)",
                                                   options=options)
        if file_path:
            # Tạo QPixmap từ tệp đã chọn và hiển thị trên QLabel
            self.image_raw = cv2.imread(file_path)
            send_image = threading.Thread(target=self.send_image, args=(self.image_raw,))
            send_image.start()
            image = cv2.cvtColor(self.image_raw, cv2.COLOR_BGR2RGB)
            image_resize = cv2.resize(image, (self.imageRawLab.width(), self.imageRawLab.height()))
            height, width, channel = image_resize.shape
            bytes_per_line = 3 * width
            self.qimage_raw = QImage(image_resize.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.imageRawLab.setPixmap(QPixmap.fromImage(self.qimage_raw))

            # pixmap = QPixmap(file_path)
            # resize_pixmap = pixmap.scaled(self.imageRawLab.size(), Qt.KeepAspectRatio)
            # self.imageRawLab.setPixmap(resize_pixmap)
        self.handleImageBut.setDisabled(False)

    def handle_image(self):
        self.imageDetectLab.clear()
        model = YOLO("yolov8n.pt")
        results = model(self.image_raw)
        result = results[0]
        detection_info = f"{result.boxes.shape[0]} đối tượng được nhận diện"
        annotated_img = result.plot()
        send_image = threading.Thread(target=self.send_image, args=(annotated_img,))
        send_image.start()
        annotated_img_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
        image_resize = cv2.resize(annotated_img_rgb, (self.imageRawLab.width(), self.imageRawLab.height()))
        height, width, channel = image_resize.shape
        bytes_per_line = 3 * width
        self.qimage_handle = QImage(image_resize.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.imageDetectLab.setPixmap(QPixmap.fromImage(self.qimage_handle))
        self.chatTextEdit.append(detection_info)

    def send_image(self, image):
        # _, buffer = cv2.imencode('.jpg', image)
        # image_data = buffer.tobytes()
        # image_size = len(image_data)
        # self.client.socket_client.sendall(image_size.to_bytes(4, byteorder='big'))
        # self.client.socket_client.sendall(image_data)
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
