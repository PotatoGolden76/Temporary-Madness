import datetime

from src.repository.repository import RepositoryException
from src.services.movieService import MovieService
from src.services.rentalService import RentalService
from src.services.clientService import ClientService

from src.domain.movie import Movie
from src.domain.rental import Rental
from src.domain.client import Client

from undo import UndoService, Call, CascadedOperation, Operation
from settings import Settings

from enum import Enum
from tester import Tester


class UIException(Exception):
    pass


class AppState(Enum):
    MainMenu = 1
    MovieMenu = 2
    RentalMenu = 3
    ClientMenu = 4
    SearchMenu = 5
    StatMenu = 6


class AppUI:
    """
    AppUI Class
    """

    def __init__(self, settings):
        """
        Services
        """
        self._movieService = MovieService(settings)
        self._rentalService = RentalService(settings)
        self._clientService = ClientService(settings)

        self._undoService = UndoService()

        self.__state = AppState.MainMenu

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value

    @property
    def movie_service(self):
        return self._movieService

    @property
    def rental_service(self):
        return self._rentalService

    @property
    def client_service(self):
        return self._clientService

    def print_menu(self):
        """
        Menu printing based on current app state
        :return:
        """
        print("")
        match self.state:
            case AppState.MainMenu:
                AppUI.print_main_menu()
            case AppState.ClientMenu:
                AppUI.print_client_menu()
            case AppState.RentalMenu:
                AppUI.print_rentals_menu()
            case AppState.MovieMenu:
                AppUI.print_movie_menu()
            case AppState.SearchMenu:
                AppUI.print_search_menu()
            case AppState.StatMenu:
                AppUI.print_stat_menu()
            case _:
                raise UIException("Unrecognised State")

    def execute(self, command):
        """
        Command execution based on current app state
        :param command: command to be executed
        :return:
        """
        match self.state:
            case AppState.MainMenu:
                self.process_main_menu(command)
            case AppState.ClientMenu:
                self.process_client_menu(command)
            case AppState.RentalMenu:
                self.process_rental_menu(command)
            case AppState.MovieMenu:
                self.process_movie_menu(command)
            case AppState.SearchMenu:
                self.process_search_menu(command)
            case AppState.StatMenu:
                self.process_stat_menu(command)

    @staticmethod
    def get_command():
        """
        Static method for input reading
        :return:
        """
        cmd = input("Enter your command: ")
        try:
            cmd = int(cmd)
            return cmd
        except ValueError:
            print("Invalid Command")
            return None

    @staticmethod
    def parse_date(date):
        """
        Static method for date parsing
        :param date: given date
        :return:
        """
        if date.lower() == "pending":
            date = datetime.datetime.min
        else:
            date = datetime.datetime.strptime(date, "%d/%m/%Y")
        return date

    """
    State Menu Printers
    """

    @staticmethod
    def print_main_menu():
        print("1. Manage Movies")
        print("2. Manage Clients")
        print("3. Manage Rentals")
        print("4. Search")
        print("5. Statistics")
        print("6. Exit")

        print("7 - undo")
        print("8 - redo")

    @staticmethod
    def print_movie_menu():
        print("1. Add Movie")
        print("2. Update Movie")
        print("3. Remove Movie")
        print("4. List Movies")
        print("5. Back")

    @staticmethod
    def print_client_menu():
        print("1. Add Client")
        print("2. Update Client")
        print("3. Remove Client")
        print("4. List Clients")
        print("5. Back")

    @staticmethod
    def print_rentals_menu():
        print("1. Rent a movie")
        print("2. Update Rental")
        print("3. Remove Rental")
        print("4. List Rentals")
        print("5. Return a movie")
        print("6. Back")

    def process_main_menu(self, command):
        """
        Main menu command processor
        :param command:
        :return:
        """
        match command:
            case 1:  # Movie
                self.state = AppState.MovieMenu
            case 2:  # Client
                self.state = AppState.ClientMenu
            case 3:  # Rental
                self.state = AppState.RentalMenu
            case 4:  # Search
                self.state = AppState.SearchMenu
            case 5:  # Stat
                self.state = AppState.StatMenu
            case 6:  # Exit
                exit()
            case 7:
                self._undoService.undo()
            case 8:
                self._undoService.redo()
            case _:  # Wildcard
                raise UIException("Unrecognised Command")

    def process_rental_menu(self, command):
        """
        Rental menu command processor
        :param command:
        :return:
        """
        match command:
            case 1:  # Add
                try:
                    rental_id = ""
                    ok = False
                    while not ok:
                        rental_id = input("Enter new rental ID: ")
                        if not self._rentalService.has_item(rental_id):
                            ok = True
                        else:
                            print("ID already in use")

                    movie_id = ""
                    ok = False
                    while not ok:
                        movie_id = input("Enter new rental movie ID: ")
                        if self._movieService.has_item(movie_id):
                            ok = True
                        else:
                            print("Invalid Movie ID")

                    client_id = ""
                    ok = False
                    while not ok:
                        client_id = input("Enter new rental client ID: ")
                        if self._clientService.has_item(client_id):
                            ok = True
                        else:
                            print("Invalid Client ID")
                    if self._rentalService.get_client_passed_rentals(client_id):
                        raise UIException("Client has rented movies that passed their due date for return")

                    rented_date = AppUI.parse_date(input("Enter rented date (DD/MM/YY): "))
                    due_date = AppUI.parse_date(input("Enter due date (DD/MM/YY): "))
                    returned_date = AppUI.parse_date(input("Enter returned date (DD/MM/YY) or 'Pending': "))

                    r = Rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
                    redo = Call(self._rentalService.add, r)
                    undo = Call(self._rentalService.remove, r.id)

                    op = Operation(undo, redo)
                    self._undoService.record(op)
                    self._rentalService.add(r)
                except ValueError as ve:
                    print(str(ve))
                except UIException as ue:
                    print(str(ue))
                except RepositoryException as re:
                    print(str(re))
            case 2:  # Update

                rental_id = ""
                ok = False
                while not ok:
                    rental_id = input("Enter the ID of the rental you want to update: ")
                    if self._rentalService.has_item(rental_id):
                        ok = True
                    else:
                        print("ID not in use")

                movie_id = ""
                ok = False
                while not ok:
                    movie_id = input("Enter new rental movie ID: ")
                    if self._movieService.has_item(movie_id):
                        ok = True
                    else:
                        print("Invalid Movie ID")

                client_id = ""
                ok = False
                while not ok:
                    client_id = input("Enter new rental client ID: ")
                    if self._clientService.has_item(client_id):
                        ok = True
                    else:
                        print("Invalid Client ID")

                rented_date = AppUI.parse_date(input("Enter rented date (DD/MM/YYYY): "))
                due_date = AppUI.parse_date(input("Enter due date (DD/MM/YYYY): "))
                returned_date = AppUI.parse_date(input("Enter returned date (DD/MM/YYYY) or 'Pending': "))

                try:
                    r = Rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
                    old_r = self._clientService.data[r.id]
                    self._rentalService.update(r)

                    redo = Call(self._rentalService.update, r)
                    undo = Call(self._rentalService.update, old_r)

                    op = Operation(undo, redo)
                    self._undoService.record(op)
                except ValueError as ve:
                    print(str(ve))
            case 3:  # Remove
                rental_id = input("Enter the ID of the rental you want to remove: ")

                try:
                    r = self.rental_service.data[rental_id]
                    self._rentalService.remove(rental_id)

                    undo = Call(self._rentalService.add, r)
                    redo = Call(self._rentalService.remove, r.id)

                    op = Operation(undo, redo)
                    self._undoService.record(op)
                except KeyError:
                    print("Nonexistent ID")
            case 4:  # List
                print(self._rentalService.list())
            case 5:  # Return
                rental_id = ""
                ok = False
                while not ok:
                    rental_id = input("Enter the ID of the rental you want to return: ")
                    if self._rentalService.has_item(rental_id):
                        ok = True
                    else:
                        print("ID not in use")
                try:
                    self._rentalService.return_movie(rental_id)

                    undo = Call(self._rentalService.return_movie, rental_id)
                    redo = Call(self._rentalService.unreturn_movie, rental_id)

                    op = Operation(undo, redo)
                    self._undoService.record(op)
                except KeyError:
                    print("Invalid ID")
            case 6:  # Back
                self.state = AppState.MainMenu
            case _:  # Wildcard
                raise UIException("Unrecognised Command")

    def process_client_menu(self, command):
        """
        Client menu command processor
        :param command:
        :return:
        """
        match command:
            case 1:  # Add
                client_id = ""
                ok = False
                while not ok:
                    client_id = input("Enter new client ID: ")
                    if not self._clientService.has_item(client_id):
                        ok = True
                    else:
                        print("ID already in use")
                name = input("Enter new client name: ")

                try:
                    c = Client(client_id, name)
                    self._clientService.add(c)

                    redo = Call(self._clientService.add, c)
                    undo = Call(self._clientService.remove, c.id)

                    op = Operation(undo, redo)
                    self._undoService.record(op)
                except ValueError as ve:
                    print(str(ve))
                except RepositoryException as re:
                    print(str(re))

            case 2:  # Update
                client_id = ""
                ok = False
                while not ok:
                    client_id = input("Enter the ID of the client you want to update: ")
                    if self._clientService.has_item(client_id):
                        ok = True
                    else:
                        print("ID not in use")
                name = input("Enter new client name: ")

                try:
                    c = Client(client_id, name)
                    old_c = self._clientService.data[c.id]
                    self._clientService.update(c)

                    redo = Call(self._clientService.update, c)
                    undo = Call(self._clientService.update, old_c)

                    op = Operation(undo, redo)
                    self._undoService.record(op)
                except ValueError as ve:
                    print(str(ve))
            case 3:  # Remove
                client_id = input("Enter the ID of the client you want to remove: ")

                try:
                    undo = Call(self._clientService.add, self._clientService.data[client_id])
                    redo = Call(self._clientService.remove, client_id)
                    op = Operation(undo, redo)

                    c_op = CascadedOperation()
                    c_op.add(op)
                    self._clientService.remove(client_id)
                    ls = self.rental_service.get_client_rentals(client_id)
                    for i in ls:
                        self.rental_service.remove(i.id)
                        redo = Call(self.rental_service.remove, i.id)
                        undo = Call(self.rental_service.add, i)

                        op = Operation(undo, redo)
                        c_op.add(op)

                    self._undoService.record(c_op)
                except KeyError:
                    print("Nonexistent ID")
            case 4:  # List
                print(self._clientService.list())
            case 5:  # Back
                self.state = AppState.MainMenu
            case _:  # Wildcard
                raise UIException("Unrecognised Command")

    def process_movie_menu(self, command):
        """
        Movie menu command processor
        :param command:
        :return:
        """
        op = ""
        match command:
            case 1:  # Add
                movie_id = ""
                ok = False
                while not ok:
                    movie_id = input("Enter new movie ID: ")
                    if not self._movieService.has_item(movie_id):
                        ok = True
                    else:
                        print("ID already in use")
                title = input("Enter new movie title: ")
                desc = input("Enter new movie description: ")
                genre = input("Enter new movie genre: ")

                try:
                    m = Movie(movie_id, title, desc, genre)
                    self._movieService.add(m)

                    redo = Call(self._movieService.add, m)
                    undo = Call(self._movieService.remove, m.id)

                    op = Operation(undo, redo)
                    self._undoService.record(op)
                except ValueError as ve:
                    print(str(ve))
                except RepositoryException as re:
                    print(str(re))
            case 2:  # Update
                movie_id = ""
                ok = False
                while not ok:
                    movie_id = input("Enter the ID of the movie you want to update: ")
                    if self._movieService.has_item(movie_id):
                        ok = True
                    else:
                        print("ID not in use")
                title = input("Enter new movie title: ")
                desc = input("Enter new movie description: ")
                genre = input("Enter new movie genre: ")

                try:
                    m = Movie(movie_id, title, desc, genre)
                    old_m = self._movieService.data[movie_id]
                    self._movieService.update(m)

                    redo = Call(self._movieService.update, m)
                    undo = Call(self._movieService.update, old_m)

                    op = Operation(undo, redo)
                    self._undoService.record(op)
                except ValueError as ve:
                    print(str(ve))
            case 3:  # Remove
                movie_id = input("Enter the ID of the movie you want to remove: ")

                try:
                    undo = Call(self._movieService.add, self._movieService.data[movie_id])
                    redo = Call(self._movieService.remove, movie_id)
                    op = Operation(undo, redo)

                    c_op = CascadedOperation()
                    c_op.add(op)
                    self._movieService.remove(movie_id)
                    ls = self.rental_service.get_movie_rentals(movie_id)
                    for i in ls:
                        self.rental_service.remove(i.id)
                        redo = Call(self.rental_service.remove, i.id)
                        undo = Call(self.rental_service.add, i)

                        op = Operation(undo, redo)
                        c_op.add(op)

                    self._undoService.record(c_op)
                except KeyError:
                    print("ID not in use")
            case 4:  # List
                print(self._movieService.list())
            case 5:  # Back
                self.state = AppState.MainMenu
            case _:  # Wildcard
                raise UIException("Unrecognised Command")

    @classmethod
    def print_search_menu(cls):
        print("1. Search Clients by ID")
        print("2. Search Clients by Name")
        print("<-------------------------->")
        print("3. Search Movies by ID")
        print("4. Search Movies by Title")
        print("5. Search Movies by Description")
        print("6. Search Movies by Genre")
        print("<-------------------------->")
        print("7. Back")

    def process_search_menu(self, command):
        match command:
            case 1:  # Client/ID
                query = input("Enter your query: ").strip()
                ls = self._clientService.search_id(query)

                s = ""
                for e in ls:
                    s += f"ID: {e.id}\n" \
                         f"Title: {e.name}\n\n"

                print(s)
            case 2:  # Client/Name
                query = input("Enter your query: ").strip()
                ls = self._clientService.search_name(query)

                s = ""
                for e in ls:
                    s += f"ID: {e.id}\n" \
                         f"Title: {e.name}\n\n"

                print(s)
            case 3:  # Movie/ID
                query = input("Enter your query: ").strip()
                ls = self._movieService.search_id(query)

                s = ""
                for e in ls:
                    s += f"ID: {e.id}\n" \
                         f"Title: {e.title}\n" \
                         f"Genre: {e.genre}\n" \
                         f"Description: {e.description}\n\n"

                print(s)
            case 4:  # Movie/Title
                query = input("Enter your query: ").strip()
                ls = self._movieService.search_title(query)

                s = ""
                for e in ls:
                    s += f"ID: {e.id}\n" \
                         f"Title: {e.title}\n" \
                         f"Genre: {e.genre}\n" \
                         f"Description: {e.description}\n\n"

                print(s)
            case 5:  # Movie/Desc
                query = input("Enter your query: ").strip()
                ls = self._movieService.search_desc(query)

                s = ""
                for e in ls:
                    s += f"ID: {e.id}\n" \
                         f"Title: {e.title}\n" \
                         f"Genre: {e.genre}\n" \
                         f"Description: {e.description}\n\n"

                print(s)
            case 6:  # Movie/Genre
                query = input("Enter your query: ").strip()
                ls = self._movieService.search_genre(query)

                s = ""
                for e in ls:
                    s += f"ID: {e.id}\n" \
                         f"Title: {e.title}\n" \
                         f"Genre: {e.genre}\n" \
                         f"Description: {e.description}\n\n"

                print(s)
            case 7:  # Back
                self.state = AppState.MainMenu
            case _:  # Wildcard
                raise UIException("Unrecognised Command")

    @classmethod
    def print_stat_menu(cls):
        print("1. Most Rented Movies")
        print("2. Most Active Clients")
        print("3. Late Rentals")
        print("4. Back")

    def process_stat_menu(self, command):
        match command:
            case 1:  # Movie
                ls = []
                for x in self._movieService.data.data:
                    tls = self._rentalService.get_movie_rentals(x.id)
                    s = 0
                    for e in tls:
                        if e.returned_date != datetime.datetime.min:
                            s += e.rented_days
                    ls.append((x.title, s))

                    ls.sort(reverse=True, key=AppUI.sort_movies)

                s = ""
                for e in ls:
                    s += f"Title: {e[0]}\n" \
                         f"Rented Days: {e[1]}\n\n"
                print(s)

            case 2:  # Client
                ls = []
                for x in self._clientService.data.data:
                    tls = self._rentalService.get_client_rentals(x.id)
                    s = 0
                    for e in tls:
                        if e.returned_date != datetime.datetime.min:
                            s += e.rented_days
                    ls.append((x.name, s))

                    ls.sort(reverse=True, key=AppUI.sort_clients)

                s = ""
                for e in ls:
                    s += f"Name: {e[0]}\n" \
                         f"Rented Days: {e[1]}\n\n"
                print(s)
            case 3:  # Rental
                lst = []
                for x in self._clientService.data.data:
                    lst.extend(self._rentalService.get_client_passed_rentals(x.id))

                lst.sort(reverse=True, key=AppUI.sort_rentals)

                s = ""
                for e in lst:
                    s += f"ID: {e.id}\n" \
                         f"Client: {e.client_id}\n" \
                         f"Movie: {e.movie_id}\n" \
                         f"Rented Date: {e.rented_date.strftime('%d/%m/%Y')}\n" \
                         f"Due Date: {e.due_date.strftime('%d/%m/%Y')}\n"
                    s += f"Delay: {e.rented_days}\n\n"

                print(s)
            case 4:  # Exit
                self.state = AppState.MainMenu
            case _:  # Wildcard
                raise UIException("Unrecognised Command")

    @staticmethod
    def sort_rentals(e):
        return e.rented_days

    @staticmethod
    def sort_movies(e):
        return e[1]

    @staticmethod
    def sort_clients(e):
        return e[1]


class App:
    """
    Main App Class
    """

    def __init__(self, settings):
        self._ui = AppUI(settings)

    @property
    def ui(self):
        return self._ui

    def start(self):
        """
        App start
        :return: N/A
        """
        while True:
            self.ui.print_menu()
            command = AppUI.get_command()

            if command is not None:
                try:
                    self.ui.execute(command)
                except UIException as ue:
                    print(str(ue))


if __name__ == "__main__":

    settings = Settings()
    app = App(settings)

    app.start()


