from src.repository.repository import Repository
import pickle


class BinaryRepository(Repository):
    def __init__(self, file_name):
        super().__init__()
        self._fileName = file_name[1:len(file_name)-1]

    @property
    def data(self):
        return super().data

    @property
    def values(self):
        return super().values

    def __read_elements(self):
        with open(self._fileName, "rb") as f:
            try:
                d = pickle.load(f)
            except EOFError:
                d = {}
                print("empty!!!!")
            for elem in d:
                super().add_element(d[elem])

    def __update_file(self):
        with open(self._fileName, "wb") as f:
            pickle.dump(self.data, f)
        self.data.clear()

    def add_element(self, obj):
        self.__read_elements()
        super().add_element(obj)
        self.__update_file()

    def has_element(self, i_id):
        self.__read_elements()
        r = super().has_element(i_id)
        self.__update_file()
        return r

    def __getitem__(self, item):
        self.__read_elements()
        i = super().__getitem__(item)
        self.__update_file()
        return i

    def __setitem__(self, key, value):
        self.__read_elements()
        super().__setitem__(key, value)
        self.__update_file()

    def __delitem__(self, key):
        self.__read_elements()
        super().__delitem__(key)
        self.__update_file()

    def __str__(self):
        self.__read_elements()
        r = super().__str__()
        self.__update_file()
        return r
