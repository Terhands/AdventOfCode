

class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __repr__(self):
    return str(self)

  def __str__(self):
    return "({x}, {y})".format(x=self.x, y=self.y)

  def manhattan_distance_to_point(self, other_point):
    return abs(self.x - other_point.x) + abs(self.y - other_point.y)

  def manhattan_distance_to_origin(self): 
    return abs(self.x) + abs(self.y) 

  def get_new_point_by_moving(self, direction, distance):
    if direction == 'R':
      return Point(self.x + distance, self.y)
    elif direction == 'L':
      return Point(self.x - distance, self.y)
    elif direction == 'U':
      return Point(self.x, self.y + distance)
    elif direction == 'D':
      return Point(self.x, self.y - distance)


class Line(object):
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2

  def __repr__(self):
    return str(self)

  def __str__(self):
    return "{p1} -- {p2}".format(p1=self.p1, p2=self.p2)

  def is_vertical(self):
    return self.p1.x == self.p2.x

  def is_horizontal(self):
    return self.p1.y == self.p2.y

  def intersection_points(self, line):
    intersections = []

    def perpendicular_intersection(v, h):
      if (h.p1.x <= v.p1.x <= h.p2.x or h.p2.x <= v.p1.x <= h.p1.x) and \
         (v.p1.y <= h.p1.y <= v.p2.y or v.p2.y <= h.p1.y <= v.p1.y):
        return [Point(v.p1.x, h.p1.y)]
      return []

    def parallel_intersections(l1, l2):
      if l1.is_vertical() and l2.is_vertical():
        # the only vertical case where they could intersect
        if l1.p1.x == l2.p1.x:
          l1_ys = [i for i in range(min(l1.p1.y, l1.p2.y), max(l1.p1.y, l1.p2.y) + 1)]
          l2_ys = [i for i in range(min(l2.p1.y, l2.p2.y), max(l2.p1.y, l2.p2.y) + 1)] 
          return [Point(l1.p1.x, y) for y in l1_ys if y in l2_ys]
      if l1.is_horizontal() and l2.is_horizontal():
        # the only horizontal case where they could intersect
        if l1.p1.y == l2.p1.y:
          l1_xs = [i for i in range(min(l1.p1.x, l1.p2.x), max(l1.p1.x, l1.p2.x) + 1)]
          l2_xs = [i for i in range(min(l2.p1.x, l2.p2.x), max(l2.p1.x, l2.p2.x) + 1)] 
          return [Point(x, l1.p1.y) for x in l1_xs if x in l2_xs]
      return []  # there was no parallel intersection

    if self.is_vertical() and line.is_horizontal():
      return perpendicular_intersection(self, line)
    elif self.is_horizontal() and line.is_vertical():
      return perpendicular_intersection(line, self)
    else:
      return parallel_intersections(self, line)
 

def read_input(filename):
  def no_empties(x):
    return x is not None and x != ''

  with open(filename) as f_in:
    return filter(no_empties, [l.replace('\n', '').strip() for l in f_in.readlines()])


def to_wire_path(line):
  wire_path = [Point(0, 0)]  # wires will all start at the same initial point in space
  for directive in line.split(','):
    direction = directive[0]
    distance  = int(directive[1:])
    wire_path.append(wire_path[-1].get_new_point_by_moving(direction, distance))
  # print wire_path
  return wire_path


def find_intersections(wire_1, wire_2):
  intersections = []
  for i in range(len(wire_1) - 1):
    l1 = Line(wire_1[i], wire_1[i+1])
    for n in range(len(wire_2) - 1):
      l2 = Line(wire_2[n], wire_2[n+1])
      # print l1, l2
      # print l1.intersection_points(l2)
      intersections += l1.intersection_points(l2)
  # The origin doesn't count as an intersection_point
  return [i for i in intersections if not (i.x == 0 and i.y == 0)]

def solve_part_1(filename):
  wires = [to_wire_path(line) for line in read_input(filename)]
  intersection_points = find_intersections(*wires)  # I'm cheating here - I know there are only ever 2 wires in the input
  # print intersection_points
  
  closest_intersection = None
  intersection_distance = 999999999
  # I could do this in a list comprehension but I'm guessing that part 2 will ask me about the actual point coordinates, that or ask abot the euclidian distance :P
  for intersection_point in intersection_points:
    distance = intersection_point.manhattan_distance_to_origin()
    if distance < intersection_distance:
      closest_intersection = intersection_point
      intersection_distance = distance

  return closest_intersection, intersection_distance


def solve_part_2(filename):
  pass

