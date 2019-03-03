# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DisplayFeatureForm.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DisplayFeatureForm(object):
    def setupUi(self, DisplayFeatureForm):
        DisplayFeatureForm.setObjectName("DisplayFeatureForm")
        DisplayFeatureForm.resize(800, 777)
        self.closeBtn = QtWidgets.QPushButton(DisplayFeatureForm)
        self.closeBtn.setGeometry(QtCore.QRect(170, 20, 75, 23))
        self.closeBtn.setObjectName("closeBtn")
        self.pushToJiraBtn = QtWidgets.QPushButton(DisplayFeatureForm)
        self.pushToJiraBtn.setGeometry(QtCore.QRect(460, 20, 101, 23))
        self.pushToJiraBtn.setObjectName("pushToJiraBtn")
        self.featureText = QtWidgets.QTextEdit(DisplayFeatureForm)
        self.featureText.setGeometry(QtCore.QRect(20, 50, 751, 701))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.featureText.setFont(font)
        self.featureText.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.featureText.setObjectName("featureText")

        self.retranslateUi(DisplayFeatureForm)
        QtCore.QMetaObject.connectSlotsByName(DisplayFeatureForm)

    def retranslateUi(self, DisplayFeatureForm):
        _translate = QtCore.QCoreApplication.translate
        DisplayFeatureForm.setWindowTitle(_translate("DisplayFeatureForm", "Dialog"))
        self.closeBtn.setText(_translate("DisplayFeatureForm", "Close"))
        self.pushToJiraBtn.setText(_translate("DisplayFeatureForm", "Push to JIRA"))

