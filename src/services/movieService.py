from src.repository.repository import Repository
from src.repository.fileRepository import FileRepository
from src.repository.binaryRepository import BinaryRepository

import random
from src.domain.movie import Movie


class MovieService:
    """
    The Movie service class
    """

    def __init__(self, settings):
        if settings.repo_type == "inmemory":
            self.__data = Repository()
        elif settings.repo_type == "file":
            self.__data = FileRepository(settings.movies_file, Movie)
        elif settings.repo_type == "binary":
            self.__data = BinaryRepository(settings.movies_file)

        self.populate()

    @property
    def data(self):
        return self.__data

    def add(self, elem):
        """
        Function to add a movie
        :param elem: Movie to add, instance of the Movie class
        :return:
        """
        self.__data.add_element(elem)

    def update(self, updated):
        """
        Function to update a movie by replacing the object with one with updated data
        :param updated: the updated object
        :return:
        """
        self.__data[updated.id] = updated

    def remove(self, r_id):
        """
        Function to remove a movie
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

    def search_title(self, s):
        ls = []
        for elem in self.__data.data:
            if s.lower() in elem.title.lower():
                ls.append(elem)

        return ls

    def search_genre(self, s):
        ls = []
        for elem in self.__data.data:
            if s.lower() in elem.genre.lower():
                ls.append(elem)

        return ls

    def search_desc(self, s):
        ls = []
        for elem in self.__data.data:
            if s.lower() in elem.description.lower():
                ls.append(elem)

        return ls

    def populate(self):
        name_choices = ["Invader Of Our Ship", "Invader Of Exploration", "Hunter In The News", "Boy Of The Orbit",
                        "Clone Of War", "Men Of The Dead", "Spies In The News", "Defenders Of Our Ship",
                        "Traitors Of The Stars", "Of The Past", "Spies And Pilots", "Leaders And Martians",
                        "Defenders And Spies", "Aliens And", "Friends And Women", "Ruins Of Darkness",
                        "Ruins Of Sunshine", "Star Of Society", "Carnage Of Darkness", "Revenge Of Our Culture",
                        "Broken The Armies", "Failure Of A Nuclear War", "Anxious For The Secrets",
                        "Puzzle Of", "Crazy Of The Troopers"]
        genre_choices = ["action", "comedy", "sci-fi", "romance", "drama", "thriller", "horror"]
        for i in range(1, 21):
            name = random.choice(name_choices)
            name_choices.remove(name)
            genre = random.choice(genre_choices)
            m = Movie(i, name, f"Generic Description {i}", genre)
            self.add(m)
