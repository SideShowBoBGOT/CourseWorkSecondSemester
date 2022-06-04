import sys
import pygame

from Battleship import Battleship
from Board import Board
from GameLogic import GameLogic
from game_colors import WHITE, GREEN, GREY
from game_constants import FONT_SIZE, WIDTH, HEIGHT
from other_functions import get_font


class Game:
    """
    Клас, що представляє гру

    ...

    Атрибут
    -------

    screen          : pygame.Surface
        Екран, на який малюються об'єкти гри
    options_menu    : Menu
        Об'єкт меню опцій
    game_logic      : GameLogic
        Об'єкт ігрової логіки
    board           : Board
        Об'єкт дошки

    Мутоди
    ------

    ********************************************************
    ********************************************************
    def __init__(self, screen, options_menu)
        Розташовує кнопки у правильному порядку

        Аргументи:

        1) self - об'єкт класу
        2) sceen - екран
        3) options_menu - об'єкт класу Menu

        Повертає: None
    ********************************************************
    ********************************************************
    def prepare_to_play(self)
        Підготовує гру до початку

        Аргументи:

        1) self - об'єкт класу

        Повертає: None
    ********************************************************
    ********************************************************
    def play(self)
        Підготовує гру до початку

        Аргументи:

        1) self - об'єкт класу

        Повертає: None
    ********************************************************
    ********************************************************
    """

    def __init__(self, screen, options_menu):
        self.__screen = screen
        self.__options_menu = options_menu
        self.__game_logic = None
        self.__board = None

    def prepare_to_play(self):
        self.__game_logic = GameLogic(self.__options_menu.buttons[0].switched,
                                      self.__options_menu.buttons[1].switched)
        self.__board = Board(self.__screen, self.__options_menu, self.__game_logic)
        for player_number, player in enumerate((self.__game_logic.player1, self.__game_logic.player2)):
            if player.is_human:
                self.__board.order_buttons()
                while not self.__board.set_ships_button.switched:
                    placing_ships = False
                    GAME_MOUSE_POSITION = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if event.type == pygame.K_ESCAPE:
                            return
                        if event.type == pygame.MOUSEBUTTONDOWN:

                            for i1, button in enumerate(self.__board.ship_size_buttons):
                                if button.check_for_input(GAME_MOUSE_POSITION):
                                    button.switched = not button.switched
                                    for i2, other_button in enumerate(self.__board.ship_size_buttons):
                                        if i2 != i1:
                                            other_button.switched = False
                                    break

                            for i1, button in enumerate(self.__board.ship_size_buttons):
                                if button.switched:
                                    placing_ships = True
                                    if player_number + 1 == 1:
                                        row, col, index = self.__board.position_grid1.check_for_input(
                                            GAME_MOUSE_POSITION)
                                    elif player_number + 1 == 2:
                                        row, col, index = self.__board.position_grid2.check_for_input(
                                            GAME_MOUSE_POSITION)
                                    if index is not None:
                                        orientation = 'h' if pygame.mouse.get_pressed()[0] else 'v'
                                        ship = Battleship(size=int(button.text_input), row=row,
                                                          col=col, orientation=orientation)
                                        if player.check_ship(ship):
                                            player.ships.append(ship)
                                            self.__board.used_ship_size_buttons. \
                                                append(self.__board.ship_size_buttons.pop(i1))
                                            self.__board.order_buttons()

                            if not placing_ships:
                                for i1, ship in enumerate(player.ships):
                                    if player_number + 1 == 1:
                                        row, col, index = self.__board.position_grid1.check_for_input(
                                            GAME_MOUSE_POSITION)
                                    elif player_number + 1 == 2:
                                        row, col, index = self.__board.position_grid2.check_for_input(
                                            GAME_MOUSE_POSITION)
                                    if index in ship.ship_indexes:
                                        for i2, used_button in enumerate(self.__board.used_ship_size_buttons):
                                            if ship.size == int(used_button.text_input):
                                                used_button.switched = False
                                                self.__board.ship_size_buttons. \
                                                    append(self.__board.used_ship_size_buttons.pop(i2))
                                                break
                                        self.__board.order_buttons()
                                        player.ships.pop(i1)

                            if self.__board.set_ships_button.check_for_input(GAME_MOUSE_POSITION) \
                                    and not self.__board.ship_size_buttons:
                                self.__board.set_ships_button.switched = not self.__board.set_ships_button.switched

                    self.__board.draw(draw_buttons=True)
                    pygame.display.update()

                self.__board.ship_size_buttons, self.__board.used_ship_size_buttons = \
                    self.__board.used_ship_size_buttons, self.__board.ship_size_buttons
                for button in self.__board.ship_size_buttons:
                    button.switched = not button.switched
                self.__board.set_ships_button.switched = not self.__board.set_ships_button.switched
                player.indexes = [
                    ind for sub in list(map(lambda x: x.ship_indexes, player.ships))
                    for ind in sub
                ]
        self.play()

    def play(self):
        pause = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                    mouse_pos = pygame.mouse.get_pos()
                    if not self.__game_logic.over:
                        row, col, index = self.__board.check_for_input(mouse_pos, self.__game_logic.player1_turn)
                        if index is not None:
                            self.__game_logic.make_move(index)
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        return

                    if event.key == pygame.K_SPACE and not self.__game_logic.over:
                        pause = not pause

            if not pause:
                self.__board.draw(draw_buttons=False)

                if not self.__game_logic.over and self.__game_logic.computer_turn:
                    self.__game_logic.computer_algorithm()

                if self.__game_logic.over:
                    text = "Player " + str(self.__game_logic.result) + " wins!"
                    textbox = get_font(FONT_SIZE).render(text, False, GREY, WHITE)
                    self.__screen.blit(textbox, (WIDTH // 5, HEIGHT // 2.22))
            elif pause and not self.__game_logic.over:
                text = "Pause"
                textbox = get_font(FONT_SIZE).render(text, False, GREY, WHITE)
                self.__screen.blit(textbox, (WIDTH // 2.7, HEIGHT // 2.22))
            pygame.time.delay(0)
            pygame.display.update()
