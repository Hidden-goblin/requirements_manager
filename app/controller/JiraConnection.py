# -*- coding: utf-8 -*-
import requests
import json
import base64


class JiraConnection:
    STORY = "Story"
    EPIC = "Epic"
    TEST = "Test"
    IMPROVEMENT = "Improvement"
    TEST_EXECUTION = "Test Execution"

    ROLE_JIRA_KEY = "customfield_10503"
    ACTION_JIRA_KEY = "customfield_10504"
    BENEFIT_JIRA_KEY = "customfield_10505"
    IMPROVEMENT_FIELD_KEY = "customfield_10506"

    def __init__(self, url = None, username = None, password = None):

        self.url = url.rstrip(" /.")
        self.token = base64.b64encode(str.encode("{}:{}".format(username, password))).decode()
        self.project_id = None
        self.issues_id = {}

    def is_connected(self):
        return self.token and self.project_id

    def header(self):
        return {'Authorization': "Basic {}".format(self.token), 'content-type': 'application/json'}

    ###############################
    ## PROJECT
    ###############################
    def get_project(self):
        response = requests.get("{}/rest/api/2/project".format(self.url), headers = self.header())
        if response.status_code != 200:
            raise Exception("Getting project cast an error {}".format(response.text))
        else:
            return response

    def get_project_id(self, project_name = None, project_key = None):
        if self.project_id:
            return self.project_id
        else:
            self.set_project_id(project_name = project_name, project_key = project_key)

    def set_project_id(self, project_id = None, project_name = None, project_key = None):
        if project_id:
            self.project_id = project_id
        else:
            try:
                project_list = self.get_project().json()
            except Exception as exception:
                raise Exception("Retrieving project list fail; {}".format(repr(exception)))

            if project_name or project_key:
                for project_dict in project_list:
                    if project_key and project_dict['key'] == project_key:
                        self.project_id = project_dict['id']
                        return self.project_id
                    elif project_name and project_dict['name'] == project_name:
                        self.project_id = project_dict['id']
                        return self.project_id
                    else:
                        pass
            raise Exception("No data to search")

    #########################################
    ## ISSUES
    #########################################

    def get_issue_meta(self):
        return requests.get("{}/rest/api/2/issue/createmeta".format(self.url), headers = self.header(),
                            params = {'projectIds': str(self.project_id)})

    def get_issue(self, issue_key = None):
        return requests.get("{}/rest/api/2/issue/{}".format(self.url, issue_key),
                            headers = self.header())

    def get_issue_identifier(self, issue_type = None):
        """
        Retrieve the issue id of a specific issue
        :param issue_type: the issue name
        :return: an id
        """
        if self.issues_id and issue_type in self.issues_id.keys():
            return self.issues_id[issue_type]
        else:
            if self.project_id:
                response = requests.get("{}/rest/api/2/issue/createmeta".format(self.url), headers = self.header(),
                                        params = {'projectIds': str(self.project_id)})
                for rep in response.json()["projects"][0]["issuetypes"]:
                    print(rep['name'])
                    if rep['name'] == issue_type:
                        self.issues_id[issue_type] = rep["id"]
                        return self.get_issue_identifier(issue_type = issue_type)
                raise Exception("Issue {} not found".format(issue_type))
            else:
                pass

    def update_issue_description(self, issue_key = None, description = None):
        data = {"update": {"description": [{'set': description}]}}
        return requests.put("{}/rest/api/2/issue/{}".format(self.url, issue_key),
                            data = json.dumps(data),
                            headers = self.header())

    def get_issue_attachments_id(self, issue_key = None):
        rep = self.get_issue(issue_key = issue_key)
        data = rep.json()["fields"]["attachment"]
        return [tmp["id"] for tmp in data]

    def get_issue_status(self, issue_key = None):
        response = requests.get("{}/rest/api/2/issue/{}".format(self.url, issue_key),
                                headers = self.header())
        if response.status_code == 200:
            return response.json()['fields']['status']['name']
        else:
            raise Exception(
                "Get issue status return\n response code: '{}'\n response text: '{}'".format(response.status_code,
                                                                                             response.text))

    def create_issue(self, issue_data = None):
        if issue_data:
            return requests.post("{}/rest/api/2/issue".format(self.url), data = json.dumps(issue_data),
                                 headers = self.header())
        else:
            raise Exception("Can't create an issue without data")

    def update_issue(self, issue_key = None, issue_data = None):
        if issue_data and issue_key:
            return requests.put("{}/rest/api/2/issue/{}".format(self.url, issue_key),
                                data = json.dumps(issue_data),
                                headers = self.header())
        else:
            raise Exception("Can't create an issue without data")

    def create_link(self, from_key = None, to_key = None, link_type = None):
        data = {
            "type": {
                "name": str(link_type)
                },
            "inwardIssue": {
                "key": str(from_key)
                },
            "outwardIssue": {
                "key": str(to_key)
                }
            }
        return requests.post("{}/rest/api/2/issueLink".format(self.url), data = json.dumps(data),
                             headers = self.header())

    ############################################
    ## STORY
    ############################################

    def create_story(self, title = None, description = None, epic_key = None, actor = None, action = None,
                     benefit = None):
        """
        Request the creation of a story
        :param action:
        :param benefit:
        :param actor:
        :param epic_key:
        :param title:
        :param description:
        :return: request response
        """
        data = {"fields": {"project": {"id": str(self.project_id)},
                           "summary": title,
                           "issuetype": {"id": str(self.get_issue_identifier(issue_type = JiraConnection.STORY))},
                           "description": description,
                           "customfield_10002": epic_key,
                           JiraConnection.ROLE_JIRA_KEY: actor,
                           JiraConnection.ACTION_JIRA_KEY: action,
                           JiraConnection.BENEFIT_JIRA_KEY: benefit}}
        return self.create_issue(issue_data = data)

    def update_story(self, issue_key = None, title = None, description = None, epic_key = None, actor = None,
                     action = None, benefit = None):
        data = {"fields": {"summary": title,
                           "description": description,
                           "customfield_10002": epic_key,
                           JiraConnection.ROLE_JIRA_KEY: actor,
                           JiraConnection.ACTION_JIRA_KEY: action,
                           JiraConnection.BENEFIT_JIRA_KEY: benefit}}
        return self.update_issue(issue_key = issue_key, issue_data = data)

    def add_attachments_to_issue(self, issue_key = None, file_name = None):
        """

        :param issue_key:
        :param file_name:
        :return:
        """
        with open(file_name, "rb") as file:
            return requests.post("{}/rest/api/2/issue/{}/attachments".format(self.url, issue_key),
                                 files = {'file': file},
                                 headers = {'Authorization': "Basic {}".format(self.token),
                                            'X-Atlassian-Token': "no-check"})

    def delete_attachments(self, issue_key = None, attachment_id = None):
        if issue_key is not None and attachment_id is None:
            for att_id in self.get_issue_attachments_id(issue_key = issue_key):
                self.delete_attachments(attachment_id = att_id)
        elif issue_key is None and attachment_id is not None:
            return requests.delete("{}/rest/api/2/attachment/{}".format(self.url, attachment_id),
                                   headers = self.header())
        else:
            print("Error")

    ###########################################
    ## EPIC
    ###########################################

    def get_epics(self):
        """
        Get all epics related to a project
        :return: a list of key-epic name sets
        """
        data = {"jql": "project = {} AND type = Epic".format(self.project_id),
                "fields": ["key", "customfield_10004"]}
        list_rep = []
        response = requests.post("{}/rest/api/2/search".format(self.url),
                                 data = json.dumps(data),
                                 headers = self.header())
        print(response.text)
        issues = response.json()["issues"]
        for item in issues:
            list_rep.append((item["key"], item["fields"]["customfield_10004"]))
        return list_rep

    def add_epic(self, epic_name = None, epic_summary = None):
        data = {"fields": {"project": {"id": str(self.project_id)},
                           "summary": epic_summary,
                           "issuetype": {"id": str(self.get_issue_identifier(issue_type = JiraConnection.EPIC))},
                           "customfield_10004": epic_name}}
        return self.create_issue(issue_data = data)

    ###########################################
    ## TEST
    ###########################################

    def add_test(self, story_key = None, test_description = None, test_name = None, test_type = None):
        data = {"fields": {
            "project": {
                "id": str(self.project_id)
                },
            "summary": test_name,
            "description": "",
            "issuetype": {
                "id": str(self.get_issue_identifier(issue_type = JiraConnection.TEST))
                },
            "customfield_10202": {"value": "Cucumber"},
            "customfield_10203": {"value": str(test_type)},
            "customfield_10204": test_description
            }
            }
        print(data)
        response = self.create_issue(issue_data = data)
        print(response.text)
        key = response.json()["key"]

        response = self.create_link(from_key = key, to_key = story_key, link_type = "Tests")
        return response, key

    def update_test(self, test_key = None, test_description = None, test_name = None, test_type = None):
        data = {"fields": {
            "summary": test_name,
            "description": "",
            "customfield_10202": {"value": "Cucumber"},
            "customfield_10203": {"value": str(test_type)},
            "customfield_10204": test_description
            }
            }
        return self.update_issue(issue_key = test_key, issue_data = data)

    def get_link_type(self):
        return requests.get("{}/rest/api/2/issueLinkType".format(self.url), headers = self.header())
