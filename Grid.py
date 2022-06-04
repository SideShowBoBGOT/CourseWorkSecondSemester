import pygame
from game_colors import WHITE, GREEN, COLORS
from game_constants import MAP_SIZE, SQ_SIZE, INDENT


class Grid:
    """
    Клас, що використовується для представлення градки

    ...

    Атрибути
    --------

    screen  :   pygame.display.Surface
        екран, на який буде намальована градка
    player  :   Player
        гравець, який володіє даною градкою
    left    :   int
        відступ від лівого боку екрана
    top     :   int
        відступ від верху екрана

    Методи
    ------
    ********************************************************
    ********************************************************
    __init__(self, screen, player, left=0, top=0)
        Конструктор класу Grid

        Аргументи:

        1) self - об'єкт класу
        2) screen - екран
        3) player - гравець
        4) top - зміщення догори
        5) left - зміщення наліво

        Повертає: None
    ********************************************************
    ********************************************************
    def draw_grid(self, search=False)
        Відображає об'єкт класу на екрані

        Аргументи:

        1) self - об'єкт класу
        2) search - поле гравця

        Повертає: None
    ********************************************************
    ********************************************************
    def draw_grid(self, search=False)
        Відображає об'єкт класу на екрані

        Аргументи:

        1) self - об'єкт класу
        2) search - поле гравця

        Повертає: None
    ********************************************************
    ********************************************************
    def check_for_input(self, position)
        Реєструє нитискання на градку

        Аргументи:

        1) self - об'єкт класу
        2) position - позиція миші

        Повертає: None
    ********************************************************
    ********************************************************
    def draw_ships(self)
        Відображає кораблі

        Аргументи:

        1) self - об'єкт класу

        Повертає: None
    ********************************************************
    ********************************************************
    """

    def __init__(self, screen, player, left=0, top=0):
        self.__screen = screen
        self.__player = player
        self.__left = left
        self.__top = top
        self.__right = left + MAP_SIZE * SQ_SIZE
        self.__bottom = top + MAP_SIZE * SQ_SIZE

    @property
    def screen(self):
        return self.__screen

    @screen.setter
    def screen(self, value):
        self.__screen = value

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, value):
        self.__player = value

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, value):
        self.__left = value

    @property
    def top(self):
        return self.__top

    @top.setter
    def top(self, value):
        self.__top = value

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, value):
        self.__right = value

    @property
    def bottom(self):
        return self.__bottom

    @bottom.setter
    def bottom(self, value):
        self.__bottom = value

    def draw_grid(self, search=False):
        for i in range(MAP_SIZE ** 2):
            x = self.left + i % MAP_SIZE * SQ_SIZE
            y = self.top + i // MAP_SIZE * SQ_SIZE
            square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(self.screen, WHITE, square, width=3)
            if search:
                x += SQ_SIZE // 2
                y += SQ_SIZE // 2
                pygame.draw.circle(self.screen,
                                   COLORS[self.player.search[i]],
                                   (x, y), radius=SQ_SIZE // 4)

    def check_for_input(self, position):
        x1, y1 = self.left, self.top
        x2 = self.left + (MAP_SIZE ** 2 - 1) % MAP_SIZE * SQ_SIZE
        y2 = self.top + (MAP_SIZE ** 2 - 1) // MAP_SIZE * SQ_SIZE
        top_left_square = pygame.Rect(x1, y1, SQ_SIZE, SQ_SIZE)
        bottom_right_square = pygame.Rect(x2, y2, SQ_SIZE, SQ_SIZE)
        row, col, index = None, None, None
        if position[0] in range(top_left_square.left, bottom_right_square.right) \
                and position[1] in range(top_left_square.top, bottom_right_square.bottom):
            row = (position[1] - self.top) // SQ_SIZE
            col = (position[0] - self.left) // SQ_SIZE
            index = row * MAP_SIZE + col
        return row, col, index

    def draw_ships(self):
        for ship in self.player.ships:
            x = self.left + ship.col * SQ_SIZE + INDENT
            y = self.top + ship.row * SQ_SIZE + INDENT
            if ship.orientation == 'h':
                width = ship.size * SQ_SIZE - INDENT * 2
                height = SQ_SIZE - INDENT * 2
            elif ship.orientation == 'v':
                width = SQ_SIZE - INDENT * 2
                height = ship.size * SQ_SIZE - INDENT * 2
            rectangle = pygame.Rect(x, y, width, height)
            pygame.draw.rect(self.screen, GREEN, rectangle, border_radius=15)
