class Client:
    """
    Class for the clients
    """
    def __init__(self, _id, name):
        """
        Constructor
        :param _id: the id, IDs are strings internally
        :param name: the name of the client
        """
        Client._validate_name(name)

        self.__id = str(_id)
        self._name = name

    def __str__(self):
        """
        String conversion
        :return: string form of a client
        """
        s = f"ID: {self.id}\n" \
            f"Name: {self.name}"
        return s

    @staticmethod
    def get_from_string(st):
        s = st.strip().split(",")
        return Client(s[0], s[1])

    @staticmethod
    def get_string_form(obj):
        s = f"{obj.id},{obj.name}"
        return s


    """
    Getters and Setters
    """
    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        Client._validate_name(value)
        self._name = value

    @staticmethod
    def _validate_name(value):
        if not isinstance(value, str):
            raise ValueError("Name not a string")
        if value == "":
            raise ValueError("Empty name")
