# -*- coding: utf-8 -*-
import tempfile
import logging
import html
import zipfile
import json
from tinydb import TinyDB
from tinydb.operations import set as tinyset
from shutil import copyfile, make_archive, rmtree
from os import remove as os_remove, sep, makedirs, rename
from os.path import isfile, basename, exists
from zipfile import ZipFile
from app.data.irepository import IRepository
from app.controller.Validator import Validator
from app.data.Generator import ElementGenerator

"""
Implement the IRepository interface

contains 
"""

logger = logging.getLogger('simpleExample')


class TinyDbRepository(IRepository):
    #ATTACHMENT_FILE = "file"
    #ATTACHMENT_UML = "uml"

    def __init__(self, file_name = None):
        """

        :param file_name:
        """
        super().__init__(file_name)
        logger.debug("TinyDbRepository constructor")
        self.__repository = {}
        # self.__feature_keys = ["name", "role", "action", "benefit", "summary", "business value", "status",
        #                        "current foreign id", "past foreign ids", "scenarios", "attachments", "epic"]
        # self.__scenario_keys = ["name", "given", "when", "then", "examples", "linked to feature", "status",
        #                         "current foreign id", "past foreign ids"]
        # self.__attachment_keys = ["type", "name", "data"]
        # self.__settings_keys = ["project_id", "end_point"]

        if file_name is not None:
            self.__repository["name"] = file_name
            self.__repository["folder"] = "{0}{1}USMAN{1}{2}{1}".format(tempfile.gettempdir(),
                                                                        sep,
                                                                        basename(file_name).split(".")[0])
            if not exists(self.__repository["folder"]):
                makedirs(self.__repository["folder"])

            self.__repository["working"] = self.__repository["folder"] + basename(file_name)
            self.__repository["attachments"] = self.__repository["folder"] + "attachments" + sep

            if isfile(file_name):
                #Legacy behaviour#
                #Check if file is archive:  [Yes] --> unzip to dedicated temp folder
                #                           [No]  --> create temp folder + replace file with archive one
                if zipfile.is_zipfile(file_name):
                    with ZipFile(file_name) as repository_zip:
                        repository_zip.extractall(path = self.__repository["folder"])
                else:
                    copyfile(self.__repository["name"], self.__repository["working"])
                    if not exists(self.__repository["attachments"]):
                        makedirs(self.__repository["attachments"])
                    make_archive(base_name = file_name, root_dir = self.__repository["folder"], format = "zip")
            else:
                if not exists(self.__repository["attachments"]):
                    makedirs(self.__repository["attachments"])

            self.__repository["object"] = TinyDB(self.__repository["working"])
            self.__repository["tables"] = {}
            with open("app/resources/db_schema.json") as db_schema:
                self.__db_schema = json.load(db_schema)

            with open("app/resources/db_linkto.json") as db_linkto:
                self.__db_linkto = json.load(db_linkto)

            for key in self.__db_schema.keys():
                self.__repository["tables"][key] = self.__repository["object"].table(key)

            self.save_repository()

            self.check_keys()
            print("Repository successfully created")
        else:
            raise Exception("File name can't be empty")

    def get_repository_name(self):
        return self.__repository['name']

    def get_working_repository_name(self):
        return self.__repository['working']

    def save_repository(self):
        """
        Save the repository to the given name file.

        It remove the previous file and get the new one from the working directory.
        :return: boolean
        """
        try:
            if isfile(self.__repository["name"]):
                os_remove(self.__repository["name"])

            make_archive(base_name = self.__repository["name"], root_dir = self.__repository["folder"], format = "zip")
            rename(self.__repository["name"] + ".zip", self.__repository["name"])
            return True
        except Exception as e:
            print(format(e))
            return False

    def close_repository(self, save = False):
        """"
        Save the repository to the given name file if asked and remove all files in the working directory (cleaning)

        It calls the save_repository method
        """
        try:
            if save:
                if not self.save_repository():
                    return False
            self.__repository["object"].close()

            if exists(self.__repository["folder"]):
                rmtree(self.__repository["folder"])

            del self.__repository
            del self.__db_schema
            del self.__db_linkto
            return True
        except Exception as e:
            print(format(e))
            return False

    # @staticmethod
    # def create_empty_feature():
    #     """
    #
    #     :return:
    #     """
    #     return {"name": "",
    #             "role": "",
    #             "action": "",
    #             "benefit": "",
    #             "summary": "",
    #             "business value": "",
    #             "status": "",
    #             "epic": "",
    #             "current foreign id": "",
    #             "past foreign ids": [],
    #             "scenarios": [],
    #             "attachments": []}
    #
    # @staticmethod
    # def create_feature(name = None, role = None, action = None, benefit = None, summary = None, business_value = 0,
    #                    status = None, current_foreign_id = None, past_foreign_ids = None, linked_scenarios = None,
    #                    attachments = None):
    #     """
    #
    #     :param attachments:
    #     :param name:
    #     :param role:
    #     :param action:
    #     :param benefit:
    #     :param summary:
    #     :param business_value:
    #     :param status:
    #     :param current_foreign_id:
    #     :param past_foreign_ids:
    #     :param linked_scenarios:
    #     :return:
    #     """
    #     if name is None or role is None or action is None or benefit is None:
    #         raise Exception("feature must have a role, an action and a benefit")
    #     else:
    #         return {"name": name,
    #                 "role": role,
    #                 "action": action,
    #                 "benefit": benefit,
    #                 "summary": summary,
    #                 "business value": business_value,
    #                 "status": status,
    #                 "current foreign id": current_foreign_id,
    #                 "past foreign ids": past_foreign_ids,
    #                 "scenarios": linked_scenarios,
    #                 "attachments": attachments}
    #
    # @staticmethod
    # def create_scenario(name = None, given = None, when = None, then = None, examples = None, feature_id = None):
    #     """
    #
    #     :param name:
    #     :param given:
    #     :param when:
    #     :param then:
    #     :param examples:
    #     :param feature_id:
    #     :return:
    #     """
    #     if given and when and then and name is not None:
    #         return {"name": name,
    #                 "given": given,
    #                 "when": when,
    #                 "then": then,
    #                 "examples": examples,
    #                 "linked to feature": feature_id}
    #     else:
    #         raise Exception("No scenario created")
    #
    # @staticmethod
    # def create_table(column_number = 0, headers = None, content = None):
    #     """
    #
    #     :param column_number:
    #     :param headers:
    #     :param content:
    #     :return:
    #     """
    #     if column_number == 0:
    #         raise Exception("Can't create an table with no column")
    #     elif column_number != len(headers):
    #         raise Exception("Declared number of column doesn't match the headers")
    #     elif len(content) == 0:
    #         raise Exception("Empty table is not allowed")
    #     elif all(len(row) == column_number for row in content):
    #         return {"column": column_number,
    #                 "headers": headers,
    #                 "content": content}
    #     else:
    #         raise Exception("Unexpected error creating table")
    #
    # @staticmethod
    # def create_empty_table():
    #     """
    #
    #     :return:
    #     """
    #     return {"column": 0,
    #             "headers": [],
    #             "content": []}
    #
    # @staticmethod
    # def create_example(name = None, table = None):
    #     """
    #
    #     :param name:
    #     :param table:
    #     :return:
    #     """
    #     if name is not None and table is not None:
    #         return {'name': name,
    #                 'table': table}
    #     else:
    #         raise Exception("Error creating example")

    def check_keys(self):
        """

        :return:
        """
        for table in self.__db_schema.keys():
            for element in self.__repository["tables"][table].all():
                diff = (set(self.__db_schema[table].keys())).difference(element.keys())
                if diff:
                    for key in diff:
                        self.update_element(element_id = element.doc_id, element_key = key, element_value = None,
                                            table = table)
        # for feature in self.__features.all():
        #     diff = (set(self.__feature_keys)).difference(feature.keys())
        #     if diff:
        #         for key in diff:
        #             self.update_feature_value(feature_id = feature.doc_id, feature_key = key, key_value = None)
        #
        # for scenario in self.__scenarios.all():
        #     diff = (set(self.__scenario_keys)).difference(scenario.keys())
        #     if diff:
        #         for key in diff:
        #             self.__scenarios.update(tinyset(key, None), doc_ids = [scenario.doc_id, ])

    def add_element(self, element = None, table = None, file_name = None):
        if table:
            #Insert element in table
            valid = Validator.validate(element = element, schema = self.__db_schema[table])
            if (valid["code"] == 0 or valid["code"] == 1) and not file_name:  #Non-attachment item
                #Add into table
                key = self.__repository["tables"][table].insert(valid["element"])
            elif (valid["code"] == 0 or valid["code"] == 1) and file_name:  #Attachment item
                #Save file
                save = self.__add_file(name = file_name)
                if save['code'] == 0:
                    #Add into table
                    key = self.__repository["tables"][table].insert(valid["element"])
                else:
                    return save
            else:
                return {"code": 3,
                        "message": valid["message"]}
            #check the link dependencies
            error_messages = ""
            if self.__db_linkto["one-one"][table].keys():
                #Update the dependencies
                for link in self.__db_linkto["one-one"][table]:
                    #Check if there is link data
                    if valid["element"][link] is not None and valid["element"][link]:
                        #Get the parent one-many list
                        attached_to = self.get_element(element_id = valid["element"][link],
                                                       table = self.__db_linkto["one-one"][table][link][0],
                                                       keys = [self.__db_linkto["one-one"][table][link][1]])
                        if attached_to["code"] == 0:  #List retrieved
                            attached_to["element"].append(key)  #Update the list
                            self.update_element(element_id = valid["element"][link],
                                                element_key = self.__db_linkto["one-one"][table][link][1],
                                                element_value = attached_to["element"],
                                                table = self.__db_linkto["one-one"][table][link][
                                                0])  #Update the parent element with the new list
                        else:
                            error_messages = "{}\n{}".format(error_messages, attached_to["message"])
            if error_messages:
                return {"code": 1,
                        "message": error_messages}
            else:
                return {"code": 0,
                        "message": "Successful insertion.",
                        "id": key}
        else:
            return {"code": 3,
                    "message": "Can't insert an element into the null table."}

    def get_elements(self, table = None, filtering = None):
        if table:
            if filtering is not None:
                pass  #elements tag will contains the element id
            else:
                return {"code": 0,
                        "elements": self.__repository["tables"][table].all()}
        else:
            return {"code": 3,
                    "message": "Can't get elements from the null table."}

    def get_elements_id(self, table = None):
        if table:
            return {"code": 0,
                    "elements": [element.doc_id for element in self.__repository["tables"][table].all()]}

    def __get_element(self, element_id = None, table = None):
        if table:
            if element_id is not None:
                return {"code": 0,
                        "message": "Success",
                        "element": self.__repository["tables"][table].get(doc_id = int(element_id)),
                        "id": element_id}
            else:
                return {"code": 3,
                        "message": "Can't retrieve an unidentified element. Missing Id"}
        else:
            return {"code": 3,
                    "message": "Can't retrieve element from an unidentified table. Missing table name."}

    def get_element(self, element_id = None, table = None, keys = None):
        if table is not None:
            element = self.__get_element(element_id = element_id, table = table)
            if isinstance(keys, list) and keys and element["code"] == 0:
                fields = dict((key, element["element"][1][key]) for key in keys)
                return {"code": 0,
                        "element": fields,
                        "id": element_id}
            else:
                return element
        else:
            return {"code": 3,
                    "message": "Can't retrieve element's fields from an empty key list. Missing key list."}

    def get_empty_element(self, table = None):
        if table is not None:
            return ElementGenerator.generate_element(self.__db_schema[table])
        else:
            raise TypeError("Table is None")

    def get_attachments_folder(self):
        return self.__repository["attachments"]

    def __update_element(self, element_id = None, element = None, table = None):
        if table:
            if element_id:
                valid = Validator.validate(element = element, schema = self.__db_schema[table])
                if valid["code"] in (0, 1):
                    self.__repository["tables"][table].update(element, doc_ids = [
                        int(element_id), ])  #update method return nothing
                    return {"code": 0,
                            "message": "Update successful."}
                else:
                    return valid
            else:
                return {"code": 3,
                        "message": "Can't update an unknown element. Missing ID"}
        else:
            return {"code": 3,
                    "message": "Can't retrieve element from an unidentified table. Missing table name."}

    def update_element(self, element_id = None, element = None, element_key = None, element_value = None, table = None):
        if table:
            if element_id:
                if element_key and element:
                    return {"code": 3,
                            "message": "Can't update the whole element AND a specific field."}
                elif not element_key and element:
                    return self.__update_element(element_id = element_id, element = element, table = table)
                elif element_key and not element:
                    if (self.__db_schema[table][element_key]["mandatory"] and element_value)\
                            or not self.__db_schema[table][element_key]["mandatory"]:
                        self.__repository["tables"][table].update(tinyset(element_key, element_value),
                                                                  doc_ids = [
                                                                      int(element_id), ])  #update method return nothing
                        return {"code": 0,
                                "message": "Update successful."}
                    else:
                        return {"code": 3,
                                "message": "Can't update element. Missing value for a mandatory field."}

                else:
                    return {"code": 3,
                            "message": "Can't update element. Missing field to update or element."}
            else:
                return {"code": 3,
                        "message": "Can't update an unknown element. Missing ID"}
        else:
            return {"code": 3,
                    "message": "Can't retrieve element from an unidentified table. Missing table name."}

    # def add_feature(self, feature = None):
    #     """
    #
    #     :param feature:
    #     :return:
    #     """
    #     if feature is not None and all(key in feature.keys() for key in self.__feature_keys):
    #         self.__features.insert(feature)
    #     else:
    #         raise Exception("Can't create feature with less than role, action, benefit and summary value")
    #
    # def get_feature(self, feature_id = None, feature_key = None):
    #     """
    #     Retrieve the whole feature or only one key value
    #
    #     :param feature_id:
    #     :param feature_key:
    #     :return:
    #     """
    #     if feature_id is not None:
    #         if feature_key is None:
    #             return self.__features.get(doc_id = int(feature_id))
    #         elif feature_key is not None and feature_key in self.__feature_keys:
    #             return self.__features.get(doc_id = int(feature_id))[feature_key]
    #         else:
    #             raise Exception("feature key is not a valid one")
    #     else:
    #         raise Exception("Missing identifier to retreive the feature")
    #
    # def list_features(self):
    #     """
    #
    #     :return:
    #     """
    #     return [(feature.doc_id,
    #              "As {}, I want to {}, So that {}".format(feature['role'], feature['action'], feature['benefit'])) for
    #             feature in self.__features.all()]
    #
    # def update_feature(self, feature_id = None, new_feature = None):
    #     """
    #
    #     :param feature_id:
    #     :param new_feature:
    #     :return:
    #     """
    #     if feature_id is not None and new_feature is not None:
    #         self.__features.update(new_feature, doc_ids = [int(feature_id), ])
    #     else:
    #         raise Exception("Something wrong happens")
    #
    # def update_feature_value(self, feature_id = None, feature_key = None, key_value = None):
    #     """
    #
    #     :param feature_id:
    #     :param feature_key:
    #     :param key_value:
    #     :return:
    #     """
    #     if feature_id is None or feature_key is None:
    #         raise Exception("Need the feature id to update and the field to update")
    #     elif feature_key not in self.__feature_keys:
    #         raise Exception("feature key is not a feature one")
    #     else:
    #         print("Set {} with value {}".format(feature_key, key_value))
    #         self.__features.update(tinyset(feature_key, key_value), doc_ids = [int(feature_id), ])
    #
    # def display_feature(self, feature_id = None, is_html_output = False, is_jira_output = False):
    #     """
    #
    #     :param is_jira_output:
    #     :param feature_id:
    #     :param is_html_output:
    #     :return:
    #     """
    #     if feature_id is not None:
    #         feature = self.get_feature(feature_id = int(feature_id))
    #         if is_html_output:
    #             text = """<h1>Feature: {}</h1>
    #              <br />
    #               <b>AS</b> {}<br />
    #               <b>I WANT TO</b> {}<br />
    #               <b>SO THAT</b> {}<br />
    #                <h2>Description</h2> {}
    #                 <h2>Scenario(s)</h2>""".format(feature['name'],
    #                                                feature['role'],
    #                                                feature['action'],
    #                                                feature['benefit'],
    #                                                feature['summary'])
    #             for scenario_id in feature['scenarios']:
    #                 text += self.display_scenario(scenario_id = scenario_id, is_html_output = is_html_output)
    #         elif is_jira_output:
    #             text = """h1. Description
    #             *AS* {}
    #             *I want to* {}
    #             *So that* {}
    #             h1. Business Value: {}
    #             h1. Business Rules
    #             {}
    #             h1. Acceptance scenarios
    #             """.format(feature['role'],
    #                        feature['action'],
    #                        feature['benefit'],
    #                        feature['business value'],
    #                        feature['summary'])
    #             for scenario_id in feature['scenarios']:
    #                 text += self.display_scenario(scenario_id = scenario_id, is_jira_output = is_jira_output)
    #         else:
    #             text = "Feature: {}\n\n".format(feature['name'])
    #             text += "\tAs {}\n\tI want to {}\n\tSo that {}\n\n".format(feature['role'],
    #                                                                        feature['action'],
    #                                                                        feature['benefit'])
    #             text += "Description:\n\t{}\n\n".format(feature['summary'])
    #             for scenario_id in feature['scenarios']:
    #                 text += self.display_scenario(scenario_id = scenario_id, is_html_output = is_html_output)
    #         return text
    #     else:
    #         text = ""
    #         for feature in self.__features.all():
    #             text += self.display_feature(feature_id = feature.doc_id, is_html_output = is_html_output)
    #         return text
    #
    # def export_feature_to_gherkin(self, folder_name = None, feature_id = None):
    #     """
    #
    #     :param folder_name:
    #     :param feature_id:
    #     :return:
    #     """
    #     if folder_name is not None:
    #         if feature_id:
    #             file_name = self.get_feature(feature_id = feature_id, feature_key = 'name')
    #             file_name = file_name.replace(" ", "") + ".feature"
    #             file_name = folder_name + "/" + file_name
    #
    #             with open(file_name, "w") as file:
    #                 file.write(self.display_feature(feature_id = feature_id))
    #         else:
    #             for feature in self.__features.all():
    #                 self.export_feature_to_gherkin(folder_name = folder_name, feature_id = feature.doc_id)
    #     else:
    #         raise Exception("A folder name is mandatory to export")
    #
    # def add_scenario(self, scenario = None, feature_id = None):
    #     """
    #
    #     :param scenario:
    #     :param feature_id:
    #     :return:
    #     """
    #     if scenario is not None and all(key in scenario.keys() for key in self.__scenario_keys):
    #         if scenario['linked to feature'] is None:
    #             scenario['linked to feature'] = [feature_id, ]
    #             key = self.__scenarios.insert(scenario)
    #             sc_keys = self.get_feature(feature_id = int(feature_id), feature_key = "scenarios")
    #             sc_keys.append(key)
    #             self.update_feature_value(feature_id = int(feature_id), feature_key = "scenarios", key_value = sc_keys)
    #         elif feature_id == scenario['linked to feature']:
    #             key = self.__scenarios.insert(scenario)
    #             sc_keys = self.get_feature(feature_id = int(feature_id), feature_key = "scenarios")
    #             sc_keys.append(key)
    #             self.update_feature_value(feature_id = int(feature_id), feature_key = "scenarios", key_value = sc_keys)
    #         else:
    #             raise Exception("Scenario refers to another feature.")
    #     else:
    #         raise Exception("Can't add a scenario with those data")
    #
    # def update_scenario(self, scenario_id = None, scenario = None):
    #     """
    #
    #     :param scenario_id:
    #     :param scenario:
    #     :return:
    #     """
    #     if scenario_id is None or not scenario:
    #         raise Exception("Need the scenario id and the scenario dictionary")
    #     else:
    #         self.__scenarios.update(scenario, doc_ids = [int(scenario_id), ])
    #
    # def update_scenario_value(self, scenario_id = None, scenario_key = None, key_value = None):
    #     """
    #
    #     :param scenario_id:
    #     :param scenario_key:
    #     :param key_value:
    #     :return:
    #     """
    #     if scenario_id is None or scenario_key is None:
    #         raise Exception("Need the scenario id and field to update scenario")
    #     elif scenario_key not in self.__scenario_keys:
    #         raise Exception("Scenario key is not a scenario one")
    #     else:
    #         self.__scenarios.update(tinyset(scenario_key, key_value), doc_ids = [int(scenario_id), ])
    #
    # def get_scenario(self, scenario_id = None):
    #     """
    #
    #     :param scenario_id:
    #     :return:
    #     """
    #     return self.__scenarios.get(doc_id = int(scenario_id))
    #
    # def display_scenario_part(self, scenario_part = None,
    #                           scenario_part_data = None,
    #                           is_html_output = False,
    #                           is_jira_output = False):
    #     """
    #
    #     :param is_jira_output:
    #     :param scenario_part:
    #     :param scenario_part_data:
    #     :param is_html_output:
    #     :return:
    #     """
    #     text = ""
    #     for step in enumerate(scenario_part_data):
    #         if step[0] == 0:
    #             title = scenario_part[0].capitalize() + scenario_part[1:]
    #         else:
    #             title = "And"
    #
    #         if is_html_output:
    #             text += "<b>{}</b>".format(title)
    #             if isinstance(step[1], dict):
    #                 text += " {}<br />\n{}<br />\n".format(step[1]['name'],
    #                                                        self.display_table(step_table = step[1]['table'],
    #                                                                           is_html_output = is_html_output))
    #             else:
    #                 text += " {}<br />\n".format(html.escape(step[1]))
    #         elif is_jira_output:
    #             text += "*{}*".format(title)
    #             if isinstance(step[1], dict):
    #                 text += " {}\n {}\n".format(step[1]['name'],
    #                                             self.display_table(step_table = step[1]['table'],
    #                                                                is_html_output = is_html_output,
    #                                                                is_jira_output = is_jira_output))
    #             else:
    #                 text += " {}\n".format(step[1])
    #         else:
    #             text += "\t{} ".format(title)
    #             if isinstance(step[1], dict):
    #                 text += " {}\n{}\n".format(step[1]['name'], self.display_table(step_table = step[1]['table'],
    #                                                                                is_html_output = is_html_output))
    #             else:
    #                 text += " {}\n".format(step[1])
    #     return text
    #
    # @staticmethod
    # def display_table(step_table = None, is_html_output = False, is_jira_output = False):
    #     """
    #
    #     :param is_jira_output:
    #     :param step_table:
    #     :param is_html_output:
    #     :return:
    #     """
    #     print("display table")
    #     print(repr(step_table))
    #     if is_html_output:
    #         table = "<table border=\"1\" border-style=\"solid\" border-collapse=\"1\">\n<tr>\n"
    #         for header in step_table['headers']:
    #             table += "<th> {} </th>\n".format(header)
    #         table += "</tr>\n"
    #         for row in step_table['content']:
    #             table += "<tr>\n"
    #             for item in row:
    #                 table += "<td> {} </td>\n".format(item)
    #             table += "</tr>\n"
    #         table += "</table>\n"
    #         return table
    #     elif is_jira_output:
    #         table = "|| "
    #         for header in step_table['headers']:
    #             table += " {} ||".format(header)
    #         table += "\n"
    #         for row in step_table['content']:
    #             table += "| "
    #             for item in row:
    #                 table += " {} |".format(item)
    #             table += "\n"
    #         return table
    #     else:
    #         table = "\t\t| "
    #         for header in step_table['headers']:
    #             table += " {} |".format(header)
    #         table += "\n"
    #         for row in step_table['content']:
    #             table += "\t\t| "
    #             for item in row:
    #                 table += " {} |".format(item)
    #             table += "\n"
    #         return table
    #
    # @staticmethod
    # def display_step(step = None, is_html_output = False, is_jira_output = False):
    #     """
    #
    #     :param is_jira_output:
    #     :param step:
    #     :param is_html_output:
    #     :return:
    #     """
    #     if isinstance(step, dict):
    #         if is_html_output:
    #             table = "<table>\n<tr>\n"
    #             for header in step['table']['headers']:
    #                 table += "<th> {} </th>\n".format(header)
    #             table += "</tr>\n"
    #             for row in step['table']['content']:
    #                 table += "<tr>\n"
    #                 for item in row:
    #                     table += "<td> {} </td>\n".format(item)
    #                 table += "</tr>\n"
    #             table += "</table>\n"
    #             return table
    #         elif is_jira_output:
    #             table = "{}\n".format(step['name'])
    #             table += "|| "
    #             for header in step['table']['headers']:
    #                 table += " {} ||".format(header)
    #             table += "\n"
    #             for row in step['table']['content']:
    #                 table += "| "
    #                 for item in row:
    #                     table += " {} |".format(item)
    #                 table += "\n"
    #             return table
    #         else:
    #             table = "{}\n".format(step['name'])
    #             table += "| "
    #             for header in step['table']['headers']:
    #                 table += " {} |".format(header)
    #             table += "\n"
    #             for row in step['table']['content']:
    #                 table += "| "
    #                 for item in row:
    #                     table += " {} |".format(item)
    #                 table += "\n"
    #             return table
    #     elif isinstance(step, str):
    #         return "{}\n".format(step)
    #     else:
    #         raise Exception("Not an expected type")
    #
    # def display_examples(self, examples = None, is_html_output = False, is_jira_output = False):
    #     """
    #
    #     :param is_jira_output:
    #     :param examples:
    #     :param is_html_output:
    #     :return:
    #     """
    #     text = ""
    #     for example in examples:
    #         if is_html_output:
    #             text += "<h4>Examples: {}</h4>\n".format(example['name'])
    #         elif is_jira_output:
    #             text += "h3. Examples: {}\n".format(example['name'])
    #         else:
    #             text += "\tExamples: {}\n".format(example['name'])
    #         text += self.display_table(step_table = example['table'],
    #                                    is_html_output = is_html_output,
    #                                    is_jira_output = is_jira_output)
    #     return text
    #
    # def display_scenario(self, scenario_id = None, is_html_output = False, is_jira_output = False):
    #     """
    #
    #     :param is_jira_output:
    #     :param scenario_id:
    #     :param is_html_output:
    #     :return:
    #     """
    #     if scenario_id is not None:
    #         scenario = self.__scenarios.get(doc_id = int(scenario_id))
    #         if scenario['examples']:
    #             if is_html_output:
    #                 scenario_text = "<h3> Scenario outline: {}</h3>\n".format(scenario['name'])
    #             elif is_jira_output:
    #                 scenario_text = "h2. Scenario outline: {}\n".format(scenario['name'])
    #             else:
    #                 scenario_text = "Scenario outline: {}\n".format(scenario['name'])
    #         else:
    #             if is_html_output:
    #                 scenario_text = "<h3> Scenario: {}</h3>\n".format(scenario['name'])
    #             elif is_jira_output:
    #                 scenario_text = "h2. Scenario: {}\n".format(scenario['name'])
    #             else:
    #                 scenario_text = "Scenario: {}\n".format(scenario['name'])
    #
    #         scenario_text += self.display_scenario_part(scenario_part = "given",
    #                                                     scenario_part_data = scenario['given'],
    #                                                     is_html_output = is_html_output,
    #                                                     is_jira_output = is_jira_output)
    #         scenario_text += self.display_scenario_part(scenario_part = "when",
    #                                                     scenario_part_data = scenario['when'],
    #                                                     is_html_output = is_html_output,
    #                                                     is_jira_output = is_jira_output)
    #         scenario_text += self.display_scenario_part(scenario_part = "then",
    #                                                     scenario_part_data = scenario['then'],
    #                                                     is_html_output = is_html_output,
    #                                                     is_jira_output = is_jira_output)
    #         scenario_text += "\n\n"
    #
    #         if scenario['examples']:
    #             scenario_text += self.display_examples(examples = scenario['examples'],
    #                                                    is_html_output = is_html_output,
    #                                                    is_jira_output = is_jira_output)
    #
    #         return scenario_text
    #

    def __add_file(self, name = None):
        """
        Create an attachment.
        :param name: the file name or the graph name
        :return:
        """
        if name:
            #copy file to [User Temp]/USMAN/[repository name]/attachments/name
            if not isfile("{}{}".format(self.__repository["attachments"], basename(name))):
                copyfile(name, "{}{}".format(self.__repository["attachments"], basename(name)))
                return {"code": 0,
                        "message": "File successfully integrated in the repository."}
            else:
                return {"code": 3,
                        "message": "Attachment file already exist in the repository"}
        else:
            return {"code": 3,
                    "message": "Attachment file name is empty"}

    #
    # def get_attachment(self, attachment_id = None):
    #     """
    #
    #     :param attachment_id:
    #     :return:
    #     """
    #     if attachment_id:
    #         return self.__attachments.get(doc_id = int(attachment_id))
    #     else:
    #         raise Exception("No attachment reference in input.")
    #

    def remove_attachment(self, attachment_id = None, feature_id = None):
        """

        :param attachment_id:
        :param feature_id:
        :return:
        """
        try:
            if attachment_id and feature_id:
                attachment = self.get_attachment(attachment_id = int(attachment_id))
                if attachment["type"] == self.ATTACHMENT_FILE:
                    os_remove("{}{}{}{}".format(self.__working_folder, "attachments", sep, attachment["name"]))

                if self.__attachments.contains(doc_ids = [int(attachment_id), ]):
                    self.__attachments.remove(doc_ids = [int(attachment_id), ])
                attachment_list = self.get_feature(feature_id = feature_id, feature_key = "attachments")
                attachment_list.remove(int(attachment_id))
                self.update_feature_value(feature_id = feature_id, feature_key = "attachments",
                                          key_value = attachment_list)
            else:
                raise Exception("No attachment reference in input")
        except Exception as exception:
            print(repr(exception))
    #
    # def update_attachment(self, attachment_id = None, attachment = None):
    #     """
    #
    #     :param attachment_id:
    #     :param attachment:
    #     :return:
    #     """
    #     try:
    #         if attachment_id and attachment:
    #             self.__attachments.update(attachment, doc_ids = [int(attachment_id), ])
    #     except Exception as exception:
    #         print(repr(exception))
