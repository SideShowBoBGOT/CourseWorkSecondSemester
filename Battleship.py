from game_constants import MAP_SIZE


class Battleship:
    """
    Клас, що представляє корабель

    ...

    Атрибути
    --------

    row             :   int
        Рядок, у якому розташовується ніс корабля
    col             :   int
        Колонка, у якій розташовується ніс корабля
    size            :   int
        Розмір корабля
    orientation     :   str
        Оріентація корабля
    indexes         :   list
        Список індексів, які займає корабель повністю
    ship_indexes    :   list
        Список індексів, які власне займає лише корабель

    Методи
    ------

    ********************************************************
    ********************************************************
    def __init__(self, size, row, col, orientation)
        Конструктор класу

        Аргументи:

        1) self - об'єкт класу
        2) size - розмір
        3) row - рядок
        4) col - колонка
        5) orientation - орієнтація

        Повертає: None
    ********************************************************
    ********************************************************
    def compute_indexes(self)
        Розраховує розташування корабля

        Аргументи:

        1) self - об'єкт класу

        Повертає: None
    ********************************************************
    ********************************************************
    """

    def __init__(self, size, row, col, orientation):
        self.__row = row
        self.__col = col
        self.__size = size
        self.__orientation = orientation
        self.__indexes = self.compute_indexes()
        self.__ship_indexes = self.indexes[:size]

    @property
    def row(self):
        return self.__row

    @row.setter
    def row(self, value):
        self.__row = value

    @property
    def col(self):
        return self.__col

    @col.setter
    def col(self, value):
        self.__col = value

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    @property
    def orientation(self):
        return self.__orientation

    @orientation.setter
    def orientation(self, value):
        self.__orientation = value

    @property
    def indexes(self):
        return self.__indexes

    @indexes.setter
    def indexes(self, value):
        self.__indexes = value

    @property
    def ship_indexes(self):
        return self.__ship_indexes

    @ship_indexes.setter
    def ship_indexes(self, value):
        self.__ship_indexes = value

    def compute_indexes(self):
        start_index = self.row * MAP_SIZE + self.col
        result_indexes = []
        if self.orientation == 'h':
            indexes = [start_index + i for i in range(self.size)]
            top_left_padding = [indexes[0] - 1 - MAP_SIZE]
            left_padding = [indexes[0] - 1]
            bottom_left_padding = [indexes[0] - 1 + MAP_SIZE]
            bottom_padding = [i + MAP_SIZE for i in indexes]
            bottom_right_padding = [indexes[-1] + 1 + MAP_SIZE]
            right_padding = [indexes[-1] + 1]
            top_right_padding = [indexes[-1] + 1 - MAP_SIZE]
            top_padding = [i - MAP_SIZE for i in indexes]
            result_indexes += indexes
        elif self.orientation == 'v':
            indexes = [start_index + i * MAP_SIZE for i in range(self.size)]
            top_left_padding = [indexes[0] - 1 - MAP_SIZE]
            left_padding = [i - 1 for i in indexes]
            bottom_left_padding = [indexes[-1] - 1 + MAP_SIZE]
            bottom_padding = [indexes[-1] + MAP_SIZE]
            bottom_right_padding = [indexes[-1] + 1 + MAP_SIZE]
            right_padding = [i + 1 for i in indexes]
            top_right_padding = [indexes[0] + 1 - MAP_SIZE]
            top_padding = [indexes[0] - MAP_SIZE]
            result_indexes += indexes
        if left_padding[0] // MAP_SIZE == indexes[0] // MAP_SIZE:
            result_indexes += left_padding
        if top_padding[0] >= 0:
            result_indexes += top_padding
        if left_padding[0] // MAP_SIZE == indexes[0] // MAP_SIZE and top_padding[0] >= 0:
            result_indexes += top_left_padding
        if bottom_padding[0] < MAP_SIZE ** 2:
            result_indexes += bottom_padding
        if left_padding[0] // MAP_SIZE == indexes[0] // MAP_SIZE and bottom_padding[0] < MAP_SIZE ** 2:
            result_indexes += bottom_left_padding
        if right_padding[0] // MAP_SIZE == indexes[0] // MAP_SIZE:
            result_indexes += right_padding
        if right_padding[0] // MAP_SIZE == indexes[0] // MAP_SIZE and bottom_padding[0] < MAP_SIZE ** 2:
            result_indexes += bottom_right_padding
        if right_padding[0] // MAP_SIZE == indexes[0] // MAP_SIZE and top_padding[0] >= 0:
            result_indexes += top_right_padding
        return result_indexes
