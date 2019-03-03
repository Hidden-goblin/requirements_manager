# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, qApp, QMessageBox
from app.ui.StepForm import Ui_SimpleStepForm
from app.static.ui_utilities import display_error_message


class StepAdder(QDialog, Ui_SimpleStepForm):
    def __init__(self, parent = None, list_to_add = None, update_index = None):
        super(StepAdder, self).__init__(parent)
        print("Launch step adder")
        self.parent = parent
        self.list_to_add = list_to_add
        self.update_index = update_index
        self.setupUi(self)
        if update_index is not None:
            self.update_index = int(update_index)
            self.StepLdt.insert(self.list_to_add[self.update_index])
            self.AddBtn.setText("Update")
        self.AddBtn.clicked.connect(self.add)
        self.CancelBtn.clicked.connect(self.close)

    def add(self):
        try:
            if len(self.StepLdt.text()) == 0:
                display_error_message(title = "Error", content = "You can't add an empty step")
            elif self.update_index is None:
                self.list_to_add.append(self.StepLdt.text())
            else:
                self.list_to_add[int(self.update_index)] = self.StepLdt.text()
            self.close()
        except Exception as exception:
            display_error_message(title = "Add step error", content = exception)


