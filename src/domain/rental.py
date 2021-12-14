import datetime


class Rental:
    def __init__(self, _id, movie_id, client_id, rented_date, due_date, returned_date):
        Rental._validate_rented_date(rented_date)
        Rental._validate_due_date(due_date)
        Rental._validate_returned_date(returned_date)

        if rented_date > due_date or (rented_date > returned_date != datetime.datetime.min):
            raise ValueError("Invalid dates")

        self.__id = str(_id)
        self._movie_id = str(movie_id)
        self._client_id = str(client_id)
        self._rented_date = rented_date
        self._due_date = due_date
        self._returned_date = returned_date

    def __str__(self):
        s = f"ID: {self.id}\n" \
            f"Client ID: {self.client_id}\n" \
            f"Movie ID: {self.movie_id}\n" \
            f"Rented Date: {self.rented_date.strftime('%d/%m/%Y')}\n" \
            f"Due Date: {self.due_date.strftime('%d/%m/%Y')}\n"
        s += f"Returned Date: {self.returned_date.strftime('%d/%m/%Y')}" if self.returned_date != datetime.datetime.min \
            else "Returned Date: Pending"
        return s
    
    @property
    def rented_days(self):
        return (self._returned_date - self._rented_date).days if self._returned_date != datetime.datetime.min else (datetime.datetime.today() - self._due_date).days
    
    @property
    def id(self):
        return self.__id

    @property
    def movie_id(self):
        return self._movie_id

    @movie_id.setter
    def movie_id(self, value):
        self._movie_id = value

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        self._client_id = value

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        Rental._validate_due_date(value)
        self._due_date = value

    @property
    def returned_date(self):
        return self._returned_date

    @returned_date.setter
    def returned_date(self, value):
        Rental._validate_returned_date(value)
        self._returned_date = value

    @property
    def rented_date(self):
        return self._rented_date

    @rented_date.setter
    def rented_date(self, value):
        Rental._validate_rented_date(value)
        self._rented_date = value

    @staticmethod
    def _validate_returned_date(value):
        if not isinstance(value, datetime.date):
            raise ValueError("Returned date not a date")

    @staticmethod
    def _validate_due_date(value):
        if not isinstance(value, datetime.date):
            raise ValueError("Due date not a date")

    @staticmethod
    def _validate_rented_date(value):
        if not isinstance(value, datetime.date):
            raise ValueError("Rented date not a date")

    @staticmethod
    def get_from_string(st):
        s = st.strip().split(",")
        return Rental(s[0], s[1], s[2], datetime.datetime.strptime(s[3], '%d/%m/%Y'), datetime.datetime.strptime(s[4], '%d/%m/%Y'), datetime.datetime.strptime(s[5], '%d/%m/%Y'))

    @staticmethod
    def get_string_form(obj):
        s = f"{obj.id},{obj.movie_id},{obj.client_id},{obj.rented_date.strftime('%d/%m/%Y')},{obj.due_date.strftime('%d/%m/%Y')},{obj.returned_date.strftime('%d/%m/%Y')}"
        return s
