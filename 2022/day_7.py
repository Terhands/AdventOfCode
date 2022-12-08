import re

from aoc_utils import read_from_file, get_filename

dir_type, file_type = 'd', 'f'


class FileNode:
    def __init__(self, name, node_type, size, parent):
        self.name = name
        self.node_type = node_type
        self._size = size
        self.parent = parent
        self.children = []
        
    def add_child(self, child):
        if child.name not in [c.name for c in self.children]:
            self.children.append(child)

    def get_child(self, name):
        for child in self.children:
            if child.name == name:
                return child

    def size(self):
        if self.node_type == file_type:
            return self._size
        return sum([child.size() for child in self.children])

    def pretty_print(self, prefix=""):
        if self.node_type == file_type:
            print(f"{prefix}{self.name}\t(file)\t{self.size()}")
        else:
            print(f"{prefix}{self.name}\t(dir)\tContent Size: {self.size()}")
        for child in self.children:
            child.pretty_print(f"{prefix}{self.name if self.parent else ''}/")



def build_file_system(contents):
    root_node = FileNode('/', dir_type, 0, None)
    current_node = root_node
    for line in contents[1:]:
        navigation_match = re.search('cd (.+)', line)
        directory_match = re.search('dir (.+)', line)
        file_match = re.search('(\d+) (.+)', line)

        if navigation_match:
            to_dir = navigation_match.groups()[0]
            if to_dir == '..':  # our regex matches to a single . for some reason...
                current_node = current_node.parent or current_node
            else:
                matching_child = current_node.get_child(to_dir) or FileNode(to_dir, dir_type, 0, current_node)
                current_node.add_child(matching_child)
                current_node = matching_child
        
        elif directory_match:
            dir_name = directory_match.groups()[0]
            directory = current_node.get_child(dir_name) or FileNode(dir_name, dir_type, 0, current_node)
            current_node.add_child(directory)

        elif file_match:
            size, filename = file_match.groups()
            _file = current_node.get_child(filename) or FileNode(filename, file_type, int(size), current_node)
            current_node.add_child(_file)

    return root_node

def directories_with_size_between(node, min_threshold=0, max_threshold=100000):
    all_directories = []
    for child in node.children:
        if child.node_type == dir_type:
            if min_threshold <= child.size() <= max_threshold:
                all_directories.append(child)
            all_directories += directories_with_size_between(child, min_threshold, max_threshold)
    return all_directories


def part_1():
    commands = read_from_file(get_filename(7, is_sample=False), lambda x: x.strip())
    root_node = build_file_system(commands)
    target_directories = directories_with_size_between(root_node, 0, 100000)
    print(f"Part 1: Directories with size <= 100000 summed total: {sum([d.size() for d in target_directories])}")


def part_2():
    total_space = 70000000
    required_space = 30000000

    commands = read_from_file(get_filename(7, is_sample=False), lambda x: x.strip())
    root_node = build_file_system(commands)
    used_space = root_node.size()
    potential_directories = directories_with_size_between(root_node, required_space - (total_space - used_space), total_space)
    print(f"Part 2: Directories with size <= 100000 summed total: {min([d.size() for d in potential_directories])}")


part_1()
part_2()
