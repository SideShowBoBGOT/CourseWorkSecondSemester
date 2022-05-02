import random
import inspect
import sys
import pygame
from game_colors import WHITE, GREEN, GREY, LIGHT_GREY, COLORS
from game_constants import MAP_SIZE, SHIPS_SIZES, SQ_SIZE, \
    INDENT, FONT_SIZE, WIDTH, HEIGHT, H_MARGIN, V_MARGIN
from other_functions import get_font


class Grid:
    def __init__(self, screen, player, left=0, top=0):
        self.screen = screen
        self.player = player
        self.left = left
        self.top = top
        self.right = left + MAP_SIZE * SQ_SIZE
        self.bottom = top + MAP_SIZE * SQ_SIZE

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

    # function to draw ships onto the position grids
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


class Battleship:
    def __init__(self, size, row, col, orientation):
        self.row = row
        self.col = col
        self.size = size
        self.orientation = orientation
        self.indexes = self.compute_indexes()
        self.ship_indexes = self.indexes[:size]

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


class Player:
    def __init__(self, is_human):
        self.ships = []
        self.search = ['U' for _ in range(MAP_SIZE ** 2)]  # 'U' for unknown
        self.is_human = is_human
        if not self.is_human:
            print('lala')
            self.place_ships_ai(sizes=SHIPS_SIZES)
            self.indexes = [
                ind for sub in list(map(lambda x: x.ship_indexes, self.ships))
                for ind in sub
            ]

    # check if placement of the ship is possible
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

    # place player`s ship onto the board
    def place_ships_ai(self, sizes):
        for size in sizes[::-1]:
            placed = False
            while not placed:
                # create new ship
                ship = Battleship(size=size, row=random.randint(0, MAP_SIZE - 1),
                                  col=random.randint(0, MAP_SIZE - 1),
                                  orientation=random.choice(["h", "v"]))
                # place the ship
                if self.check_ship(ship):
                    self.ships.append(ship)
                    placed = True

    def show_ships(self):
        indexes = ['-' if i not in self.indexes else 'X' for i in range(MAP_SIZE ** 2)]
        for row in range(MAP_SIZE):
            print(' '.join(indexes[(row - 1) * MAP_SIZE:row * MAP_SIZE]))


class GameLogic:
    def __init__(self, is_human1, is_human2):
        self.player1 = Player(is_human1)
        self.player2 = Player(is_human2)
        self.player1_turn = True
        self.computer_turn = True if not self.player1.is_human else False
        self.over = False
        self.result = None

    def make_move(self, i):
        player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1
        hit = False
        # check if square had been marked as "H","S" or "M" before the click
        if player.search[i] != 'U':
            hit = True
        # set miss "M" or hit "H" and "S" for sunken ship
        elif i in opponent.indexes:
            player.search[i] = 'H'
            hit = True
            # check if ship is sunk
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

        # check if game is over
        game_over = True
        for i in opponent.indexes:
            if player.search[i] == 'U':
                game_over = False
        self.over = game_over
        self.result = 1 if self.player1_turn else 2

        # change the active player
        if not hit:
            self.player1_turn = not self.player1_turn

            # switch between human and computer turns
            if (self.player1.is_human and not self.player2.is_human) or (
                    not self.player1.is_human and self.player2.is_human):
                self.computer_turn = not self.computer_turn

    def random_ai(self):
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square == 'U']
        if unknown:
            random_index = random.choice(unknown)
            self.make_move(random_index)

    def basic_ai(self):

        # setup
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square == 'U']
        hits = [i for i, square in enumerate(search) if square == 'H']

        # search in neighbourhood of hits
        unknown_with_neighbouring_hits1 = []
        unknown_with_neighbouring_hits2 = []
        for u in unknown:
            if u + 1 in hits or u - 1 in hits or u - MAP_SIZE in hits or u + MAP_SIZE in hits:
                unknown_with_neighbouring_hits1.append(u)
            if u + 2 in hits or u - 2 in hits or u - MAP_SIZE * 2 in hits or u + MAP_SIZE * 2 in hits:
                unknown_with_neighbouring_hits2.append(u)
        # pick "U" square with direct and level-2-neighbour both marked as "H"
        for u in unknown:
            if u in unknown_with_neighbouring_hits1 and u in unknown_with_neighbouring_hits2:
                self.make_move(u)
                return

        # pick square that has neighbour marked as "H"
        if unknown_with_neighbouring_hits1:
            self.make_move(random.choice(unknown_with_neighbouring_hits1))
            return

        # checker board pattern
        checker_board = []
        for u in unknown:
            row = u // MAP_SIZE
            col = u % MAP_SIZE
            if (row + col) % 2 == 0:
                checker_board.append(u)
        if checker_board:
            self.make_move(random.choice(checker_board))
            return

        # random move
        self.random_ai()


