from utils import read_from_file, d_print


class Simulation():

    FLOOR = '.'
    EMPTY = 'L'
    OCCUPIED = '#'

    def __init__(self, seats):
        self.states = [seats]
        self.num_rows = len(seats)
        self.num_seats_per_row = len(seats[0])

    def next_state(self):
        state = self.last_state
        new_state = []
        for row_index in range(len(state)):
            new_state.append([])
            for seat_index in range(len(state[row_index])):
                
                seat = state[row_index][seat_index]
                if seat == self.FLOOR:
                    new_state[row_index].append(self.FLOOR)
                    continue

                adjacent_seats = self.get_adjacent_seats(row_index, seat_index)
                num_occupied = sum([self.is_seat_occupied(s[0], s[1], state) for s in adjacent_seats])
                d_print("Seat ({}, {}) has {} occupied adjacent seats.".format(row_index, seat_index, num_occupied))
                if seat == self.EMPTY and num_occupied == 0:
                    new_state[row_index].append(self.OCCUPIED)
                    continue

                if seat == self.OCCUPIED and num_occupied >= 4:
                    new_state[row_index].append(self.EMPTY)
                    continue

                # otherwise the seat doesn't change
                new_state[row_index].append(state[row_index][seat_index])

        self.states.append(new_state)

    def next_state_v2(self):
        state = self.last_state
        new_state = []
        for row_index in range(len(state)):
            new_state.append([])
            for seat_index in range(len(state[row_index])):
                
                seat = state[row_index][seat_index]
                if seat == self.FLOOR:
                    new_state[row_index].append(self.FLOOR)
                    continue

                num_occupied = self.num_occupied_visible_seats(row_index, seat_index)
                #d_print("Seat ({}, {}) has {} occupied adjacent seats.".format(row_index, seat_index, num_occupied))
                if seat == self.EMPTY and num_occupied == 0:
                    new_state[row_index].append(self.OCCUPIED)
                    continue

                if seat == self.OCCUPIED and num_occupied >= 5:
                    new_state[row_index].append(self.EMPTY)
                    continue

                # otherwise the seat doesn't change
                new_state[row_index].append(state[row_index][seat_index])

        self.states.append(new_state)

    def num_occupied_visible_seats(self, seat_row, seat_col):
        state = self.last_state
        num_visible_occupied = 0
        directions = [(1, 1), (1, 0), (0, 1), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        for y_direction, x_direction in directions:
            y, x = seat_row, seat_col

            #if seat_row == 0 and seat_col == 0:
            #    d_print("Checking aroun seat ({}, {})".format(y, x))
            y += y_direction
            x += x_direction
            while 0 <= y < self.num_rows and 0 <= x < self.num_seats_per_row:
                #if seat_row == 0 and seat_col == 0:
                #    d_print("Checking seat: ({}, {})".format(y, x))
                if state[y][x] == self.EMPTY:
                    # apparently empty seats break line of sight
                    break
                if self.is_seat_occupied(y, x, state):
                    num_visible_occupied += 1
                    break
                y += y_direction
                x += x_direction
        return num_visible_occupied

    def get_adjacent_seats(self, row_index, seat_index):
        seats = [
            (row_index - 1, seat_index - 1),
            (row_index - 1, seat_index),
            (row_index - 1, seat_index + 1),
            (row_index, seat_index - 1),
            (row_index, seat_index + 1),
            (row_index + 1, seat_index - 1),
            (row_index + 1, seat_index),
            (row_index + 1, seat_index + 1)
        ]
        # python is fun and uses negatives for reverse indexing, so we'll just strip these out.
        seats = [(row, seat) for row, seat in seats if row >=0 and seat >=0] 
        return seats

    def is_seat_occupied(self, row_index, seat_index, state):
        try:
            is_occupied = state[row_index][seat_index] == self.OCCUPIED
        except IndexError:
            # if the seat doesn't exist it can't be occupied
            is_occupied = False
        #d_print("Seat ({}, {}) {}.".format(row_index, seat_index, "occupied" if is_occupied else "unoccupied"))
        return 1 if is_occupied else 0

    @property
    def last_state(self):
        return self.states[-1]

    def has_stabilized(self):
        return len(self.states) > 1 and self.states[-1] == self.states[-2]

    def steps_taken(self):
        return len(self.states) - 1 # our initial state doesn't count as a step taken

    def current_occupied_seats(self):
        state = self.last_state
        occupied_seats_total = 0
        for row in state:
            for seat in row:
                if seat == self.OCCUPIED:
                    occupied_seats_total += 1
        return occupied_seats_total

    def print_current_state(self):
        state = self.last_state
        for row in state:
            d_print(row)


def format_input(lines):
    seats = [line.strip() for line in lines if line.strip()]
    return Simulation(seats)


def solve_1(filename):
    simulation = format_input(read_from_file(filename))
    simulation.print_current_state()
    while not simulation.has_stabilized():
        d_print('-------------------------')
        simulation.next_state()
        simulation.print_current_state()
        #input()
    return simulation.current_occupied_seats()


def solve_2(filename):
    simulation = format_input(read_from_file(filename))
    simulation.print_current_state()
    while not simulation.has_stabilized():
        d_print('-------------------------')
        simulation.next_state_v2()
        simulation.print_current_state()
        #input()
    return simulation.current_occupied_seats()


