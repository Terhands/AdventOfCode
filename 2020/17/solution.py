from utils import read_from_file, d_print
from collections import defaultdict



class EnergyNode():
    def __init__(self, x, y, z, w=0):
        self.x, self.y, self.z, self.w = x, y, z, w
        self.connections = set()

    def is_connected(self, x, y, z):
        x_diff = abs(self.x - x)
        y_diff = abs(self.y - y)
        z_diff = abs(self.z - z)

        # to be adjacent they can't be more than 1 away in any direction.
        if x_diff in [1, 0] and y_diff in [1, 0] and z_diff in [1, 0]:
            # all 0 diffs mean this is the same point, so it shouldn't count as connected 
            return 1 in [x_diff, y_diff, z_diff]

    def is_connected_4d(self, x, y, z, w):
        x_diff = abs(self.x - x)
        y_diff = abs(self.y - y)
        z_diff = abs(self.z - z)
        w_diff = abs(self.w - w)

        # to be adjacent they can't be more than 1 away in any direction.
        if x_diff in [1, 0] and y_diff in [1, 0] and z_diff in [1, 0] and w_diff in [1, 0]:
            # all 0 diffs mean this is the same point, so it shouldn't count as connected 
            return 1 in [x_diff, y_diff, z_diff, w_diff]

def format_input(lines):
    active_nodes = []
    for y, line in enumerate(lines):
        for x, state in enumerate(line):
            if state == '#':
                active_nodes.append(EnergyNode(x, y, 0, 0))
    return active_nodes


def get_search_ranges(active_nodes):
    min_x, max_x = active_nodes[0].x, active_nodes[0].x
    min_y, max_y = active_nodes[0].y, active_nodes[0].y
    min_z, max_z = active_nodes[0].z, active_nodes[0].z

    for node in active_nodes:
        if node.x > max_x:
            max_x = node.x
        if node.x < min_x:
            min_x = node.x
        if node.y > max_y:
            max_y = node.y
        if node.y < min_y:
            min_y = node.y
        if node.z > max_z:
            max_z = node.z
        if node.z < min_z:
            min_z = node.z
    # range is inclusive on the bottom end and exclusive on the top of the range, add 2 to the top
    # to make sure we expand each step appropriately 
    return list(range(min_x-1, max_x+2)), list(range(min_y-1, max_y+2)), list(range(min_z-1, max_z+2))

def next(active_nodes):
    x_range, y_range, z_range = get_search_ranges(active_nodes)

    connections_to_points = defaultdict(int)
    # ooof
    for x in x_range:
        for y in y_range:
            for z in z_range:
                for node in active_nodes:
                    if node.is_connected(x, y, z):
                        connections_to_points[(x, y, z)] += 1

    coords_to_nodes = {(node.x, node.y, node.z): node for node in active_nodes}

    next_active_nodes = []
    for coords, connections in connections_to_points.items():
        node = coords_to_nodes.get(coords)
        if node and 2 <= connections <= 3:
            next_active_nodes.append(node)
        elif not node and connections == 3:
            next_active_nodes.append(EnergyNode(*coords))

    return next_active_nodes


def d_print_node_state(active_nodes):
    if not d_print.debug:
        return

    coords_to_nodes = {(node.x, node.y, node.z): node for node in active_nodes}
    x_range, y_range, z_range = get_search_ranges(active_nodes)
    d_print('----------------')
    for z in z_range[1:-1]:
        for y in y_range[1:-1]:
            row = ''
            for x in x_range[1:-1]:
                row += '#' if (x, y, z) in coords_to_nodes else '.'
            d_print(row)
        d_print('----------------')


def solve_1(filename):
    active_nodes = format_input(read_from_file(filename))
    for _ in range(6):
        active_nodes = next(active_nodes)
        d_print_node_state(active_nodes)
    return len(active_nodes)


def get_search_ranges_4d(active_nodes):
    min_x, max_x = active_nodes[0].x, active_nodes[0].x
    min_y, max_y = active_nodes[0].y, active_nodes[0].y
    min_z, max_z = active_nodes[0].z, active_nodes[0].z
    min_w, max_w = active_nodes[0].w, active_nodes[0].w

    for node in active_nodes:
        if node.x > max_x:
            max_x = node.x
        if node.x < min_x:
            min_x = node.x
        if node.y > max_y:
            max_y = node.y
        if node.y < min_y:
            min_y = node.y
        if node.z > max_z:
            max_z = node.z
        if node.z < min_z:
            min_z = node.z
        if node.w > max_w:
            max_w = node.w
        if node.w < min_w:
            min_w = node.w
    # range is inclusive on the bottom end and exclusive on the top of the range, add 2 to the top
    # to make sure we expand each step appropriately 
    return \
        list(range(min_x-1, max_x+2)), \
        list(range(min_y-1, max_y+2)), \
        list(range(min_z-1, max_z+2)), \
        list(range(min_w-1, max_w+2))

def next_4d(active_nodes):
    x_range, y_range, z_range, w_range = get_search_ranges_4d(active_nodes)

    connections_to_points = defaultdict(int)
    # ooof
    for x in x_range:
        for y in y_range:
            for z in z_range:
                for w in w_range:
                    for node in active_nodes:
                        if node.is_connected_4d(x, y, z, w):
                            connections_to_points[(x, y, z, w)] += 1

    coords_to_nodes = {(node.x, node.y, node.z, node.w): node for node in active_nodes}

    next_active_nodes = []
    for coords, connections in connections_to_points.items():
        node = coords_to_nodes.get(coords)
        if node and 2 <= connections <= 3:
            next_active_nodes.append(node)
        elif not node and connections == 3:
            next_active_nodes.append(EnergyNode(*coords))

    return next_active_nodes


def solve_2(filename):
    active_nodes = format_input(read_from_file(filename))
    for _ in range(6):
        active_nodes = next_4d(active_nodes)
        d_print_node_state(active_nodes)
    return len(active_nodes)



