import random
from constants import MAP_SIZE, SHIPS_SIZES


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
        if bottom_padding[0] <= MAP_SIZE ** 2:
            result_indexes += bottom_padding
        if left_padding[0] // MAP_SIZE == indexes[0] // MAP_SIZE and bottom_padding[0] <= MAP_SIZE ** 2:
            result_indexes += bottom_left_padding
        if right_padding[0] // MAP_SIZE == indexes[0] // MAP_SIZE:
            result_indexes += right_padding
        if right_padding[0] // MAP_SIZE == indexes[0] // MAP_SIZE and bottom_padding[0] <= MAP_SIZE ** 2:
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
    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.player1_turn = True
        self.over = False

    def make_move(self, i):
        player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1

        # set miss "M" or hit "H" and "S" for sunken ship
        if i in opponent.indexes:
            player.search[i] = 'H'

            # check if ship is sunk
            for ship in opponent.ships:
                sunk = True
                for i in ship.ship_indexes:
                    if player.search[i] == 'U':
                        sunk = False
                        break
                if sunk:
                    for i in ship.ship_indexes:
                        player.search[i] = 'S'
        else:
            player.search[i] = "M"

        # change the active player
        self.player1_turn = not self.player1_turn

