from aoc_utils import read_from_file, get_filename


def tree_parser(line):
    return [int(x) for x in line.strip()]


def build_tree_grid(filename):
    return read_from_file(filename, tree_parser)


def is_visible(row, column, grid, *checks):
    for check in checks:
        if check(row, column, grid):
            return True
    return False


def is_visible_from_top(row, column, grid):
    for i in reversed(range(row)):
        if grid[row][column] <= grid[i][column]:
            return False
    return True


def is_visible_from_bottom(row, column, grid):
    for i in range(row + 1, len(grid)):
        if grid[row][column] <= grid[i][column]:
            return False
    return True


def is_visible_from_right(row, column, grid):
    for i in range(column + 1, len(grid[row])):
        if grid[row][column] <= grid[row][i]:
            return False
    return True


def is_visible_from_left(row, column, grid):
    for i in reversed(range(column)):
        if grid[row][column] <= grid[row][i]:
            return False
    return True


def is_edge(row, column, grid):
    return column == 0 or column == len(grid[row]) - 1 or row == 0 or row == len(grid) - 1


def calculate_visible_trees(all_trees, *checks):
    total = 0
    for row in range(len(all_trees)):
        for column in range(len(all_trees[row])):
            total += 1 if is_visible(row, column, all_trees, *checks) else 0
    return total


def part_1():
    trees = build_tree_grid(get_filename(8, is_sample=False))
    total_visible_trees = calculate_visible_trees(
        trees, 
        is_edge,
        is_visible_from_bottom,
        is_visible_from_top,
        is_visible_from_left,
        is_visible_from_right,
    )
    print(f"Part 1: Total visible trees: {total_visible_trees}")
    

def calculate_scenic_value(row, column, grid):
    # east
    east_value = 0
    for i in reversed(range(column)):
        east_value += 1
        if grid[row][column] <= grid[row][i]:
            break
    # west
    west_value = 0
    for i in range(column + 1, len(grid[row])):
        west_value += 1
        if grid[row][column] <= grid[row][i]:
            break
    # north
    north_value = 0
    for i in reversed(range(row)):
        north_value += 1
        if grid[row][column] <= grid[i][column]:
            break
    # south
    south_value = 0
    for i in range(row + 1, len(grid)):
        south_value += 1
        if grid[row][column] <= grid[i][column]:
            break
    # print(f"{east_value} * {west_value} * {north_value} * {south_value}")
    return east_value * west_value * north_value * south_value


def calculate_max_scenic_values(all_trees):
    max_scenic_value = 0
    for row in range(len(all_trees)):
        for column in range(len(all_trees[row])):
            value = calculate_scenic_value(row, column, all_trees)
            if value > max_scenic_value:
                max_scenic_value = value
    return max_scenic_value


def part_2():
    trees = build_tree_grid(get_filename(8, is_sample=False))
    print(f"Part 2: highest scenic value: {calculate_max_scenic_values(trees)}")


part_1()
part_2()