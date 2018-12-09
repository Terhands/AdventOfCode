import collections


class Fabric(object):

    def __init__(self):
        self.num_used = 0
        self.used_by_ids = []

    def set_used(self, used_by):
        self.num_used += 1
        self.used_by_ids.append(used_by)


def read_input(filename):
    def cleanup(l):
        to_replace = [('#', ''), ('@', ''), (',', ' '), ('x', ' '), (':', ''), ('  ', ' '), ('\n', '')]
        for old, new in to_replace:
            l = l.replace(old, new)
        return map(int, l.split(' '))

    with open(filename) as f:
        return [cleanup(line) for line in f.readlines() if line.strip() != ""]


def build_model(x, y):
    return [[Fabric() for _ in range(x)] for _ in range(y)]


def populate_model(input, x_total, y_total):
    model = build_model(x_total, y_total)
    for _id, x_offset, y_offset, x_len, y_len in input:
        for x_pos in range(x_len):
            for y_pos in range(y_len):
                model[y_offset+y_pos][x_offset+x_pos].set_used(_id)
    return model


def part1(input):
    x_total, y_total = 1000, 1000
    model = populate_model(input, x_total, y_total)
    total_conflicting_inches = 0
    for y in range(y_total):
        for x in range(x_total):
            if model[y][x].num_used > 1:
                total_conflicting_inches += 1

    return total_conflicting_inches


def part2(input):
    x_total, y_total = 1000, 1000
    model = populate_model(input, x_total, y_total)
    id_conflict_map = collections.defaultdict(set)
    for y in range(y_total):
        for x in range(x_total):
            used_by_ids = model[y][x].used_by_ids
            for _id in used_by_ids:
                id_conflict_map[_id] = set(list(id_conflict_map[_id]) + used_by_ids)

    for _id, conflicting_ids in id_conflict_map.iteritems():
        if len(conflicting_ids) == 1 and _id in conflicting_ids:
            return _id
    