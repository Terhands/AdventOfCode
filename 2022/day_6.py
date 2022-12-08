from aoc_utils import read_from_file, get_filename


def is_start_marker(data, marker_length):
    return len(data) == marker_length and len(set(data)) == marker_length


def find_first_marker_end_position(message, marker_length):
    for offset in range(len(message)):
        if is_start_marker(message[offset:offset+marker_length], marker_length):
            return offset + marker_length


def read_message(contents):
    return [x for x in contents[0]]
    

def part_1():
    message = read_message(read_from_file(get_filename(6, is_sample=False), lambda x: x.strip()))
    print(f"Part 1: First marker ends at position: {find_first_marker_end_position(message, 4)}")


def part_2():
    message = read_message(read_from_file(get_filename(6, is_sample=False), lambda x: x.strip()))
    print(f"Part 2: First marker ends at position: {find_first_marker_end_position(message, 14)}")

part_1()
part_2()
