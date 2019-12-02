
class Coord(object):

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.is_finite = True

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

    def __repr__(self):
        return self.__str__()


def manhattan_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def read_input(filename):
    with open(filename) as f:
        return [Coord(*l.replace(' ', '').replace('\n', '').split(',')) for l in f.readlines() if l.replace('\n', '').strip() != ""]


def sort_by_x(coordinates):
    return sorted(coordinates, key=lambda p: p.x)


def sort_by_y(coordinates):
    return sorted(coordinates, key=lambda p: p.y)


def get_boundary(sorted_by_x, sorted_by_y):
    return (Coord(sorted_by_x[0].x, sorted_by_y[0].y), Coord(sorted_by_x[-1].x, sorted_by_y[-1].y))


def get_area(c1, sorted_by_x, sorted_by_y):
    x_index = sorted_by_x.index(c1)
    y_index = sorted_by_x.index(c1)

    top_left, bottom_right = get_boundary(sorted_by_x, sorted_by_y)
    if c1.x in [b.x for b in [top_left, bottom_right]] or c1.y in [b.y for b in [top_left, bottom_right]]:
        return 0

    # def surrounding_coordinates(index, sorted_coordinates):
    #     if 0 < index < (len(sorted_coordinates) - 1):
    #         return sorted_coordinates[index-1], sorted_coordinates[index+1]
    #     return None, None

    # x_left, x_right = surrounding_coordinates(x_index, sorted_by_x)
    # y_top, y_bottom = surrounding_coordinates(y_index, sorted_by_y)

    total = 0
    # surrounding_coordinates = [x_left, x_right, y_top, y_bottom]
    # print "%s: %s" % (c1, surrounding_coordinates)

    for y in range(top_left.y, bottom_right.y + 1):
        row = ""
        for x in range(top_left.x, bottom_right.x + 1):
            c2 = Coord(x, y)
            is_closest = True
            c1_distance = manhattan_distance(c1, c2)
            # print "%s -> %s = %s" % (c1, c2, c1_distance)
            for coord in sorted_by_x:
                # print "%s -> %s = %s" % (coord, c2, manhattan_distance(coord, c2))
                if (c1.x != coord.x or c1.y != coord.y) and manhattan_distance(coord, c2) <= c1_distance:
                    # print "closer"
                    is_closest = False
                    break
            if is_closest:
                row += "#"
                total += 1
            else:
                row += "."
        # print row
    # print "---------"
    return total


def part1(_input):
    sorted_by_x = sort_by_x(_input)
    sorted_by_y = sort_by_y(_input)

    largest_area = 0
    largest_coordinate = None
    for coordinate in _input:
        area = get_area(coordinate, sorted_by_x, sorted_by_y)
        if area > largest_area:
            largest_coordinate = coordinate
            largest_area = area
    
    return largest_coordinate, largest_area


def get_area_from(coordinates, threshold):
    sorted_by_x = sort_by_x(coordinates)
    sorted_by_y = sort_by_y(coordinates)
    top_left, bottom_right = get_boundary(sorted_by_x, sorted_by_y)
    total = 0

    for y in range(top_left.y, bottom_right.y + 1):
        row = ""
        for x in range(top_left.x, bottom_right.x + 1):
            c2 = Coord(x, y)
            is_within = True
            total_distance = 0
            # print "%s -> %s = %s" % (c1, c2, c1_distance)
            for coord in coordinates:
                # print "%s -> %s = %s" % (coord, c2, manhattan_distance(coord, c2))
                total_distance += manhattan_distance(coord, c2)
                if total_distance >= threshold:
                    # print "closer"
                    is_within = False
                    break
            if is_within:
                row += "#"
                total += 1
            else:
                row += "."
        print row
    # print "---------"
    return total    

def part2(_input, threshold):
    # sorted_by_x = sort_by_x(_input)
    # sorted_by_y = sort_by_y(_input)

    largest_area = 0
    largest_coordinate = None
    return get_area_from(_input, threshold)




