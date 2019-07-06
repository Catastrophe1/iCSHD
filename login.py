# -*- coding: UTF-8 -*-

'''
@Author: t-zhel
@Date: 2019-07-11 00:06:34
@LastEditor: t-zhel
@LastEditTime: 2019-07-12 15:04:23
@Description: Implement the login window
'''

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QIcon
from hello import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mainUI import MainWindow

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 500)
        # MainWindow.setWindowIcon(QIcon('logo.png'))
        # MainWindow.setStyleSheet("background-image:url(background.png)")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(400, 100, 300, 50))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(400, 200, 300, 50))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(300, 100, 100, 50))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(295, 200, 100, 50))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(400, 300, 75, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(600, 300, 75, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralWidget)

        self.pushButton.clicked.connect(self.word_get)
        self.pushButton_2.clicked.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "iCSHD"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Please enter your account"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Please enter your password"))
        self.label.setText(_translate("MainWindow", "Account"))
        self.label_2.setText(_translate("MainWindow", "Password"))
        self.pushButton.setText(_translate("MainWindow", "Yes"))
        self.pushButton_2.setText(_translate("MainWindow", "Cancle"))

    def word_get(self):
        login_user = self.lineEdit.text()
        login_password = self.lineEdit_2.text()
        if login_user == 'admin' and login_password == '123456':
            ui_hello.show()
            mainWindow.close()
        else:
            QMessageBox.warning(self,
                    "Warning",
                    "Username or password is incorrect!",
                    QMessageBox.Yes)
            self.lineEdit.setFocus()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui_hello = MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())