class Button:
    def __init__(self, pos, font, text_input, base_color, hovering_color, func):
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, False,
                                     self.base_color, self.hovering_color)
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
        self.func = func

    def update(self, screen):
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) \
                and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            return True
        return False

    def change_color(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) \
                and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            self.text = self.font.render(self.text_input, False, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, False, self.base_color)


class TumblerButton(Button):
    def __init__(self, pos, font, text_input, base_color, hovering_color, func):
        Button.__init__(self, pos, font, text_input, base_color, hovering_color, func)
        self.switched = False

    def change_color(self, position):
        if self.switched:
            self.text = self.font.render(self.text_input, False, self.hovering_color, self.base_color)
        else:
            self.text = self.font.render(self.text_input, False, self.base_color, self.hovering_color)


class Menu:
    def __init__(self, screen, text, buttons, funcs):
        self.screen = screen
        self.text = get_font(FONT_SIZE).render(text, False, GREY, WHITE)
        self.rect = self.text.get_rect(center=(WIDTH // 2, HEIGHT // 5))
        self.buttons = []
        for button, func in zip(enumerate(buttons), funcs):
            self.buttons.append(button[1][1](pos=(WIDTH // 2, HEIGHT // 3 + FONT_SIZE * button[0]),
                                             text_input=button[1][0],
                                             font=get_font(FONT_SIZE), base_color=WHITE,
                                             hovering_color=LIGHT_GREY, func=func))
        self.buttons.append(Button(pos=(WIDTH // 2, HEIGHT // 3 + FONT_SIZE * (button[0] + 1)),
                                   text_input='QUIT',
                                   font=get_font(FONT_SIZE), base_color=WHITE,
                                   hovering_color=LIGHT_GREY, func=None))

    def draw(self, **kwargs):
        while True:
            self.screen.fill(GREY)
            self.screen.blit(self.text, self.rect)
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.change_color(mouse_pos)
                button.update(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.check_for_input(mouse_pos):
                            if button.text_input == 'QUIT':
                                return
                            elif button.__class__.__name__ == Button.__name__:
                                if inspect.signature(button.func).parameters:
                                    button.func(**(kwargs[button.text_input]))
                                else:
                                    button.func()
                            elif button.__class__.__name__ == TumblerButton.__name__:
                                button.switched = not button.switched
            pygame.display.update()


class Board:
    def __init__(self, screen, options_menu, game_logic):
        self.screen = screen
        self.game_logic = game_logic
        self.options_menu = options_menu
        self.search_grid1 = Grid(screen=self.screen, player=self.game_logic.player1)
        self.search_grid2 = Grid(screen=self.screen, player=self.game_logic.player2,
                                 left=(WIDTH - H_MARGIN) // 2 + H_MARGIN,
                                 top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)
        self.position_grid1 = Grid(screen=self.screen, player=self.game_logic.player1,
                                   top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)
        self.position_grid2 = Grid(screen=self.screen, player=self.game_logic.player2,
                                   left=(WIDTH - H_MARGIN) // 2 + H_MARGIN)
        self.set_ships_button = TumblerButton(pos=(WIDTH // 2, SQ_SIZE * MAP_SIZE),
                                              text_input='SET SHIPS', font=get_font(FONT_SIZE // 3),
                                              base_color=GREY, hovering_color=WHITE, func=None)
        self.ship_size_buttons = []
        self.used_ship_size_buttons = []
        for i, size in enumerate(SHIPS_SIZES):
            x, y = i % 4, i // 4
            print(x, y)
            self.ship_size_buttons.append(TumblerButton(pos=(self.search_grid1.right + x * SQ_SIZE + SQ_SIZE // 2,
                                                             self.search_grid1.bottom + y * SQ_SIZE + SQ_SIZE),
                                                        font=get_font(SQ_SIZE), text_input=str(size), base_color=GREY,
                                                        hovering_color=WHITE, func=None))

    def draw(self, draw_buttons):
        self.screen.fill(GREY)
        # draw_grid search grids
        self.search_grid1.draw_grid(search=True)
        self.search_grid2.draw_grid(search=True)
        # draw labels for players
        text1 = "PLAYER1"
        textbox1 = get_font(SQ_SIZE).render(text1, False, WHITE, GREY)
        self.screen.blit(textbox1, (self.search_grid1.left, self.search_grid1.bottom))
        text2 = "PLAYER2"
        textbox2 = get_font(SQ_SIZE).render(text2, False, WHITE, GREY)
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
            textbox = get_font(SQ_SIZE * MAP_SIZE).render(text, False, WHITE, GREY)
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


class Game:
    def __init__(self, screen, options_menu):
        self.screen = screen
        self.options_menu = options_menu
        self.game_logic = None
        self.board = None

    def prepare_to_play(self):
        # set game_logic and board for game
        self.game_logic = GameLogic(self.options_menu.buttons[0].switched,
                                    self.options_menu.buttons[1].switched)
        self.board = Board(self.screen, self.options_menu, self.game_logic)
        # check if player is human
        for player_number, player in enumerate((self.game_logic.player1, self.game_logic.player2)):
            # if human then player must place its ships onto the board
            if player.is_human:
                # while all player`s ships are not placed, it can not start game
                while not self.board.set_ships_button.switched:
                    placing_ships = False
                    GAME_MOUSE_POSITION = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        # escape key to close the animation
                        if event.type == pygame.K_ESCAPE:
                            return
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # click on ship_size_buttons and chose size of a ship
                            for i1, button in enumerate(self.board.ship_size_buttons):
                                if button.check_for_input(GAME_MOUSE_POSITION):
                                    button.switched = not button.switched
                                    button.change_color(GAME_MOUSE_POSITION)
                                    for i2, other_button in enumerate(self.board.ship_size_buttons):
                                        if i2 != i1:
                                            other_button.switched = False
                                            other_button.change_color(GAME_MOUSE_POSITION)
                                    break
                            # chose square to put ship onto
                            for i1, button in enumerate(self.board.ship_size_buttons):
                                if button.switched:
                                    placing_ships = True
                                    row, col, index = self.board.__dict__[f'position_grid{player_number + 1}']. \
                                        check_for_input(GAME_MOUSE_POSITION)
                                    if index is not None:
                                        orientation = 'h' if pygame.mouse.get_pressed()[0] else 'v'
                                        ship = Battleship(size=int(button.text_input), row=row,
                                                          col=col, orientation=orientation)
                                        if player.check_ship(ship):
                                            player.ships.append(ship)
                                            self.board.used_ship_size_buttons. \
                                                append(self.board.ship_size_buttons.pop(i1))
                                            self.board.order_buttons()

                            # chose ship to be replaced
                            if not placing_ships:
                                for i1, ship in enumerate(player.ships):
                                    row, col, index = self.board.__dict__[f'position_grid{player_number + 1}']. \
                                        check_for_input(GAME_MOUSE_POSITION)
                                    if index in ship.ship_indexes:
                                        for i2, used_button in enumerate(self.board.used_ship_size_buttons):
                                            if ship.size == int(used_button.text_input):
                                                used_button.switched = False
                                                used_button.change_color(GAME_MOUSE_POSITION)
                                                self.board.ship_size_buttons. \
                                                    append(self.board.used_ship_size_buttons.pop(i2))
                                                break
                                        self.board.order_buttons()
                                        player.ships.pop(i1)

                            # check if set_button is pressed
                            if self.board.set_ships_button.check_for_input(GAME_MOUSE_POSITION) \
                                    and not self.board.ship_size_buttons:
                                self.board.set_ships_button.switched = not self.board.set_ships_button.switched

                    self.board.draw(draw_buttons=True)
                    pygame.display.update()

                self.board.ship_size_buttons, self.board.used_ship_size_buttons = \
                    self.board.used_ship_size_buttons, self.board.ship_size_buttons

                self.board.set_ships_button.switched = not self.board.set_ships_button.switched
                # player`s ships being placed, program sets player`s indexes
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

                # user mouse clicks
                if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                    mouse_pos = pygame.mouse.get_pos()
                    if not self.game_logic.over:
                        row, col, index = self.board.check_for_input(mouse_pos, self.game_logic.player1_turn)
                        if index is not None:
                            self.game_logic.make_move(index)
                if event.type == pygame.KEYDOWN:

                    # escape key to close the animation
                    if event.key == pygame.K_ESCAPE:
                        return
                    # space bar to pause and unpause the animation
                    if event.key == pygame.K_SPACE and not self.game_logic.over:
                        pause = not pause

            if not pause:
                self.board.draw(draw_buttons=False)
                # computer moves
                if not self.game_logic.over and self.game_logic.computer_turn:
                    self.game_logic.basic_ai()

                # game over message
                if self.game_logic.over:
                    text = "Player " + str(self.game_logic.result) + " wins!"
                    textbox = get_font(FONT_SIZE).render(text, False, GREY, WHITE)
                    self.screen.blit(textbox, (WIDTH // 5, HEIGHT // 2.22))
            elif pause and not self.game_logic.over:
                text = "Pause"
                textbox = get_font(FONT_SIZE).render(text, False, GREY, WHITE)
                self.screen.blit(textbox, (WIDTH // 2.7, HEIGHT // 2.22))
            pygame.time.delay(0)
            pygame.display.update()