from functools import cmp_to_key

from aoc_utils import read_from_file, get_filename


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, coords):
        return (self.x < coords.x) or (self.x == coords.x and self.y < coords.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Wall:
    def __init__(self, p1, p2):
        self.direction = 'v' if p1.x == p2.x else 'h'
        if self.direction == 'v':
            if p1.y < p2.y:
                self.start = p1
                self.end = p2
            else:
                self.start = p2
                self.end = p1
        if self.direction == 'h':
            if p1.x < p2.x:
                self.start = p1
                self.end = p2
            else:
                self.start = p2
                self.end = p1

    def __lt__(self, wall):
        return self.start < wall.start

    def __str__(self):
        return f"{self.start} -> {self.end}"

    def intersects(self, x, y):
        return self.start.x <= x <= self.end.x and self.start.y <= y <= self.end.y


class Cave:
    def __init__(self, walls, sand_origin=(500, 0)):
        self.walls = sorted(walls)
        self.lowest_y = max([w.end.y for w in self.walls])
        self.sand_origin = sand_origin
        self.resting_sand = set()

    @classmethod
    def from_coordinate_sets(cls, coordinate_sets, sand_origin=(500, 0)):
        walls = []
        for wall_coords in coordinate_sets:
            for i in range(len(wall_coords) - 1):
                walls.append(Wall(wall_coords[i], wall_coords[i+1]))
        return cls(walls, sand_origin)

    def add_sand(self, bottom=None):
        current_location = Coordinate(self.sand_origin[0], self.sand_origin[1])
        def can_fall(x, y):
            for wall in self.walls:
                if wall.intersects(x, y) or (x, y) in self.resting_sand or (bottom is not None and y == bottom):
                    return False
            return True

        while True:
            if can_fall(current_location.x, current_location.y + 1):
                current_location.y += 1
            elif can_fall(current_location.x - 1, current_location.y + 1):
                current_location.x -= 1
                current_location.y += 1
            elif can_fall(current_location.x + 1, current_location.y + 1):
                current_location.x += 1
                current_location.y += 1
            elif current_location.x == self.sand_origin[0] and current_location.y == self.sand_origin[1]:
                self.resting_sand.add((current_location.x, current_location.y))
                return False
            else:
                self.resting_sand.add((current_location.x, current_location.y))
                # print(f'Resting location: {current_location}')
                return True

            if bottom is None and current_location.y >= self.lowest_y:
                return False
            elif (current_location.x, current_location.y) == self.sand_origin:
                return False



def coordinate_parser(line):
    line = line.strip().split(' -> ')
    return [Coordinate(*[int(x) for x in coord_group.split(',')]) for coord_group in line]



def part_1():
    cave = Cave.from_coordinate_sets(read_from_file(get_filename(14, is_sample=False), coordinate_parser))
    while cave.add_sand():
        pass
    print(f'Part 1: Maximum sand was {len(cave.resting_sand)}')
    

def part_2():
    cave = Cave.from_coordinate_sets(read_from_file(get_filename(14, is_sample=False), coordinate_parser))
    while cave.add_sand(bottom=cave.lowest_y + 2):
        pass
    print(f'Part 2: Maximum sand was {len(cave.resting_sand)}')


# part_1()
part_2()
