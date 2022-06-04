from Grid import Grid
from TumblerButton import TumblerButton
from game_colors import WHITE, GREEN, GREY
from game_constants import MAP_SIZE, SHIPS_SIZES, SQ_SIZE, FONT_SIZE, WIDTH, HEIGHT, H_MARGIN, V_MARGIN
from other_functions import get_font


class Board:
    """
    Клас, що представляє дошку

    ...

    Атрибути
    --------

    screen                      :   pygame.Surface
        Екран, на який малюється дошка
    game_logic                  :   GameLogic
        Об'єкт ігрової логіки
    options_menu                :   Menu
        Об'єкт меню опцій
    search_grid1                :   Grid
        Пошукова градка першого гравця
    search_grid2                :    Grid
        Пошукова градка другого гравця
    position_grid1              :   Grid
        Позиційна градка першого гравця
    position_grid2              :    Grid
        Позиційна градка другого гравця
    set_ships_button            :   TumblerButton
        Кнопка дя закінчення розставлення кораблів
    ship_size_buttons           :   list
        Кнопки, які позначають кораблі
    used_ship_size_buttons      :   list
        Використані кнопки, що позначають кораблі

    Методи
    ------

    ********************************************************
    ********************************************************
    def __init__(self, screen, text, buttons, funcs)
        Конструктор класу

        Аргументи:

        1) self - об'єкт класу
        2) screen - екран
        3) options_menu - об'єкт класу Menu
        4) game_logic - об'єкт класу GameLogic

        Повертає: None
    ********************************************************
    ********************************************************
    draw(self, draw_buttons)
        Відображає дошку на екрані

        Аргументи:

        1) self - об'єкт класу
        2) draw_buttons - значення, чи треба відображати об'єкти класу Button

        Повертає: None
    ********************************************************
    ********************************************************
    def check_for_input(self, position, player1_turn)
        Реєструє нитискання на дошку

        Аргументи:

        1) self - об'єкт класу
        2) position - позиція миші

        Повертає: None
    ********************************************************
    ********************************************************
    def order_buttons(self)
        Розташовує кнопки у правильному порядку

        Аргументи:

        1) self - об'єкт класу

        Повертає: None
    ********************************************************
    ********************************************************
    """

    def __init__(self, screen, options_menu, game_logic):
        self.__screen = screen
        self.__game_logic = game_logic
        self.__options_menu = options_menu
        self.__search_grid1 = Grid(screen=self.__screen, player=self.__game_logic.player1)
        self.__search_grid2 = Grid(screen=self.__screen, player=self.__game_logic.player2,
                                   left=(WIDTH - H_MARGIN) // 2 + H_MARGIN,
                                   top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)
        self.__position_grid1 = Grid(screen=self.__screen, player=self.__game_logic.player1,
                                     top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)
        self.__position_grid2 = Grid(screen=self.__screen, player=self.__game_logic.player2,
                                     left=(WIDTH - H_MARGIN) // 2 + H_MARGIN)
        self.__set_ships_button = TumblerButton(pos=(WIDTH // 2, SQ_SIZE * MAP_SIZE),
                                                text_input='SET SHIPS', font=get_font(FONT_SIZE // 3),
                                                base_color=GREY, hovering_color=WHITE, func=None)
        self.__ship_size_buttons = []
        self.__used_ship_size_buttons = []
        for i, size in enumerate(SHIPS_SIZES):
            x, y = i % 4, i // 4
            self.__ship_size_buttons.append(TumblerButton(pos=(self.__search_grid1.right + x * SQ_SIZE + SQ_SIZE // 2,
                                                               self.__search_grid1.bottom + y * SQ_SIZE + SQ_SIZE),
                                                          font=get_font(int(SQ_SIZE // 1.5)), text_input=str(size),
                                                          base_color=GREY,
                                                          hovering_color=WHITE, func=None))

    @property
    def screen(self):
        return self.__screen

    @screen.setter
    def screen(self, value):
        self.__screen = value

    @property
    def game_logic(self):
        return self.__game_logic

    @game_logic.setter
    def game_logic(self, value):
        self.__game_logic = value

    @property
    def game_logic(self):
        return self.__game_logic

    @game_logic.setter
    def game_logic(self, value):
        self.__game_logic = value

    @property
    def options_menu(self):
        return self.__options_menu

    @options_menu.setter
    def options_menu(self, value):
        self.__options_menu = value

    @property
    def search_grid1(self):
        return self.__search_grid1

    @search_grid1.setter
    def search_grid1(self, value):
        self.__search_grid1 = value

    @property
    def search_grid2(self):
        return self.__search_grid2

    @search_grid2.setter
    def search_grid2(self, value):
        self.__search_grid2 = value

    @property
    def position_grid1(self):
        return self.__position_grid1

    @position_grid1.setter
    def position_grid1(self, value):
        self.__position_grid1 = value

    @property
    def position_grid2(self):
        return self.__position_grid2

    @position_grid2.setter
    def position_grid2(self, value):
        self.__position_grid2 = value

    @property
    def set_ships_button(self):
        return self.__set_ships_button

    @set_ships_button.setter
    def set_ships_button(self, value):
        self.__set_ships_button = value

    @property
    def ship_size_buttons(self):
        return self.__ship_size_buttons

    @ship_size_buttons.setter
    def ship_size_buttons(self, value):
        self.__ship_size_buttons = value

    @property
    def used_ship_size_buttons(self):
        return self.__used_ship_size_buttons

    @used_ship_size_buttons.setter
    def used_ship_size_buttons(self, value):
        self.__used_ship_size_buttons = value

    def draw(self, draw_buttons):
        self.screen.fill(GREY)
        # draw_grid search grids
        self.search_grid1.draw_grid(search=True)
        self.search_grid2.draw_grid(search=True)
        # draw labels for players
        text1 = "PLAYER1"
        textbox1 = get_font(int(SQ_SIZE // 1.5)).render(text1, False, WHITE, GREY)
        self.screen.blit(textbox1, (self.search_grid1.left, self.search_grid1.bottom))
        text2 = "PLAYER2"
        textbox2 = get_font(int(SQ_SIZE // 1.5)).render(text2, False, WHITE, GREY)
        self.screen.blit(textbox2, (self.position_grid2.left, self.position_grid2.bottom))
        # draw_grid buttons
        if draw_buttons:
            if self.ship_size_buttons:
                for button in self.ship_size_buttons:
                    button.update(self.screen)
            else:
                self.set_ships_button.update(self.screen)
        if self.game_logic.player1.is_human ^ self.game_logic.player2.is_human:
            text = "PC"
            textbox = get_font(int(SQ_SIZE * MAP_SIZE // 1.5)).render(text, False, WHITE, GREY)
            if self.game_logic.player1.is_human:
                self.position_grid1.draw_grid()
                self.position_grid1.draw_ships()
                self.screen.blit(textbox, (self.position_grid2.left, self.position_grid2.top))
            else:
                self.position_grid2.draw_grid()
                self.position_grid2.draw_ships()
                self.screen.blit(textbox, (self.position_grid1.left, self.position_grid1.top))
        else:
            # draw_grid position grids
            self.position_grid1.draw_grid()
            self.position_grid2.draw_grid()
            # draw_grid ships onto position grids
            self.position_grid1.draw_ships()
            self.position_grid2.draw_ships()

    def check_for_input(self, position, player1_turn):
        row, col, index = None, None, None
        if player1_turn:
            row, col, index = self.search_grid1.check_for_input(position)
        elif not player1_turn:
            row, col, index = self.search_grid2.check_for_input(position)
        return row, col, index

    def order_buttons(self):
        self.ship_size_buttons.sort(key=lambda x: int(x.text_input), reverse=True)
        for i, button in enumerate(self.ship_size_buttons):
            x, y = i % 4, i // 4
            button.text_rect = button.text.get_rect(
                center=(SQ_SIZE * MAP_SIZE + x * SQ_SIZE + SQ_SIZE // 2,
                        SQ_SIZE * MAP_SIZE + y * SQ_SIZE + SQ_SIZE))
