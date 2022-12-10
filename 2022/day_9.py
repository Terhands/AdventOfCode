import math

from aoc_utils import read_from_file, get_filename


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def position(self):
        return self.x, self.y

    def move(self, direction):
        if 'R' in direction:
            self.x += 1
        if 'L' in direction:
            self.x -= 1
        if 'U' in direction:
            self.y += 1
        if 'D' in direction:
            self.y -= 1
        
    def direction_from(self, point):
        def diagonal_vert():
            if self.y - point.y > 0:
                return 'D'
            elif self.y - point.y < 0:
                return 'U'
            return ''

        def diagonal_horiz():
            if self.x - point.x > 0:
                return 'L'
            elif self.x - point.x < 0:
                return 'R'
            return ''

        direction = ''
        if self.x - point.x > 1:
            direction += 'L' + diagonal_vert()
        elif self.x - point.x < -1:
            direction += 'R' + diagonal_vert()

        if self.y - point.y > 1:
            direction += 'D' + diagonal_horiz()
        elif self.y - point.y < -1:
            direction += 'U' + diagonal_horiz()
        
        # print(direction)
        return direction


class Rope:
    def __init__(self, size=2):
        self.knots = [Point(0, 0) for _ in range(size)]
        self.visited_tail_positions = {self.knots[-1].position()}

    def move_head(self, direction, distance):
        for _ in range(distance):
            self.knots[0].move(direction)
            self.update_knot(1)

    def update_knot(self, knot_position):
        knot = self.knots[knot_position]
        follow_in_direction = knot.direction_from(self.knots[knot_position-1])
        if follow_in_direction:
            knot.move(follow_in_direction)
            if knot_position == len(self.knots) - 1:
                self.visited_tail_positions.add(knot.position())
            else:
                self.update_knot(knot_position + 1)


def parse_moves(line):
    direction, distance = line.strip().split(' ')
    return direction, int(distance)


def rope_simulation(filename, size):
    moves = read_from_file(filename, parse_moves)
    rope = Rope(size)
    for direction, distance in moves:
        rope.move_head(direction, distance)
    return rope

# Part 1: Spaces visited by tail: 5878
def part_1():
    rope = rope_simulation(get_filename(9, is_sample=False), 2)
    print(f"Part 1: Spaces visited by tail: {len(rope.visited_tail_positions)}")


def part_2():
    rope = rope_simulation(get_filename(9, is_sample=False), 10)
    print(f"Part 1: Spaces visited by tail: {len(rope.visited_tail_positions)}")


part_1()
part_2()
