from src.domain.movie import Movie
from src.repository.collection import Collection

class RepositoryException(Exception):
    """
    Repository exception class
    """
    pass


class Repository:
    """
    Repository class
    """
    def __init__(self):
        self.__data = Collection()

    @property
    def data(self):
        return self.__data

    @property
    def values(self):
        return self.__data.values

    def add_element(self, obj):
        """
        Function to add elements to a repository
        :param obj: object
        :return:
        """
        if self.__data.has_element(obj):
            raise RepositoryException(f"Object with Id {str(obj.id)} already exists in repository")
        self.__data.add(obj.id, obj)

    def has_element(self, i_id):
        """
        function to check if repository has an element
        :param i_id: id to check for, string form
        :return: True if the object exists or False if not
        """
        return self.__data.has_id(i_id)

    """
    [] access built-in methods
    """
    def __getitem__(self, item):
        return self.__data[item]

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __delitem__(self, key):
        del self.__data[key]

    def __str__(self):
        s = ""
        for i in self.__data:
            s += str(i) + "\n\n"
        return s


def test_repository():
    """
    Test for the Repository class`
    :return:
    """
    r = Repository()
    r.add_element(Movie(100, "Title", "Desc", "Genre"))
    r["100"].title = "Generic Title 2"
    assert r["100"].title == "Generic Title 2"

    try:
        r.add_element(Movie(100, "Title_2", "Desc_2", "Genre_2"))
        assert False
    except RepositoryException as re:
        assert str(re) == "Object with Id 100 already exists in repository"


test_repository()
