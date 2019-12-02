import re


class Velocity(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Star(object):

    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity

    def position_at(self, time_elapsed):
        return self.x + (self.velocity.x * time_elapsed), self.y + (self.velocity.y * time_elapsed)


class Sky(object):

    def __init__(self, stars):
        self.stars = stars
        self.time_elapsed = 0

    def boundaries(self):
        current_positions = zip(*(s.position_at(self.time_elapsed) for s in self.stars))
        x_min = min(current_positions[0])
        y_min = min(current_positions[1])
        x_max = max(current_positions[0])
        y_max = max(current_positions[1])
        # print current_positions
        return (x_min, y_min), (x_max, y_max)

    def display_at_time(self, time):
        self.time_elapsed = time
        print self

    def __repr__(self):
        top_left, bottom_right = self.boundaries()
        sky = ""
        print top_left, bottom_right
        # print range(top_left[1], bottom_right[1])
        # print range(top_left[0] - 1, bottom_right[0] + 2)
        # give it a nice border (-1, +2)
        if bottom_right[1] - top_left[1] > len(self.stars):
            return "Nothing Yet."
        if bottom_right[0] - top_left[0] > len(self.stars):
            return "Nothing Yet."

        for y in range(top_left[1] - 1, bottom_right[1] + 2):
            for x in range(top_left[0] - 1, bottom_right[0] + 2):
                has_star = False
                for s in self.stars:
                    if s.position_at(self.time_elapsed) == (x, y):
                        has_star = True
                        break
                sky += "#" if has_star else "." 
            sky += "\n"
        return sky


pattern = re.compile(r'position=<(?P<pos_x>-?\d+),(?P<pos_y>-?\d+)>velocity=<(?P<vel_x>-?\d+),(?P<vel_y>-?\d+)>')


def read_input(filename):
    with open(filename) as f:
        return [pattern.match(line.replace('\n', '').replace(' ', '')) for line in f.readlines() if line.strip() != ""]


def build_sky(matches):
    return Sky([Star(int(match.group('pos_x')), int(match.group('pos_y')), Velocity(int(match.group('vel_x')), int(match.group('vel_y')))) for match in matches if match])


def part1(input):
    sky = build_sky(input)
    return sky


