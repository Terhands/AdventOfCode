import collections


class MarblesGame(object):

    scores = collections.defaultdict(int)

    def __init__(self, num_players):
        self.current_node = Node(0, None, None)
        self.marbles_in_play = 1
        self.num_players = num_players

    def place_marble(self, value):
        if value % 23 == 0:
            # this is gross...
            to_remove = self.current_node.left.left.left.left.left.left.left
            self.current_node = to_remove.right
            to_remove.right.left = to_remove.left
            to_remove.left.right = to_remove.right
            self.scores[value % self.num_players] += value + to_remove.value
            self.marbles_in_play -= 1
        else:
            place_beside = self.current_node.right
            prev_right = place_beside.right
            place_beside.right = Node(value, place_beside, prev_right)
            prev_right.left = place_beside.right
            self.current_node = place_beside.right
            self.marbles_in_play += 1

    def high_score(self):
        return max(self.scores.values())

    def __repr__(self):
        cw_list = []
        ccw_list = []
        curr_cw, curr_ccw = self.current_node, self.current_node
        # sanity check for the full loop in both directions
        for _ in range(self.marbles_in_play + 1):
            cw_list.append(str(curr_cw))
            ccw_list.append(str(curr_ccw))
            curr_cw = curr_cw.right
            curr_ccw = curr_ccw.left
        
        return '%s\n%s' % ('->'.join(cw_list), '<-'.join(ccw_list))


class Node(object):

    def __init__(self, value, ccw_neighbour, cw_neighbour):
        self.value = value
        self.left = ccw_neighbour or self
        self.right = cw_neighbour or self

    def __repr__(self):
        return "%s" % self.value


def read_input(filename):
    with open(filename) as f:
        return [l.replace('\n', '') for l in f.readlines() if l.strip() != ""]


def parse(line):
    parts = line.split(' ')
    players = int(parts[0])
    last_marble = int(parts[6])
    return players, last_marble


def part1(lines):
    for l in lines:  # loop over the sample inputs

        players, num_marbles = parse(l)
        game = MarblesGame(players)

        for next_marble in range(1, num_marbles + 1):
            game.place_marble(next_marble)

        print "High Score: %s" % game.high_score()


def part2():
    lines = read_input('input-p2.txt')
    part1(lines)
