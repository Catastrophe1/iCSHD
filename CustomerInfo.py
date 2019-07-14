# -*- coding: UTF-8 -*-

'''
@Author: t-zhel
@Date: 2019-07-13 23:06:18
@LastEditor: t-zhel
@LastEditTime: 2019-07-14 15:26:01
@Description: file content
'''

import numpy as np
from PyQt5.QtWidgets import (QWidget, QPushButton, QTextEdit,
                             QHBoxLayout, QVBoxLayout)

class CaseButton(QPushButton):
    def __init__(self, parent=None, **kwargs):
        super().__init__(kwargs.get('buttonText', ""), parent)

        self.SLA = kwargs.get('SLA', 'default SLA')
        self.FDR = kwargs.get('FDR', 'default FDR')
        self.labor = kwargs.get('labor', 123)
        self.owner = kwargs.get('owner', "")
        self.caseAge = kwargs.get('caseAge', 0)
        self.idleTime = kwargs.get('idleTime', 0)
        self.recentCPE = kwargs.get('recentCPE', 0)
        self.isResolved = kwargs.get('isResolved', 0)
        self.ongoingCases = kwargs.get('ongoingCases', 3)
        self.estimatedScore = kwargs.get('estimatedScore', 5)
        self.productSupported = kwargs.get('productSupported', "")
        self.customerSentimental = kwargs.get('customerSentimental', 0)

class CustomerInfo(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)

        TAM = kwargs.get('TAM', "default TAM")
        name = kwargs.get('name', "")
        email = kwargs.get('email', "")
        company = kwargs.get('company', "")
        relatedCases = kwargs.get('relatedCases', [])
        engineerAlias = kwargs.get('engineerAlias', "")
        estimatedScore = kwargs.get('estimatedScore', 5)
        surveyProbability = kwargs.get('surveyProbability', 0)

        # Initialize parameters
        custBtnWidth  = 400
        custBtnHeight = 200
        caseBtnWidth  = 200
        caseBtnHeight = 50
        suggestEditorWidth  = 400
        suggestEditorHeight = 200
        commentEditorWidth  = 400
        commentEditorHeight = 200

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        # TODO: Customize the shape of the button
        # TODO: Show long company name
        # Cutomer button
        buttonText = ("Customer: %s\nEmail: %s\nCompany: %s\nTAM: %s\n"
                    + "Survey Probability: %s%%\nEstimated score: %s") \
                    % (name, email, company, TAM, surveyProbability, estimatedScore)
        custBtn = QPushButton(buttonText, self)
        custBtn.setFixedSize(custBtnWidth, custBtnHeight)
        hbox.addWidget(custBtn)

        # Case buttons
        for case in relatedCases:
            # Take the first five characters of CaseID as the name of the CaseButton
            caseBtn = CaseButton(self,
                                 buttonText="CaseID: %s" % case[0][0:5],
                                 caseAge=case[1],
                                 idleTime=case[2],
                                 customerSentimental=case[3],
                                 productSupported=case[4],
                                 recentCPE=case[5],
                                 isResolved=case[6],
                                 owner=case[7])

            # if the case hase been resolved
            if caseBtn.isResolved == 1:
                # if the case belong to current engineer
                if caseBtn.owner == engineerAlias:
                    caseBtn.setStyleSheet("color: green; border: 2px groove blue;")
                else:
                    caseBtn.setStyleSheet("color: green")
            else:
                if caseBtn.owner == engineerAlias:
                    caseBtn.setStyleSheet("color: red; border: 2px groove blue;")
                else:
                    caseBtn.setStyleSheet("color: red")

            caseBtn.setToolTip(case[0])
            caseBtn.setFixedSize(caseBtnWidth, caseBtnHeight)
            caseBtn.clicked.connect(self.showGraph)
            vbox.addWidget(caseBtn)
        hbox.addLayout(vbox)

        # Suggest editor
        self.suggestEditor = QTextEdit(self)
        self.suggestEditor.setPlaceholderText("AI suggestion")
        self.suggestEditor.setFixedSize(suggestEditorWidth, suggestEditorHeight)
        hbox.addWidget(self.suggestEditor)

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

        # Get suggestions from AI
        suggestion = self.getSuggestionFromAI(caseBtn)
        self.suggestEditor.setText(suggestion)

        # Turn on the interactive mode. plt.show() is not needed in interactive mode.
        plt.ion()

        labels = ["CaseAge: "+str(caseBtn.caseAge), "Idle Time: "+str(caseBtn.idleTime),
                  "labor: "+str(caseBtn.labor), "Cust Senti: "+str(caseBtn.customerSentimental),
                  "Recent CPE: "+str(caseBtn.recentCPE), "Ongoing Cases: "+str(caseBtn.ongoingCases)]

        data = np.array([caseBtn.caseAge, caseBtn.idleTime, caseBtn.labor, caseBtn.customerSentimental,
                         caseBtn.recentCPE, caseBtn.ongoingCases])
        data = np.concatenate((data, [data[0]]))

        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))

        fig = plt.figure(figsize=(18, 6))

        ax1 = fig.add_subplot(121, polar=True)
        ax1.plot(angles, data, 'ro-', linewidth=2)
        ax1.set_thetagrids(angles * 180 / np.pi, labels)
        ax1.set_title("Customer Analysis", va='bottom')
        ax1.grid(True)

        # TODO: Hidden the row label
        ax2 = fig.add_subplot(122)
        plt.axis("off")
        colLabels = ['Information']
        rowLabels = ['Owner','Product','SLA', 'FDR', 'IsResolved', 'EstimatedScore']
        cellText = [[caseBtn.owner], [caseBtn.productSupported], [caseBtn.SLA],
                    [caseBtn.FDR], [caseBtn.isResolved], [caseBtn.estimatedScore]]
        ax2.table(cellText=cellText, rowLabels=rowLabels,
                  colLabels=colLabels, cellLoc='center', loc='center')

        # Turn off the interactive mode
        plt.ioff()
    
    def getSuggestionFromAI(self, caseBtn):
        suggestion = ""

        # TODO: Better algorithm
        if caseBtn.idleTime > 3:
            suggestion += "Idle Time is too large!\n"
        if caseBtn.caseAge > 3000:
            suggestion += "Case Age is too large!\n"
        if caseBtn.customerSentimental < 20:
            suggestion += "Customer Sentimental is too small!\n"
        if caseBtn.labor > 600:
            suggestion += "Labor Time is too large!\n"
        
        return suggestion