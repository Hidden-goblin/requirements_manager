# -*- coding: utf-8 -*-
"""
Provide common ui utilities
"""
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QComboBox, QMessageBox, QTableWidgetItem, QPushButton


def fill_cmb(values, combobox):
    """Insert in the combobox the text/data.

        Arguments:
           values -- a list of pair (displayed text, data)
           combobox -- combobox object
    """
    for pos, item in enumerate(values):
        combobox.insertItem(pos, str(item[0]), item[1])
    combobox.insertItem(-1, "None selected", None)


def add_value_in_combobox(combobox, text_title, text_input):
    """Insert a value in a combobox. This is a workaround for the "editable" QComboBox option.

        Arguments:
            combobox -- the combobox reference
            text_title -- The dialog window title
            text_input -- The input line title
    """
    (text, is_ok_pressed) = QInputDialog.getText(None, text_title, text_input, QLineEdit.Normal, "")

    if is_ok_pressed:
        combobox.insertItem(combobox.count()+1, text, text)


def not_in_list(list_of_dictionary, key, value):
    """Return True if one item has the (key: value) element."""
    try:
        if value:
            return value not in [item[key] for item in list_of_dictionary]
        elif value == 0:
            return 0 not in [item[key] for item in list_of_dictionary]
        else:
            return False
    except KeyError as keyerror:
        print("'not_in_list' throw {}".format(keyerror))
    except Exception as exception:
        print("'not_in_list' throw {}".format(exception))


def display_message(title = "", content = ""):
    """Pops a message box which is a "display only" data"""
    msg = QMessageBox()
    msg.setTextFormat(1)
    msg.setWindowTitle(title)
    msg.setText(content)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def display_error_message(title = "", content = ""):
    msg = QMessageBox()
    msg.setTextFormat(1)
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle(title)
    msg.setText(content)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def array_name_and_update_button(table_widget = None, linked_function = None, list_to_display = None, parent = None):
    table_widget.clear()
    table_widget.setColumnCount(3)
    table_widget.setRowCount(len(list_to_display))
    for index, element in enumerate(list_to_display):
        table_widget.setItem(index, 0, QTableWidgetItem(str(index)))
        if isinstance(element, str):
            table_widget.setItem(index, 1, QTableWidgetItem(element))
        else:
            table_widget.setItem(index, 1, QTableWidgetItem(element['name']))
        update_button = QPushButton("Update", parent)
        update_button.clicked.connect(linked_function)
        table_widget.setCellWidget(index, 2, update_button)
    table_widget.hideColumn(0)
    parent.update()


def list_contains_empty_element(list_to_check = None):
    if list_to_check is None:
        print("No argument")
    elif not list_to_check:
        pass
    else:
        contain_empty_elem = True
        for elem in list_to_check:
            if elem:
                contain_empty_elem = False
                break
        return contain_empty_elem
