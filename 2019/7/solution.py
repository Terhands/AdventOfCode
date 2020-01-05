import itertools

debug = False

class DoneException(Exception):
  pass


class PauseException(Exception):
  pass


def read_input(filename):
  def no_empties(x):
    return x is not None and x != ''

  with open(filename) as f_in:
    return filter(no_empties, [l.replace('\n', '').strip() for l in f_in.readlines()])


def to_value(line):
  return map(int, line.split(','))


def print_debug(*args):
  if debug:
    for arg in args:
      print arg,
    print

class Buffer(object):
  """This buffer is essentially a FIFO queue."""
  def __init__(self):
    self.buffer = []

  def __str__(self):
    return str([v.value for v in self.buffer])

  def add(self, value):
    self.buffer.append(value)

  def next(self):
    # pause the program here and pass off execution to the next program
    if len(self.buffer) == 0:
      raise PauseException()

    value = self.buffer[0]
    self.buffer = self.buffer[1:]
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


class IntcodeProgram(object):

  def __init__(self, instructions, input_buffer, output_buffer):
    self.opcodes = {
      1: self.add,
      2: self.mult,
      3: self._input,
      4: self._output,
      5: self.jump_if_true,
      6: self.jump_if_false,
      7: self.less_than,
      8: self.equals,
      99: self.halt,
    }

    self.instructions = instructions
    self.program_counter = 0
    self.input_buffer = input_buffer
    self.output_buffer = output_buffer

  def run_next_instruction(self):
    # The actual operation is the two right-most digits
    opcode = int(str(self.instructions[self.program_counter])[-2:])
    operation = self.opcodes[opcode]
    self.program_counter = operation()

  def opcode_and_vals_to_variables(self, opcode, vars):
    var_mapping = str(opcode)[:-2]

    prefix = ''
    for _ in range(len(vars) - len(var_mapping)):
      prefix += '0'
      
    mapping = map(int, list(prefix + var_mapping))
    mapping.reverse()  # now flip the mapping as they get applied to the vars right to left
    return [Variable(self.instructions, mode, address_or_value) for mode, address_or_value in zip(mapping, vars)]

  def add(self):
    next_position = self.program_counter + 4
    opcode, v1, v2, storage_location = self.instructions[self.program_counter:next_position]
    v1, v2 = self.opcode_and_vals_to_variables(opcode, [v1, v2])
    self.instructions[storage_location] = v1.value + v2.value
    print_debug(self.program_counter, "add: ", v1.value, v2.value)
    return next_position


  def mult(self):
    next_position = self.program_counter + 4
    opcode, v1, v2, storage_location = self.instructions[self.program_counter:next_position]
    v1, v2 = self.opcode_and_vals_to_variables(opcode, [v1, v2])
    self.instructions[storage_location] = v1.value * v2.value
    print_debug(self.program_counter, "multiply: ", v1.value, v2.value)
    return next_position


  def halt(self):
    raise DoneException('Computation is complete')

  def _input(self):
    next_position = self.program_counter + 2
    _, storage_location = self.instructions[self.program_counter:next_position]
    self.instructions[storage_location] = self.input_buffer.next().value
    print_debug(self.program_counter, "from buffer: ", self.instructions[storage_location])
    return next_position

  def _output(self):
    next_position = self.program_counter + 2
    opcode, var = self.instructions[self.program_counter:next_position]
    var = self.opcode_and_vals_to_variables(opcode, [var])
    self.output_buffer.add(var[0])
    print_debug(self.program_counter, "to buffer: ", var[0].value)
    return next_position

  def jump_if_true(self):
    next_position = self.program_counter + 3
    opcode, v1, to_address = self.instructions[self.program_counter:next_position]
    v1, to_address = self.opcode_and_vals_to_variables(opcode, [v1, to_address])
    if v1.value != 0:
      next_position = to_address.value
    print_debug(self.program_counter, "if true: ", v1.value, next_position)
    return next_position

  def jump_if_false(self):
    next_position = self.program_counter + 3
    opcode, v1, to_address = self.instructions[self.program_counter:next_position]
    v1, to_address = self.opcode_and_vals_to_variables(opcode, [v1, to_address])
    if v1.value == 0:
      next_position = to_address.value
    print_debug(self.program_counter, "if false: ", v1.value, next_position)
    return next_position

  def less_than(self):
    next_position = self.program_counter + 4
    opcode, v1, v2, storage_location = self.instructions[self.program_counter:next_position]
    v1, v2 = self.opcode_and_vals_to_variables(opcode, [v1, v2])
    self.instructions[storage_location] = 1 if v1.value < v2.value else 0
    print_debug(self.program_counter, "less than: ", v1.value, v2.value)
    return next_position

  def equals(self):
    next_position = self.program_counter + 4
    opcode, v1, v2, storage_location = self.instructions[self.program_counter:next_position]
    v1, v2 = self.opcode_and_vals_to_variables(opcode, [v1, v2])
    self.instructions[storage_location] = 1 if v1.value == v2.value else 0
    print_debug(self.program_counter, "equals: ", v1.value, v2.value)
    return next_position


def sequences(base_sequence):
  return list(itertools.permutations(base_sequence, 5))

# for part 1 run with parameters 'input.txt'
def solve_part_1(filename):
  highest_result = 0

  for sequence in sequences(range(5)):

    input_signal = 0
    # start out the input buffer with the value 1
    for value in sequence:
      instructions = to_value(read_input(filename)[0])
      buffer = Buffer()
      # no sharing buffers between programs - just the last output signal
      amplifier = IntcodeProgram(instructions, buffer, buffer)
      
      buffer.add(Variable(None, 1, value))
      buffer.add(Variable(None, 1, input_signal))
    
      while True:
        try:
          amplifier.run_next_instruction()
        except DoneException:
          input_signal = buffer.next().value
          break
    
    if highest_result < input_signal:
      highest_result = input_signal
    
  print highest_result

def solve_part_2(filename):
  highest_result = 0

  for sequence in sequences(range(5, 10)):

    input_signal = 0

    amplifiers = []
    for value in sequence:
      input_buffer = Buffer()
      input_buffer.add(Variable(None, 1, value))
      amplifiers.append(IntcodeProgram(to_value(read_input(filename)[0]), input_buffer, None))

    for i in range(len(amplifiers)):
      # wrap to the first amplifier once we're on the last one
      output_buffer_index = 0 if i == len(amplifiers) - 1 else i + 1
      amplifiers[i].output_buffer = amplifiers[output_buffer_index].input_buffer

    initial_buffer = amplifiers[0].input_buffer
    initial_buffer.add(Variable(None, 1, input_signal))

    current_amplifier = 0

    while True:
      try:
        amplifiers[current_amplifier].run_next_instruction()
      except PauseException:
        current_amplifier = (current_amplifier + 1) % len(amplifiers)
        print_debug("Concede to: " + str(current_amplifier))
      except DoneException:
        if current_amplifier == len(amplifiers) - 1:
          input_signal = amplifiers[current_amplifier].output_buffer.next().value
          print_debug(input_signal)
          break
        else:
          # we need to let ALL the amplifiers complete before we get our final amplified value
          current_amplifier += 1

    if highest_result < input_signal:
      highest_result = input_signal

  print(highest_result)
