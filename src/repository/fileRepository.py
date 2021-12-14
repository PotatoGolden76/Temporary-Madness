from src.repository.repository import Repository


class FileRepository(Repository):
    def __init__(self, file_name, entity_type):
        self._entity_type = entity_type
        super().__init__()
        self._fileName = file_name[1:len(file_name)-1]

    @property
    def data(self):
        return super().data

    @property
    def values(self):
        return super().values

    def __read_elements(self):
        with open(self._fileName, "a+") as f:
            f.seek(0)
            lines = f.readlines()
            for line in lines:
                if line != "\n":
                    super().add_element(self._entity_type.get_from_string(line))

    def __update_file(self):
        with open(self._fileName, "wt") as f:
            s = ""
            for element in super().data:
                s += str(self._entity_type.get_string_form(super().data[element]))
                s += "\n"
            f.write(s)
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
