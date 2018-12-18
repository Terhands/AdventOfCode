NORTH = 'N'
EAST = 'E'
SOUTH = 'S'
WEST = 'W'

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

def read_input(filename):
    with open(filename) as f:
        return [l.replace('\n', '') for l in f.readlines()]


class Tracks(object):

    def __init__(self, lines):
        
        self.time_elapsed = 0
        self.carts = []
        self.track = [l for l in lines]
        
        self.width = len(lines[0])
        self.height = len(lines)

        self.done = False

        for y in range(self.height):
            self.track[y] = list(self.track[y])
            for x in range(self.width):
                self.track[y][x] = self._cart_to_track(self.track[y][x], x, y)

    def __repr__(self):
        cart_map = {(cart.x, cart.y): cart for cart in self.carts}
        # print cart_map
        result = ""
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in cart_map:
                    result += cart_map[(x, y)].direction
                else:
                    result += self.track[y][x]
            result += '\n'
        return result
                
    def _cart_to_track(self, cart_token, x, y):
        if cart_token in ['^', 'v']:
            if cart_token == '^':
                self.carts.append(Cart(x, y, NORTH))
            else:
                self.carts.append(Cart(x, y, SOUTH))
            return '|'
        if cart_token in ['>', '<']:
            if cart_token == '>':
                self.carts.append(Cart(x, y, EAST))
            else:
                self.carts.append(Cart(x, y, WEST))
            return '-'
        return cart_token

    def loop(self):
        self.time_elapsed += 1
        sorted_carts = sorted(self.carts, key=lambda c: (c.y, c.x))
        for cart in sorted_carts:
            cart.move(self.track)
            if cart.has_collided(sorted_carts) is not None:
                print "Collision at: %s" % cart
                self.done = True
                return

    def loop2(self):
        self.time_elapsed += 1
        sorted_carts = sorted(self.carts, key=lambda c: (c.y, c.x))
        unsafe_cart_ids = []
        for cart in sorted_carts:
            cart.move(self.track)
            other_cart = cart.has_collided(sorted_carts)
            if other_cart is not None:
                unsafe_cart_ids += [other_cart.id, cart.id]
                # print "Collision at: %s" % cart
        safe_carts = [cart for cart in self.carts if cart.id not in unsafe_cart_ids]
        # print safe_carts
        self.carts = safe_carts
                

class Cart(object):

    turn_choices = 'LSR'

    def __init__(self, x, y, direction):
        self.id = '%s,%s' % (x, y) # the original position is unique
        self.next_choice = 0
        self.x = x
        self.y = y
        self.direction = direction

    def __repr__(self):
        return "%s: (%s, %s)" % (self.direction, self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def next_direction(self):
        turn = self.turn_choices[self.next_choice]
        self.next_choice = (self.next_choice + 1) % 3
        if turn == 'L':
            self.direction = DIRECTIONS[(DIRECTIONS.index(self.direction) - 1) % len(DIRECTIONS)]
        elif turn == 'R':
            self.direction = DIRECTIONS[(DIRECTIONS.index(self.direction) + 1) % len(DIRECTIONS)]

    def has_collided(self, carts):
        for cart in carts:
            if cart.id != self.id and self == cart:
                return cart
        return None

    # This is gross...
    def move(self, track):
        if self.direction == NORTH:
            self.y -= 1
            track_at = track[self.y][self.x]
            if track_at == '\\':
                self.direction = WEST
            if track_at == '/':
                self.direction = EAST

        elif self.direction == SOUTH:
            self.y += 1
            track_at = track[self.y][self.x]
            if track_at == '\\':
                self.direction = EAST
            if track_at == '/':
                self.direction = WEST

        elif self.direction == EAST:
            self.x += 1
            track_at = track[self.y][self.x]
            if track_at == '\\':
                self.direction = SOUTH
            if track_at == '/':
                self.direction = NORTH

        elif self.direction == WEST:
            self.x -= 1
            track_at = track[self.y][self.x]
            if track_at == '\\':
                self.direction = NORTH
            if track_at == '/':
                self.direction = SOUTH
        
        if track_at == '+':
            self.next_direction()


def part1(input):
    tracks = Tracks(input)
    i = 0
    while not tracks.done:
        # print tracks
        tracks.loop()
        i += 1
        # if i == 15:
        #     break
    return tracks

def part2(input):
    tracks = Tracks(input)
    i = 0
    while len(tracks.carts) > 1:
        # print tracks
        tracks.loop2()
        i += 1
        # if i == 15:
        #     break
    print tracks.carts[0]
    return tracks
