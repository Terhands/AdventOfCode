import itertools


def is_line_possible(l):
  #l = [int(i) for i in line.split(" ") if i != '']
  
  for a, b, c in itertools.permutations(l):
    if a >= (b + c):
      return False
  return True


def parse_lines(lines):
  parsed_lines = []
  for line in lines:  
     parsed_lines.append([int(i) for i in line.split(" ") if i != ''])

  triangles = []
  for i in range(0, len(parsed_lines), 3):
    parsed_lines[i:i+3]
    for j in range(3):
      triangles.append((parsed_lines[i][j], parsed_lines[i+1][j], parsed_lines[i+2][j]))

  print len(triangles)
  print len(parsed_lines)

  return triangles

def solve(lines):
  print parse_lines(lines)
  print len([line for line in parse_lines(lines) if is_line_possible(line)])


  
