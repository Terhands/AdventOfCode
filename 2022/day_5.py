import math
import re
from aoc_utils import read_from_file


sample_file = 'inputs/day5_sample.txt'
input_file = 'inputs/day5_input.txt'


class CratesState:
    def __init__(self, crate_stacks):
        self.crate_stacks = crate_stacks
        [s.reverse() for s in self.crate_stacks]

    def move(self, src_stack, dest_stack, num_crates):
        # print(self.crate_stacks)
        # print(f"moving {num_crates} from {src_stack} to {dest_stack}")
        src, dest = self.crate_stacks[src_stack-1], self.crate_stacks[dest_stack-1]
        for _ in range(num_crates):
            dest.append(src.pop())

    def multi_move(self, src_stack, dest_stack, num_crates):
        src, dest = self.crate_stacks[src_stack-1], self.crate_stacks[dest_stack-1]
        # print(f"moving {num_crates}({src[-num_crates:]}) from {src_stack} to {dest_stack}")
        dest += src[-num_crates:]
        [src.pop() for _ in range(num_crates)]
        # print(self.crate_stacks)


    def __str__(self):
        return f'{"".join([stack[-1] for stack in self.crate_stacks])}'



def parse_crate_stacks(lines):
    width = 3
    stacks = []
    for line in lines:
        num_stacks = math.ceil(len(line) / 4)
        if len(stacks) < num_stacks:
            stacks = [[] for _ in range(num_stacks)]
        for i, crate in enumerate([line[(width*i)+i:(width*(i+1))+i].replace('[', '').replace(']', '').strip() for i in range(num_stacks)]):
            if crate:
                stacks[i].append(crate)
    return CratesState(stacks)



def apply_moves(state: CratesState, movement_data: str):
    for data in movement_data:
        crates_to_move, source_stack, dest_stack = re.search('move (\d+) from (\d+) to (\d+)', data).groups()
        state.move(int(source_stack), int(dest_stack), int(crates_to_move))


def restack_crates(filename, moving_fn):
    contents = read_from_file(filename, lambda x: x.replace('\n', ''))
    cutoff_index = contents.index('')
    crate_state = parse_crate_stacks(contents[:cutoff_index-1])
    moving_fn(crate_state, contents[cutoff_index+1:])
    return crate_state
    

def part_1():
    print(f"Part 1: Crate tops after restacking: {restack_crates(input_file, apply_moves)}")


def apply_multi_moves(state: CratesState, movement_data: str):
    for data in movement_data:
        crates_to_move, source_stack, dest_stack = re.search('move (\d+) from (\d+) to (\d+)', data).groups()
        state.multi_move(int(source_stack), int(dest_stack), int(crates_to_move))


def part_2():
    print(f"Part 2: Crate tops after restacking: {restack_crates(input_file, apply_multi_moves)}")


part_1()
part_2()
