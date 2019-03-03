# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PasswordForm.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PasswordForm(object):
    def setupUi(self, PasswordForm):
        PasswordForm.setObjectName("PasswordForm")
        PasswordForm.resize(400, 92)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(PasswordForm)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(PasswordForm)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.passwordLdt = QtWidgets.QLineEdit(PasswordForm)
        self.passwordLdt.setAutoFillBackground(False)
        self.passwordLdt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLdt.setObjectName("passwordLdt")
        self.horizontalLayout_2.addWidget(self.passwordLdt)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.connectBtn = QtWidgets.QPushButton(PasswordForm)
        self.connectBtn.setObjectName("connectBtn")
        self.horizontalLayout_3.addWidget(self.connectBtn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.cancelBtn = QtWidgets.QPushButton(PasswordForm)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout_3.addWidget(self.cancelBtn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(PasswordForm)
        QtCore.QMetaObject.connectSlotsByName(PasswordForm)

    def retranslateUi(self, PasswordForm):
        _translate = QtCore.QCoreApplication.translate
        PasswordForm.setWindowTitle(_translate("PasswordForm", "Enter password"))
        self.label.setText(_translate("PasswordForm", "Password"))
        self.connectBtn.setText(_translate("PasswordForm", "Connect"))
        self.cancelBtn.setText(_translate("PasswordForm", "Cancel"))

