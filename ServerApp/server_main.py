from server import Server
import socket
import sys
from server_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
#test git
server = Server(HOST=socket.gethostname(), PORT=22222)
server.start()
ui = Ui_MainWindow()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())