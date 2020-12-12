from utils import read_from_file, d_print
from enum import Enum
from math import cos, sin, radians

directions = {
    'N': (0, 1),
    'S': (0, -1),
    'E': (1, 0),
    'W': (-1, 0),
}

# right will be +, left will be -
ordered_directions = ['N', 'E', 'S', 'W']

turning_direction = {
    'R': 1,
    'L': -1,
}


class Ship():

    def __init__(self):
        self.position = (0, 0)
        # we start facing East
        self.facing_direction_index = 1
        self.waypoint = (10, 1)

    def move(self, command, distance):
        if command == 'F':
            command = ordered_directions[self.facing_direction_index]
        x, y = directions[command]
        curr_x, curr_y  = self.position
        self.position = (curr_x + (x * distance), curr_y + (y * distance))

    def turn(self, command, angle):
        rotate_by = angle / 90  # how many rotational 'units' we need to change by
        self.facing_direction_index += rotate_by * turning_direction[command]
        # wrap when we've turned past our directions list 
        self.facing_direction_index = int(self.facing_direction_index % len(ordered_directions))
        d_print(self.facing_direction_index)
 
    def move_to_waypoint(self, times):
        curr_x, curr_y = self.position
        way_x, way_y = self.waypoint
        self.position = (curr_x + (way_x * times), curr_y + (way_y * times))

    def move_waypoint(self, direction, distance): 
        x, y = directions[direction]
        curr_x, curr_y  = self.waypoint
        self.waypoint = (curr_x + (x * distance), curr_y + (y * distance))

    def rotate_waypoint(self, direction, angle): 
        angle *= -1 if direction == 'R' else 1
        r_angle = radians(angle)
        d_print("Rotating {} degrees -> {} radians".format(angle, r_angle))
        # our origin is 0, 0 (relative to the ship, so we don't have to factor that in
        # x = cos * x - sin * y
        # y = sin * x + cos * y
        curr_x, curr_y = self.waypoint
        new_x = round((curr_x * cos(r_angle)) - (curr_y * sin(r_angle)))
        new_y = round((curr_y * cos(r_angle)) + (curr_x * sin(r_angle)))
        d_print("Rotated waypoint from ({}, {}) to ({}, {})".format(curr_x, curr_y, new_x, new_y))
        self.waypoint = (new_x, new_y)

    def manhattan_distance(self):
        x, y = self.position
        return abs(x) + abs(y)

    def print_state(self):
        facing = ordered_directions[self.facing_direction_index]
        x, y = self.position
        d_print("The ship is at position ({}, {}) facing {}.".format(x, y, facing))
        x, y = self.waypoint
        d_print("The wanypoint is at position ({}, {}) relative to the ship.".format(x, y))

def format_input(lines):
    instructions = []
    for line in lines:
        if not line:
            continue

        command = line[0]
        distance = int(line[1:])
        instructions.append((command, distance))
    return instructions


def solve_1(filename):
    instructions = format_input(read_from_file(filename))
    ship = Ship()
    for command, distance in instructions:
        if command in ['L', 'R']:
            ship.turn(command, distance)
        else:
            ship.move(command, distance)
        ship.print_state()
    return ship.manhattan_distance()


def solve_2(filename):
    instructions = format_input(read_from_file(filename))
    ship = Ship()
    for command, distance in instructions:
        if command in ['L', 'R']:
            ship.rotate_waypoint(command, distance)
        elif command == 'F':
            ship.move_to_waypoint(distance)
        else:
            ship.move_waypoint(command, distance)
        ship.print_state()
    return ship.manhattan_distance()








