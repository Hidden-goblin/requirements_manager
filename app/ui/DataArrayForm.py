# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DataArrayForm.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CreateArrayForm(object):
    def setupUi(self, CreateArrayForm):
        CreateArrayForm.setObjectName("CreateArrayForm")
        CreateArrayForm.resize(893, 454)
        self.nameLdt = QtWidgets.QLineEdit(CreateArrayForm)
        self.nameLdt.setGeometry(QtCore.QRect(230, 30, 221, 20))
        self.nameLdt.setObjectName("nameLdt")
        self.ArrayHeadersTab = QtWidgets.QTableWidget(CreateArrayForm)
        self.ArrayHeadersTab.setGeometry(QtCore.QRect(20, 100, 831, 41))
        self.ArrayHeadersTab.setObjectName("ArrayHeadersTab")
        self.ArrayHeadersTab.setColumnCount(0)
        self.ArrayHeadersTab.setRowCount(0)
        self.ArrayDataTab = QtWidgets.QTableWidget(CreateArrayForm)
        self.ArrayDataTab.setGeometry(QtCore.QRect(20, 180, 831, 131))
        self.ArrayDataTab.setObjectName("ArrayDataTab")
        self.ArrayDataTab.setColumnCount(0)
        self.ArrayDataTab.setRowCount(0)
        self.DataArrayName = QtWidgets.QLabel(CreateArrayForm)
        self.DataArrayName.setGeometry(QtCore.QRect(40, 30, 181, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.DataArrayName.setFont(font)
        self.DataArrayName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.DataArrayName.setObjectName("DataArrayName")
        self.label = QtWidgets.QLabel(CreateArrayForm)
        self.label.setGeometry(QtCore.QRect(20, 70, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(CreateArrayForm)
        self.label_2.setGeometry(QtCore.QRect(20, 150, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setUnderline(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.addPBtn = QtWidgets.QPushButton(CreateArrayForm)
        self.addPBtn.setGeometry(QtCore.QRect(500, 30, 75, 23))
        self.addPBtn.setObjectName("addPBtn")
        self.resetPBtn = QtWidgets.QPushButton(CreateArrayForm)
        self.resetPBtn.setGeometry(QtCore.QRect(700, 30, 75, 23))
        self.resetPBtn.setObjectName("resetPBtn")
        self.cancelPBtn = QtWidgets.QPushButton(CreateArrayForm)
        self.cancelPBtn.setGeometry(QtCore.QRect(780, 30, 75, 23))
        self.cancelPBtn.setObjectName("cancelPBtn")

        self.retranslateUi(CreateArrayForm)
        QtCore.QMetaObject.connectSlotsByName(CreateArrayForm)

    def retranslateUi(self, CreateArrayForm):
        _translate = QtCore.QCoreApplication.translate
        CreateArrayForm.setWindowTitle(_translate("CreateArrayForm", "Data array"))
        self.DataArrayName.setText(_translate("CreateArrayForm", "Name"))
        self.label.setText(_translate("CreateArrayForm", "Array headers"))
        self.label_2.setText(_translate("CreateArrayForm", "Array data"))
        self.addPBtn.setText(_translate("CreateArrayForm", "Add"))
        self.resetPBtn.setText(_translate("CreateArrayForm", "Reset"))
        self.cancelPBtn.setText(_translate("CreateArrayForm", "Cancel"))

