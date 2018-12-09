import re
import collections
import datetime


pattern = re.compile(r"\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (Guard #(?P<guard_id>\d+) )?(?P<action>\w+)")


def read_input(filename):
    with open(filename) as f:
        return [pattern.match(line.strip()) for line in sorted(f.readlines()) if line.strip() != ""]


def input_to_dict(matches):
    guard_behaviour_dict = collections.defaultdict(list)
    for match in matches:
        timestamp = datetime.datetime.strptime(match.group('timestamp'), "%Y-%m-%d %H:%M")
        new_guard_id = match.group('guard_id')
        action = match.group('action')

        if new_guard_id:
            # don't really care when they start just that they have
            guard_id = new_guard_id
        elif "falls" in action:
            asleep_timestamp = timestamp
        else:
            # print timestamp, guard_id, action
            guard_behaviour_dict[guard_id].append((asleep_timestamp, timestamp))
    return guard_behaviour_dict


def guard_asleep_most(guard_behaviour_dict):
    guard_to_minutes_asleep_map = collections.defaultdict(int)
    for guard, sleep_ranges in guard_behaviour_dict.iteritems():
        for asleep_timestamp, awake_timestamp in sleep_ranges:
            guard_to_minutes_asleep_map[guard] += (awake_timestamp - asleep_timestamp).seconds / 60

    most_minutes = 0
    sleepiest_guard = None
    for guard, minutes in guard_to_minutes_asleep_map.iteritems():
        if most_minutes < minutes:
            most_minutes = minutes
            sleepiest_guard = guard

    return sleepiest_guard


def minute_asleep_most(sleep_ranges):
    minutes_per_day = [0 for _ in range(60)]
    for asleep_time, awake_time in sleep_ranges:
        for i in range((awake_time - asleep_time).seconds / 60):
            minutes_per_day[i + asleep_time.minute] += 1
    max_minute = 0
    sleepiest_minute = None
    for i in range(len(minutes_per_day)):
        if minutes_per_day[i] > max_minute:
            sleepiest_minute = i
            max_minute = minutes_per_day[i]
    return sleepiest_minute, max_minute


def part1(matches):
    guard_behaviour_dict = input_to_dict(matches)
    # print guard_behaviour_dict
    sleepiest_guard = guard_asleep_most(guard_behaviour_dict)
    sleepiest_minute, _ = minute_asleep_most(guard_behaviour_dict[sleepiest_guard])
    return int(sleepiest_guard) * sleepiest_minute


def guard_to_minutes_asleep_count(guard_behaviour_dict):
    guard_to_most_minute_and_count_map = {}
    sleepiest_guard = None
    sleepiest_minute = None
    most_times_asleep = 0
    for guard, sleep_ranges in guard_behaviour_dict.iteritems():
        minute, times_asleep = minute_asleep_most(sleep_ranges)
        if times_asleep > most_times_asleep:
            most_times_asleep = times_asleep
            sleepiest_minute = minute
            sleepiest_guard = guard
    return sleepiest_guard, sleepiest_minute

        

def part2(matches):
    guard_behaviour_dict = input_to_dict(matches)
    guard, minute = guard_to_minutes_asleep_count(guard_behaviour_dict)
    return int(guard) * minute
        