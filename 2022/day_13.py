from functools import cmp_to_key

from aoc_utils import read_from_file, get_filename


def parse_list(line):
    line = line.strip()
    if line:
        return eval(line)


def build_pairs(file_contents):
    pairs = []
    current_pair = []
    for line in file_contents:
        if line is not None:
            current_pair.append(line)
        else:
            pairs.append(tuple(current_pair))
            current_pair = []
    return pairs


def ensure_type(left, right):
    if type(left) != type(right):
        if isinstance(left, int):
            return ensure_type([left], right)
        return ensure_type(left, [right])
    return left, right


def get_next(_list):
    if len(_list) > 0:
        return _list[0]
    return None


def compare(left: list, right: list):
    for i in range(min(len(left), len(right))):
        possible_result = _is_suborder_correct(left[i], right[i])
        if possible_result != 0:
            return possible_result

    if len(left) < len(right):
        return -1
    elif len(left) > len(right):
        return 1
    return 0

def _is_suborder_correct(left, right):
    l0, r0 = ensure_type(left, right)
    if isinstance(l0, int) and l0 < r0:
        return -1
    if isinstance(l0, int) and l0 > r0:
        return 1
    if isinstance(l0, int) and l0 == r0:
        return 0

    return compare(l0, r0)


def part_1():
    pairs = build_pairs(read_from_file(get_filename(13, is_sample=False), parse_list))
    correct_indices = [index+1 for index, (left, right) in enumerate(pairs) if compare(left, right) < 0]
    print(f"Part 1: Valid data packet sum is {sum(correct_indices)}")


def part_2():
    pairs = build_pairs(read_from_file(get_filename(13, is_sample=False), parse_list))
    divider_packets = [[[2]], [[6]]]
    all_packets = [] + divider_packets
    for pair in pairs:
        all_packets += list(pair)
    all_packets.sort(key=cmp_to_key(compare))
    divider_indices = (all_packets.index(divider_packets[0]) + 1) * (all_packets.index(divider_packets[1]) + 1)
    print(f"Part 2: Valid data packet sum is {divider_indices}")


part_1()
part_2()
