# -*- coding: utf-8 -*-
class RepositoryError(Exception):
    """Base class for repository error"""
    pass


class NonUniqueIDEntry(RepositoryError):
    """
    Exception raised for errors on duplicate ID
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class NotAFunctionality(RepositoryError):
    """
    Exception raised for functionality dictionary fields
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class NotAUsecase(RepositoryError):
    """
    Exception raised for use case dictionary fields
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class NotAnAutomaton(RepositoryError):
    """
    Exception raised for automaton dictionary fields
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class IncorrectLink(RepositoryError):
    """
    Exception raised when a link is incorrect either needed but absent or pointing to nothing
    """
    def __init__(self, message):
        self.message = message
