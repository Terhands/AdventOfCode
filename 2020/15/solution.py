from utils import read_from_file, d_print


def solve(sequence, limit):
    index_map = {}
    for index, value in enumerate(sequence):
        index_map[value] = index
    d_print(index_map)
    while index < limit-1:
        if value in index_map:
            previous_index = index_map[value]
            index_map[value] = index
            value = index - previous_index
        else:
            index_map[value] = index
            value = 0
        index += 1
        d_print("Turn {}: {}".format(index, value))
    return value


def solve_1(sequence):
    return solve(sequence, 2020)


def solve_2(sequence):
    return solve(sequence, 30000000)


