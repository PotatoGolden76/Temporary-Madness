import unittest

from src.services.movieService import MovieService
from src.services.clientService import ClientService

from src.domain.movie import Movie
from src.domain.client import Client

import copy


class Tester(unittest.TestCase):
    def test_movie(self):
        self._movieService = MovieService()

        movie_list = copy.deepcopy(self._movieService.data)
        movie = Movie(42, "Whatever", "desc", "genre")

        # ADD test
        movie_list.add_element(movie)
        self._movieService.add(movie)

        self.assertEqual(list(movie_list.data), list(self._movieService.data.data))

        # UPDATE test
        movie = Movie(42, "Whatever222222", "desc", "genre")
        movie_list["42"].title = "Whatever222222"
        self._movieService.update(movie)

        self.assertEqual(list(movie_list.data), list(self._movieService.data.data))

        # REMOVE test
        del movie_list["42"]
        self._movieService.remove("42")

        self.assertEqual(list(movie_list.data), list(self._movieService.data.data))

        # List test
        self.assertEqual(str(movie_list), self._movieService.list())

    def test_client(self):
        self._clientService = ClientService()

        client_list = copy.deepcopy(self._clientService.data)
        client = Client(42, "Whatever")

        # ADD test
        client_list.add_element(client)
        self._clientService.add(client)

        self.assertEqual(list(client_list.data), list(self._clientService.data.data))

        # UPDATE test
        client = Client(42, "Whatever222222")
        client_list["42"].title = "Whatever222222"
        self._clientService.update(client)

        self.assertEqual(list(client_list.data), list(self._clientService.data.data))

        # REMOVE test
        del client_list["42"]
        self._clientService.remove("42")

        self.assertEqual(list(client_list.data), list(self._clientService.data.data))

        # List test
        self.assertEqual(str(client_list), self._clientService.list())


if __name__ == '__main__':
    unittest.main()