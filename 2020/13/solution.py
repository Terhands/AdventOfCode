from utils import read_from_file, d_print

# bus_loop_minutes - (earliest_time % bus_loop_minutes)
def format_input(lines):
    earliest_time = int(lines[0])
    bus_loop_minutes_list = [int(x) if x != 'x' else -1 for x in lines[1].split(',')]
    return earliest_time, bus_loop_minutes_list


def solve_1(filename):
    earliest_time, bus_data = format_input(read_from_file(filename))
    best_wait_time_data = (-1, None)  # negative to indicate infinite wait time
    for bus_loop_minutes in bus_data:
        if bus_loop_minutes == -1:
            continue  # skip these, we don't know what x means for part 1
        wait_time = bus_loop_minutes - (earliest_time % bus_loop_minutes)
        d_print("Waiting for Bus ({}) will mean a {} minute wait time.".format(bus_loop_minutes, wait_time)) 
        if wait_time < best_wait_time_data[0] or best_wait_time_data[0] == -1:
            best_wait_time_data = (wait_time, bus_loop_minutes)
    best_wait_time, best_bus = best_wait_time_data
    return best_wait_time * best_bus


def slow_strategy(bus_data, start_at_loop=0):
    t, keep_going = -1, True
    loop_times = start_at_loop
    while keep_going:
        loop_times += 1
        t = (loop_times * bus_data[0]) - 1
        d_print("Time: {}".format(t))
        input()
        keep_going = False
        for bus_id in bus_data:
            t += 1
            if bus_id != -1 and not (-0.0001 <= (t % bus_id) <=  0.0001):
                keep_going = True
                break
            d_print("{} is a factor of {}.".format(bus_id, t))
    return t


def fast_strategy(bus_data, start_at_loop=0):
    skip_count = 0
    condensed_bus_data = []
    for index, loop_length in enumerate(bus_data):
        if bus_data[index] == -1:
            skip_count += 1
            continue
        elif skip_count:
            condensed_bus_data.append((-1, skip_count))
            skip_count = 0
        
        condensed_bus_data.append((bus_data[index], 1))

    d_print(condensed_bus_data)
    longest_loop_time = max(bus_data)
    longest_loop_offset = bus_data.index(longest_loop_time)
    d_print("Longest Time {} at offset {}.".format(longest_loop_time, longest_loop_offset))
    
    time, current_loop, keep_going = -1, start_at_loop, True
    while keep_going:
        current_loop += 1
        time = (current_loop * longest_loop_time) - longest_loop_offset
        if time < 0:
            print("oh no.. we ran out of numbers...")
            return
        d_print("Starting at Time: {}".format(time))
        keep_going = False
        for bus_id, time_increment_amount in condensed_bus_data:
            d_print("{}: Bus ID {} - %0 result = {}".format(time, bus_id, time % bus_id))
            if bus_id == -1 or time % bus_id == 0:
                time += time_increment_amount
            else:
                keep_going = True
                break
    return (current_loop * longest_loop_time) - longest_loop_offset


# the number of steps between the factors will be the same each time. Figure out how many iterations of x there are
# until two numbers lines up, then you can jump by that much instead of the first number each time.
def fastest_strategy(bus_data, start_at_loop=0): 
    skip_count = 0
    condensed_bus_data = []
    for index, loop_length in enumerate(bus_data):
        if bus_data[index] == -1:
            skip_count += 1
            continue
        elif skip_count:
            condensed_bus_data.append((-1, skip_count))
            skip_count = 0
        
        condensed_bus_data.append((bus_data[index], 1))
    d_print(condensed_bus_data)
    
    time, current_loop, keep_going = 0, start_at_loop, True
    most_factors_in_a_row = 1
    factor_steps = current_loop
    base_factor = condensed_bus_data[0][0]
    while keep_going:
        current_loop += 1
        factor_steps += 1
        time += base_factor
        if time < 0:
            print("oh no.. we ran out of numbers...")
            return

        d_print("Time: {}".format(time))
        #input()
        keep_going = False
        common_factors = []
        time_this_loop = 0
        for bus_id, time_increment_amount in condensed_bus_data:
            if bus_id == -1 or (time + time_this_loop) % bus_id == 0:
                if bus_id > -1:
                    common_factors.append((time_this_loop, bus_id))
                time_this_loop += time_increment_amount
            else:
                keep_going = True
                break
        d_print("Common factors: {}".format(common_factors))
        if len(common_factors) > most_factors_in_a_row:
            sample_time = time + (factor_steps * base_factor)
            d_print("Jumping {}".format(factor_steps * base_factor))
            d_print("Sample Time: {}, Factor steps: {}, Factor: {}".format(sample_time, factor_steps, base_factor))
            #input()
            for factor in common_factors:
                result = (sample_time + factor[0]) % factor[1]
                d_print("{} + {} % {} = {}".format(sample_time, factor[0], factor[1], result))
            #input() 
            if all([(sample_time + factor[0]) % factor[1] == 0 for factor in common_factors]):
                base_factor = factor_steps * base_factor
                most_factors_in_a_row = len(common_factors)
                d_print("New base factor {}".format(base_factor))
                #input()
            factor_steps = 0  # reset factor steps since we're going to start jumping by a bigger number

    return time

def solve_2(filename):
    _, bus_data = format_input(read_from_file(filename)) 
    loop_times = 0 if filename == 'sample.txt' else 100000000000000 / bus_data[0]
    print("Starting at loop {}".format(round(loop_times)))
    #return slow_strategy(bus_data)
    #return fast_strategy(bus_data, start_at_loop=round(loop_times))
    return fastest_strategy(bus_data)

    
