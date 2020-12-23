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
        self.piece_to_piece_map = self.generate_connections_map()

    def generate_edge_map(self):
        edge_to_piece_map = defaultdict(list)
        for piece in self.pieces:
            edges = [piece.top, piece.bottom, piece.left, piece.right]
            reversed_edges = [piece.top[::-1], piece.bottom[::-1], piece.left[::-1], piece.right[::-1]]
            for edge in edges + reversed_edges:
                edge_to_piece_map[edge].append(piece)
        for k, v in edge_to_piece_map.items():
            d_print('{}: {}'.format(k, v))
        return edge_to_piece_map

    def generate_connections_map(self):
        piece_to_piece_map = defaultdict(set)
        for pieces in self.edge_map.values():
            if len(pieces) == 2:
                p1, p2 = pieces
                piece_to_piece_map[p1].add(p2)
                piece_to_piece_map[p2].add(p1)
        return piece_to_piece_map

    def get_corners(self):
        # The corner pieces should be the only 4 pieces that have 2 edges with no connections in the edge map twice
        corners = []
        for k, v in self.piece_to_piece_map.items():
            d_print("{} -> {}".format(k, v))
            if len(v) == 2:
                corners.append(k)
        return corners

    def orient_piece_to_the_left(self, right_edge, to_connect):
        if to_connect.left == right_edge:
            pass
        elif to_connect.top == right_edge:
            to_connect.rotate(1)
            to_connect.flip(horizontal)
        elif to_connect.right == right_edge:
            to_connect.flip(horizontal)
        elif to_connect.bottom == right_edge:
            to_connect.rotate(1)
        elif to_connect.left[::-1] == right_edge:
            to_connect.flip(vertical)
        elif to_connect.top[::-1] == right_edge:
            to_connect.rotate(3)
        elif to_connect.right[::-1] == right_edge:
            to_connect.rotate(2)
        elif to_connect.bottom[::-1] == right_edge:
            to_connect.d_print()
            to_connect.flip(horizontal)
            to_connect.rotate(1)
        return to_connect

    def orient_piece_below(self, bottom_edge, to_connect):
        if to_connect.top == bottom_edge:
            pass
        elif to_connect.left == bottom_edge:
            to_connect.rotate(1)
            to_connect.flip(horizontal)
        elif to_connect.bottom == bottom_edge:
            to_connect.flip(vertical)
        elif to_connect.right == bottom_edge:
            to_connect.rotate(3)
        elif to_connect.top[::-1] == bottom_edge:
            to_connect.flip(horizontal)
        elif to_connect.left[::-1] == bottom_edge:
            to_connect.rotate(1)
        elif to_connect.bottom[::-1] == bottom_edge:
            to_connect.rotate(2)
        elif to_connect.right[::-1] == bottom_edge:
            to_connect.flip(horizontal)
            to_connect.rotate(1)
        return to_connect

    # At first I was thinking of a divide and conquer strategey here... but you might end up with different sized
    # edges that seem harder to match. What I'm thinking now is with the piece -> pieces mapping, identifying the
    # corners and edge pieces should be fairly trivial, so take my IRL approach to solving puzzles and do the border
    # first then use the piece map to fill in the middle (getting the edges to line up is going to be the tricky bit
    # but I think once the corners are oriented properly then it _should_ just be a matter of flipping/rotating until
    # the adjacent pieces fit.
    #
    # Not going to tackle this now though. My brain hurts.
    # 1. Get the first top-left corner set and oriented so it's edges that connect with other pieces face down and to the 
    # right. (Shouldn't matter which corner we choose to start with).
    # 2. Then, take the right edge and connect that edge to it's other piece until you get to the piece that has no
    #   connection to it's right edge (this will be the top right corner for the first row, then just the right edge
    #   piece for each following row).
    # 3. Rinse and repeat until all of the pieces are set.
    #
    # The sea monster pattern search will then just be walking through the puzzle checking for matches in various
    # directions. (JUST :P)
    def arrange_pieces(self):
        start_piece = self.get_corners()[0]
        disconnected_pieces = {piece for piece in self.pieces if piece != start_piece}
        # Orient the starting corner as the top left corner of the puzzle
        while len(self.edge_map[start_piece.bottom]) < 2 or len(self.edge_map[start_piece.right]) < 2:
            start_piece.rotate(1)
            d_print(self.edge_map[start_piece.bottom])
            d_print(self.edge_map[start_piece.right])
            d_print(start_piece)
            start_piece.d_print()
        start_piece.d_print()
        current_piece = start_piece
        rows = [[] for _ in range(self.dimensions)]
        rows[0].append(current_piece)
        row_index = 0
        while len(disconnected_pieces) > 0:
            connections = [piece for piece in self.edge_map[current_piece.right] if piece != current_piece]
            if len(connections) == 0:
                # we've hit the edge of this row, time to start the next row
                current_piece = rows[row_index][0]
                connections = [piece for piece in self.edge_map[current_piece.bottom] if piece != current_piece]
                d_print("Connecting edge piece")
                to_connect.d_print()
                to_connect = connections[0]
                to_connect = self.orient_piece_below(current_piece.bottom, to_connect)
                row_index += 1
            else:
                to_connect = connections[0]
                d_print("Starting next row")
                to_connect.d_print()
                to_connect = self.orient_piece_to_the_left(current_piece.right, to_connect)
            rows[row_index].append(to_connect)
            disconnected_pieces.remove(to_connect)
            current_piece = to_connect
        return rows

    def assemble_pieces(self):
        arranged_pieces = self.arrange_pieces()
        assembled_pixels = []
        for pieces_row in arranged_pieces:
            assembled_row = [[] for _ in range(len(pieces_row[0].pixels) - 2)]
            for piece in pieces_row:
                piece.strip_borders()
                for row_index in range(len(piece.pixels)):
                    assembled_row[row_index] += piece.pixels[row_index]
            assembled_pixels += assembled_row
        return Piece(1, assembled_pixels)
            

