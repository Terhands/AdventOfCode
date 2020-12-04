
def parse_line(line):
  return [(e.strip()[0], int(e.strip()[1:])) for e in line.split(',')]


def solve_for_directions(directions_tuples):
  facing = 0
  previous_locations = [(0, 0)]
  x, y = 0, 0
  for direction, distance in directions_tuples:
    if direction == 'R':
      facing = facing + 1
    if direction == 'L':
      facing = facing - 1 % 4
    facing = facing % 4  # N, E, S, W
  
    if facing == 0:  # N
      print 'N' + str(distance)
      y += distance
    elif facing == 1:  # E
      print 'E' + str(distance)
      x += distance
    elif facing == 2:  # S
      print 'S' + str(distance)
      y -= distance
    elif facing == 3:  # W
      print 'W' + str(distance)
      x -= distance
 
    # for part 2
    for x1, y1 in get_all_visited_between(previous_locations[-1], (x, y)):
      if (x1, y1) in previous_locations:
        return abs(x1) + abs(y1)
      previous_locations.append((x1, y1))

  return abs(x) + abs(y)

def get_all_visited_between(p1, p2):
  visited = []
  p = p1[0]
  if p1[0] > p2[0]:
    for i in range(1, abs(p1[0] - p2[0]) + 1):
      visited.append((p1[0] - i, p1[1]))
    return visited

  if p1[0] < p2[0]:
    for i in range(1, abs(p1[0] - p2[0]) + 1):
      visited.append((p1[0] + i, p1[1]))
    return visited

  if p1[1] > p2[1]:
    for i in range(1, abs(p1[1] - p2[1]) + 1):
      visited.append((p1[0], p1[1] - i))
    return visited

  if p1[1] < p2[1]:
    for i in range(1, abs(p1[1] - p2[1]) + 1):
      visited.append((p1[0], p1[1] + i))
    return visited

