from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore


class MyTextEdit(QTextEdit):
    launch_update = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            self.launch_update.emit(True)

        super().keyPressEvent(event)
