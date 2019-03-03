# -*- coding: utf-8 -*-

"""
Main application for the usecase GUI

Author: EAI
First edited: September 2017
"""

import json
import tempfile
import logging
from PyQt5.QtWidgets import QMainWindow, qApp, QTableWidgetItem, QFileDialog,\
    QMessageBox, QPushButton, QTreeWidgetItem
from PyQt5.QtCore import pyqtSignal
from os.path import isfile, basename, exists
from app.ui.MainWindow import Ui_MainWindow
from app.controller.FeatureAdder import FeatureAdder
from app.controller.DisplayFeatureDialog import DisplayFeatureDialog
from app.controller.JiraConnection import JiraConnection
from app.controller.RepositorySettings import RepositorySettings
from app.controller.CapturePassword import CapturePassword
from app.data.TinyDBRepository import TinyDbRepository
from app.static.ui_utilities import display_message, display_error_message
from app.static.export_utilities import export_repository, export_usecase
from app.static.import_utilities import import_testinsight

logger = logging.getLogger('simpleExample')


class MainApplication(QMainWindow, Ui_MainWindow):
    """This is the main application program. It contains all data used by the several panels.

        It aims to improve feature writing quality as well as ease the test creation.
    """

    #Application signal
    repository_update_signal = pyqtSignal(bool)

    def __init__(self):
        super(MainApplication, self).__init__()
        self.setupUi(self)
        #class vars
        logger.debug("Init Var")
        self.settings_filename = "{}/USMAN/setting.cfg".format(tempfile.gettempdir())
        self.repository = None
        #self.testReqFileName = ""
        #self.testReqWorkingFileName = ""
        self.is_repository_need_saving = False
        self.jira = None
        self.settings = None
        logger.debug("Tab init")
        #Connections Menu & Action
        logger.debug("Connections menu")
        self.actionExit.triggered.connect(self.exit_application)
        self.actionOpen_Repository.triggered.connect(self.open_repository)
        self.actionSave_Repository.triggered.connect(self.save_repository)
        self.actionNew_Repository.triggered.connect(self.new_repository)
        self.actionExport_feature.triggered.connect(self.export_feature)
        self.actionClose_Repository.triggered.connect(self.close_repository)
        self.actionRepository_settings.triggered.connect(self.set_repository)
        self.actionConnect_to_Jira.triggered.connect(self.init_jira_connection)
        #Connections buttons
        logger.debug("Connections button")
        self.addFeatureBtn.clicked.connect(self.on_add_feature)
        #Signals
        logger.debug("Signal")
        self.repository_update_signal.connect(self.update_title)
        #Menu enabling
        logger.debug("Action enabling")
        self.menuExport.setEnabled(False)
        self.menuImport.setEnabled(False)
        self.actionImport_from_TestInsight.setEnabled(False)
        self.actionImport_Excel.setEnabled(False)
        self.actionSave_Repository.setEnabled(False)
        self.actionClose_Repository.setEnabled(False)
        self.actionRepository_settings.setEnabled(False)
        self.actionConnect_to_Jira.setEnabled(False)
        self.show()
        logger.debug("Show time")
        self.repository_update_signal.emit(False)
        if isfile(self.settings_filename):
            logger.debug("isfile returned true")
            with open(self.settings_filename) as file:
                self.settings = json.load(file)
        else:
            self.settings = {}
        logger.debug("Launched")

    def closeEvent(self, event):
        """
        Re-implement the default close event.
        :param event: the event
        :return:
        """
        self.exit_application()

    def exit_application(self):
        """
        Exit the application properly
        :return:
        """
        try:
            if self.repository is not None:
                self.close_repository()
            qApp.quit()
        except Exception as exception:
            display_error_message(title = "Error while exiting the app", content = repr(exception))

    def new_repository(self):
        """Create a new repository asking the name of the repository."""
        try:
            if self.repository is not None:
                self.close_repository()

            requested_file_name = QFileDialog.getSaveFileName(self, 'New File', "", "Text files (*.us)")[0]
            if requested_file_name:
                self.repository = TinyDbRepository(file_name = requested_file_name)
                self.setWindowTitle("MainWindow : {}".format(self.repository.get_repository_name()))
                self.actionClose_Repository.setEnabled(True)
                self.menuImport.setEnabled(True)
                self.actionImport_from_TestInsight.setEnabled(True)
                self.actionImport_Excel.setEnabled(False)
                self.actionRepository_settings(True)
                self.actionConnect_to_Jira.setEnabled(True)
        except Exception as exception:
            display_error_message(title = "New repository error", content = exception)

    def open_repository(self):
        """Call the Qt FileDialog in order to open a valid repository file (*.us).
            Valid means:
              - is a zip file
              - contains a json file which can be parsed by tinydb database
              - contains an attachments subfolder with files
        """
        #Check another repository is not open: close it if open
        if self.repository is not None:
            self.close_repository()

        #Ask for the repository name
        testReqFileName = QFileDialog.getOpenFileName(self, 'Open File', "", "Text files (*.us)")[0]
        try:
            logger.debug(" '{}' retrieved".format(testReqFileName))
            if testReqFileName:
                self.repository = TinyDbRepository(file_name = testReqFileName)
        except IOError as ioexcep:
            logger.debug("No File selected '{}'".format(ioexcep))
        except Exception as excep:
            logger.debug("An exception is raised! {0}".format(excep))
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Can't open '{}'.\nReceive error message : {}".format(testReqFileName, excep))
            msg.setWindowTitle("Open fail")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(self.open_repository)
            msg.exec_()
        #A valid name is given, open
        try:
            if testReqFileName:
                self.setWindowTitle("MainWindow : {}".format(self.repository.get_repository_name()))
                self.menuExport.setEnabled(True)
                self.actionClose_Repository.setEnabled(True)
                self.actionRepository_settings.setEnabled(True)
                self.actionConnect_to_Jira.setEnabled(True)
                self.display_element_list()

        except Exception as exception:
            display_error_message(title = "Open repository error", content = exception)

    def save_repository(self):
        """Save the current repository to file"""
        try:
            self.repository.save_repository()
            self.is_repository_need_saving = False
            self.repository_update_signal.emit(False)
            self.actionSave_Repository.setEnabled(False)
        except Exception as exception:
            display_error_message(title = "Save repository error", content = exception)

    def close_repository(self):
        """Close the current repository"""
        try:
            if self.is_repository_need_saving:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setText("Your repository has been updated.\n Do you want to save it before closing?")
                msg.setWindowTitle("Open fail")
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.exec_()
                if msg.clickedButton() == msg.button(QMessageBox.Yes):
                    self.save_repository()
            #Close db and remove working file
            self.repository.close_repository()
            #Back to default
            self.treeWidget.clear()
            self.is_repository_need_saving = False
            #Disabling menu & tab
            self.actionClose_Repository.setEnabled(False)
            self.actionSave_Repository.setEnabled(False)
            self.menuExport.setEnabled(False)
            self.menuImport.setEnabled(False)
            self.actionImport_from_TestInsight.setEnabled(False)
            self.actionImport_Excel.setEnabled(False)
            self.actionRepository_settings.setEnabled(False)
            self.actionConnect_to_Jira.setEnabled(False)
            self.repository = None
            self.update_title()
        except Exception as exception:
            display_error_message(title = "Close repository error", content = exception)

    def set_repository(self):
        """Add settings to the repository
        """
        settings = RepositorySettings(parent = self)
        settings.exec_()
        with open(self.settings_filename, "w") as file:
            file.write(json.dumps(self.settings))

    def init_jira_connection(self):
        """
        Connect to JIRA with the settings
        TODO Update with the new logic
        :return:
        """
        if self.jira is None:
            password = CapturePassword(parent = self)
            password.exec_()
            if password.password:
                self.jira = JiraConnection(
                    url = self.settings[basename(self.testReqFileName).split(".")[0]]["endpoint"],
                    username = self.settings[basename(self.testReqFileName).split(".")[0]]["username"],
                    password = password.password)
                self.jira.set_project_id(
                    project_name = self.settings[basename(self.testReqFileName).split(".")[0]]["project_name"],
                    project_key = self.settings[basename(self.testReqFileName).split(".")[0]]["project_key"])
                display_message("Connection succeed", "You have been identified in Jira.")
            else:
                display_error_message(title = "Not Connected to Jira",
                                      content = "You have to provide a valid password in order to be connected to Jira")

    def export_feature(self):
        """
        Export a feature to directory
        :return:
        """
        try:
            directory = QFileDialog.getExistingDirectory(self, "Open Directory", '',
                                                         QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
            if directory:
                self.repository.export_feature_to_gherkin(folder_name = directory)
                display_message("Export feature to gherkin",
                                "All features have been successfully exported to {}".format(directory))
        except Exception as exception:
            display_error_message(title = "Export feature error", content = exception)

    def export_whole_repository(self):
        """
        Export the whole repository using an export utility
        :return:
        """
        try:
            export_repository(parent = self)
        except Exception as exception:
            display_error_message(title = "Export whole repository error", content = exception)

    def export_test_plan(self):
        try:
            logger.debug("Export use cases")
            export_usecase(parent = self)
        except Exception as exception:
            display_error_message(title = "Export test plan error", content = exception)

    def export_displayed_use_case(self):
        logger.debug("Export selected!!")

    def import_from_excel(self):
        try:
            import_testinsight(self)
        except Exception as exception:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(exception)
            msg.setWindowTitle("Import fail")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            logger.debug("import_from_excel cast {}".format(exception))

    def update_title(self, updated = False):
        """
        Update the window title depending on the
        :param updated:
        :return:
        """
        try:
            logger.debug("Update title")
            if updated and self.is_repository_need_saving:
                self.setWindowTitle("MainWindow : {}{}".format(self.repository.get_repository_name(), "*"))
                self.actionSave_Repository.setEnabled(True)
            elif not updated and self.is_repository_need_saving:
                self.setWindowTitle("MainWindow : {}{}".format(self.repository.get_repository_name(), "*"))
                self.actionSave_Repository.setEnabled(True)
            elif updated and not self.is_repository_need_saving:
                self.setWindowTitle("MainWindow : {}{}".format(self.repository.get_repository_name(), "*"))
                self.actionSave_Repository.setEnabled(True)
                self.is_repository_need_saving = True
            elif not updated and not self.is_repository_need_saving and self.repository is not None:
                self.setWindowTitle("MainWindow : {}{}".format(self.repository.get_repository_name(), ""))
            else:
                logger.debug("update_title : else clause")
                self.setWindowTitle("MainWindow : {}{}".format("", ""))
        except Exception as exception:
            display_error_message(title = "Update title error", content = exception)

    #Feature management
    def display_element_list(self):
        """
        Display the repository in Tree view.
        :return:
        """
        try:
            self.treeWidget.clear()
            self.treeWidget.setColumnCount(3)
            themes = self.repository.get_elements(table = "themes")
            logger.debug("'{}'".format(themes))
            logger.debug("'{}'".format(themes["elements"]))
            epics = []
            features = []
            #Theme and downward
            for theme_id, theme in enumerate(themes["elements"]):
                logger.debug("In the theme loop")
                logger.debug("Element '{}'".format(theme))
                logger.debug("ID '{}'".format(theme_id))
                item = QTreeWidgetItem(self.treeWidget)
                item.setText(0, theme["name"])
                item.setText(1, str(theme_id + 1))  #Id starts from 1, get a list which starts from 0
                item.setText(2, "themes")
                if theme["epics"]:
                    for epic_id in theme["epics"]:
                        logger.debug("in the epics loop")
                        epic = self.repository.get_element(table = "epics", element_id = epic_id)
                        epic_item = QTreeWidgetItem([epic["element"]["name"], str(epic_id), "epics"])
                        item.addChild(epic_item)
                        epics.append(epic_id)
                        if epic["element"]["features"]:
                            for feature_id in epic["element"]["features"]:
                                feature = self.repository.get_element(table = "features", element_id = feature_id)
                                feature_item = QTreeWidgetItem(
                                    [feature["element"]["name"], str(feature_id), "features"])
                                epic_item.addChild(feature_item)
                                features.append(feature_id)
                self.treeWidget.addTopLevelItem(item)
            logger.debug("List of epics id '{}'\n Processed epics id '{}'".format(
                self.repository.get_elements_id(table = "epics"), epics))

            #Epics not linked to a theme and downward
            all_epic_id = self.repository.get_elements_id(table = "epics")
            item = QTreeWidgetItem(self.treeWidget)
            item.setText(0, "Orphan Epics")
            item.setText(1, "NA")
            for epic_id in set(all_epic_id['elements']).difference(epics):
                epic = self.repository.get_element(table = "epics", element_id = epic_id)
                epic_item = QTreeWidgetItem([epic["element"]["name"], str(epic_id), "epics"])
                item.addChild(epic_item)
                if epic["element"]["features"]:
                    for feature_id in epic["element"]["features"]:
                        feature = self.repository.get_element(table = "features", element_id = feature_id)
                        feature_item = QTreeWidgetItem([feature["element"]["name"], str(feature_id), "features"])
                        epic_item.addChild(feature_item)
                        features.append(feature_id)
            self.treeWidget.addTopLevelItem(item)

            #Feature not linked to an epic
            item = QTreeWidgetItem(self.treeWidget)
            item.setText(0, "Orphan Features")
            item.setText(1, "NA")
            for feature_id in set(self.repository.get_elements_id(table = "features")["elements"]).difference(features):
                feature = self.repository.get_element(table = "features", element_id = feature_id)
                feature_item = QTreeWidgetItem([feature["element"]["name"], str(feature_id), "features"])
                item.addChild(feature_item)
            self.treeWidget.addTopLevelItem(item)
            self.treeWidget.itemDoubleClicked.connect(self.tree_element_clicked)
            self.treeWidget.hideColumn(1)
            self.treeWidget.hideColumn(2)
            self.update()

        except Exception as exception:
            display_error_message(title = "Display feature list error", content = exception)

    def tree_element_clicked(self, item, column_no):
        """
        Call the proper action depending on the element clicked in the Tree view
        :param item: the tree item clicked
        :param column_no: the column number clicked
        :return:
        """
        logger.debug(
            "tree_element_clicked item is \n column 1 '{}'\n column 2 '{}'\n column 3 '{}' ".format(item.text(0),
                                                                                                    item.text(1),
                                                                                                    item.text(2)))
        if item.text(2) == "features":
            self.update_or_display(element_id=item.text(1), table=item.text(2))
        else:
            logger.debug("else")

    def update_or_display(self, element_id=None, table=None):
        """
        Ask whether show the element in the update form or in a view form
        :param element_id:
        :param table:
        :return:
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText('Do you want to update the element?\n Click "Yes" to update, "No" to simply display it.')
        msg.setWindowTitle("Update or Display?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.exec_()
        if msg.clickedButton() == msg.button(QMessageBox.Yes):
            if table == "features":
                self.add_feature(feature_id=element_id)
            else:
                logger.debug("update_or_display else on Yes")
        else:
            logger.debug("update_or_display else on clicked button")

    def add_feature(self, feature_id=None):
        """
        Call the specific adder
        :param feature_id: the feature id
        :return:
        """
        try:
            feature_dialog = FeatureAdder(parent=self, feature_id=feature_id)
            feature_dialog.exec_()
            self.display_element_list()
        except Exception as exception:
            display_error_message(title = "Add feature error", content=exception)

    def on_add_feature(self):
        try:
            button = self.sender()
            if button.text() == "Add Feature":
                self.add_feature()
            elif button.text() == "Update":
                index = self.featureTab.indexAt(button.pos())
                logger.debug(
                    "Row is {}, Get feature id : {}".format(index.row(), self.featureTab.item(index.row(), 0).text()))
                self.add_feature(feature_id=self.featureTab.item(index.row(), 0).text())
        except Exception as exception:
            display_error_message(title="On add feature error", content=exception)

    def on_display_feature(self):
        try:
            button = self.sender()
            index = self.featureTab.indexAt(button.pos())
            display_dialog = DisplayFeatureDialog(parent = self,
                                                  feature_id = int(self.featureTab.item(index.row(), 0).text()))

            display_dialog.exec_()
        except Exception as exception:
            display_error_message(title = "On Display Feature error", content = exception)
