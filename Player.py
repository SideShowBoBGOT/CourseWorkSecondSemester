import random
from game_constants import MAP_SIZE, SHIPS_SIZES
from Battleship import Battleship


class Player:
    """
    Клас, що представляє гравця

    ...

    Атрибути
    --------

    is_human    :   bool
        Значення, чи є гравець людиною

    Методи
    ------
    ********************************************************
    ********************************************************
    def __init__(self, is_human)
        Конструктор класу

        Аргументи:

        1) self - об'єкт класу
        2) is_human - значення, чи є гравець людиною

        Повертає: None
    ********************************************************
    ********************************************************
    check_ship(self, ship)
        Перевіряє, чи є розташування корабля можливим

        Аргументи:

        1) self - об'єкт класу
        2) ship - об'єкт класу Battleship

        Повертає:

        possible  : bool
    ********************************************************
    ********************************************************
    def place_ships_ai(self, sizes)
        Комп'ютер розставляє кораблі

        Аргументи:

        1) self - об'єкт класу
        2) sizes - список розмірів кораблів

        Повертає: None
    ********************************************************
    ********************************************************
    """

    def __init__(self, is_human):
        self.__ships = []
        self.__search = ['U' for _ in range(MAP_SIZE ** 2)]  # 'U' for unknown
        self.__is_human = is_human
        if not self.is_human:
            self.place_ships_ai(sizes=SHIPS_SIZES)
            self.__indexes = [
                ind for sub in list(map(lambda x: x.ship_indexes, self.ships))
                for ind in sub
            ]

    @property
    def ships(self):
        return self.__ships

    @ships.setter
    def ships(self, value):
        self.__ships = value

    @property
    def search(self):
        return self.__search

    @search.setter
    def search(self, value):
        self.__search = value

    @property
    def is_human(self):
        return self.__is_human

    @is_human.setter
    def is_human(self, value):
        self.__is_human = value

    @property
    def indexes(self):
        return self.__indexes

    @indexes.setter
    def indexes(self, value):
        self.__indexes = value

    def check_ship(self, ship):
        possible = True
        size = ship.size
        for i in ship.indexes[:size]:
            # indexes must be less than MAP_SIZE**2
            if i >= MAP_SIZE ** 2:
                possible = False
                break
            # ships cannot go beyond grid
            new_row = i // MAP_SIZE
            if ship.orientation == 'h' and new_row != ship.row:
                possible = False
                break
            # ships cannot intersect
            for other_ship in self.ships:
                if i in other_ship.indexes:
                    possible = False
                    break
            if not possible:
                break
        return possible

    def place_ships_ai(self, sizes):
        all_placed = False
        while not all_placed:
            for size in sizes[::-1]:
                placed = False
                counter = 0
                while not placed:
                    # create new ship
                    ship = Battleship(size=size, row=random.randint(0, MAP_SIZE - 1),
                                      col=random.randint(0, MAP_SIZE - 1),
                                      orientation=random.choice(["h", "v"]))
                    # place the ship
                    if self.check_ship(ship):
                        self.ships.append(ship)
                        placed = True
                    counter += 1
                    if counter > 100:
                        break
                if not placed:
                    self.ships.clear()
                    break
            if self.ships:
                all_placed = True
