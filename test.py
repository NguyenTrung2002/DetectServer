import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap

class ImageLoader(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Tạo QLabel để hiển thị hình ảnh
        self.label = QLabel(self)
        layout.addWidget(self.label)

        # Tạo nút để tải ảnh
        self.button = QPushButton('Load Image', self)
        self.button.clicked.connect(self.load_image)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.setWindowTitle('Image Loader')
        self.show()

    def load_image(self):
        # Mở hộp thoại chọn tệp để tải ảnh
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if file_path:
            # Tạo QPixmap từ tệp đã chọn và hiển thị trên QLabel
            pixmap = QPixmap(file_path)
            self.label.setPixmap(pixmap)
            self.label.adjustSize()  # Điều chỉnh kích thước của QLabel theo kích thước của QPixmap

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loader = ImageLoader()
    sys.exit(app.exec_())
