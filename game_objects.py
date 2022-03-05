import random


class Battleship:
    def __init__(self, size):
        self.row = random.randint(0, 10)
        self.col = random.randint(0, 10)
        self.size = size
        self.orientation = random.choice(["h", "v"])
        self.indexes = self.compute_indexes()
        self.ship_indexes = self.indexes[:size]

    def compute_indexes(self):
        start_index = self.row * 11 + self.col
        result_indexes = []
        if self.orientation == 'h':
            indexes = [start_index + i for i in range(self.size)]
            top_left_padding = [indexes[0] - 1 - 11]
            left_padding = [indexes[0] - 1]
            bottom_left_padding = [indexes[0] - 1 + 11]
            bottom_padding = [i + 11 for i in indexes]
            bottom_right_padding = [indexes[-1] + 1 + 11]
            right_padding = [indexes[-1] + 1]
            top_right_padding = [indexes[-1] + 1 - 11]
            top_padding = [i - 11 for i in indexes]
            result_indexes += indexes
        elif self.orientation == 'v':
            indexes = [start_index + i * 11 for i in range(self.size)]
            top_left_padding = [indexes[0] - 1 - 11]
            left_padding = [i - 1 for i in indexes]
            bottom_left_padding = [indexes[-1] - 1 + 11]
            bottom_padding = [indexes[-1] + 11]
            bottom_right_padding = [indexes[-1] + 1 + 11]
            right_padding = [i + 1 for i in indexes]
            top_right_padding = [indexes[0] + 1 - 11]
            top_padding = [indexes[0] - 11]
            result_indexes += indexes
        if left_padding[0] // 11 == indexes[0] // 11:
            result_indexes += left_padding
        if top_padding[0] >= 0:
            result_indexes += top_padding
        if left_padding[0] // 11 == indexes[0] // 11 and top_padding[0] >= 0:
            result_indexes += top_left_padding
        if bottom_padding[0] <= 121:
            result_indexes += bottom_padding
        if left_padding[0] // 11 == indexes[0] // 11 and bottom_padding[0] <= 121:
            result_indexes += bottom_left_padding
        if right_padding[0] // 11 == indexes[0] // 11:
            result_indexes += right_padding
        if right_padding[0] // 11 == indexes[0] // 11 and bottom_padding[0] <= 121:
            result_indexes += bottom_right_padding
        if right_padding[0] // 11 == indexes[0] // 11 and top_padding[0] >= 0:
            result_indexes += top_right_padding
        return result_indexes


class Player:
    def __init__(self):
        self.ships = []
        self.search = ['U' for i in range(121)]  # 'U' for unknown
        self.place_ships(sizes=[5, 4])

    def place_ships(self, sizes):
        for size in sizes:
            placed = False
            while not placed:
                # create new ship
                ship = Battleship(size)
                # check if placement is possible
                possible = True
                for i in ship.indexes[:size]:
                    # indexes must be less than 121
                    if i >= 121:
                        possible = False
                        break
                    # ships cannot go beyond grid
                    new_row = i // 11
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



b = Player()
for i in range(11):
    for j in range(11):
        if i*11 + j in [ind for sub in list(map(lambda x: x.ship_indexes, b.ships)) for ind in sub] :
            print('#', end='')
        else:
            print('.', end='')
    print('\n', end='')
