# -*- coding: utf-8 -*-
import abc
from tinydb import where
from app.exceptions.RepositoryException import IncorrectLink


class IRepository(abc.ABC):
    ATTACHMENT_FILE = "file"
    ATTACHMENT_UML = "uml"
    
    @abc.abstractmethod
    def __init__(self, file_name = None):
        """
                Create a new repository according to the file name or open an existing one.
                By default the working repository
                :param file_name:
        """
        pass
    
    ######################
    #Repository management
    ######################
    @abc.abstractmethod
    def save_repository(self):
        pass

    @abc.abstractmethod
    def close_repository(self, save = False):
        pass

    @abc.abstractmethod
    def get_repository_name(self):
        pass

    @abc.abstractmethod
    def get_working_repository_name(self):
        pass

    ######################
    #element management
    ######################
    @abc.abstractmethod
    def get_elements(self, table = None, filtering = None):
        pass

    @abc.abstractmethod
    def add_element(self, element = None, table = None):
        pass

    @abc.abstractmethod
    def get_element(self, element_id = None, table = None, keys = None):
        pass

    @abc.abstractmethod
    def update_element(self, element_id = None, element = None,  element_key = None, element_value = None, table = None):
        pass

    @abc.abstractmethod
    def get_attachments_folder(self):
        pass

