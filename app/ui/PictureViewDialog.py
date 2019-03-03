# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PictureViewDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PictureViewDialog(object):
    def setupUi(self, PictureViewDialog):
        PictureViewDialog.setObjectName("PictureViewDialog")
        PictureViewDialog.resize(887, 767)
        self.verticalLayout = QtWidgets.QVBoxLayout(PictureViewDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(PictureViewDialog)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.textEdit = QtWidgets.QTextEdit(PictureViewDialog)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)

        self.retranslateUi(PictureViewDialog)
        QtCore.QMetaObject.connectSlotsByName(PictureViewDialog)

    def retranslateUi(self, PictureViewDialog):
        _translate = QtCore.QCoreApplication.translate
        PictureViewDialog.setWindowTitle(_translate("PictureViewDialog", "Dialog"))
        self.pushButton.setText(_translate("PictureViewDialog", "Close"))

