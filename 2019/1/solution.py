

def read_input(filename):
  def no_empties(x):
    return x is not None and x != ''

  with open(filename) as f_in:
    return filter(no_empties, [l.replace('\n', '').strip() for l in f_in.readlines()])


def to_value(line):
  return int(line)


def calculate_fuel(mass):
  return (mass / 3) - 2


def total_fuel(mass):
  total_fuel = 0
  while mass > 0:
    fuel = calculate_fuel(mass)
    total_fuel += fuel if fuel > 0 else 0
    mass = fuel
  return total_fuel


def solve_part_1(filename):
  module_masses = [to_value(line) for line in read_input(filename)]
  module_fuels = [calculate_fuel(module_mass) for module_mass in module_masses]
  return sum(module_fuels)
     

def solve_part_2(filename):
  module_masses = [to_value(line) for line in read_input(filename)]
  module_fuels = [total_fuel(module_mass) for module_mass in module_masses]
  return sum(module_fuels)

