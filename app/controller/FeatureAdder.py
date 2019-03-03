# -*- coding: utf-8 -*-
import markdown
import logging
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QFileDialog

from app.controller.GraphCreator import GraphCreator
from app.controller.PictureViewer import PictureViewer
from app.controller.ScenarioAdder import ScenarioAdder
from app.data.TinyDBRepository import TinyDbRepository
from app.data.Generator import ElementGenerator
from app.exceptions.RepositoryException import NonUniqueIDEntry
from app.static.ui_utilities import display_error_message, fill_cmb
from app.static.jira_mardown import JiraMarkdown
from app.ui.FeatureForm import Ui_FeatureForm

logger = logging.getLogger('simpleExample')


class FeatureAdder(QDialog, Ui_FeatureForm):
    def __init__(self, parent=None, feature_id=None, feature_improvement=False):
        super(FeatureAdder, self).__init__(parent)
        print("Init Feature Adder UI")
        self.parent = parent
        self.setupUi(self)
        self.feature_id = feature_id  #The feature db id
        self.current_feature = self.parent.repository.get_empty_element(table="features")  #By default the current feature is empty
        self.current_scenarios = []  #The current scenarios (id,scenario) list
        self.current_attachments = []  #The current attachment id list
        self.scenario_updated = False
        self.is_feature_editable = False
        if feature_id is not None:
            self.is_update = True  #Feature adder in update mode
            self.feature_id = int(feature_id)
        else:
            self.is_update = False  #Feature adder in add mode
        self.clear_form()  #UI is set with default values
        self.resetBtn.clicked.connect(self.clear_form)
        self.cancelBtn.clicked.connect(self.close)
        self.addFeatureBtn.clicked.connect(self.update_feature)
        self.addScenarioBtn.clicked.connect(self.add_scenario)
        self.addAttachmentBtn.clicked.connect(self.add_attachment)
        self.addGraphBtn.clicked.connect(self.add_uml_graph)
        #self.connect(self.featureSummaryTdt, SIGNAL('doubleClicked()'), self.write)
        #self.featureSummaryTdt.doubleClicked.connect(self.write)
        self.editBtn.clicked.connect(self.write)
        self.cancelEditBtn.clicked.connect(self.cancel_writing)
        self.cancelEditBtn.hide()
        if not feature_improvement:
            self.improvementLbl.hide()
            self.improvementTdt.hide()

    def update_feature(self):
        """
        Add or update a feature.

        Get data from the UI and insert/update in the working repository
        :return:
        """
        try:
            #Update Mode
            if self.is_update:
                #Scenario has been updated/added
                if not self.scenario_updated:
                    #Get the existing feature data
                    feature = self.parent.repository.get_element(element_id = self.feature_id, table = "features")[
                        "element"]
                else:
                    #Loop on scenario and add/update scenarios
                    for scenario in self.current_scenarios:
                        if scenario[0] is None:
                            scenario[1]["linked to feature"] = self.feature_id
                            self.parent.repository.add_element(element = scenario[1], table = "scenarios")
                        else:
                            self.parent.repository.update_element(element_id = scenario[0], element = scenario[1],
                                                                  table = "scenarios")
                    #Get the existing feature data with the updated scenarios
                    feature = self.parent.repository.get_element(element_id = self.feature_id, table = "features")[
                        "element"]
                for attachment_id in self.current_attachments:
                    if attachment_id not in feature['attachments']:
                        feature['attachments'].append(attachment_id)
                feature['name'] = self.featureNameLdt.text()
                feature['role'] = self.featureAsLdt.text()
                feature['action'] = self.featureIWantLdt.text()
                feature['benefit'] = self.featureSoThatLdt.text()
                feature['summary'] = self.featureSummaryTdt.toPlainText()
                self.parent.repository.update_element(element = feature, element_id = self.feature_id,
                                                      table = "features")
            #Add Mode
            else:
                #Get empty feature
                feature = self.parent.repository.get_empty_element(table = "features")
                #Fill fields with retrieved data
                feature['name'] = self.featureNameLdt.text()
                feature['role'] = self.featureAsLdt.text()
                feature['action'] = self.featureIWantLdt.text()
                feature['benefit'] = self.featureSoThatLdt.text()
                feature['summary'] = self.featureSummaryTdt.toPlainText()
                #Add in repository
                response = self.parent.repository.add_element(element = feature, table = "features")
                #Add scenarios to the feature
                if len(self.current_scenarios) != 0 and response["code"] == 0:
                    for scenario in self.current_scenarios:
                        scenario[1]["linked to feature"] = response["id"]
                        self.parent.repository.add_element(element = scenario[1], table = "scenarios")
            self.parent.repository_update_signal.emit(True)
            self.close()
        except NonUniqueIDEntry as id_error:
            print(repr(id_error))
            display_error_message(title = "Functionality conflict", content = id_error.message)
        except Exception as exception:
            print(repr(exception))
            display_error_message(title = "Functionality conflict", content = exception)

    def clear_form(self):
        """
        Reset the form to the initial state either in update or add mode.
        :return:
        """
        try:
            if self.is_update:
                self.setWindowTitle("Update feature")
                element = self.parent.repository.get_element(element_id = self.feature_id, table = "features")
                if element["code"] == 0:
                    self.current_feature = element["element"]
                    self.featureNameLdt.setText(self.current_feature['name'])
                    self.featureAsLdt.setText(self.current_feature['role'])
                    self.featureIWantLdt.setText(self.current_feature['action'])
                    self.featureSoThatLdt.setText(self.current_feature['benefit'])
                    self.featureSummaryTdt.setPlainText(self.current_feature['summary'])
                    self.current_scenarios.clear()
                    if self.current_feature['scenarios']:
                        for scenario_id in self.current_feature['scenarios']:
                            self.current_scenarios.append(
                                (scenario_id,
                                 self.parent.repository.get_element(element_id = scenario_id, table = "scenarios")[
                                     "element"]))
                    if self.current_feature['attachments']:
                        for attachment_id in self.current_feature['attachments']:
                            self.current_attachments.append(attachment_id)
                    self.refresh_scenario_tab()
                    self.refresh_attachment_tab()
                    print("Fill cmb")
                    epics = self.parent.repository.get_elements(table = "epics")
                    if epics["code"] == 0:
                        print(epics["elements"])
                        fill_cmb(
                            values = ElementGenerator.generate_list_element(dictionary_list_input = epics["elements"],
                                                                            display_field = "name"),
                            combobox = self.epicCbx)
                    print("Fill cmb after")
                    if self.current_feature["linked to epic"] is not None:
                        self.epicCbx.setCurrentIndex(self.epicCbx.findData(self.current_feature["linked to epic"]))
                    else:
                        self.epicCbx.setCurrentIndex(0)
                    self.addFeatureBtn.setText("Update")
                else:
                    #TODO handle the error with a message box
                    logger.error(msg = element["message"])
            else:
                self.featureNameLdt.setText("")
                self.featureAsLdt.setText("")
                self.featureIWantLdt.setText("")
                self.featureSoThatLdt.setText("")
                self.featureSummaryTdt.setPlainText("")
                self.current_scenarios = []
                self.current_attachments = []
                self.scenariosTab.clear()
                self.scenariosTab.setColumnCount(0)
                self.scenariosTab.setRowCount(0)
                self.attachmentsTab.clear()
                self.attachmentsTab.setColumnCount(0)
                self.attachmentsTab.setRowCount(0)
                self.setWindowTitle("Add functionality")
            self.scenariosTab.horizontalHeader().hide()
            self.scenariosTab.verticalHeader().hide()
            self.attachmentsTab.horizontalHeader().hide()
            self.attachmentsTab.verticalHeader().hide()
            self.scenario_updated = False
        except Exception as exception:
            display_error_message(title = "Clear form conflict", content = exception)

    def add_scenario(self):
        """
        Add a new scenario
        TODO refactor to include the update action
        :return:
        """
        try:
            scenario_dialog = ScenarioAdder(parent = self)
            scenario_dialog.exec_()
            if scenario_dialog.result:
                self.current_scenarios.append((None, scenario_dialog.result))
                self.scenario_updated = True
                self.refresh_scenario_tab()
        except Exception as exception:
            display_error_message(title = "Add scenario error", content = exception)

    def on_update_scenario(self):
        """
        Action to undertake in order to update a scenario
        TODO refactor to use the add_scenario method
        :return:
        """
        try:
            button = self.sender()
            index = self.scenariosTab.indexAt(button.pos())
            scenario_dialog = ScenarioAdder(parent = self, scenario = self.current_scenarios[int(index.row())][1])
            scenario_dialog.exec_()
            if scenario_dialog.result:
                self.current_scenarios[int(index.row())] = (
                    self.current_scenarios[int(index.row())][0], scenario_dialog.result)
                self.scenario_updated = True
                self.refresh_scenario_tab()
        except Exception as exception:
            display_error_message(title = "On update scenario error", content = exception)

    def refresh_scenario_tab(self):
        """
        Refresh the scenario tab
        :return:
        """
        try:
            self.scenariosTab.clear()
            self.scenariosTab.setColumnCount(2)
            self.scenariosTab.setColumnWidth(0, 900)
            self.scenariosTab.setRowCount(len(self.current_scenarios))
            for index, scenario in enumerate(self.current_scenarios):
                self.scenariosTab.setItem(index, 0, QTableWidgetItem(str(scenario[1]['name'])))
                update_button = QPushButton("Update", self)
                update_button.clicked.connect(self.on_update_scenario)
                self.scenariosTab.setCellWidget(index, 1, update_button)
            self.update()
        except Exception as exception:
            display_error_message(title = "On refresh scenario tab error", content = exception)

    def add_attachment(self):
        """
        Add an attachment
        :return:
        """
        print("Add attachment")
        picture_name = QFileDialog.getOpenFileName(self, 'New File', "", "Text files (*.png)")[0]
        if picture_name:
            attachment_id = self.parent.repository.add_attachment(
                attachment_type = TinyDbRepository.ATTACHMENT_FILE,
                name = picture_name)

            self.current_attachments.append(attachment_id)
            self.refresh_attachment_tab()

    def refresh_attachment_tab(self):
        """"
        Refresh the attachment tab
        """
        try:
            self.attachmentsTab.clear()
            self.attachmentsTab.setColumnCount(4)
            self.attachmentsTab.setColumnWidth(1, 500)
            self.attachmentsTab.setRowCount(len(self.current_attachments))
            for index, attachment_id in enumerate(self.current_attachments):
                attachment = self.parent.repository.get_element(element_id=attachment_id, table="attachments")
                self.attachmentsTab.setItem(index, 0, QTableWidgetItem(str(attachment_id)))
                self.attachmentsTab.setItem(index, 1, QTableWidgetItem(str(attachment["element"]["name"])))
                remove_button = QPushButton("Remove", self)
                remove_button.clicked.connect(self.on_remove_attachment)
                self.attachmentsTab.setCellWidget(index, 2, remove_button)
                if attachment["element"]["type"] == TinyDbRepository.ATTACHMENT_UML:
                    update_button = QPushButton("update", self)
                    update_button.clicked.connect(self.on_update_attachment)
                    self.attachmentsTab.setCellWidget(index, 3, update_button)
                elif attachment["element"]["type"] == TinyDbRepository.ATTACHMENT_FILE:
                    show_button = QPushButton("display", self)
                    show_button.clicked.connect(self.on_display_attachment)
                    self.attachmentsTab.setCellWidget(index, 3, show_button)
            self.attachmentsTab.hideColumn(0)
            self.update()
        except Exception as exception:
            logger.debug(exception)
            display_error_message(title = "On refresh attachment tab error", content = exception)

    def on_remove_attachment(self):
        """
        Action to undertake when removing an attachment
        :return:
        """
        try:
            button = self.sender()
            index = self.attachmentsTab.indexAt(button.pos())
            self.parent.repository.remove_attachment(
                attachment_id = int(self.attachmentsTab.item(int(index.row()), 0).text()),
                feature_id = self.feature_id)
            self.current_attachments.remove(int(self.attachmentsTab.item(int(index.row()), 0).text()))
            self.refresh_attachment_tab()
        except Exception as exception:
            display_error_message(title = "On remove attachment error", content = exception)

    def on_update_attachment(self):
        """
        Action to undertake when updating an attachment
        :return:
        """
        button = self.sender()
        index = self.attachmentsTab.indexAt(button.pos())
        self.add_uml_graph(attachment_id = self.attachmentsTab.item(int(index.row()), 0).text())

    def on_display_attachment(self):
        button = self.sender()
        index = self.attachmentsTab.indexAt(button.pos())
        view = PictureViewer(parent = self,
                             picture_name = "{}{}".format(self.parent.repository.get_attachments_folder(), str(
                                 self.attachmentsTab.item(int(index.row()), 1).text())))
        view.show()

    def add_uml_graph(self, attachment_id = None):
        if attachment_id:
            attachment = self.parent.repository.get_element(element_id=attachment_id,table="attachments")
            uml_creator = GraphCreator(parent = self,
                                       graph_text = attachment["element"]['data'],
                                       graph_name = attachment["element"]['name'],
                                       attachment_folder = self.parent.repository.get_attachments_folder())
        else:
            uml_creator = GraphCreator(parent = self,
                                       graph_text = "",
                                       attachment_folder = self.parent.repository.get_attachments_folder())
        uml_creator.exec_()
        if uml_creator.graph_name and attachment_id:
            self.parent.repository.update_attachment(attachment_id = attachment_id,
                                                     attachment = {'type': TinyDbRepository.ATTACHMENT_UML,
                                                                   'name': uml_creator.graph_name,
                                                                   'data': uml_creator.graph})
        elif uml_creator.graph_name and not attachment_id:
            returned_id = self.parent.repository.add_attachment(attachment_type = TinyDbRepository.ATTACHMENT_UML,
                                                                name = uml_creator.graph_name,
                                                                data = uml_creator.graph)
            self.current_attachments.append(returned_id)
        self.refresh_attachment_tab()

    def write(self):
        """
        Toggle the write ability on the feature summary
        :return:
        """
        if not self.is_feature_editable:
            self.editBtn.setText("Save")
            self.featureSummaryTdt.setReadOnly(False)
            self.is_feature_editable = True
            self.featureSummaryTdt.setPlainText(self.current_feature["summary"])
            self.cancelEditBtn.show()
        else:
            self.editBtn.setText("Edit")
            self.featureSummaryTdt.setReadOnly(True)
            self.is_feature_editable = False
            self.cancelEditBtn.hide()
            self.current_feature["summary"] = self.featureSummaryTdt.toPlainText()
            self.featureSummaryTdt.setHtml(JiraMarkdown.jira_to_html(self.current_feature["summary"]))

    def cancel_writing(self):
        """
        Cancel the actual feature summary updates
        :return:
        """
        if self.is_feature_editable:
            self.editBtn.setText("Edit")
            self.featureSummaryTdt.setReadOnly(True)
            self.is_feature_editable = False
            self.cancelEditBtn.hide()
            self.featureSummaryTdt.setPlainText(self.current_feature["summary"])
            self.featureSummaryTdt.setHtml(JiraMarkdown.jira_to_html(self.current_feature["summary"]))
