

class PowerCell(object):

    def __init__(self, level, combined_level):
        self.level = level
        self.combined_level = combined_level

    def __repr__(self):
        return "<PC>%s" % self.level


def split_int(number):
    digits = []
    while number:
        digits.append(number % 10)
        number //= 10
    return digits


def power_level(x, y, serial_number):
    """
    Find the fuel cell's rack ID, which is its X coordinate plus 10.
    Begin with a power level of the rack ID times the Y coordinate.
    Increase the power level by the value of the grid serial number (your puzzle input).
    Set the power level to itself multiplied by the rack ID.
    Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
    Subtract 5 from the power level.
    """
    rack_id = x + 10
    power_level = ((rack_id * y) + serial_number) * rack_id
    level_digits = split_int(power_level)
    return (level_digits[2] if len(level_digits) > 2 else 0) - 5


def part1(serial_number, square_size=3):
    grid = [[None for _ in range(300)] for _ in range(300)]
    # building it in reverse, can compute the combined at the same time as each cell this way (the cells below/to the right are already known)
    cell_nums = range(300)
    cell_nums.reverse()
    greatest_combined = 0
    best_cell = (None, None)
    for y in cell_nums:
        for x in cell_nums:
            # print x, y
            level = power_level(x, y, serial_number)
            combined_level = level
            if y <= 300 - square_size and x <= 300 - square_size:  # there are at least 2 cells below, and beside this one, we can combine them
                for y2 in range(square_size):
                    for x2 in range(square_size):
                        if x2 > 0 or y2 > 0:
                            combined_level += grid[y+y2][x+x2].level
                if combined_level > greatest_combined:
                    greatest_combined = combined_level
                    best_cell = (x, y)
            grid[y][x] = PowerCell(level, combined_level)
    return best_cell, greatest_combined

def part2(serial_number):
    best_size, best_cell, best_level = 0, None, 0
    for size in range(300):
        print size
        cell, level = part1(serial_number, square_size=size)
        if level > best_level:
            best_cell = cell
            best_level = level
            best_size = size
            print best_cell, best_size, best_level
    return best_cell, best_size, best_level

