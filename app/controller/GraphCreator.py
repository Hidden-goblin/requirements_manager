# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QFileDialog
from app.ui.GraphFrom import Ui_GraphForm
from os import remove
from os.path import isfile
from app.static.generator_utilities import generate_plantuml_graph


class GraphCreator(QDialog, Ui_GraphForm):
    """
    Display and control the Graph Creator screen
    """

    def __init__(self, parent = None, graph_text = None, graph_name = None, attachment_folder = None):
        super(GraphCreator, self).__init__(parent)
        print("Init graph creator")
        print("Graph name is {}".format(graph_name))
        self.parent = parent
        self.setupUi(self)
        self.graph_name = graph_name
        if attachment_folder and not graph_name:
            self.file_graph_name = "UML_temp" #"{}{}".format(attachment_folder, "UML_temp.txt")
        elif attachment_folder and graph_name:
            self.graphNameLdt.setText(graph_name)
            self.file_graph_name = "{}".format(graph_name.replace(" ", "")) #"{}{}{}".format(attachment_folder, graph_name.replace(" ", ""), ".txt")
        else:
            raise Exception("Can't create temp files")
        self.graph = graph_text
        self.attachment_folder = attachment_folder
        self.inputGraphTdt.setPlainText(self.graph)
        self.inputGraphTdt.launch_update.connect(self.generate_picture)
        self.updateBtn.clicked.connect(self.on_update)
        self.closeBtn.clicked.connect(self.on_close)
        if graph_text is not None:
            self.generate_picture()
        self.refresh()

    def on_update(self):
        """
        Implement the actions done when "Update" button is clicked
        :return:
        """
        filename = "{}{}".format(self.attachment_folder, self.file_graph_name)
        if isfile("{}.txt".format(filename)):
            remove("{}.txt".format(filename))
        if isfile("{}.png".format(filename)):
            remove("{}.png".format(filename))
        self.graph = self.inputGraphTdt.toPlainText()
        self.graph_name = self.graphNameLdt.text()
        del filename
        self.close()

    def on_close(self):
        """
        Implement the actions done when "Close" button is clicked
        :return:
        """
        filename = "{}{}".format(self.attachment_folder, self.file_graph_name)
        if isfile("{}.txt".format(filename)):
            remove("{}.txt".format(filename))
        if isfile("{}.png".format(filename)):
            remove("{}.png".format(filename))
        del filename
        self.graph = self.inputGraphTdt.toPlainText()
        self.graph_name = None
        self.close()

    def refresh(self):
        pass

    def generate_picture(self):
        """
        Generate the graph picture related to the given graph description
        :return:
        """
        try:
            print("Generate picture")
            out_file_name = generate_plantuml_graph(graph_name = self.file_graph_name, graph_data = self.inputGraphTdt.toPlainText(),
                                                    attachment_folder = self.attachment_folder)
            self.viewGraphTdt.clear()
            print(out_file_name)
            self.viewGraphTdt.setHtml("<img src='{}' >".format(out_file_name))
        except Exception as exception:
            self.viewGraphTdt.setHtml("<h1>Error!</h1> <b> Can't generate graph view<br>{}".format(exception))
