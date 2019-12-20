
class OrbitObj(object):

  def __init__(self, name):
    self.name = name
    self.orbiting_planet = None # we'll just set these all after creation
    self.orbiters = []

  def total_direct_orbits(self):
    total = len(self.orbiters)
    for orbiter in self.orbiters:
      total += orbiter.total_direct_orbits()
    return total

  def total_indirect_orbits(self):
    total = 0
    for orbiter in self.orbiters:
      total += orbiter.total_direct_orbits()
      total += orbiter.total_indirect_orbits()
    return total

  def total_orbits(self):
    return self.total_direct_orbits() + self.total_indirect_orbits()

  def distance_to_target(self, target):
    visited_planets = [self]
    next_possible_routes = filter(None, self.orbiters + [self.orbiting_planet])

    current_distance = -1 # we are already in orbit, or being orbited by our intial routes
    while True:
      possible_routes = [planet for planet in next_possible_routes if planet not in visited_planets]
      next_possible_routes = []
      for planet in possible_routes:
        if planet == target:
          return current_distance
        next_possible_routes += filter(None, [planet.orbiting_planet] + planet.orbiters)
        visited_planets.append(planet)
      current_distance += 1

def read_input(filename):
  def no_empties(x):
    return x is not None and x != ''

  with open(filename) as f_in:
    return filter(no_empties, [l.replace('\n', '').strip() for l in f_in.readlines()])


def to_values(line):
  return line.split(')')


def to_orbit_map(orbit_pairs):
  total_mapping = dict()
  for orbitee, orbiter in orbit_pairs:
    if orbitee not in total_mapping:
      total_mapping[orbitee] = OrbitObj(orbitee)
    orbitee = total_mapping[orbitee]

    if orbiter not in total_mapping:
      total_mapping[orbiter] = OrbitObj(orbiter)
    orbiter = total_mapping[orbiter]
    orbiter.orbiting_planet = orbitee
    orbitee.orbiters.append(orbiter)
  return total_mapping


def solve_part_1(filename):
  orbital_map = to_orbit_map([to_values(line) for line in read_input(filename)])
  centre_of_mass = orbital_map['COM']
  return centre_of_mass.total_orbits()


def solve_part_2(filename):
  orbital_map = to_orbit_map([to_values(line) for line in read_input(filename)])
  my_location = orbital_map['YOU']
  target_location = orbital_map['SAN']
  return my_location.distance_to_target(target_location)
