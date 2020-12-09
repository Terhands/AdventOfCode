from utils import read_from_file, d_print
from collections import defaultdict


def parse_contains_data(data):
    if 'no other bags' in data:
        return 0, None
    pieces = data[:-1].strip().split(' ')  # stip off the '.' and cut it into pieces
    num_bags = int(pieces[0])
    identifier = ' '.join(pieces[1:-1]).strip()  # rebuild the key minus the number and the 'bag' variation
    return num_bags, identifier

# identifier contain # identifier, ...
def format_input(lines):
    bottom_up_bag_mapping, top_down_bag_mapping = defaultdict(list), defaultdict(list)
    for line in lines:
        if not line:
            continue
        bag_identifier, contains_data = line.split(' contain')
        bag_identifier = bag_identifier.replace(' bags', '')
        for data in contains_data.split(','):
            bag_count, child_bag = parse_contains_data(data)
            if child_bag:
                bottom_up_bag_mapping[child_bag].append((bag_identifier, bag_count))
                top_down_bag_mapping[bag_identifier].append((child_bag, bag_count))
    return bottom_up_bag_mapping, top_down_bag_mapping


def solve_1(filename):
    bottom_up_bag_mapping, top_down_bag_mapping = format_input(read_from_file(filename))
    d_print(bottom_up_bag_mapping)
    bag_key = 'shiny gold'
    bags_to_check = bottom_up_bag_mapping[bag_key]
    checked_bags = set()
    while bags_to_check:
        d_print(bags_to_check)
        bag_to_check, _ = bags_to_check.pop()
        if bag_to_check not in checked_bags:
            checked_bags.add(bag_to_check)
            bags_to_check += bottom_up_bag_mapping[bag_to_check]
    return len(checked_bags)


def get_total(bag_key, bag_count, bag_map):
    contained_bags = bag_map[bag_key]
    num_contained_bags = 0
    for _bag_key, _bag_count in contained_bags:
        num_contained_bags += get_total(_bag_key, _bag_count, bag_map)
    total_bags = (bag_count * num_contained_bags)
    total_bags += bag_count if bag_key != 'shiny gold' else 0 # we only want contained bags
    d_print("{}: {}".format(bag_key, total_bags))
    return total_bags


def solve_2(filename):
    _, top_down_bag_mapping = format_input(read_from_file(filename))
    bag_key = 'shiny gold'
    return get_total(bag_key, 1, top_down_bag_mapping)

