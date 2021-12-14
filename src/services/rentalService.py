import random
from src.domain.rental import Rental

from src.repository.repository import Repository
from src.repository.fileRepository import FileRepository
from src.repository.binaryRepository import BinaryRepository

import datetime


class RentalService:
    """
    Rental service class
    """

    def __init__(self, settings):
        if settings.repo_type == "inmemory":
            self.__data = Repository()
        elif settings.repo_type == "file":
            self.__data = FileRepository(settings.rental_file, Rental)
        elif settings.repo_type == "binary":
            self.__data = BinaryRepository(settings.rental_file)

        self.populate()

    @property
    def data(self):
        return self.__data

    def add(self, elem):
        self.__data.add_element(elem)

    def update(self, updated):
        self.__data[updated.id] = updated

    def remove(self, r_id):
        del self.__data[r_id]

    def has_item(self, i_id):
        return self.__data.has_element(i_id)

    def return_movie(self, i_id):
        self.__data[i_id].returned_date = datetime.datetime.today() if self.__data[i_id].returned_date == datetime.datetime.min else self.__data[i_id].returned_date

    def unreturn_movie(self, i_id):
        self.__data[i_id].returned_date = datetime.datetime.min if self.__data[i_id].returned_date != datetime.datetime.min else self.__data[i_id].returned_date

    def list(self):
        return str(self.__data)

    def get_movie_rentals(self, m_id):
        ls = self.__data.values
        r_list = [x for x in ls if x.movie_id == str(m_id)]
        return r_list

    def get_client_rentals(self, c_id):
        ls = self.__data.values
        r_list = [x for x in ls if x.client_id == str(c_id)]
        return r_list

    def get_client_passed_rentals(self, c_id):
        ls = self.__data.values
        r_list = [x for x in ls if x.client_id == str(c_id) and (x.due_date < datetime.datetime.today() and x.returned_date == datetime.datetime.min)]
        return r_list

    def search_id(self, s):
        ls = []
        for elem in self.__data.data:
            if s.lower() == self.__data.data[elem].id.lower():
                ls.append(self.__data[elem])

        return ls

    def search_client_id(self, s):
        ls = []
        for elem in self.__data.data:
            if s.lower() == self.__data.data[elem].client_id.lower():
                ls.append(self.__data[elem])

        return ls

    def search_movie_id(self, s):
        ls = []
        for elem in self.__data.data:
            if s.lower() == self.__data.data[elem].movie_id.lower():
                ls.append(self.__data[elem])

        return ls

    def populate(self):
        random.seed()
        return_dates = [datetime.datetime.strptime('1/1/2008', '%d/%m/%Y'),
                        datetime.datetime.strptime('6/2/2008', '%d/%m/%Y'),
                        datetime.datetime.strptime('7/3/2008', '%d/%m/%Y'),
                        datetime.datetime.strptime('8/4/2008', '%d/%m/%Y'),
                        datetime.datetime.strptime('9/5/2008', '%d/%m/%Y'),
                        datetime.datetime.min]
        due_dates = [datetime.datetime.strptime('1/1/2009', '%d/%m/%Y'),
                     datetime.datetime.strptime('6/2/2009', '%d/%m/%Y'),
                     datetime.datetime.strptime('7/3/2009', '%d/%m/%Y'),
                     datetime.datetime.strptime('8/4/2009', '%d/%m/%Y'),
                     datetime.datetime.strptime('9/5/2009', '%d/%m/%Y')]

        rent_dates = [datetime.datetime.strptime('1/1/2005', '%d/%m/%Y'),
                      datetime.datetime.strptime('6/2/2005', '%d/%m/%Y'),
                      datetime.datetime.strptime('7/3/2005', '%d/%m/%Y'),
                      datetime.datetime.strptime('8/4/2005', '%d/%m/%Y'),
                      datetime.datetime.strptime('9/5/2005', '%d/%m/%Y')]
        for i in range(1, 21):
            movie = random.randint(1, 20)
            client = random.randint(1, 20)
            r = Rental(i, movie, client, random.choice(rent_dates), random.choice(due_dates),
                       random.choice(return_dates))
            self.add(r)
