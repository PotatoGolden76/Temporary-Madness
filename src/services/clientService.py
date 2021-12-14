from src.repository.repository import Repository
from src.repository.fileRepository import FileRepository
from src.repository.binaryRepository import BinaryRepository

import random
from src.domain.client import Client


class ClientService:
    """
    The client service, that uses a repository to hold clients
    """
    def __init__(self, settings):

        if settings.repo_type == "inmemory":
            self.__data = Repository()
        elif settings.repo_type == "file":
            self.__data = FileRepository(settings.client_file, Client)
        elif settings.repo_type == "binary":
            self.__data = BinaryRepository(settings.client_file)

        self.populate()

    @property
    def data(self):
        return self.__data

    def add(self, elem):
        """
        Function to add a client
        :param elem: client to add, instance of the Client class
        :return:
        """
        self.__data.add_element(elem)

    def update(self, updated):
        """
        Function to update a client by replacing the object with one with updated data
        :param updated: the updated object
        :return:
        """
        self.__data[updated.id] = updated

    def remove(self, r_id):
        """
        Function to remove a client
        :param r_id: id to remove
        :return:
        """
        del self.__data[r_id]

    def has_item(self, i_id):
        """
        has_item wrapper for the service
        :param i_id: 
        :return: 
        """
        return self.__data.has_element(i_id)

    def list(self):
        """
        Function to return the string representation of the repository
        :return:
        """
        return str(self.__data)

    def search_id(self, s):
        ls = []
        for elem in self.__data.data:
            if s.lower() in elem.id.lower():
                ls.append(elem)
        return ls

    def search_name(self, s):
        ls = []
        for elem in self.__data.data:
            if s.lower() in elem.name.lower():
                ls.append(elem)

        return ls

    def populate(self):
        """
        Random generator function
        """
        choices = ["Willard Baldry", "Ernst Potter", "Dalton Sherris", "Blair Barbary", "Pleasant Lite",
                   "Walter Monaghan", "Lionel Suchet", "Tony Hill", "Turner Corney", "Josh Stevens",
                   "Jane Hand", "Lenna Ming", "Filomena Heriot", "Arrie Delagney", "Hertha Lamb",
                   "Inga Middlemiss", "Leola Ruth", "Mellie Baldry", "Winnie Fergusson", "Josephine Griffin"]
        for i in range(1, 21):
            c = Client(i, random.choice(choices))
            choices.remove(c.name)
            self.add(c)
