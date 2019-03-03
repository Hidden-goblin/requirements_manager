# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger('simpleExample')


class ElementGenerator:
    """
        Generate empty element from the data base schema
    """

    @staticmethod
    def generate_element(schema = None):
        """
        Generate an empty element from the schema
        :param schema: dictionary { "field name": {"mandatory": True/False}, "field name 2": {"mandatory": True/False},...}
        :return: The element as a
        """
        if schema is not None and isinstance(schema, dict):
            element = {}
            for key in schema.keys():
                if schema[key]["mandatory"]:
                    element[key] = "Default text"
                else:
                    element[key] = None

            return element
        else:
            raise TypeError("Schema has the wrong type or is None")

    @staticmethod
    def generate_list_element(dictionary_list_input = None, display_field = None):
        #Todo add assertion input
        logger.debug(msg = "Get input: {}\n with display field: {}".format(dictionary_list_input, display_field))
        output = []
        for pos, elem in enumerate(dictionary_list_input):
            output.append((elem[display_field], pos))

        return output