sea_monster = [
    list('                  # '),
    list('#    ##    ##    ###'),
    list(' #  #  #  #  #  #   '),
]


class Piece():
    def __init__(self, identifier, pixels):
        self.identifier = identifier
        self.pixels = pixels

    def __repr__(self):
        return 'Piece<{}>'.format(self.identifier)

    @property
    def top(self):
        return tuple(px for px in self.pixels[0])

    @property
    def bottom(self):
        return tuple(px for px in self.pixels[-1])
       
    @property 
    def left(self):
        return tuple(row[0] for row in self.pixels)

    @property
    def right(self):
        return tuple(row[-1] for row in self.pixels)

    def rotate(self, rotations):
        for _ in range(rotations):
            self.pixels = list(list(x)[::-1] for x in zip(*self.pixels))

    def flip(self, direction):
        if direction == vertical:
            self.pixels = self.pixels[::-1]
        else:
            self.pixels = [row[::-1] for row in self.pixels]

    def strip_borders(self):
        self.pixels = self.pixels[1:-1]
        self.pixels = [row[1:-1] for row in self.pixels]

    def d_print(self):
        d_print('----------')
        for row in self.pixels:
            d_print(row)

    def identify_sea_monsters(self):
        monster_length = len(sea_monster[0])
        monster_height = len(sea_monster)

        def _tag_sea_monster(top_left, bottom_right):
            x_start, y_start = top_left
            x_end, y_end = bottom_right
            for y in range(y_start, y_end + 1):
                y_offset = y - y_start
                for x in range(x_start, x_end):
                    x_offset = x - x_start
                    d_print((x_offset, y_offset))
                    if sea_monster[y_offset][x_offset] == '#':
                        self.pixels[y][x] = '0'

        def _matches_sea_monster(px_segment, sm_segment):
            for px, sm in zip(px_segment, sm_segment):
                # I'm not sure if sea monsters can overlap
                if sm == '#' and (px != '#' and px != '0'):
                    return False
            return True 

        for y_index in range(len(self.pixels) - len(sea_monster)):
            for x_index in range(len(self.pixels[0]) - len(sea_monster[0])):
                if _matches_sea_monster(self.pixels[y_index][x_index:x_index+monster_length+1], sea_monster[0]) and \
                        _matches_sea_monster(self.pixels[y_index+1][x_index:x_index+monster_length+1], sea_monster[1]) and \
                        _matches_sea_monster(self.pixels[y_index+2][x_index:x_index+monster_length+1], sea_monster[2]):
                    _tag_sea_monster((x_index, y_index), (x_index + monster_length, y_index + 2)) 

    def compute_choppiness(self):
        total = 0
        for px_row in self.pixels:
            for pixel in px_row:
                if pixel == '#':
                    total += 1
        return total


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


def solve_2(filename):
    puzzle = format_input(read_from_file(filename))
    piece = puzzle.assemble_pieces()
    # we need to check for sea monsters in every orientation of the piece, so we'll rotate, check, 
    # then check that rotation, but flipped, then flip it back to make sure we're rotating in a consistent
    # direction. There are 4 rotations possible.
    for _ in range(4):
        piece.rotate(1)
        piece.identify_sea_monsters()
        piece.flip(horizontal)
        piece.identify_sea_monsters()
        piece.flip(horizontal)
    piece.d_print()
    return piece.compute_choppiness()

