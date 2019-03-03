# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, qApp, QMessageBox
from app.ui.ArrayWidthForm import Ui_ArrayWidthForm
from app.static.ui_utilities import display_error_message


class ArrayWidthAdder(QDialog, Ui_ArrayWidthForm):
    def __init__(self, parent = None):
        super(ArrayWidthAdder, self).__init__(parent)
        self.setupUi(self)
        self.width = 0
        self.AddBtn.clicked.connect(self.width_given)
        self.CancelBtn.clicked.connect(self.close)

    def width_given(self):
        try:
            if self.numberOfColumnSBx.value() == 0:
                error_message = display_error_message("Unvalid value", "The array width can't be 0.")
            else:
                self.width = self.numberOfColumnSBx.value()
                self.close()
        except Exception as exception:
            display_error_message(title = "Functionality conflict", content = exception)
