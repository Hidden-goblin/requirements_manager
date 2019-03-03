# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QFileDialog
from app.ui.PasswordForm import Ui_PasswordForm


class CapturePassword(QDialog, Ui_PasswordForm):
    def __init__(self, parent = None):
        super(CapturePassword, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        # Connections
        self.connectBtn.clicked.connect(self.connect)
        self.cancelBtn.clicked.connect(self.cancel)

        self.password = ""

    def connect(self):
        if self.passwordLdt.text():
            self.password = self.passwordLdt.text()

        self.close()

    def cancel(self):
        self.close()
