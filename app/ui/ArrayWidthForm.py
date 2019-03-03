# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ArrayWidthForm.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ArrayWidthForm(object):
    def setupUi(self, ArrayWidthForm):
        ArrayWidthForm.setObjectName("ArrayWidthForm")
        ArrayWidthForm.resize(465, 152)
        self.AddBtn = QtWidgets.QPushButton(ArrayWidthForm)
        self.AddBtn.setGeometry(QtCore.QRect(270, 100, 75, 23))
        self.AddBtn.setObjectName("AddBtn")
        self.CancelBtn = QtWidgets.QPushButton(ArrayWidthForm)
        self.CancelBtn.setGeometry(QtCore.QRect(360, 100, 75, 23))
        self.CancelBtn.setObjectName("CancelBtn")
        self.label = QtWidgets.QLabel(ArrayWidthForm)
        self.label.setGeometry(QtCore.QRect(10, 50, 371, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.numberOfColumnSBx = QtWidgets.QSpinBox(ArrayWidthForm)
        self.numberOfColumnSBx.setGeometry(QtCore.QRect(390, 50, 51, 22))
        self.numberOfColumnSBx.setObjectName("numberOfColumnSBx")

        self.retranslateUi(ArrayWidthForm)
        QtCore.QMetaObject.connectSlotsByName(ArrayWidthForm)

    def retranslateUi(self, ArrayWidthForm):
        _translate = QtCore.QCoreApplication.translate
        ArrayWidthForm.setWindowTitle(_translate("ArrayWidthForm", "Creating array data"))
        self.AddBtn.setText(_translate("ArrayWidthForm", "Submit"))
        self.CancelBtn.setText(_translate("ArrayWidthForm", "Cancel"))
        self.label.setText(_translate("ArrayWidthForm", "Please enter the number of column of your array"))

