import aoc_utils


def to_int(value):
    if value.strip() != '':
        return int(value)


def calories_per_elf(filename):
    calorie_counts = aoc_utils.read_from_file(filename, to_int)
    
    current_total = 0
    total_per_elf = []
    for calories in calorie_counts:
        if calories is None:
            # last line of the file must be blank to avoid an off by one here
            total_per_elf.append(current_total)
            current_total = 0
        else:
            current_total += calories
    return total_per_elf
        


def part_1():
    max_calories = max(calories_per_elf("inputs/day1_input.txt"))
    print(f"The most calories carried: {max_calories}")


def pop_current_max(_list):
    current_max = max(_list)
    _list.remove(current_max)
    return current_max


def part_2():
    per_elf = calories_per_elf("inputs/day1_input.txt")
    top_three = [pop_current_max(per_elf) for _ in range(3)]
    print(f"The top three calories carried are: {top_three} which totals {sum(top_three)} calories")

