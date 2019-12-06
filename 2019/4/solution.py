from collections import defaultdict


def read_input(filename):
  def no_empties(x):
    return x is not None and x != ''

  with open(filename) as f_in:
    return filter(no_empties, [l.replace('\n', '').strip() for l in f_in.readlines()])


def to_value(line):
  return map(int, line.split('-'))

def meets_criteria(password):
  current = None
  has_double = False
  for s in str(password):
    i = int(s)
    if current is not None:
      if i == current:
        has_double = True
      if i < current:
        return False
    current = i
  return has_double

def solve_part_1(filename):
  start, end = to_value(read_input(filename)[0])
  valid_passwords = 0
  for candidate_password in range(start, end+1):
    if meets_criteria(candidate_password):
      valid_passwords += 1
  return valid_passwords
      
def has_one_double_only(password):
  pw = str(password)
  # could do this in a loop, but with only 4 True cases, meh.
  if pw[0] == pw[1] != pw[2]:
    return True
  if pw[0] != pw[1] == pw[2] != pw[3]:
    return True
  if pw[1] != pw[2] == pw[3] != pw[4]:
    return True
  if pw[2] != pw[3] == pw[4] != pw[5]:
    return True
  if pw[3] != pw[4] == pw[5]:
    return True
  return False


def solve_part_2(filename):
  start, end = to_value(read_input(filename)[0])
  valid_passwords = 0
  for candidate_password in range(start, end+1):
    if meets_criteria(candidate_password) and has_one_double_only(candidate_password):
      valid_passwords += 1
  return valid_passwords

