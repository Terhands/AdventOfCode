import reader


def solve(filename):
  registers = {'c': 1}
  instructions = reader.get_lines_from_file(filename)
  pc = 0

  while pc < len(instructions):
    pc += perform_instruction(instructions[pc], registers)

  print registers

def perform_instruction(instruction, registers):
  parts = instruction.split(' ')
  if parts[0] == 'cpy':
    registers[parts[2]] = get_value(parts[1], registers)
    return 1
  elif parts[0] == 'inc':
    registers[parts[1]] += 1
    return 1
  elif parts[0] == 'dec':
    registers[parts[1]] -= 1
    return 1
  elif parts[0] == 'jnz':
    if get_value(parts[1], registers) == 0:
      return 1
    else:
      return get_value(parts[2], registers)
    
def get_value(a, registers):
  try:
    return int(a)
  except:
    return registers.get(a, 0)


