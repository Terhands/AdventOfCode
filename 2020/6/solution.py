from utils import read_from_file, d_print
from collections import defaultdict


def format_input(lines):
    groups = []
    current_group = []
    for line in lines:
        if not line:
            d_print(current_group)
            groups.append(':'.join(current_group))
            current_group = []
        else:
            current_group.append(line)
    return groups


def unique_yes_counts_for_group(group):
    yes_counts = defaultdict(int)
    for answer in group:
        if answer != ':':
            yes_counts[answer] += 1
    return yes_counts


def all_yeses_per_group(group):
    yes_counts = 0
    individuals = group.split(':')
    d_print(individuals)
    # since we only care about all members containing a value, we can just grab a member at random
    # and check their yes-es vs everyone else's
    yes_set = set(individuals[0])
    for individual in individuals:  # we are all individuals
        yes_set &= set(individual)  # I'm not!
    return yes_set


def solve_1(filename):
    group_responses = format_input(read_from_file(filename))
    total = 0
    for group in group_responses:
        counts_dict = unique_yes_counts_for_group(group)
        total += len(counts_dict.keys())
    return total


def solve_2(filename): 
    group_responses = format_input(read_from_file(filename))
    total = 0
    for group in group_responses:
        yes_set = all_yeses_per_group(group)
        total += len(yes_set)
    return total

