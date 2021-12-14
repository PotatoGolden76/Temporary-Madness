import unittest

from movie import Movie
from client import Client
from rental import Rental

import datetime


class TestCases(unittest.TestCase):
    def test_movie(self):
        m = Movie(2, "Movie_title", "Movie_desc", "Genre")
        self.assertEqual(m.id, "2")
        self.assertEqual(m.title, "Movie_title")
        self.assertEqual(m.description, "Movie_desc")
        self.assertEqual(m.genre, "Genre")

        with self.assertRaises(ValueError) as ve:
            m.title = 2
            ex = ve.exception
            self.assertEqual(ex, "Title not a string")

            m.description = 2
            ex = ve.exception
            self.assertEqual(ex, "Description not a string")

            m.genre = 2
            ex = ve.exception
            self.assertEqual(ex, "Genre not a string")

            m.title = ""
            ex = ve.exception
            self.assertEqual(ex, "Empty title")

            m.description = ""
            ex = ve.exception
            self.assertEqual(ex, "Empty description")

            m.genre = ""
            ex = ve.exception
            self.assertEqual(ex, "Empty genre")

        m.title = "tt"
        self.assertEqual(m.title, "tt")

        m.description = "tt"
        self.assertEqual(m.description, "tt")

        m.genre = "tt"
        self.assertEqual(m.genre, "tt")

    def test_client(self):
        c = Client(2, "name")
        self.assertEqual(c.id, "2")
        self.assertEqual(c.name, "name")

        with self.assertRaises(ValueError) as ve:
            c.name = 2
            ex = ve.exception
            self.assertEqual(ex, "Name not a string")

            c.title = ""
            ex = ve.exception
            self.assertEqual(ex, "Empty name")

        c.name = "tt"
        self.assertEqual(c.name, "tt")

    def test_rental(self):
        r = Rental("1", "2", "3", datetime.date.today(), datetime.date.today(), datetime.date.today())
        self.assertEqual(r.id, "1")
        self.assertEqual(r.movie_id, "2")
        self.assertEqual(r.client_id, "3")
        self.assertEqual(r.due_date, datetime.date.today())
        self.assertEqual(r.returned_date, datetime.date.today())
        self.assertEqual(r.rented_date, datetime.date.today())

        self.assertEqual(r.rented_days, 0)

        with self.assertRaises(ValueError) as ve:
            r.due_date = 2
            ex = ve.exception
            self.assertEqual(ex, "Due date not a date")

            r.rented_date = 2
            ex = ve.exception
            self.assertEqual(ex, "Rented date not a date")

            r.returned_date = 2
            ex = ve.exception
            self.assertEqual(ex, "Returned date not a date")


if __name__ == '__main__':
    unittest.main()
