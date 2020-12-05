from utils import read_from_file, d_print


right = (1, 0)
left = (-1, 0)
down = (0, 1)
up = (0, -1)


class Hill():

    def __init__(self, _map):
        self.origin = (0, 0)
        self.current_position = self.origin
        self.map = _map

        self.width = len(_map[0])
        self.height = len(_map)

    def reset(self):
        self.current_position = self.origin

    def move(self, direction):
        self.current_position = (
            (self.current_position[0] + direction[0]) % self.width, 
            (self.current_position[1] + direction[1])
        )

    def is_tree(self):
        x, y = self.current_position
        return y < self.height and self.map[y][x] == '#'

    def is_at_bottom(self):
        return self.current_position[1] >= self.height

    def print_state(self):
        d_print("**************************\n")
        for y, row in enumerate(self.map):
            row_to_print = ''
            for x, col in enumerate(row):
                if (x, y) == self.current_position:
                    row_to_print += 'X' if self.is_tree() else 'O'
                else:
                    row_to_print += self.map[y][x]
            d_print(row_to_print)


def format_input(lines):
    return Hill(lines)
    
    
def solve_1(filename):
    hill = format_input(read_from_file(filename))
    directions = [right, right, right, down]
    trees_hit = 0

    while not hill.is_at_bottom():
        for direction in directions:
            hill.move(direction)
        if hill.is_tree():
            trees_hit += 1
        hill.print_state()

    return trees_hit


def solve_2(filename):
    hill = format_input(read_from_file(filename))
    direction_sets = [
        (right, down), 
        (right, right, right, down),
        (right, right, right, right, right, down),
        (right, right, right, right, right, right, right, down),
        (right, down, down),
    ]

    trees_hit_product = 1

    for directions in direction_sets:
        trees_hit = 0
        while not hill.is_at_bottom():
            for direction in directions:
                hill.move(direction)
            if hill.is_tree():
                trees_hit += 1
            # hill.print_state()
        hill.reset()
        trees_hit_product *= trees_hit

    return trees_hit_product 

