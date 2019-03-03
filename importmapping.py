# -*- coding: utf-8 -*-
from MappingForm import Ui_MappingForm
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, qApp, QMessageBox


class ImportMapping(QDialog, Ui_MappingForm):
    def __init__(self, parent = None):
        print("Constructor start")
        super(ImportMapping, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        print("Constructor start")
        self.okBtn.clicked.connect(self.on_ok)
        self.cancelBtn.clicked.connect(self.close)

    def on_ok(self):
        self.parent.mapping = {
            "functionality ID": {'row': self.fctIDSpin.value(),
                                 'replacement text': self.fctIDRepLdt.text(),
                                 'header': self.fctIDHeaderLdt.text()},
            "functionality Name": {'row': self.fctNameSpin.value(),
                                   'replacement text': self.fctNameRepLdt.text(),
                                   'header': self.fctNameHeaderLdt.text()},
            "functionality Channel": {'row': self.fctChannelSpin.value(),
                                      'replacement text': self.fctChannelRepLdt.text(),
                                      'header': self.fctChannelHeaderLdt.text()},
            "functionality Description": {'row': self.fctDescriptionSpin.value(),
                                          'replacement text': self.fctDescriptionRepLdt.text(),
                                          'header': self.fctDescriptionHeaderLdt.text()},
            "functionality Criticality": {'row': self.fctCriticalitySpin.value(),
                                          'replacement text': self.fctCriticalityRepLdt.text(),
                                          'header': self.fctCriticalityHeaderLdt.text()},
            "functionality Usage": {'row': self.fctUsageSpin.value(),
                                    'replacement text': self.fctUsageRepLdt.text(),
                                    'header': self.fctUsageHeaderLdt.text()},
            "use case ID": {'row': self.ucIDSpin.value(),
                            'replacement text': self.ucIDRepLdt.text(),
                            'header': self.ucIDHeaderLdt.text()},
            "use case Name": {'row': self.ucNameSpin.value(),
                              'replacement text': self.ucNameRepLdt.text(),
                              'header': self.ucNameHeaderLdt.text()},
            "use case Description": {'row': self.ucDescriptionSpin.value(),
                                     'replacement text': self.ucDescriptionRepLdt.text(),
                                     'header': self.ucDescriptionHeaderLdt.text()},
            "use case Pre requisite": {'row': self.ucPreSpin.value(),
                                       'replacement text': self.ucPreRepLdt.text(),
                                       'header': self.ucPreHeaderLdt.text()},
            "use case Steps": {'row': self.ucStepsSpin.value(),
                               'replacement text': self.ucStepsRepLdt.text(),
                               'header': self.ucStepsHeaderLdt.text()},
            "use case Post condition": {'row': self.ucPostSpin.value(),
                                        'replacement text': self.ucPostRepLdt.text(),
                                        'header': self.ucPostHeaderLdt.text()},
            "use case Exceptional": {'row': self.ucExcpSpin.value(),
                                     'replacement text': self.ucExcpRepLdt.text(),
                                     'header': self.ucExcpHeaderLdt.text()},
            "use case Require": {'row': self.ucRequireSpin.value(),
                                 'replacement text': self.ucRequireRepLdt.text(),
                                 'header': self.ucRequireHeaderLdt.text()},
            "use case Type": {'row': self.ucTypeSpin.value(),
                              'replacement text': self.ucTypeRepLdt.text(),
                              'header': self.ucTypeHeaderLdt.text()},
            "use case Critical": {'row': self.ucCriticalSpin.value(),
                                  'replacement text': self.ucCriticalRepLdt.text(),
                                  'header': self.ucCriticalHeaderLdt.text()},
            "use case Average": {'row': self.ucAverageSpin.value(),
                                 'replacement text': self.ucAverageRepLdt.text(),
                                 'header': self.ucAverageHeaderLdt.text()},
            "use case Automated": {'row': self.ucAutomatedSpin.value(),
                                   'replacement text': self.ucAutomatedRepLdt.text(),
                                   'header': self.ucAutomatedHeaderLdt.text()},
            "use case Automatable": {'row': self.ucAutomatableSpin.value(),
                                     'replacement text': self.ucAutomatableRepLdt.text(),
                                     'header': self.ucAutomatableHeaderLdt.text()},
            "use case Release": {'row': self.ucReleaseSpin.value(),
                                 'replacement text': self.ucReleaseRepLdt.text(),
                                 'header': self.ucReleaseHeaderLdt.text()},
            "use case Functionality": {'row': self.ucFunctionalitySpin.value(),
                                       'replacement text': self.ucFunctionalityRepLdt.text(),
                                       'header': self.ucFunctionalityHeaderLdt.text()},
            "use case Automaton": {'row': self.ucAutomatonSpin.value(),
                                   'replacement text': self.ucAutomatonRepLdt.text(),
                                   'header': self.ucAutomatonHeaderLdt.text()},
            "header row": self.headerRowSpin.value(),
            "data row": self.firstDataRowSpin.value(),
            "functionality on same sheet": True,
            "functionality repeated": False
            }
        self.close()
