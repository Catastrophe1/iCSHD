# -*- coding: UTF-8 -*-

'''
@Author: t-zhel
@Date: 2019-07-09 13:48:38
@LastEditor: t-zhel
@LastEditTime: 2019-07-12 15:04:30
@Description: Implement the GUI of iCSHD
'''

import sys
import pyodbc
import numpy as np
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import (QWidget, QPushButton, QScrollArea, QTextEdit, QLabel,
                             QHBoxLayout, QVBoxLayout, QMainWindow, QApplication)

class CaseButton(QPushButton):
    def __init__(self, text, caseAge, idleTime, customerSentimental, recentCPE, parent=None):
        super().__init__(text, parent)
        self.caseAge   = caseAge
        self.idleTime  = idleTime
        self.recentCPE = recentCPE
        self.customerSentimental = customerSentimental

class CustomerInfo(QWidget):
    def __init__(self, name, email, SurveyProbability, relatedCases, parent=None):
        super().__init__(parent)

        # Initialize parameters
        custBtnWidth  = 400
        custBtnHeight = 100
        caseBtnWidth  = 200
        caseBtnHeight = 50
        suggestEditorWidth  = 400
        suggestEditorHeight = 200
        commentEditorWidth  = 400
        commentEditorHeight = 200

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        # TODO: Customize the shape of the button
        # Cutomer button
        buttonText = "Customer: %s\nEmail: %s\nSurveyProbability: %s%%" % (name, email, SurveyProbability)
        custBtn = QPushButton(buttonText, self)
        custBtn.setFixedSize(custBtnWidth, custBtnHeight)
        hbox.addWidget(custBtn)

        # Case buttons
        for case in relatedCases:
            # Take the first five characters of CaseID as the name of the CaseButton
            caseBtn = CaseButton("CaseID: %s" % case[0][0:5], case[1], case[2], case[3], case[4], self)

            # Set font color to red if the case hasn't been resolved
            if case[5] == 1:
                caseBtn.setStyleSheet("color: green")
            else:
                caseBtn.setStyleSheet("color: red")

            caseBtn.setToolTip(case[0])
            caseBtn.setFixedSize(caseBtnWidth, caseBtnHeight)
            caseBtn.clicked.connect(self.showGraph)
            vbox.addWidget(caseBtn)
        hbox.addLayout(vbox)

        # Suggest editor
        suggestEditor = QTextEdit(self)
        suggestEditor.setPlaceholderText("Enter your suggestion here")
        suggestEditor.setFixedSize(suggestEditorWidth, suggestEditorHeight)
        hbox.addWidget(suggestEditor)

        # Comment editor
        commentEditor = QTextEdit(self)
        commentEditor.setPlaceholderText("Enter your comment here")
        commentEditor.setFixedSize(commentEditorWidth, commentEditorHeight)
        hbox.addWidget(commentEditor)

        self.setLayout(hbox)

    def showGraph(self):
        # TODO: why must import pyplot here
        import matplotlib.pyplot as plt

        caseBtn = self.sender()

        # Turn on the interactive mode. plt.show() is not needed in interactive mode.
        plt.ion()

        data = np.array([caseBtn.caseAge, caseBtn.idleTime, caseBtn.customerSentimental, caseBtn.recentCPE])
        labels = [str(i) for i in data]
        data = np.concatenate((data, [data[0]]))
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)
        ax.plot(angles, data, 'ro-', linewidth=2)
        ax.set_thetagrids(angles * 180 / np.pi, labels)
        ax.set_title("Customer Analysis", va='bottom')
        ax.grid(True)

        # Turn off the interactive mode
        plt.ioff()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the connection to SQL Server
        self.initSqlServer()

        # Current engineer
        self.alias = "ruiwzhan"

        # Get the information of all customers that current engineer serves
        relatedCustomers = self.getRelatedCustomer(self.alias)

        # TODO: Add prompt bar
        # TODO: Let scrollWidget be the same size with MainWindow
        scrollWidget = QWidget()
        vbox = QVBoxLayout()

        for customer in relatedCustomers:
            vbox.addWidget(CustomerInfo(customer[1],
                                        customer[2],
                                        customer[3],
                                        self.getRelatedCase(customer[0]),
                                        scrollWidget))

        scrollWidget.setLayout(vbox)
        scrollArea = QScrollArea()
        scrollArea.setWidget(scrollWidget)
        self.setCentralWidget(scrollArea)

        self.resize(1550, 1000)
        self.setWindowTitle('Current Engineer: %s' % self.alias)


    def getRelatedCustomer(self, engineerAlias):
        print('Getting the information of all related customers')
        cur = self.conn.cursor()

        sql = '''
        select iCSHD_Customer.CustomerId, iCSHD_Customer.Name, Email, SurveyProbability
        from iCSHD_Case, iCSHD_Customer, iCSHD_Engineer
        where iCSHD_Case.CustomerId = iCSHD_Customer.CustomerId
          and iCSHD_Case.EngineerId = iCSHD_Engineer.EngineerId
          and iCSHD_Engineer.Alias = '%s'
        ''' % engineerAlias

        cur.execute(sql)
        print('Done')
        return cur.fetchall()

    def getRelatedCase(self, customerID):
        print('Getting all related cases')
        cur = self.conn.cursor()

        sql = '''
        select CaseId, CaseAge, IdleTime, CustomerSentimental, RecentCPE, IsResolved
        from iCSHD_Case, iCSHD_Customer
        where iCSHD_Case.CustomerId = iCSHD_Customer.CustomerId and iCSHD_Customer.CustomerId = '%s'
        ''' % customerID

        cur.execute(sql)
        print('Done')
        return cur.fetchall()

    def initSqlServer(self):
        driver = 'SQL Server Native Client 11.0'
        server = 'shmsdsql.database.windows.net'
        user = 'msdadmin'
        password = 'PasSw0rd01'
        database = 'SDCasesTEST'
        self.conn = pyodbc.connect(driver=driver,
                                   server=server,
                                   user=user,
                                   password=password,
                                   database=database)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
