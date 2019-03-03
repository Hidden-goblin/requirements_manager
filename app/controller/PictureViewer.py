# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QFileDialog
from app.ui.PictureViewDialog import Ui_PictureViewDialog


class PictureViewer(QDialog, Ui_PictureViewDialog):
    def __init__(self, parent = None, picture_name = None):
        super(PictureViewer, self).__init__(parent)
        print("Init Feature Adder UI")
        self.parent = parent
        self.setupUi(self)
        self.textEdit.setHtml("<img src='{}' >".format(picture_name))
        self.pushButton.clicked.connect(self.close)
