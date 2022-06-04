import random

from Player import Player
from game_constants import MAP_SIZE


class GameLogic:
    """
    Клас, що представляє об'єкт ігрової логіки

    ...

    Атрибути
    --------

    player1         :   Player
        Перший гравець
    player2         :   Player
        Другий гравець
    player1_turn    :   bool
        Значення, чи ходить перший гравець на даному ході
    computer_turn   :   bool
        Значення, чи ходить комп'ютер на даному ході
    over            :   bool
        Значення, чи закінчена гра
    result          :   int
        Значення, який гравець переміг

    Методи
    ------
    ********************************************************
    ********************************************************
    def __init__(self, is_human1, is_human2)
        Конструктор класу

        Аргументи:

        1) self - об'єкт класу
        2) is_human1 - значення, чи є гравець 1 людиною
        3) is_human2 - значення, чи є гравець 2 людиною

        Повертає: None
    ********************************************************
    ********************************************************
    def make_move(self, i)
        Робить хід

        Аргументи:

        1) self - об'єкт класу
        2) I - індекс клітинки

        Повертає: None
    ********************************************************
    ********************************************************
    def computer_algorithm(self)
        Комп'ютер ходить по клітинці

        Аргументи:

        1) self - об'єкт класу

        Повертає: None
    ********************************************************
    ********************************************************
    """

    def __init__(self, is_human1, is_human2):
        self.__player1 = Player(is_human1)
        self.__player2 = Player(is_human2)
        self.__player1_turn = True
        self.__computer_turn = True if not self.player1.is_human else False
        self.__over = False
        self.__result = None

    @property
    def player1(self):
        return self.__player1

    @player1.setter
    def player1(self, value):
        self.__player1 = value

    @property
    def player2(self):
        return self.__player2

    @player2.setter
    def player2(self, value):
        self.__player2 = value

    @property
    def player1_turn(self):
        return self.__player1_turn

    @player1_turn.setter
    def player1_turn(self, value):
        self.__player1_turn = value

    @property
    def computer_turn(self):
        return self.__computer_turn

    @computer_turn.setter
    def computer_turn(self, value):
        self.__computer_turn = value

    @property
    def over(self):
        return self.__over

    @over.setter
    def over(self, value):
        self.__over = value

    @property
    def result(self):
        return self.__result

    @result.setter
    def result(self, value):
        self.__result = value

    def make_move(self, i):
        player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1
        hit = False

        if player.search[i] != 'U':
            hit = True

        elif i in opponent.indexes:
            player.search[i] = 'H'
            hit = True
            for ship in opponent.ships:
                sunk = True
                for i in ship.ship_indexes:
                    if player.search[i] == 'U':
                        sunk = False
                        break
                if sunk:
                    for i in ship.indexes:
                        player.search[i] = 'M'
                    for i in ship.ship_indexes:
                        player.search[i] = 'S'
        else:
            player.search[i] = "M"

        game_over = True
        for i in opponent.indexes:
            if player.search[i] == 'U':
                game_over = False
        self.over = game_over
        self.result = 1 if self.player1_turn else 2

        if not hit:
            self.player1_turn = not self.player1_turn

            if (self.player1.is_human and not self.player2.is_human) or (
                    not self.player1.is_human and self.player2.is_human):
                self.computer_turn = not self.computer_turn

    def computer_algorithm(self):

        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square == 'U']
        hits = [i for i, square in enumerate(search) if square == 'H']

        neighbours1 = []
        neighbours2 = []
        for u in unknown:
            if u + 1 in hits or u - 1 in hits or u - MAP_SIZE in hits or u + MAP_SIZE in hits:
                neighbours1.append(u)
            if u + 2 in hits or u - 2 in hits or u - MAP_SIZE * 2 in hits or u + MAP_SIZE * 2 in hits:
                neighbours2.append(u)

        is_both_neighbour = False
        for u in unknown:
            if u in neighbours1 and u in neighbours2:
                is_both_neighbour = True
                self.make_move(u)
                break
        if not is_both_neighbour:

            if neighbours1:
                self.make_move(random.choice(neighbours1))
            else:
                checker_board = []
                for u in unknown:
                    row = u // MAP_SIZE
                    col = u % MAP_SIZE
                    if (row + col) % 2 == 0:
                        checker_board.append(u)
                if checker_board:
                    self.make_move(random.choice(checker_board))
                else:
                    if unknown:
                        random_index = random.choice(unknown)
                        self.make_move(random_index)
        return
