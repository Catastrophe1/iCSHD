# -*- coding: UTF-8 -*-

'''
@Author: t-zhel
@Date: 2019-07-13 23:05:14
@LastEditTime: 2019-07-13 23:16:01
@LastEditTime: 2019-07-18 17:03:41
@Description: file content
'''

from PyQt5.QtWidgets import (QWidget, QScrollArea, QAction, QLabel,
                             QHBoxLayout, QVBoxLayout, QMainWindow,
                             QApplication, QTextEdit, QPushButton, QLineEdit)

class LineWidget(QWidget):
    def __init__(self, lineLabel, parent=None, **kwargs):
        super().__init__(parent)
        hbox = QHBoxLayout()

        label = QLabel(lineLabel, self)
        label.setFixedSize(220, 40)
        hbox.addWidget(label)

        textEditWidth = kwargs.get("textEditWidth", 220)
        textEditHeight = kwargs.get("textEditHeight", 40)
        self.textEdit = QLineEdit(self)
        self.textEdit.setFixedSize(textEditWidth, textEditHeight)
        self.textEdit.setReadOnly(True)
        hbox.addWidget(self.textEdit)

        self.setLayout(hbox)

class SearchLineWidget(QWidget):
    def __init__(self, sqlcon, parent=None):
        super().__init__(parent)

        self.sqlcon = sqlcon

        hbox = QHBoxLayout()

        self.textEdit = QLineEdit(self)
        self.textEdit.setFixedHeight(40)
        self.textEdit.setPlaceholderText("Enter case ID to search")
        hbox.addWidget(self.textEdit)

        button = QPushButton("Search", self)
        button.setFixedSize(100, 40)
        button.clicked.connect(self.searchByCaseID)
        hbox.addWidget(button)

        self.setLayout(hbox)

    def searchByCaseID(self):
        cur = self.sqlcon.cursor()

        sql = '''
        select * from iCSHD_Case where CaseNumber = '%s'
        ''' % self.textEdit.text()

        cur.execute(sql)
        case = cur.fetchall()[0]

        self.parent().caseAgeWidget.textEdit.setText(str(case[2]))
        self.parent().caseAgeWidget.setVisible(True)
        self.parent().idleTimeWidget.textEdit.setText(str(case[3]))
        self.parent().idleTimeWidget.setVisible(True)
        self.parent().serverityWidget.textEdit.setText(str(case[4]))
        self.parent().serverityWidget.setVisible(True)
        self.parent().custSentimentalWidget.textEdit.setText(str(case[7]))
        self.parent().custSentimentalWidget.setVisible(True)
        self.parent().productSupportedWidget.textEdit.setText(case[8])
        self.parent().productSupportedWidget.setVisible(True)
        self.parent().engineerIDWidget.textEdit.setText(case[11])
        self.parent().engineerIDWidget.setVisible(True)
        self.parent().isFDRWidget.textEdit.setText(str(case[12]))
        self.parent().isFDRWidget.setVisible(True)
        self.parent().isResolvedWidget.textEdit.setText(str(case[13]))
        self.parent().isResolvedWidget.setVisible(True)

class SearchCaseWin(QWidget):
    def __init__(self, sqlcon, parent=None, **kwargs):
        super().__init__(parent)

        vbox = QVBoxLayout()

        self.searchLineWidget = SearchLineWidget(sqlcon, self)
        vbox.addWidget(self.searchLineWidget)

        self.caseAgeWidget = LineWidget("Case Age")
        self.caseAgeWidget.setVisible(False)
        vbox.addWidget(self.caseAgeWidget)

        self.idleTimeWidget = LineWidget("Idle Time")
        self.idleTimeWidget.setVisible(False)
        vbox.addWidget(self.idleTimeWidget)

        self.serverityWidget = LineWidget("Serverity")
        self.serverityWidget.setVisible(False)
        vbox.addWidget(self.serverityWidget)

        self.custSentimentalWidget = LineWidget("Customer Sentimental")
        self.custSentimentalWidget.setVisible(False)
        vbox.addWidget(self.custSentimentalWidget)

        self.productSupportedWidget = LineWidget("Product Supported")
        self.productSupportedWidget.setVisible(False)
        vbox.addWidget(self.productSupportedWidget)

        self.engineerIDWidget = LineWidget("Engineer ID")
        self.engineerIDWidget.setVisible(False)
        vbox.addWidget(self.engineerIDWidget)

        self.isFDRWidget = LineWidget("isFDR")
        self.isFDRWidget.setVisible(False)
        vbox.addWidget(self.isFDRWidget)

        self.isResolvedWidget = LineWidget("isResolved")
        self.isResolvedWidget.setVisible(False)
        vbox.addWidget(self.isResolvedWidget)

        self.setLayout(vbox)