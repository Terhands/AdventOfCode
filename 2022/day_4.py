from aoc_utils import read_from_file


class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f"({self.start}, {self.end})"

    def fully_contains(self, range):
        return self.start <= range.start and self.end >= range.end

    def overlaps(self, range):
        return self.fully_contains(range) or (range.start <= self.start <= range.end) or (range.start <= self.end <= range.end)


def parse_assignments(line):
    assignments = line.split(',')
    return [Range(*map(int, a.split('-'))) for a in assignments]


def count_contained_assignments(filename):
    total = 0
    assignments_per_elf = read_from_file(filename, parse_assignments)
    for assignment_1, assignment_2 in assignments_per_elf:
        if assignment_1.fully_contains(assignment_2) or assignment_2.fully_contains(assignment_1):
            total += 1
    return total


sample_file = 'inputs/day4_sample.txt'
input_file = 'inputs/day4_input.txt'


def part_1():
    total_contained_single_elf_assignments = count_contained_assignments(input_file)
    print(f'Part 1: Individuals with fully contained assignments: {total_contained_single_elf_assignments}')


def count_overlapping_assignments(filename):
    total = 0
    assignments_per_elf = read_from_file(filename, parse_assignments)
    for assignment_1, assignment_2 in assignments_per_elf:
        if assignment_1.overlaps(assignment_2):
            total += 1
    return total


def part_2():
    total_overlapping_single_elf_assignments = count_overlapping_assignments(input_file)
    print(f'Part 2: Individuals with overlapping assignments: {total_overlapping_single_elf_assignments}')


part_1()
part_2()
