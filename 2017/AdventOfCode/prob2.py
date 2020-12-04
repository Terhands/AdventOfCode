
key_pad = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

key_pad_v2 = [(0, 0, 1, 0, 0), (0, 2, 3, 4, 0), (5, 6, 7, 8, 9), (0, 'A', 'B', 'C', 0), (0, 0, 'D', 0, 0)]

def parse_line(l):
  return [i for i in l]

def solve_for_instruction(start_pos, instructions):
  x, y = start_pos
  for inst in instructions:
    if inst == 'U':
      y = move_y(x, y, -1)
    elif inst == 'D':
      y = move_y(x, y, 1)
    elif inst == 'R':
      x = move_x(x, y, 1)
    elif inst == 'L':
      x = move_x(x, y, -1)
    print "(%s, %s)" % (x, y)
  return key_pad_v2[y][x], (x, y)

def move_y(x, y, move):
  if 0 <= y + move <= 4 and key_pad_v2[y+move][x] != 0:
    y += move
  return y

def move_x(x, y, move):
  if 0 <= x + move <= 4 and key_pad_v2[y][x+move] != 0:
    x += move
  return x

# part 1
# def move(start, move):
#  if 0 <= (start + move) <= 2:
#    return start + move
#  return start

def solve(lines):
  pos = (0, 2)
  code = ""
  for line in lines:
    l = parse_line(line)
    num, pos = solve_for_instruction(pos, l)
    code += str(num)
  print code

