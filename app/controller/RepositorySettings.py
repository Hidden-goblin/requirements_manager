# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QFileDialog
from os.path import basename
from app.ui.JiraSettingsForm import Ui_jiraSettingsForm
from app.static.ui_utilities import display_error_message


class RepositorySettings(QDialog, Ui_jiraSettingsForm):
    def __init__(self, parent = None):
        super(RepositorySettings, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        # Connections
        self.saveBtn.clicked.connect(self.save)
        self.cancelBtn.clicked.connect(self.cancel)
        #Infos
        self.entry = basename(self.parent.testReqFileName).split(".")[0]
        if self.entry in self.parent.settings:
            self.nameLdt.setText(self.parent.settings[self.entry]["project_name"])
            self.keyLdt.setText(self.parent.settings[self.entry]["project_key"])
            self.urlLdt.setText(self.parent.settings[self.entry]["endpoint"])
            self.usernameLdt.setText(self.parent.settings[self.entry]["username"])
        else:
            self.parent.settings[self.entry] = {}

    def save(self):
        if self.urlLdt.text() and self.usernameLdt.text() and (self.nameLdt.text() or self.keyLdt.text()):
            self.parent.settings[self.entry]["project_name"] = self.nameLdt.text()
            self.parent.settings[self.entry]["project_key"] = self.keyLdt.text()
            self.parent.settings[self.entry]["endpoint"] = self.urlLdt.text()
            self.parent.settings[self.entry]["username"] = self.usernameLdt.text()
            self.close()
        else:
            display_error_message(title = "Incomplete settings",
                                  content = "The URL to your Jira is mandatory.\n Your user name on this Jira is mandatory.\n The project name or project key this repository is related to is mandatory.")

    def cancel(self):
       self.close()