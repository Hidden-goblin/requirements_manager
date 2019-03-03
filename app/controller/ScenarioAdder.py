# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, qApp, QMessageBox
from copy import deepcopy
from app.ui.ScenarioForm import Ui_ScenarioForm
from app.controller.StepAdder import StepAdder
from app.controller.DataArrayAdder import DataArrayAdder
from app.static.ui_utilities import array_name_and_update_button
from app.data.TinyDBRepository import TinyDbRepository


class ScenarioAdder(QDialog, Ui_ScenarioForm):
    def __init__(self, parent = None, scenario = None):
        super(ScenarioAdder, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.result = {}
        #list
        if scenario is None:
            self.given_list = []
            self.when_list = []
            self.then_list = []
            self.example_list = []
        else:
            self.given_list = deepcopy(scenario['given'])
            self.when_list = deepcopy(scenario['when'])
            self.then_list = deepcopy(scenario['then'])
            self.example_list = deepcopy(scenario['examples'])
            self.scenarioNameLdt.insert(scenario['name'])
            self.refresh()

        #Given buttons
        self.GivenAddStepBtn.clicked.connect(lambda: self.add_a_step(list_to_update = self.given_list))
        self.GivenAddDataBtn.clicked.connect(lambda: self.add_a_data_array(list_to_update = self.given_list))
        self.GivenRemoveBtn.clicked.connect(lambda: self.remove(list_to_update = self.given_list))
        #When buttons
        self.WhenAddStepBtn.clicked.connect(lambda: self.add_a_step(list_to_update = self.when_list))
        self.WhenAddDataBtn.clicked.connect(lambda: self.add_a_data_array(list_to_update = self.when_list))
        self.WhenRemoveBtn.clicked.connect(lambda: self.remove(list_to_update = self.when_list))
        #Then buttons
        self.ThenAddStepBtn.clicked.connect(lambda: self.add_a_step(list_to_update = self.then_list))
        self.ThenAddDataBtn.clicked.connect(lambda: self.add_a_data_array(list_to_update = self.then_list))
        self.ThenRemoveBtn.clicked.connect(lambda: self.remove(list_to_update = self.then_list))
        #Example button
        self.AddExampleBtn.clicked.connect(lambda: self.add_a_data_array(list_to_update = self.example_list))
        self.ExampleRemoveBtn.clicked.connect(lambda: self.remove(list_to_update = self.example_list))

        self.AddScenarioBtn.clicked.connect(self.add_scenario)
        self.CancelBtn.clicked.connect(self.on_cancel)
        #Remove tab headers
        self.GivenTab.horizontalHeader().hide()
        self.WhenTab.horizontalHeader().hide()
        self.ThenTab.horizontalHeader().hide()
        self.ExampleTab.horizontalHeader().hide()

    def on_cancel(self):
        self.result = {}
        self.close()

    def add_a_step(self, list_to_update = None, item_id = None):
        add_step_display = StepAdder(parent = self, list_to_add = list_to_update, update_index = item_id)
        add_step_display.exec_()
        self.refresh()

    def add_a_data_array(self, list_to_update = None, item_id = None):
        print("Add an data array")
        # todo add the label update
        if item_id is not None:
            data_array_dialog = DataArrayAdder(parent = self, example = list_to_update[int(item_id)], label = "Step description")
        else:
            data_array_dialog = DataArrayAdder(parent = self, label = "Step description")

        if data_array_dialog.column != 0:
            data_array_dialog.exec_()
            if item_id is not None:
                list_to_update[int(item_id)] = TinyDbRepository.create_example(name = data_array_dialog.name,
                                                                               table = data_array_dialog.table)
            else:
                list_to_update.append(TinyDbRepository.create_example(name = data_array_dialog.name,
                                                                      table = data_array_dialog.table))
        else:
            print("Don't display array")
        self.refresh()

    def remove(self, list_to_update = None, item_id = None):
        print("Remove last")
        if item_id is not None:
            list_to_update.pop(int(item_id))
        else:
            list_to_update.pop()
        self.refresh()

    def refresh(self):
        array_name_and_update_button(table_widget = self.GivenTab, linked_function = self.update_given_step, parent = self,
                                     list_to_display = self.given_list)
        array_name_and_update_button(table_widget = self.WhenTab, linked_function = self.update_when_step, parent = self,
                                     list_to_display = self.when_list)
        array_name_and_update_button(table_widget = self.ThenTab, linked_function = self.update_then_step, parent = self,
                                     list_to_display = self.then_list)
        array_name_and_update_button(table_widget = self.ExampleTab, linked_function = self.update_example, parent = self,
                                     list_to_display = self.example_list)

    def on_update(self, element_index = None, list_to_update = None):
        self.add_a_step(list_to_update = list_to_update, item_id = element_index)

    def update_given_step(self):
        button = self.sender()
        index = self.GivenTab.indexAt(button.pos())
        if index:
            element_index = self.GivenTab.item(index.row(), 0).text()
            if isinstance(self.given_list[int(element_index)], str):
                self.add_a_step(list_to_update = self.given_list, item_id = element_index)
            else:
                self.add_a_data_array(list_to_update = self.given_list, item_id = element_index)
        else:
            print("Error")
    
    def update_when_step(self):
        button = self.sender()
        index = self.WhenTab.indexAt(button.pos())
        if index:
            element_index = self.WhenTab.item(index.row(), 0).text()
            if isinstance(self.when_list[int(element_index)], str):
                self.add_a_step(list_to_update = self.when_list, item_id = element_index)
            else:
                self.add_a_data_array(list_to_update = self.when_list, item_id = element_index)
        else:
            print("Error")
    
    def update_then_step(self):
        button = self.sender()
        index = self.ThenTab.indexAt(button.pos())
        if index:
            element_index = self.ThenTab.item(index.row(), 0).text()
            if isinstance(self.then_list[int(element_index)], str):
                self.add_a_step(list_to_update = self.then_list, item_id = element_index)
            else:
                self.add_a_data_array(list_to_update = self.then_list, item_id = element_index)
        else:
            print("Error")
    
    def update_example(self):
        button = self.sender()
        index = self.ExampleTab.indexAt(button.pos())
        if index:
            element_index = self.ThenTab.item(index.row(), 0).text()
            self.add_a_data_array(list_to_update = self.example_list, item_id = element_index)
        else:
            print("Error")

    def add_scenario(self):
        self.result = TinyDbRepository.create_scenario(name = self.scenarioNameLdt.text(), given = self.given_list,
                                                       when = self.when_list, then = self.then_list,
                                                       examples = self.example_list)
        self.close()
