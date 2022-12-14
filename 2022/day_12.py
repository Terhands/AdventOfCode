from aoc_utils import read_from_file, get_filename

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return int(f"{self.x}{self.y}")

    def __eq__(self, coords):
        return hash(self) == hash(coords)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Location:

    def __init__(self, coordinates, elevation):
        self.coordinates = coordinates
        self.elevation = elevation
        self.connected_locations = []
        self.distance_from_start = None

    def __hash__(self):
        return hash(self.coordinates)

    def __str__(self):
        return f"{self.coordinates} [{self.elevation}]: {', '.join([str(loc.coordinates) for loc in self.connected_locations])}"

    def add_connection(self, location):
        if location and location.elevation - self.elevation <= 1:
            self.connected_locations.append(location)


def  build_map(map_data):
    # Pass 1: Convert our map points to a Location Grid
    starting_location, target_location = None, None
    location_grid = []
    for row in range(len(map_data)):
        location_row = []
        for col in range(len(map_data[row])):
            if 'S' == map_data[row][col]:
                # This is the starting point - essentially, our root node.
                location = Location(Coordinates(col, row), ord('a'))
                starting_location = location
            elif 'E' == map_data[row][col]:
                # This is the target location.
                location = Location(Coordinates(col, row), ord('z'))
                target_location = location
            else:
                location = Location(Coordinates(col, row), ord(map_data[row][col]))
            location_row.append(location)
        location_grid.append(location_row)
    # Pass 2: Connect our locations, now that they all exist
    def get_location(_row, _col):
        try:
            # python will wrap the list if we pass in a negative :P
            if _row >= 0 and _col >= 0:
                return location_grid[_row][_col]
        except:
            pass
        return None

    for row in range(len(location_grid)):
        for col in range(len(location_grid[row])):
            location = location_grid[row][col]
            location.add_connection(get_location(row-1, col))
            location.add_connection(get_location(row+1, col))
            location.add_connection(get_location(row, col-1))
            location.add_connection(get_location(row, col+1))
    return starting_location, target_location, location_grid


def compute_distances_from(starting_location):
    # BFS to implement djikstra's for path lengths
    locations_to_compute = [starting_location]
    
    depth = 0
    while len(locations_to_compute) > 0:
        child_locations = []
        for location in locations_to_compute:
            location.distance_from_start = depth
            child_locations += location.connected_locations
        locations_to_compute = list({l for l in child_locations if l.distance_from_start is None})
        depth += 1
    

def part_1():
    starting_location, target_location, _ = build_map(read_from_file(get_filename(12, is_sample=False), lambda line: [p for p in line.strip()]))
    compute_distances_from(starting_location)
    print(f"Part 1: Shortest path from {starting_location} -> {target_location} is {target_location.distance_from_start} steps.")


def get_potential_starting_locations(location_grid):
    possible_starting_locations = []
    for row in location_grid:
        for location in row:
            if location.elevation == 97:
                possible_starting_locations.append(location)
    return possible_starting_locations


def reset_location_distances(location_grid):
    for row in location_grid:
        for location in row:
            location.distance_from_start = None


def compute_shortest_distance_from_all_possible_starting_locations(possible_starting_locations, target_location, location_grid):
    distances = []
    for starting_location in possible_starting_locations:
        compute_distances_from(starting_location)
        if target_location.distance_from_start:
            distances.append(target_location.distance_from_start)
        reset_location_distances(location_grid)
    return min(distances)


def part_2():
    _, target_location, location_grid = build_map(read_from_file(get_filename(12, is_sample=False), lambda line: [p for p in line.strip()]))
    starting_locations = get_potential_starting_locations(location_grid)
    shortest_distance = compute_shortest_distance_from_all_possible_starting_locations(starting_locations, target_location, location_grid)
    print(f"Part 2: Shortest path from any starting location -> {target_location} is {shortest_distance} steps.")


part_1()
part_2()
