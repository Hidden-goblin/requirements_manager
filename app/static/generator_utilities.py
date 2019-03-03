# -*- coding: utf-8 -*-
from os.path import isfile
from os import remove
import subprocess
import markdown


def generate_plantuml_graph(graph_name = None, graph_data = None, attachment_folder = None):
    if graph_name and graph_data and attachment_folder:
        file_name = "{}{}{}".format(attachment_folder, graph_name.replace(" ", ""), ".txt")
        if isfile("{}{}".format(file_name.split(".")[0], ".png")):
            remove("{}{}".format(file_name.split(".")[0], ".png"))

        with open(file_name, "w") as graph:
            graph.write(graph_data)
        out = subprocess.run(
            ["java", "-jar", "app/external/plantuml.1.2018.1.jar", file_name, "-o ", attachment_folder])

        if out.returncode == 0:
            return "{}{}".format(file_name.split(".")[0], ".png")
        else:
            raise Exception("Can't generate UML graph")


def generate_cucumber_scenario_body(given = None, when = None, then = None, examples = None):
    text = "{}{}{}".format(generate_scenario_part(part_name = "Given", part_data = given),
                           generate_scenario_part(part_name = "When", part_data = when),
                           generate_scenario_part(part_name = "Then", part_data = then))
    if examples:
        for example in examples:
            text += "Examples: {}\n{}".format(example["name"], generate_table(step_table = example["table"]))

    return text


def generate_table(step_table = None, is_html_output = False, is_jira_output = False):
    """

    :param is_jira_output:
    :param step_table:
    :param is_html_output:
    :return:
    """

    if is_jira_output or is_html_output:
        table = "|| "
        for header in step_table['headers']:
            table += " {} ||".format(header)
        table += "\n"
        for row in step_table['content']:
            table += "| "
            for item in row:
                table += " {} |".format(item)
            table += "\n"
    else:
        table = "\t\t| "
        for header in step_table['headers']:
            table += " {} |".format(header)
        table += "\n"
        for row in step_table['content']:
            table += "\t\t| "
            for item in row:
                table += " {} |".format(item)
            table += "\n"
        return table

    if is_html_output:
        return markdown.markdown(table)
    else:
        return table


def generate_scenario_step(step = None, is_html_output = False, is_jira_output = False):
    """

    :param is_jira_output:
    :param step:
    :param is_html_output:
    :return:
    """
    if isinstance(step, dict):
        if is_jira_output or is_html_output:
            table = "{}\n {}".format(step['name'],
                                     generate_table(step_table = step['table'], is_html_output = is_html_output,
                                                    is_jira_output = is_jira_output))
        else:
            table = "{}\n {}".format(step['name'],
                                     generate_table(step_table = step['table'], is_html_output = is_html_output,
                                                    is_jira_output = is_jira_output))
            return table
        if is_html_output:
            return markdown.markdown(table)
        else:
            return table
    elif isinstance(step, str):
        return "{}\n".format(step)
    else:
        raise Exception("Not an expected type")


def generate_scenario_part(part_name = None, part_data = None, is_html_output = False, is_jira_output = False):
    text = ""
    for step in enumerate(part_data):
        if step[0] == 0:
            title = part_name[0].capitalize() + part_name[1:]
        else:
            title = "And"

        if is_jira_output or is_html_output:
            text += "*{}* {}".format(title, generate_scenario_step(step[1], is_html_output = False,
                                                                   is_jira_output = is_jira_output))
        else:
            text += "\t{} {}".format(title, generate_scenario_step(step[1], is_html_output = is_html_output,
                                                                   is_jira_output = is_jira_output))

    if is_html_output:
        return markdown.markdown(text)
    else:
        return text

def get_jira_markdown(text = None):
    #strong
    pass