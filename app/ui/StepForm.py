# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StepForm.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SimpleStepForm(object):
    def setupUi(self, SimpleStepForm):
        SimpleStepForm.setObjectName("SimpleStepForm")
        SimpleStepForm.resize(465, 152)
        self.AddBtn = QtWidgets.QPushButton(SimpleStepForm)
        self.AddBtn.setGeometry(QtCore.QRect(270, 100, 75, 23))
        self.AddBtn.setObjectName("AddBtn")
        self.CancelBtn = QtWidgets.QPushButton(SimpleStepForm)
        self.CancelBtn.setGeometry(QtCore.QRect(360, 100, 75, 23))
        self.CancelBtn.setObjectName("CancelBtn")
        self.label = QtWidgets.QLabel(SimpleStepForm)
        self.label.setGeometry(QtCore.QRect(20, 20, 47, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.StepLdt = QtWidgets.QLineEdit(SimpleStepForm)
        self.StepLdt.setGeometry(QtCore.QRect(30, 60, 411, 20))
        self.StepLdt.setObjectName("StepLdt")

        self.retranslateUi(SimpleStepForm)
        QtCore.QMetaObject.connectSlotsByName(SimpleStepForm)

    def retranslateUi(self, SimpleStepForm):
        _translate = QtCore.QCoreApplication.translate
        SimpleStepForm.setWindowTitle(_translate("SimpleStepForm", "Dialog"))
        self.AddBtn.setText(_translate("SimpleStepForm", "Add"))
        self.CancelBtn.setText(_translate("SimpleStepForm", "Cancel"))
        self.label.setText(_translate("SimpleStepForm", "Step"))

