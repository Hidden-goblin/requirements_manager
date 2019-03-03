# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'JiraSettingsForm.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_jiraSettingsForm(object):
    def setupUi(self, jiraSettingsForm):
        jiraSettingsForm.setObjectName("jiraSettingsForm")
        jiraSettingsForm.resize(528, 396)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(jiraSettingsForm)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(jiraSettingsForm)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.urlLdt = QtWidgets.QLineEdit(jiraSettingsForm)
        self.urlLdt.setObjectName("urlLdt")
        self.horizontalLayout.addWidget(self.urlLdt)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(jiraSettingsForm)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.keyLdt = QtWidgets.QLineEdit(jiraSettingsForm)
        self.keyLdt.setObjectName("keyLdt")
        self.horizontalLayout_2.addWidget(self.keyLdt)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(jiraSettingsForm)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.nameLdt = QtWidgets.QLineEdit(jiraSettingsForm)
        self.nameLdt.setObjectName("nameLdt")
        self.horizontalLayout_5.addWidget(self.nameLdt)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(jiraSettingsForm)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.usernameLdt = QtWidgets.QLineEdit(jiraSettingsForm)
        self.usernameLdt.setObjectName("usernameLdt")
        self.horizontalLayout_3.addWidget(self.usernameLdt)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.saveBtn = QtWidgets.QPushButton(jiraSettingsForm)
        self.saveBtn.setObjectName("saveBtn")
        self.horizontalLayout_4.addWidget(self.saveBtn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.cancelBtn = QtWidgets.QPushButton(jiraSettingsForm)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout_4.addWidget(self.cancelBtn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(jiraSettingsForm)
        QtCore.QMetaObject.connectSlotsByName(jiraSettingsForm)

    def retranslateUi(self, jiraSettingsForm):
        _translate = QtCore.QCoreApplication.translate
        jiraSettingsForm.setWindowTitle(_translate("jiraSettingsForm", "Jira Settings"))
        self.label.setText(_translate("jiraSettingsForm", "Jira URL"))
        self.label_2.setText(_translate("jiraSettingsForm", "Project Key"))
        self.label_4.setText(_translate("jiraSettingsForm", "Project Name"))
        self.label_3.setText(_translate("jiraSettingsForm", "User name"))
        self.saveBtn.setText(_translate("jiraSettingsForm", "Save settings"))
        self.cancelBtn.setText(_translate("jiraSettingsForm", "Cancel"))

