# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTableWidget, QWidget, QMainWindow, qApp

class UseCaseListDisplay(QTableWidget):
    def __init__(self, usecases = () ,parent=none):
        super(QTableWidget, self).__init__(parent)
        if len( usecases ) == 0:
            self.ee

