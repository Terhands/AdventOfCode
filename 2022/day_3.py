from aoc_utils import read_from_file


def to_priority(item):
    if item.islower():
        return ord(item) - 96
    return ord(item) - 38


def calculate_priority(compartment_1, compartment_2):
    duplicate = (set(compartment_1) & set(compartment_2)).pop()
    return to_priority(duplicate)


def split_by_compartment(contents):
    all_contents = [x for x in contents]
    middle = int(len(all_contents) / 2)
    return all_contents[:middle], all_contents[middle:]


sample_file = "inputs/day3_sample.txt"
input_file = "inputs/day3_input.txt"


def part_1():
    rucksacks = read_from_file(input_file, lambda x: x.strip())
    print(f"Part 1: Total Priority: {sum([calculate_priority(*split_by_compartment(all_contents)) for all_contents in rucksacks])}")
        

def calculate_priority_2(bag_1, bag_2, bag_3):
    duplicate = (set(bag_1) & set(bag_2) & set(bag_3)).pop()
    return to_priority(duplicate)


def group_bags(all_bags):
    group_size = 3
    total_groups = int(len(all_bags) / group_size)
    return [all_bags[group_size*i:group_size*(i+1)] for i in range(total_groups)]


def part_2():
    rucksacks = read_from_file(input_file, lambda x: x.strip())
    print(f"Part 2: Total Priority: {sum([calculate_priority_2(*bags) for bags in group_bags(rucksacks)])}")


part_1()
part_2()
