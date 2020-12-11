from utils import read_from_file, d_print
from functools import reduce


def format_input(lines):
    adapter_ratings = [int(line) for line in lines if line]
    adapter_ratings += [0]  # the seat outlet
    adapter_ratings += [max(adapter_ratings) + 3]  # my device
    return adapter_ratings


def compute_differences(adapter_ratings):
    sorted_adapters = sorted(adapter_ratings)
    differences = []
    for index in range(len(sorted_adapters) - 1):
        difference = sorted_adapters[index+1] - sorted_adapters[index]
        differences.append(difference)
    return differences

def solve_1(filename):
    adapter_ratings = format_input(read_from_file(filename))
    differences = compute_differences(adapter_ratings)
    _1_diff_count = 0
    _3_diff_count = 0
    for difference in differences:
        if difference == 1:
            _1_diff_count += 1
        elif difference == 3:
            _3_diff_count += 1
    d_print("1-count = {} 3-count = {}".format(_1_diff_count, _3_diff_count))
    return _1_diff_count * _3_diff_count


def possible_connections_tree(adapters):
    diff_tree = {a: [] for a in adapters}
    index = 0
    while index < len(adapters):
        for comparison_index in range(index+1, index+4):
            if comparison_index == len(adapters):
                break
            delta = adapters[comparison_index] - adapters[index]
            if delta <= 3:
                diff_tree[adapters[index]].append(adapters[comparison_index])
        index += 1
    return diff_tree

# as soon as we know the total number of connections under a branch, save that in a secondary storage
# adn check that storage before bothering with the full traversal
def total_configurations(current_adapter, d_tree, connection_store):
    if current_adapter in connection_store:
        return connection_store[current_adapter]

    total = 1 if d_tree[current_adapter] == [] else 0
    for next_adapter in d_tree[current_adapter]:
        total += total_configurations(next_adapter, d_tree, connection_store)
    connection_store[current_adapter] = total
    return total


def solve_2(filename):
    adapter_ratings = format_input(read_from_file(filename))
    d_print(sorted(adapter_ratings))
    d_tree = possible_connections_tree(sorted(adapter_ratings))
    d_print(d_tree)
    total = total_configurations(0, d_tree, {})
    return total


