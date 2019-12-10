class DoneException(Exception):
  pass


def read_input(filename):
  def no_empties(x):
    return x is not None and x != ''

  with open(filename) as f_in:
    return filter(no_empties, [l.replace('\n', '').strip() for l in f_in.readlines()])


def to_value(line):
  return map(int, line.split(','))


class Buffer(object):
  """This buffer is essentially a FIFO queue."""
  def __init__(self):
    self.buffer = []

  def __str__(self):
    return str([v.value for v in self.buffer])

  def add(self, value):
    self.buffer.append(value)

  def next(self):
    value = self.buffer[-1]
    self.buffer = self.buffer[:-1]
    return value

class Variable(object):
  def __init__(self, program, mode, address_or_value):
    self.program = program
    self.mode = mode
    self.address_or_value = address_or_value

  @property
  def value(self):
    if self.mode == 0:
      return self.program[self.address_or_value]
    elif self.mode == 1:
      return self.address_or_value
    raise Exception("Invalid mode '{mode}'".format(mode=self.mode))


def opcode_and_vals_to_variables(program, opcode, vars):
  var_mapping = str(opcode)[:-2]

  prefix = ''
  for _ in range(len(vars) - len(var_mapping)):
    prefix += '0'
    
  mapping = map(int, list(prefix + var_mapping))
  mapping.reverse()  # now flip the mapping as they get applied to the vars right to left
  return [Variable(program, mode, address_or_value) for mode, address_or_value in zip(mapping, vars)]


def add(program, position, iobuffer):
  next_position = position + 4
  opcode, v1, v2, storage_location = program[position:next_position]
  v1, v2 = opcode_and_vals_to_variables(program, opcode, [v1, v2])
  program[storage_location] = v1.value + v2.value
  return next_position


def mult(program, position, iobuffer):
  next_position = position + 4
  opcode, v1, v2, storage_location = program[position:next_position]
  v1, v2 = opcode_and_vals_to_variables(program, opcode, [v1, v2])
  program[storage_location] = v1.value * v2.value
  return next_position


def halt(program, position, iobuffer):
  raise DoneException('Computation is complete')


def _input(program, position, iobuffer):
  next_position = position + 2
  _, storage_location = program[position:next_position]
  program[storage_location] = iobuffer.next()
  return next_position


def _output(program, position, iobuffer):
  next_position = position + 2
  opcode, var = program[position:next_position]
  var = opcode_and_vals_to_variables(program, opcode, [var])
  iobuffer.add(var[0])
  return next_position


def jump_if_true(program, position, iobuffer):
  next_position = position + 3
  opcode, v1, to_address = program[position:next_position]
  v1, to_address = opcode_and_vals_to_variables(program, opcode, [v1, to_address])
  if v1.value != 0:
    next_position = to_address.value
  return next_position

def jump_if_false(program, position, iobuffer):
  next_position = position + 3
  opcode, v1, to_address = program[position:next_position]
  v1, to_address = opcode_and_vals_to_variables(program, opcode, [v1, to_address])
  if v1.value == 0:
    next_position = to_address.value
  return next_position

def less_than(program, position, iobuffer):
  next_position = position + 4
  opcode, v1, v2, storage_location = program[position:next_position]
  v1, v2 = opcode_and_vals_to_variables(program, opcode, [v1, v2])
  program[storage_location] = 1 if v1.value < v2.value else 0
  return next_position


def equals(program, position, iobuffer):
  next_position = position + 4
  opcode, v1, v2, storage_location = program[position:next_position]
  v1, v2 = opcode_and_vals_to_variables(program, opcode, [v1, v2])
  program[storage_location] = 1 if v1.value == v2.value else 0
  return next_position


opcodes = {
  1: add,
  2: mult,
  3: _input,
  4: _output,
  5: jump_if_true,
  6: jump_if_false,
  7: less_than,
  8: equals,
  99: halt,
}


def run_intcode_from_position(program, position, iobuffer):
  # The actual operation is the two right-most digits
  opcode = int(str(program[position])[-2:])
  operation = opcodes[opcode]
  return operation(program, position, iobuffer)

# for part 1 run with parameters 'input.txt', 12, 2
def solve_part_1(filename):
  # this is a one liner of input
  intcode = to_value(read_input(filename)[0])
  buffer = Buffer()
  # start out the input buffer with the value 1
  buffer.add(1)
  program_counter = 0
  while True:
    try:
      program_counter = run_intcode_from_position(intcode, program_counter, buffer)
    except DoneException as e:
      print(buffer)
      return intcode
  


def solve_part_2(filename):
  # this is a one liner of input
  intcode = to_value(read_input(filename)[0])
  buffer = Buffer()
  # start out the input buffer with the value 5
  buffer.add(5)
  program_counter = 0
  while True:
    try:
      program_counter = run_intcode_from_position(intcode, program_counter, buffer)
    except DoneException as e:
      print(buffer)
      return intcode
