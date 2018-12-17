import re


def read_input(filename):
    with open(filename) as f:
        lines = f.readlines()
    
    # switch out . for , since . as a regex matches all characters
    initial_state = lines[0].split(' ')[2].replace('.', ',').replace('\n', '')
    patterns = [l.replace('\n', '').replace('.', ',') for l in lines[1:] if l.strip() != '']

    return initial_state, patterns


def build_patterns(pattern_strs):
    propagation_patterns = [p.split(' => ')[0] for p in pattern_strs if p[-1] != ',']
    combined_pattern = r'(%s)' % r'|'.join(propagation_patterns)
    print combined_pattern
    return re.compile(combined_pattern)


def add_padding(state):
    padded_state = state
    f_offset = 0
    b_offset = 0
    for i in range(4):
        if state[i] == '#' and f_offset == 0:
            padded_state = ',' * (4 - i) + padded_state
            f_offset = 4 - i
        if state[-(i + 1)] == '#' and b_offset == 0:
            padded_state = padded_state + ',' * (4 - i)
            b_offset = 1
    # print "%s : %s -> %s" % (f_offset, state, padded_state)
    return padded_state, f_offset


def next_generation(state, propagation_pattern, pot_offset):
    next_state = ''
    plant_sum = 0
    
    padded_state, additional_offset = add_padding(state)
    pot_offset += additional_offset

    for i in range(len(padded_state)):
        next_state += '#' if propagation_pattern.match(padded_state[i-2:i+3]) else ','
        plant_sum += i - pot_offset if next_state[-1] == '#' else 0
    return next_state, plant_sum, pot_offset

def part1(initial_state, patterns):
    propagation_pattern = build_patterns(patterns)
    state = initial_state
    offset = 0
    print 0, state
    for i in range(1, 21):
        state, plant_sum, offset = next_generation(state, propagation_pattern, offset)
        print i, state, plant_sum
    return plant_sum

def trim_padding(state):
    first_plant = None
    last_plant = None

    position = 0
    while first_plant is None or last_plant is None:
        if state[position] == '#' and first_plant is None:
            first_plant = position
        if state[-(position+1)] == '#' and last_plant is None:
            last_plant = -(position)
        position += 1
    return state[first_plant:last_plant]


def part2(initial_state, patterns):
    propagation_pattern = build_patterns(patterns)
    state = initial_state
    offset = 0
    # print 0, state
    # total_plants = sum([1 for p in initial_state if p == '#'])
    prev_states = []
    i = 0
    while i < 170:
        state, plant_sum, offset = next_generation(state, propagation_pattern, offset)
        trimed_state = trim_padding(state)
        if trimed_state in prev_states:
            print "found a repeat from %s -> %s steps" % (prev_states.index(trimed_state), i)
            # break
        prev_states.append(trimed_state)
        if i > 160:
            # so as of iteration 166 the pattern repeats forever, but shifts over. So the additional pot sum increases by 26 each time after that generation. Gen 167 = 5011
            # Then all we need to do is add 26 for the additional (50000000000 - 167) generations left. So the final solution will be 5011 + ((50000000000 - 167) * 26)
            # so 1,300,000,000,669 should be the right answer....
            print i, state, plant_sum        

        i += 1
        
