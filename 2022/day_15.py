from intervaltree import IntervalTree
import re

from aoc_utils import read_from_file, get_filename

def parse_sensors(data):
    sensors_to_closest_beacon = []
    for line in data:
        values = [int(val) for val in re.search('Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line).groups()]
        sensors_to_closest_beacon.append(((values[0], values[1]), (values[2], values[3])))
    return sensors_to_closest_beacon


def compute_manhatten_distance(sensor, beacon):
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])


def calculate_coverage_for_row(row, sensors_to_beacons):
    covered_ranges = IntervalTree()
    covered_points = set()  # interval trees don't handle single point coverage
    for sensor, beacon in sensors_to_beacons:
        sensor_range = compute_manhatten_distance(sensor, beacon)
        distance_to_row = compute_manhatten_distance(sensor, (sensor[0], row))

        positions_covered = sensor_range - distance_to_row
        if positions_covered > 0:
            covered_ranges[sensor[0] - positions_covered:sensor[0] + positions_covered] = sensor
        if positions_covered == 0:
            covered_points.add((sensor[0], positions_covered))

    covered_ranges.merge_overlaps(strict=False)
    covered_points = {p for p in covered_points if not covered_ranges.overlaps(p[0])}
    return covered_ranges, covered_points


def part_1():
    row = 2000000
    sensors_to_beacons = parse_sensors(read_from_file(get_filename(15, is_sample=row==10), lambda x: x.strip()))
    covered_ranges, covered_points = calculate_coverage_for_row(row, sensors_to_beacons)
    row_coverage = sum([1 + i.end - i.begin for i in covered_ranges.all_intervals])
    overlapping_beacons = sum({1 for _, beacon in sensors_to_beacons if beacon[1] == row and (covered_ranges.overlaps(beacon[0]) or beacon in covered_points)})
    print(f"Part 1: Coverage for row {row} is {row_coverage + len(covered_points) - overlapping_beacons}")


def find_uncovered_point(sensors_to_beacons, boundary):
    for y in range(boundary):
        covered_ranges, _ = calculate_coverage_for_row(y, sensors_to_beacons)
        if len(covered_ranges.all_intervals) > 1:
            return sorted(list(covered_ranges.all_intervals))[0].end + 1, y


def part_2():
    row = 2000000
    sensors_to_beacons = parse_sensors(read_from_file(get_filename(15, is_sample=row==10), lambda x: x.strip()))
    x, y = find_uncovered_point(sensors_to_beacons, row * 2)
    print(f"Part 2: Tuning frequence for ({x}, {y}) is {(x * 4000000) + y}")


part_1()
part_2()
