# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, qApp, QMessageBox, QTableWidgetItem, QPushButton
from app.ui.DisplayFeatureForm import Ui_DisplayFeatureForm
from app.static.ui_utilities import display_error_message
from app.static.generator_utilities import generate_plantuml_graph, generate_cucumber_scenario_body
from app.data.TinyDBRepository import TinyDbRepository


class DisplayFeatureDialog(QDialog, Ui_DisplayFeatureForm):
    def __init__(self, parent = None, feature_id = None):
        super(DisplayFeatureDialog, self).__init__(parent)
        print("Init Display Feature UI")
        self.parent = parent
        self.setupUi(self)
        self.feature_id = feature_id
        self.pushToJiraBtn.clicked.connect(self.push_to_jira)
        self.text = self.parent.repository.display_feature(feature_id = feature_id, is_html_output = True)
        self.jira_text = self.parent.repository.display_feature(feature_id = feature_id, is_jira_output = True)
        self.featureText.setHtml(self.text)
        self.closeBtn.clicked.connect(self.close)

    def push_to_jira(self):
        print("Push to jira\n{}".format(self.jira_text))
        if self.parent.jira is not None:
            feature = self.parent.repository.get_feature(feature_id = self.feature_id)
            if feature["current foreign id"]:
                self.parent.repository.update_feature_value(feature_id = self.feature_id,
                                                            feature_key = "status",
                                                            key_value = self.parent.jira.get_issue_status(
                                                                issue_key = feature["current foreign id"]))
            if feature["status"] is None:
                response = self.parent.jira.create_story(title = feature["name"],
                                                         description = feature["summary"],
                                                         actor = feature["role"],
                                                         action = feature["action"],
                                                         benefit = feature["benefit"])
                self.parent.repository.update_feature_value(feature_id = self.feature_id,
                                                            feature_key = "current foreign id",
                                                            key_value = response.json()["key"])
                self.parent.repository.update_feature_value(feature_id = self.feature_id,
                                                            feature_key = "status",
                                                            key_value = "To Do")
                for attachment_id in feature["attachments"]:
                    attachment = self.parent.repository.get_attachment(attachment_id = attachment_id)
                    if attachment["type"] == TinyDbRepository.ATTACHMENT_FILE:
                        print("Attachment file")
                        response = self.parent.jira.add_attachments_to_issue(
                            issue_key = self.parent.repository.get_feature(feature_id = self.feature_id,
                                                                           feature_key = "current foreign id"),
                            file_name = "{}{}".format(self.parent.repository.get_attachments_folder(),
                                                      attachment["name"]))
                        print(response.status_code)
                    elif attachment["type"] == TinyDbRepository.ATTACHMENT_UML:
                        file_name = generate_plantuml_graph(graph_name = attachment["name"],
                                                            graph_data = attachment["data"],
                                                            attachment_folder = self.parent.repository.get_attachments_folder())
                        response = self.parent.jira.add_attachments_to_issue(
                            issue_key = self.parent.repository.get_feature(feature_id = self.feature_id,
                                                                           feature_key = "current foreign id"),
                            file_name = file_name)
                        print(response.status_code)
                    else:
                        print("Unknown attachment type")

                for scenario_id in feature["scenarios"]:
                    scenario = self.parent.repository.get_scenario(scenario_id = scenario_id)
                    if scenario["examples"]:
                        test_type = "Scenario"
                    else:
                        test_type = "Scenario Outline"

                    response = self.parent.jira.add_test(
                        story_key = self.parent.repository.get_feature(feature_id = self.feature_id,
                                                                       feature_key = "current foreign id"),
                        test_description = generate_cucumber_scenario_body(given = scenario["given"],
                                                                           when = scenario["when"],
                                                                           then = scenario["then"],
                                                                           examples = scenario["examples"]),
                        test_name = scenario["name"],
                        test_type = test_type)
                    self.parent.repository.update_scenario_value(scenario_id = scenario_id,
                                                                 scenario_key = "current foreign id",
                                                                 key_value = response[1])

                #Todo Add test and attachments
            elif feature["status"] == "To Do":
                response = self.parent.jira.update_story(issue_key = feature["current foreign id"],
                                                         title = feature["name"],
                                                         description = feature["summary"],
                                                         actor = feature["role"],
                                                         action = feature["action"],
                                                         benefit = feature["benefit"])
                for scenario_id in feature["scenarios"]:
                    scenario = self.parent.repository.get_scenario(scenario_id = scenario_id)
                    if scenario["examples"]:
                        test_type = "Scenario"
                    else:
                        test_type = "Scenario Outline"

                    if scenario["current foreign id"]:
                        response = self.parent.jira.update_test(test_key = scenario["current foreign id"],
                                                                test_description = generate_cucumber_scenario_body(
                                                                    given = scenario["given"],
                                                                    when = scenario["when"],
                                                                    then = scenario["then"],
                                                                    examples = scenario["examples"]),
                                                                test_name = scenario["name"],
                                                                test_type = test_type
                                                                )
                    else:
                        response = self.parent.jira.add_test(
                            story_key = self.parent.repository.get_feature(feature_id = self.feature_id,
                                                                           feature_key = "current foreign id"),
                            test_description = generate_cucumber_scenario_body(given = scenario["given"],
                                                                               when = scenario["when"],
                                                                               then = scenario["then"],
                                                                               examples = scenario["examples"]),
                            test_name = scenario["name"],
                            test_type = test_type)
                        self.parent.repository.update_scenario_value(scenario_id = scenario_id,
                                                                     scenario_key = "current foreign id",
                                                                     key_value = response[1])
                    # Delete attachments
                    response = self.parent.jira.delete_attachments(issue_key = feature["current foreign id"])

                    # Recreate attachments
                    for attachment_id in feature["attachments"]:
                        attachment = self.parent.repository.get_attachment(attachment_id = attachment_id)
                        if attachment["type"] == TinyDbRepository.ATTACHMENT_FILE:
                            print("Attachment file")
                            response = self.parent.jira.add_attachments_to_issue(
                                issue_key = self.parent.repository.get_feature(feature_id = self.feature_id,
                                                                               feature_key = "current foreign id"),
                                file_name = "{}{}".format(self.parent.repository.get_attachments_folder(),
                                                          attachment["name"]))
                            print(response.status_code)
                        elif attachment["type"] == TinyDbRepository.ATTACHMENT_UML:
                            file_name = generate_plantuml_graph(graph_name = attachment["name"],
                                                                graph_data = attachment["data"],
                                                                attachment_folder = self.parent.repository.get_attachments_folder())
                            response = self.parent.jira.add_attachments_to_issue(
                                issue_key = self.parent.repository.get_feature(feature_id = self.feature_id,
                                                                               feature_key = "current foreign id"),
                                file_name = file_name)
                            print(response.status_code)
                        else:
                            print("Unknown attachment type")
            else:
                #Todo Create improvement and add link, test and attachments
                print("another")
        else:
            display_error_message(title = "Permission denied",
                                  content = "You're not authentified on Jira.\n Please connect")
