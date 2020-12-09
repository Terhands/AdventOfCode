from utils import read_from_file, d_print
from collections import deque
from itertools import combinations


def format_input(lines):
    return [int(line) for line in lines if line]


def solve_1(filename, numbers_to_consider=25):
    data = format_input(read_from_file(filename))
    index = numbers_to_consider
    while True:
        start_index = index - numbers_to_consider
        end_index = index
        current_number = data[index]
        is_valid = False
        d_print(current_number)
        d_print(data[start_index:end_index])
        d_print("{} - {}:{}".format(index, start_index, end_index))
        for c in combinations(data[start_index:end_index], 2):
            if sum(c) == current_number:
                d_print(c)
                is_valid = True
                break
        if not is_valid:
            return current_number
        index += 1
            

def solve_2(filename, sum_to=1309761972):
    data = format_input(read_from_file(filename))
    start_index, end_index = 0, 0
    current_sum = data[start_index]
    d_print(data)
    while True:
        d_print("sum({}) = {}".format(data[start_index:end_index+1], current_sum)) 
        if current_sum > sum_to:
            d_print("Moving start up, and subtracting {}".format(data[start_index]))
            current_sum -= data[start_index]
            start_index += 1
            # the list isn't sorted, so we may need to backtrack
            while current_sum > sum_to:
                d_print("Moving end back, and substracting {}".format(data[end_index]))
                current_sum -= data[end_index]
                end_index -= 1

            if end_index <= start_index:
                end_index = start_index
                current_sum = data[start_index]

        elif current_sum < sum_to:
            d_print("Moving end up and adding {}".format(data[end_index]))
            end_index += 1
            current_sum += data[end_index]

        else:
            # we have a contiguous sum that equals our goal
            sorted_data = sorted(data[start_index:end_index+1])
            return sorted_data[0] + sorted_data[-1]

