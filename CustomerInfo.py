# -*- coding: UTF-8 -*-

'''
@Author: t-zhel
@Date: 2019-07-13 23:06:18
@LastEditor: t-zhel
@LastEditTime: 2019-07-17 23:48:41
@Description: file content
'''

import numpy as np
from PyQt5.QtWidgets import (QWidget, QPushButton, QTextEdit,
                             QHBoxLayout, QVBoxLayout)

class CaseButton(QPushButton):
    def __init__(self, case, estimatedScore, surveyProbability, parent=None):
        super().__init__(parent)

        self.caseNumber = case[0]
        self.caseAge = case[1]
        self.idleTime = case[2]
        self.customerSentimental = case[3]
        self.productSupported = case[4]
        self.recentCPE = case[5]
        self.isResolved = case[6]
        self.owner = case[7]
        self.isSLA = case[8]
        self.isFDR = case[9]
        self.labor = 123
        self.ongoingCases = 3
        self.estimatedScore = estimatedScore
        self.surveyProbability = surveyProbability

        buttonText = "CaseID: %s\nEstimated Score: %s\nCase Owner: %s\nSurvey Probability: %s%%" \
                    % (self.caseNumber, self.estimatedScore, self.owner, self.surveyProbability)
        self.setText(buttonText)

class CustomerInfo(QWidget):
    def __init__(self, sqlcon, customer, engineerAlias, parent=None):
        super().__init__(parent)

        self.sqlcon = sqlcon

        customerID = customer[0]
        name = customer[1]
        email = customer[2]
        surveyProbability = customer[3]
        company = customer[4]
        tam = customer[5]
        relatedCases = self.getRelatedCase(customerID)

        # Initialize parameters
        custBtnWidth  = 400
        custBtnHeight = 150
        caseBtnWidth  = 270
        caseBtnHeight = 150
        suggestEditorWidth  = 400
        suggestEditorHeight = 200
        commentEditorWidth  = 400
        commentEditorHeight = 200

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        # TODO: Customize the shape of the button
        # Cutomer button
        buttonText = ("Customer: %s\nEmail: %s\nCompany: %s\nTAM: %s\nSurvey Probability: %s%%") \
                   % (name, email, company, tam, surveyProbability)
        custBtn = QPushButton(buttonText, self)
        custBtn.setFixedSize(custBtnWidth, custBtnHeight)
        custBtn.clicked.connect(self.showParams)
        hbox.addWidget(custBtn)

        self.paramsScore = self.getCustomerScoreParameter(customerID)
        self.paramsSurvey = self.getCustomerSurveyParameter(customerID)
        self.aveWeek = self.getWeeklyAverage(customerID)

        # Place the cases belong to current engineer in front of the list
        for i in range(0, len(relatedCases)):
            for j in range(i + 1, len(relatedCases)):
                if relatedCases[j][7] == engineerAlias:
                    relatedCases[i], relatedCases[j] = relatedCases[j], relatedCases[i]

        # Case buttons
        for case in relatedCases:
            # Do not show the case if it has been resolved
            if case[6] == 1:
                continue

            estimatedScore = self.getEstimatedScoreFromAI(case, self.paramsScore)
            surveyProbability = self.getSurveyProbability(case, self.paramsSurvey)

            caseBtn = CaseButton(case, estimatedScore, surveyProbability, self)

            # if the case belong to current engineer
            if caseBtn.owner == engineerAlias:
                caseBtn.setStyleSheet("color: green; border: 2px groove blue;")

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

        # If the customer has opening cases
        if vbox.count():
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

        fig = plt.figure(figsize=(18, 6))

        labels = ["Case Age", "Idle Time", "Labor", "Cust Senti", "Recent CPE", "Ongoing Cases"]
        value = [caseBtn.caseAge, caseBtn.idleTime, caseBtn.labor, caseBtn.customerSentimental,
                 caseBtn.recentCPE, caseBtn.ongoingCases]
        value = np.concatenate((value, [value[0]]))
        aveWeek = self.aveWeek
        aveWeek = np.concatenate((aveWeek, [aveWeek[0]]))
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))

        ax1 = fig.add_subplot(121, polar=True)
        ax1.plot(angles, value, 'o-', linewidth=2, label='Current Case')
        ax1.fill(angles, value, alpha=0.25)
        ax1.plot(angles, aveWeek, 'o-', linewidth=2, label='Average of Last Week')
        ax1.fill(angles, aveWeek, alpha=0.25)

        ax1.set_thetagrids(angles * 180 / np.pi, labels, fontsize='15', color='blue')
        ax1.set_ylim(0, np.max([np.max(value), np.max(aveWeek)]))
        ax1.set_title('Customer Analysis')
        ax1.grid(True)
        ax1.legend(loc = 'upper right')

        ax2 = fig.add_subplot(122)
        plt.axis("off") # Hidden the axis
        row_colors = ['green'] * 6
        rowLabels = ['Owner','Product','SLA', 'FDR', 'IsResolved', 'EstimatedScore']
        cellText = [[caseBtn.owner], [caseBtn.productSupported], [caseBtn.isSLA],
                    [caseBtn.isFDR], [caseBtn.isResolved], [caseBtn.estimatedScore]]
        table = ax2.table(cellText=cellText, rowLabels=rowLabels, rowColours=row_colors,
                          cellLoc='center', loc='center', bbox=[0.25, 0.25, 0.5, 0.5])
        table.set_fontsize(15)

        # Set the color of the font of cell
        # for i in range(len(rowLabels)):
        #     table._cells[(i, 0)]._text.set_color('red')
        table._cells[(5, 0)]._text.set_color('red')

        # Set the color of row labels
        tableProps = table.properties()
        tableCells = tableProps['child_artists']
        tableCells[len(tableCells) - 1]._text.set_color('yellow')

        # Turn off the interactive mode
        plt.ioff()

    def showParams(self):
        import matplotlib.pyplot as plt
        plt.ion()
        fig = plt.figure(figsize=(18, 6))
        ax = plt.subplot(111)
        labels = ['Cust Senti','Recent CPE','Labor', 'Case Age', 'Idle Time',
                  'Ongoing Cases', 'SLA', 'FDR', 'Resolved']
        ax.bar(range(len(self.paramsScore)), self.paramsScore, tick_label=labels)
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

    def getRelatedCase(self, customerID):
        print('Getting all related cases')
        cur = self.sqlcon.cursor()

        sql = '''
        select CaseNumber, CaseAge, IdleTime, CustomerSentimental, ProductSupported,
               RecentCPE, IsResolved, Alias, SlaState, isFDR
        from iCSHD_Case, iCSHD_Customer, iCSHD_Engineer
        where iCSHD_Case.CustomerId = iCSHD_Customer.CustomerId
          and iCSHD_Customer.CustomerId = '%s'
          and iCSHD_Case.EngineerId = iCSHD_Engineer.EngineerId
        ''' % customerID

        cur.execute(sql)
        print('Done')
        return cur.fetchall()

    def getEstimatedScoreFromAI(self, case, params):
        return 5

    def getSurveyProbability(self, case, params):
        return 50

    def getCustomerScoreParameter(self, customerID):
        return [1.5, 0.6, 7.8, 6, 5.2, 6.6, 3.1, 2.7, 1.9]

    def getCustomerSurveyParameter(self, customerID):
        return
    
    def getWeeklyAverage(self, customerID):
        return [50, 50, 30, 40, 60, 160]