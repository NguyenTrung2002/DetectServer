# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClientApp/client_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(679, 584)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(170, 20, 339, 78))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.connectBut = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.connectBut.setObjectName("connectBut")
        self.horizontalLayout.addWidget(self.connectBut)
        self.ipLine = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.ipLine.setText("")
        self.ipLine.setObjectName("ipLine")
        self.horizontalLayout.addWidget(self.ipLine)
        self.disconnectBut = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.disconnectBut.setObjectName("disconnectBut")
        self.horizontalLayout.addWidget(self.disconnectBut)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(40, 110, 601, 271))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.imageRawLab = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.imageRawLab.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.imageRawLab.setText("")
        self.imageRawLab.setScaledContents(False)
        self.imageRawLab.setObjectName("imageRawLab")
        self.horizontalLayout_2.addWidget(self.imageRawLab)
        self.imageDetectLab = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.imageDetectLab.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.imageDetectLab.setText("")
        self.imageDetectLab.setScaledContents(False)
        self.imageDetectLab.setObjectName("imageDetectLab")
        self.horizontalLayout_2.addWidget(self.imageDetectLab)
        self.chatTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.chatTextEdit.setGeometry(QtCore.QRect(40, 390, 601, 161))
        self.chatTextEdit.setObjectName("chatTextEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.connectBut.setText(_translate("MainWindow", "Kết nối với Server"))
        self.disconnectBut.setText(_translate("MainWindow", "Ngắt kết nối"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
