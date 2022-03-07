import random
from game_constants import MAP_SIZE, SHIPS_SIZES


class Battleship:
    def __init__(self, size):
        self.row = random.randint(0, MAP_SIZE - 1)
        self.col = random.randint(0, MAP_SIZE - 1)
        self.size = size
        self.orientation = random.choice(["h", "v"])
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
    def __init__(self):
        self.ships = []
        self.search = ['U' for _ in range(MAP_SIZE ** 2)]  # 'U' for unknown

        self.place_ships(sizes=SHIPS_SIZES)
        self.indexes = [
            ind for sub in list(map(lambda x: x.ship_indexes, self.ships))
            for ind in sub
        ]


    def place_ships(self, sizes):
        for size in sizes:
            placed = False
            while not placed:
                # create new ship
                ship = Battleship(size)
                # check if placement is possible
                possible = True
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
                # place the ship
                if possible:
                    self.ships.append(ship)
                    placed = True

    def show_ships(self):
        indexes = ['-' if i not in self.indexes else 'X' for i in range(MAP_SIZE ** 2)]
        for row in range(MAP_SIZE):
            print(' '.join(indexes[(row - 1) * MAP_SIZE:row * MAP_SIZE]))


class Game:
    def __init__(self, is_human1, is_human2):
        self.is_human1 = is_human1
        self.is_human2 = is_human2
        self.player1 = Player()
        self.player2 = Player()
        self.player1_turn = True
        self.computer_turn = True if not self.is_human1 else False
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
            if (self.is_human1 and not self.is_human2) or (not self.is_human1 and self.is_human2):
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
    def __init__(self, pos, font, text_input, base_color, hovering_color):
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, False,
                                     self.base_color, self.hovering_color)
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

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


class ButtonShip(Button):
    def __init__(self,  pos, font, text_input, base_color, hovering_color):
        Button.__init__(self, pos, font, text_input, base_color, hovering_color)
        self.switched = False

    def change_color(self, position):
        if self.switched:
            Button.change_color(self, position)