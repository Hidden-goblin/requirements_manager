# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphFrom.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GraphForm(object):
    def setupUi(self, GraphForm):
        GraphForm.setObjectName("GraphForm")
        GraphForm.resize(1105, 884)
        self.verticalLayout = QtWidgets.QVBoxLayout(GraphForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(GraphForm)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.graphNameLdt = QtWidgets.QLineEdit(GraphForm)
        self.graphNameLdt.setObjectName("graphNameLdt")
        self.horizontalLayout_3.addWidget(self.graphNameLdt)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.inputGraphTdt = MyTextEdit(GraphForm)
        self.inputGraphTdt.setObjectName("inputGraphTdt")
        self.horizontalLayout.addWidget(self.inputGraphTdt)
        self.viewGraphTdt = QtWidgets.QTextEdit(GraphForm)
        self.viewGraphTdt.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.viewGraphTdt.setObjectName("viewGraphTdt")
        self.horizontalLayout.addWidget(self.viewGraphTdt)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 25, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.updateBtn = QtWidgets.QPushButton(GraphForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.updateBtn.sizePolicy().hasHeightForWidth())
        self.updateBtn.setSizePolicy(sizePolicy)
        self.updateBtn.setObjectName("updateBtn")
        self.horizontalLayout_2.addWidget(self.updateBtn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.closeBtn = QtWidgets.QPushButton(GraphForm)
        self.closeBtn.setObjectName("closeBtn")
        self.horizontalLayout_2.addWidget(self.closeBtn)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(GraphForm)
        QtCore.QMetaObject.connectSlotsByName(GraphForm)

    def retranslateUi(self, GraphForm):
        _translate = QtCore.QCoreApplication.translate
        GraphForm.setWindowTitle(_translate("GraphForm", "Dialog"))
        self.label.setText(_translate("GraphForm", "Graph Name:"))
        self.updateBtn.setText(_translate("GraphForm", "Update"))
        self.closeBtn.setText(_translate("GraphForm", "Close"))

from app.ui.MyTextEdit import MyTextEdit
