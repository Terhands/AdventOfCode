
def read_input(filename):
  with open(filename) as f:
    return f.readlines()


def format_input(lines):
  return map(int, filter(lambda x: x.strip() != "", lines)) 


def solve_part1(filename):
  print sum(format_input(read_input(filename)))


def solve_part2(filename):
  frequency_changes = format_input(read_input(filename))
  previous_frequencies = [0]
  current_frequency = 0
  while True:
    for change in frequency_changes:
      current_frequency += change
      if current_frequency in previous_frequencies:
        return current_frequency
      previous_frequencies.append(current_frequency)

