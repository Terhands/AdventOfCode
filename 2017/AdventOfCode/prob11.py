import collections
import itertools


class State():

  def __init__(self, pair_positions, elevator_position):
    self.elevator_position = elevator_position
    self.pair_positions = pair_positions

  def __hash__(self):
    return sorted(list(self.pair_positions.itervalues()))

  def display(self):
    lines = []
    for i in range(4):
      line = 'F%s: ' % i
      for k, v in self.pair_positions.iteritems():
        if v[0] == i:
          line += ' %sM ' % k
        if v[1] == i:
          line += ' %sG ' % k
      if self.elevator_position == i:
          line += ' <<< '
      lines.append(line)
    lines.reverse()
    for l in lines:
      print l
      pass
    #print self.pair_positions

  def is_winning_state(self):
    if all([k == v == 3 for k, v in self.pair_positions.itervalues()]):
      print "Winning State: %s" % self.pair_positions
      self.display()
      return True
    return False

  def is_safe(self):
    for i in range(4):
      items = [pair for pair in self.pair_positions.itervalues() if pair[0] == i]
      return all([m == g for m, g in items]) or all([m != g for m, g in items])

  def move(self, direction, item1, item2):
    op1, op2 = self.pair_positions[item1[0]], self.pair_positions[item2[0]] if item2 else None
    new_pairs = self.pair_positions.copy()
    new_pairs[item1[0]] = (op1[0], op1[1] + direction) if item1[-1] == 'G' else (op1[0] + direction, op1[1])
    if item2:
      new_pairs[item2[0]] = (op2[0], op2[1] + direction) if item2[-1] == 'G' else (op2[0] + direction, op2[1])
    state = State(new_pairs, self.elevator_position + direction)
    if not all([0 <= a <= 3 and 0 <= b <= 3 for a, b in new_pairs.itervalues()]):
      print "-----------------------------"
      self.display()
      print "Move %s, %s in direction %s" % (item1, item2, direction)
    #state.display()
    return state
 
  def possible_directions(self):
    if self.elevator_position == 0:
      return [1]
    if self.elevator_position == 3:
      return [-1]
    return [1, -1]

  def possible_moves(self):
    states = []
    options = []
    for k, v in self.pair_positions.iteritems():
      if v[0] == self.elevator_position:
        options.append('%sM' % k) 
      if v[1] == self.elevator_position:
        options.append('%sG' % k)
    options.append(None)
    
    for direction in self.possible_directions():
      for item1, item2 in itertools.combinations(options, 2):
        s = self.move(direction, item1, item2)
        if s.is_safe():
          states.append(s)
    return states

  def __eq__(self, state):
    return self.pair_positions == state.pair_positions and self.elevator_position == state.elevator_position

class Game():

  def __init__(self, lines):
    self.start_state = parse(lines)
    self.current_state = self.start_state
    self.moves = []

  def move(self, direction, a, b):
    new_state = self.current_state.positional_move(direction, a, b)
    if new_state.is_safe():
      self.moves.append(new_state)
      self.current_state = new_state
    elif new_state.is_winning_state:
      print "You won in %s moves!" % len(moves)
    else:
      print "BOOM!!"

  def undo(self):
    self.moves = self.moves[:-1]

class GameTree():

  previously_expanded_states = []

  def __init__(self, initial_state):
    self.initial_state = initial_state

  def solve(self):
    return self.solve_from(self.initial_state.possible_moves(), 0)

  def solve_from(self, states_to_expand, depth):
    while True:
      next_states_to_expand = []
      for state in states_to_expand:
        if state.is_winning_state():
          return depth
        next_states_to_expand += [s for s in state.possible_moves() if s not in self.previously_expanded_states]
        self.previously_expanded_states.append(state)
      depth += 1
      states_to_expand = next_states_to_expand

def parse(lines):
  pairs = {}
  for line in lines:
    if 'first floor' in line:
      floor = 0
    elif 'second floor' in line:
      floor = 1
    elif 'third floor' in line:
      floor = 2
    elif 'fourth floor' in line:
      floor = 3
 
    line = line.replace('floor contains a ', '::').split('::')[1]
    stuff = line.split(',')
    for item in stuff:
      p = pairs.get(item, (0, 0))
      if item[-1] == 'M':
        pairs[item[0]] = (floor, p[1])
      if item[-1] == 'G':
        pairs[item[0]] = (p[0], floor)

  return State(pairs, 0)

def is_microchip(item):
  return item[-1] == 'M'
  
def is_generator(item):
  return not is_microchip(item)

def print_map():
  for k, v in floor_map.iteritems():
    print '%s: %s' % (k, v)

