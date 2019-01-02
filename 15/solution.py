""" 
Some intial thoughts:

Start by building the map as a graph that is up to 4-connected - then we can just ignore the walls.
Each unit gets 3 attack, 200 hp

Movement then attack
do a search outwards from the units position to find the nearest enemy. 
move towards it.
If in range after (or before movement) then it gets an attack.
If there are multiple enemies in range - always attack the weakest (< hp)
"""

class Map(object):

    def __init__(self, _input, elf_power=3):
        self.tiles = []
        self.units = {
            'E': [],
            'G': []
        }
        self.rounds = -1  # initial round, round 0 is when we start moving
        self.build(_input, elf_power)

    def build(self, _input, elf_power):
        map_height = len(_input)
        map_width = len(_input[0])

        for y in range(map_height):
            self.tiles.append([])
            for x in range(map_width):
                val = _input[y][x]
                if val == '.':
                    tile = Tile(x, y, True)
                # If a unit is on the tile, then build a unit too
                elif val == 'G':
                    tile = Tile(x, y, False)
                    unit = Unit(val, tile)
                    self.units[val].append(unit)
                elif val == 'E':
                    tile = Tile(x, y, False)
                    unit = Unit(val, tile, power=elf_power)
                    self.units[val].append(unit)
                else:
                    tile = Tile(x, y, False)
                self.tiles[y].append(tile)
        
        # build up the tile ajdacency mappings, now we don't need to know about the entire map to determine distances to enemies, etc.
        for y in range(map_height):
            for x in range(map_width):
                t = self.tiles[y][x]
                # take advantage of the ordering here - precedence is reading order (i.e. top to bottom, left to right)
                if y > 0:
                    t.adjacent_tiles.append(self.tiles[y-1][x])
                if x > 0:
                    t.adjacent_tiles.append(self.tiles[y][x-1])
                if x < map_width - 1:
                    t.adjacent_tiles.append(self.tiles[y][x+1])
                if y < map_height - 1:
                    t.adjacent_tiles.append(self.tiles[y+1][x])
                # print "(%s, %s) -> %s" % (t.x, t.y, [(p.x, p.y) for p in t.adjacent_tiles])

    def is_over(self):
        # print self.rounds, self.units
        live_elves = len([e for e in self.units['E'] if e.health > 0])
        live_goblins = len([g for g in self.units['G'] if g.health > 0])
        return live_elves == 0 or live_goblins == 0

    def calculate_outcome(self):
        print self.rounds, sum([u.health for u in self.units['E'] + self.units['G']])
        return self.rounds * sum([u.health for u in self.units['E'] + self.units['G']])

    def loop(self):
        # if 31 > self.rounds > 21:
        #         print self.units
        for unit in sorted(self.units['E'] + self.units['G'], key=self._turn_order_key()):
            if unit.health == 0:
                continue

            nearest_enemies, distance_to_enemies = self.movement_phase(unit)
            if distance_to_enemies == 0 and len(nearest_enemies) > 0:
                self.attack_phase(unit, nearest_enemies)
        self.rounds += 1
    
    def movement_phase(self, unit):
        enemy_race = 'E' if unit.race == 'G' else 'G'
        nearest_enemies, distance = self.closest(unit.position, enemy_race)
        if len(nearest_enemies) > 0:
            if distance > 0:
                # our position can effect the 'closest' result because our current position is impassable
                original_position = unit.position.unit

                # this is kinda gross, but shouldn't be too bad
                for position in unit.position.open_adjacent_tiles():
                    unit.move(position)
                    enemies_after_move, distance_after_move = self.closest(position, enemy_race)
                    if distance_after_move < distance:
                        # if 31 > self.rounds > 21:
                        #     print unit, position.x, position.y
                        return enemies_after_move, distance_after_move
                # put ourselves back on the board if we didn't end up moving
                unit.move(original_position)
        return nearest_enemies, distance
    
    def attack_phase(self, unit, nearest_enemies):
        nearest_enemies = sorted(nearest_enemies, key=self._turn_order_key())
        weakest_enemy = nearest_enemies[0]
        for enemy in nearest_enemies:
            if enemy.health < weakest_enemy.health:
                weakest_enemy = enemy
        unit.attack(weakest_enemy)

    def closest(self, position, enemy_race):
        # this will be a BFS of the graph - making sure to avoid tiles that have already been visted. Essentially just doing an outward search
        # from the unit's current position until we find an enemy.
        visited_positions = [position]
        return self._closest_enemies(position.non_wall_adjacent_tiles(), visited_positions, enemy_race, 0)

    def _closest_enemies(self, positions, previously_visited, enemy_race, distance):
        next_to_check = []
        enemies = []
        for position in set(positions):
            # if 31 > self.rounds > 21:
            #     print position.x, position.y, position.non_wall_adjacent_tiles()
            if position.unit is not None and position.unit.race == enemy_race and position.unit.health > 0:
                enemies.append(position.unit)
            if position.traversable:
                next_to_check += [p for p in position.non_wall_adjacent_tiles() if p not in previously_visited]

        if len(enemies) > 0 or len(next_to_check) == 0:
            # if 31 > self.rounds > 21:
            #     print "found an enemy", enemies, distance
            return enemies, distance

        return self._closest_enemies(next_to_check, previously_visited + positions, enemy_race, distance + 1)

    def _turn_order_key(self):
        def key(u):
            return u.position.y, u.position.x
        return key

    def __repr__(self):
        result = ""
        for row in self.tiles:
            result += ''.join(map(str, row)) + '\n'
        return result


class Tile(object):

    def __init__(self, x, y, traversable):
        # adjacent tiles
        self.adjacent_tiles = []

        self.x = x
        self.y = y
        self.traversable = traversable
        self.unit = None

    def open_adjacent_tiles(self):
        return [t for t in self.adjacent_tiles if t.traversable]

    def non_wall_adjacent_tiles(self):
        return [t for t in self.adjacent_tiles if t.traversable or t.unit is not None]

    def __repr__(self):
        if self.traversable:
            return "."
        if self.unit is not None:
            return self.unit.race
        return "#"


class Unit(object):

    def __init__(self, race, position, power=3):
        self.health = 200
        self.power = power
        self.race = race
        self.position = position
        position.unit = self

    def __repr__(self):
        return "%s: (%s)" % (self.race, self.health)

    def move(self, position):
        new_position = position  # the map can decide the best place for a unit to move next
        if new_position is not None:
            self.position.traversable = True
            self.position.unit = None
            new_position.traversable = False
            new_position.unit = self
            self.position = new_position

    def attack(self, unit):
        unit.health -= self.power
        if unit.health <= 0:
            unit.health = 0
            unit.position.traversable = True
            unit.position.unit = None

def part1(filename):
    with open(filename) as f:
        lines = [l.replace('\n', '') for l in f.readlines() if l.strip() != '']
    game = Map(lines)

    while not game.is_over():
        game.loop()
        if game.rounds % 1 == 0:
            print game
    
    # print "Outcome: ", game.calculate_outcome()
    return game


def part2(filename):
    with open(filename) as f:
        lines = [l.replace('\n', '') for l in f.readlines() if l.strip() != '']

    done = False
    current_power = 20
    while not done:
        game = Map(lines, elf_power=current_power)

        while not game.is_over():
            game.loop()
            if game.rounds % 1 == 0:
                print game.rounds, game.units
                print game

        if len([e for e in game.units['E'] if e.health == 0]) == 0:
            done = True

        current_power += 1
        
    # print game.units
    print "Outcome: ", game.calculate_outcome()
    return game