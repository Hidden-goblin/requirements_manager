# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, qApp, QMessageBox, QLineEdit, QPushButton, QTableWidgetItem
from PyQt5 import QtCore
from copy import deepcopy
from app.ui.DataArrayForm import Ui_CreateArrayForm
from app.controller.ArrayWidthAdder import ArrayWidthAdder
from app.static.ui_utilities import display_error_message, list_contains_empty_element
from app.data.TinyDBRepository import TinyDbRepository


class DataArrayAdder(QDialog, Ui_CreateArrayForm):
    def __init__(self, parent = None, example = None, label = "Name"):
        super(DataArrayAdder, self).__init__(parent)
        self.setupUi(self)
        self.column = 0
        self.row = 0
        self.table = TinyDbRepository.create_empty_table()
        self.example = example
        self.name = ""
        self.is_update = False
        self.DataArrayName.setText(label)
        if example is None:
            width_dialog = ArrayWidthAdder(parent = self)
            width_dialog.exec_()
            self.column = width_dialog.width
            print("Width is {}".format(width_dialog.width))
            if self.column == 0:
                display_error_message("No column array error", "The table could not have 0 column to hold data!")
            else:
                self.table['column'] = self.column
                self.display_header()
                self.display_data()
        else:
            self.is_update = True
            self.column = self.example["table"]["column"]
            self.table["headers"] = deepcopy(self.example["table"]["headers"])
            self.table["content"] = deepcopy(self.example["table"]["content"])
            self.table["column"] = self.column
            self.name = self.example["name"]
            self.display_header()
            self.display_data()
        print("End check input")
        self.nameLdt.setText(self.name)
        self.ArrayDataTab.cellChanged.connect(self.update_data)
        self.ArrayHeadersTab.cellChanged.connect(self.update_headers)
        self.addPBtn.clicked.connect(self.add)
        self.resetPBtn.clicked.connect(self.reset)
        self.cancelPBtn.clicked.connect(self.close)
        self.nameLdt.editingFinished.connect(self.on_name_update)

    def add(self):
        try:
            if self.name and not list_contains_empty_element(self.table["headers"]):
                empty = []
                for index in range(len(self.table['content'])):
                    if list_contains_empty_element(self.table['content'][index]):
                        empty.append(index)
                if empty:
                    for item in empty:
                        self.table['content'].pop(item)
                if self.table['content']:
                    self.close()
                else:
                    display_error_message("No content!", "The array content can't be empty!\n Please revise your data.")
            elif list_contains_empty_element(self.table['headers']):
                display_error_message("No headers!", "The array must have headers values")
            else:
                print("Unexpected error")
        except Exception as exception:
            display_error_message(title = "Add array error", content = exception)

    def reset(self):
        try:
            if self.example is not None:
                self.table["headers"] = deepcopy(self.example["table"]["headers"])
                self.table["content"] = deepcopy(self.example["table"]["content"])
                self.name = self.example["name"]
                self.nameLdt.setText(self.name)
            else:
                self.table["headers"] = []
                self.table["content"] = []
                self.name = ""
                self.nameLdt.setText(self.name)
            self.display_header()
            self.display_data()
        except Exception as exception:
            display_error_message(title = "Reset error", content = exception)

    def on_name_update(self):
        self.name = self.nameLdt.text()

    def display_header(self):
        try:
            self.ArrayHeadersTab.setColumnCount(self.column)
            self.ArrayHeadersTab.setRowCount(1)
            for index in range(self.column):
                if self.is_update:
                    item = QTableWidgetItem(self.table['headers'][index])
                else:
                    item = QTableWidgetItem("")
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                self.ArrayHeadersTab.setItem(0, int(index), item)
            self.ArrayHeadersTab.horizontalHeader().hide()
        except Exception as exception:
            display_error_message(title = "Display header error", content = exception)

    def display_data(self):
        try:
            self.ArrayDataTab.cellChanged.disconnect()
        except Exception:
            pass
        try:
            self.ArrayDataTab.setColumnCount(self.column + 2)
            if self.table["content"]:
                self.ArrayDataTab.setRowCount(len(self.table['content']))
                for row_index, row in enumerate(self.table["content"]):
                    for index in range(self.column):
                        item = QTableWidgetItem(row[index])
                        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                        self.ArrayDataTab.setItem(int(row_index), int(index), item)
                    add_new_row = QPushButton("+", self)
                    add_new_row.clicked.connect(self.add_data_row)
                    self.ArrayDataTab.setCellWidget(int(row_index), int(self.column), add_new_row)
                    remove_row = QPushButton("-", self)
                    remove_row.clicked.connect(self.remove_data_row)
                    self.ArrayDataTab.setCellWidget(int(row_index), int(self.column) + 1, remove_row)
            else:
                self.ArrayDataTab.setRowCount(1)
                for index in range(self.column):
                    item = QTableWidgetItem("")
                    item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled)
                    self.ArrayDataTab.setItem(0, int(index), item)
                add_new_row = QPushButton("+", self)
                add_new_row.clicked.connect(self.add_data_row)
                self.ArrayDataTab.setCellWidget(0, int(self.column), add_new_row)
                remove_row = QPushButton("-", self)
                remove_row.clicked.connect(self.remove_data_row)
                self.ArrayDataTab.setCellWidget(0, int(self.column) + 1, remove_row)
            self.ArrayDataTab.cellChanged.connect(self.update_data)
        except Exception as exception:
            display_error_message(title = "Display data error", content = exception)

    def update_data(self, row, column):
        try:
            if len(self.table["content"]) < row:
                print("Table shorter than expected")
            elif len(self.table["content"]) == 0:
                self.table["content"].append(['']*self.column)
                self.table["content"][row][column] = self.ArrayDataTab.item(row, column).text()
            else:
                self.table["content"][row][column] = self.ArrayDataTab.item(row, column).text()
        except Exception as exception:
            display_error_message(title = "Update data error", content = exception)

    def update_headers(self, row, column):
        try:
            if not self.table['headers']:
                self.table['headers'] = ['']*self.column
            self.table['headers'][column] = self.ArrayHeadersTab.item(row, column).text()
        except Exception as exception:
            display_error_message(title = "Update header error", content = exception)

    def add_data_row(self):
        """
        Verify row is not empty and add a new row just after
        :return:
        """
        try:
            button = self.sender()
            index = self.ArrayDataTab.indexAt(button.pos())
            if not self.table["content"]:
                self.table["content"].append(['']*self.column)
            self.table["content"].insert(index.row()+1, [""]*self.column)
            self.display_data()
        except Exception as exception:
            display_error_message(title = "Add data row error", content = exception)

    def remove_data_row(self):
        try:
            if len(self.table["content"]) > 1:
                button = self.sender()
                index = self.ArrayDataTab.indexAt(button.pos())
                self.table["content"].pop(index.row())
                self.display_data()
        except Exception as exception:
            display_error_message(title = "Remove data row error", content = exception)
