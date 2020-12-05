from utils import read_from_file, d_print
from itertools import groupby


# This problem is literally just straight input conversion to binary
def format_input(lines):
    seats = []
    for line in lines:
        if not line:
            continue
        row = line[:7].replace('F', '0').replace('B', '1')
        column = line[7:].replace('L', '0').replace('R', '1')
        d_print("Pass {} is in row {}, column {}.".format(line, row, column))
        seats.append((int(row, 2), int(column, 2)))
    return seats

def get_seat_id(seat_tuple):
    row, column = seat_tuple
    return (row * 8) + column


def solve_1(filename):
    boarding_passes = format_input(read_from_file(filename))
    return max([get_seat_id(bp) for bp in boarding_passes])


def solve_2(filename):
    boarding_passes = format_input(read_from_file(filename))
    sorted_boarding_passes = sorted(boarding_passes, key=lambda x: (x[0], x[1]))
    for p in sorted_boarding_passes:
        d_print(p)
    grouped_passes = groupby(sorted_boarding_passes, key=lambda x: x[0])
    for row, grouping in grouped_passes:
        columns = [g[1] for g in grouping]
        if len(columns) < 8:
            for possible_seat in [1, 2, 3, 4, 5, 6]: # 0 and 7 are right out
                if possible_seat not in columns and \
                   possible_seat - 1 in columns and \
                   possible_seat + 1 in columns: 
                    d_print("My seat is at row: {}, column: {}".format(row, possible_seat))
                    return get_seat_id((row, possible_seat))

