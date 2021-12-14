class Movie:
    """
    Class for the movies
    """
    def __init__(self, _id, title, desc, genre):
        """
        Constructor for a new movie
        :param _id: the id, all IDs are strings internally
        :param title: title of the movie
        :param desc: description of the movie
        :param genre: genre of the movie
        """
        self.__id = str(_id)

        Movie._validate_title(title)
        Movie._validate_description(desc)
        Movie._validate_genre(genre)

        self._title = title
        self._description = desc
        self._genre = genre

    def __str__(self):
        """
        String conversion
        :return: the string form of a movie
        """
        s = f"ID: {self.id}\n" \
            f"Title: {self.title}\n" \
            f"Genre: {self.genre}\n" \
            f"Description: {self.description}"
        return s

    """
    Getters and Setters
    """
    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        Movie._validate_title(value)
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        Movie._validate_description(value)
        self._description = value

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        Movie._validate_genre(value)
        self._genre = value

    @staticmethod
    def _validate_title(value):
        if not isinstance(value, str):
            raise ValueError("Title not a string")
        if value == "":
            raise ValueError("Empty title")

    @staticmethod
    def _validate_description(value):
        if not isinstance(value, str):
            raise ValueError("Description not a string")
        if value == "":
            raise ValueError("Empty description")

    @staticmethod
    def _validate_genre(value):
        if not isinstance(value, str):
            raise ValueError("Genre not a string")
        if value == "":
            raise ValueError("Empty genre")

    @staticmethod
    def get_from_string(st):
        s = st.strip().split(",")
        return Movie(s[0], s[1], s[2], s[3])

    @staticmethod
    def get_string_form(obj):
        s = f"{obj.id},{obj.title},{obj.description},{obj.genre}"
        return s
