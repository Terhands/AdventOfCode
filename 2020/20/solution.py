from utils import read_from_file, d_print

from collections import defaultdict
import math


vertical = 1
horizontal = 0


class Puzzle():
    def __init__(self, pieces):
        self.pieces = pieces
        self.dimensions = int(math.sqrt(len(pieces)))
        self.edge_map = self.generate_edge_map()

    def generate_edge_map(self):
        edge_to_piece_map = defaultdict(list)
        for piece in self.pieces:
            edges = [piece.top, piece.bottom, piece.left, piece.right]
            reversed_edges = [piece.top, piece.bottom, piece.left, piece.right]
            [edge.reverse() for edge in reversed_edges]
            for edge in edges + reversed_edges:
                edge_to_piece_map[''.join(edge)].append(piece)
        for k, v in edge_to_piece_map.items():
            d_print('{}: {}'.format(k, v))
        return edge_to_piece_map

    def get_corners(self):
        # The corner pieces should be the only 4 pieces that have 2 edges with no connections in the edge map twice
        piece_to_piece_map = defaultdict(set)
        for pieces in self.edge_map.values():
            if len(pieces) == 2:
                p1, p2 = pieces
                piece_to_piece_map[p1].add(p2)
                piece_to_piece_map[p2].add(p1)

        corners = []
        for k, v in piece_to_piece_map.items():
            d_print("{} -> {}".format(k, v))
            if len(v) == 2:
                corners.append(k)
        return corners

    def assemble_pieces(self):
        pass

class Piece():
    def __init__(self, identifier, pixels):
        self.identifier = identifier
        self.pixels = pixels

    def __repr__(self):
        return 'Piece<{}>'.format(self.identifier)

    @property
    def top(self):
        return [px for px in self.pixels[0]]

    @property
    def bottom(self):
        return [px for px in self.pixels[-1]]
       
    @property 
    def left(self):
        return [row[0] for row in self.pixels]

    @property
    def right(self):
        return [row[-1] for row in self.pixels]

    def rotate(self):
        self.flip(vertical)
        self.flip(horizontal)

    def flip(self, direction):
        if direction == vertical:
            self.pixels.reverse()
        else:
            [row.reverse() for row in self.pixels]


def format_input(lines):
    image_pieces = []
    current_image_id = None
    current_image_piece = []
    for line in lines:
        if not line:
            image_pieces.append(Piece(current_image_id, current_image_piece))
            current_image_piece = []
        elif 'Tile' in line:
            current_image_id = int(line[5:-1])
        else:
            current_image_piece.append(line)
    return Puzzle(image_pieces)


def solve_1(filename):
    puzzle = format_input(read_from_file(filename))
    corner_pieces = puzzle.get_corners()
    d_print(corner_pieces)
    total = 1
    for piece in corner_pieces:
        total *= piece.identifier
    return total











