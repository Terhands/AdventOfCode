class Node(object):

    def __init__(self, _id, children, meta):
        self.children = children
        self.meta = meta
        self.id = _id

    def __repr__(self):
        return "%s: %s" % (self.meta, self.children)


global total_nodes
total_nodes = 0


def node_factory(children, meta):
    global total_nodes
    total_nodes += 1
    return Node(total_nodes, children, meta)


def read_input(filename):
    with open(filename) as f:
        return [int(val) for val in f.readlines()[0].replace('\n', '').split(' ')]


def build_node(values):
    num_children, num_meta = values[0], values[1]
    offset = 2
    children = []
    for _ in range(num_children):  # skip the node header info
        child, child_offset = build_node(values[offset:])
        offset += child_offset
        children.append(child)
    meta = []
    for _ in range(num_meta):
        # print "Meta: %s" % values[offset]
        meta.append(values[offset])
        offset += 1
    return node_factory(children, meta), offset


def sum_meta(node):
    total = 0
    for child in node.children:
        total += sum_meta(child)
    return total + sum(node.meta)


def part1(values):
    # print values
    root, _ = build_node(values)
    # print root
    return sum_meta(root)

def sum_ref_metas(node):
    if len(node.children) == 0:
        return sum(node.meta)

    total = 0
    for ref in node.meta:
        if 0 < ref <= len(node.children):
            total += sum_ref_metas(node.children[ref - 1])
    return total
    


def part2(values):
    root, _ = build_node(values)
    return sum_ref_metas(root)


    

