class DoneException(Exception):
  pass


def read_input(filename):
  def no_empties(x):
    return x is not None and x != ''

  with open(filename) as f_in:
    return filter(no_empties, [l.replace('\n', '').strip() for l in f_in.readlines()])


def to_value(line):
  return map(int, line.split(','))


def add():
  return lambda v1, v2: v1 + v2


def mult():
  return lambda v1, v2: v1 * v2


def halt():
  raise DoneException('Computation is complete')


opcodes = {
  1: add,
  2: mult,
  99: halt,
}


def next_position(current_index):
  return current_index + 4


def run_intcode_from_position(program, position):
  opcode, v1_location, v2_location, storage_location = program[position:position+4]
  #print opcode, v1_location, v2_location
  operation = opcodes[opcode]()
  result = operation(program[v1_location], program[v2_location])
  program[storage_location] = result

# for part 1 run with parameters 'input.txt', 12, 2
def solve_part_1(filename, noun, verb):
  # this is a one liner of input
  intcode = to_value(read_input(filename)[0])
  intcode[1] = noun
  intcode[2] = verb
  program_counter = 0
  while True:
    try:
      run_intcode_from_position(intcode, program_counter)
      program_counter += 4
    except DoneException as e:
      print(e)
      return intcode[0]
      

def solve_part_2(filename):
  correct_result_value = 19690720
  for i in range(100):
    for j in range(100):
      if solve_part_1('input.txt', i, j) == correct_result_value:
        print("Noun={noun}, Verb={verb}".format(noun=i, verb=j))
        print("Solution={solution}".format(solution=(i*100) + j))
        return i, j
  print "Failed to solve."




