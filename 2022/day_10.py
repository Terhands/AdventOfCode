import re

from aoc_utils import read_from_file, get_filename


class Screen:
    def __init__(self):
        self.pixels = [[], ]
    
    def render(self, sprite_center):
        if len(self.pixels[-1]) == 40:
            self.pixels.append([])
        if len(self.pixels[-1]) in (sprite_center-1, sprite_center, sprite_center+1):
            self.pixels[-1].append('#')
        else:
            self.pixels[-1].append('.')

    def pretty_print(self):
        for pixel_row in self.pixels:
            print(''.join(pixel_row))


class Program:
    def __init__(self, instructions, initial_x=1):
        self.instructions = instructions
        self.current_cycle = 1
        self.x_register = initial_x
        self.screen = Screen()

    def run(self, copy_x_at):
        signal_strengths = []
        for instruction in self.instructions:
            if 'noop' in instruction:
                self.tick(signal_strengths, copy_x_at, instruction)
            else:
                _, to_add = instruction.split(' ')
                self.tick(signal_strengths, copy_x_at, instruction)
                self.tick(signal_strengths, copy_x_at, instruction)
                self.x_register += int(to_add)
        return signal_strengths

    def tick(self, signal_strengths, copy_x_at, instruction):
        # print(f"({self.current_cycle}, {instruction})")
        if self.current_cycle in copy_x_at:
            signal_strengths.append(self.current_cycle * self.x_register)
        self.screen.render(self.x_register)
        self.current_cycle += 1


def parse_instruction(line):
    return line.strip()

# Part 1: Values of interest: 14920
def part_1():
    program = Program(read_from_file(get_filename(10, is_sample=False), parse_instruction))
    print(f"Part 1: Values of interest: {sum(program.run([20, 60, 100, 140, 180, 220]))}")

# 40 x 6 screen - sprint = 3px wide, x_register sets sprite possition
# each tick places the middle or the sprite base onf register x
def part_2():
    program = Program(read_from_file(get_filename(10, is_sample=False), parse_instruction))
    program.run([])
    print(f"Part 2: Screen Output:")
    program.screen.pretty_print()


part_1()
part_2()
