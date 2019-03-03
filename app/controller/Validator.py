# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger('simpleExample')


class Validator:
    @staticmethod
    def validate(element = None, schema = None):
        """
        Code 0: Ok
        Code 1: Warning
        Code 3: Error
        :param element: the element to validate
        :param schema: the schema the element should validate. The schema is a dictionary which contains at least a dictionary with the boolean value associated to the "mandatory" key for each key.
        :return:
        """
        logger.debug("{}".format(element))
        if element and schema is not None: #Work only if something is provided
            #TODO Add a type validation
            if not set(element.keys()).issubset(schema.keys()): #Element contains more keys than expected
                return {"code": 3,
                        "message": "Element contains more fields than expected."}

            mandatory = set(key for key in schema.keys() if schema[key]["mandatory"]) #The mandatory set
            if not mandatory.issubset(element.keys()) or not all([element[key] for key in mandatory]): #Element doesn't contains all the mandatory keys or all mandatory keys doesn't contains value
                return {"code": 3,
                        "message": "Element doesn't contains the mandatory fields."}
            diff = set(schema.keys()).difference(element.keys())
            logger.debug("Validate diff is '{}'".format(diff))
            if diff:
                for key in diff:
                    element[key] = None
                return {"code": 1,
                        "message": "Element has been updated to contains all fields.",
                        "element": element}
            else:
                return {"code": 0,
                        "message": "Valid element",
                        "element": element}
        else:
            return {"code": 3,
                    "message": "Can't validate if either the element or the schema is missing."}
