import math
import re

from aoc_utils import read_from_file, get_filename


class Monkey():
    def __init__(self, monkey_data):
        self.id = monkey_data['id']
        self.items = monkey_data['items']
        self.operator = monkey_data['operator']
        self.operation_value = monkey_data['value']
        self.test = monkey_data['test']
        self.throw_to_map = monkey_data['throw_to_map']
        self.total_inspections = 0
        self.worry_operation = None

    def monkey_business(self, all_monkeys):
        if self.items:
            self.inspect_item()
            throw_to_id = self.throw_to_map[self.items[0] % self.test == 0]
            throw_to = all_monkeys[throw_to_id]
            self.throw_to_monkey(throw_to)
            self.monkey_business(all_monkeys)

    def operation(self, x):
        y = x if self.operation_value == 'old' else int(self.operation_value)
        if self.operator == '*':
            return x * y
        else:
            return x + y


    def inspect_item(self):
        if self.items:
            self.total_inspections += 1
            value = self.operation(self.items[0])
            self.items[0] = self.worry_operation(value)

    def throw_to_monkey(self, to_monkey):
        to_monkey.catch(self.items[0])
        self.items = self.items[1:]
        
    def catch(self, item):
        self.items.append(item)

    def pprint(self):
        print(f"{self.id} ({self.total_inspections}): {self.items}")


def build_monkeys(contents):
    monkeys = []
    monkey_data = {'id': None, 'items': None, 'operator': None, 'value': None, 'test': None, 'throw_to_map': {True: None, False: None}}
    for line in contents:
        monkey_match = re.search('Monkey (.*):', line)
        if monkey_match:
            monkey_data['id'] = int(monkey_match.groups()[0])
            continue
        items_match = re.search('Starting items: (.*)', line)
        if items_match:
            monkey_data['items'] = [int(i) for i in items_match.groups()[0].split(', ')]
            continue
        addition_operation_match = re.search('Operation: new = old \+ (.*)', line)
        # Yikes, apparently passing around lambdas is a REALLY bad idea here. Just don't :P
        if addition_operation_match:
            value = addition_operation_match.groups()[0]
            monkey_data['operator'] = '+'
            monkey_data['value'] = value
            continue
        product_operation_match = re.search('Operation: new = old \* (.*)', line)
        if product_operation_match:
            value = product_operation_match.groups()[0]
            monkey_data['operator'] = '*'
            monkey_data['value'] = value
            continue
        test_match = re.search('Test: divisible by (\d+)', line)
        if test_match:
            value = test_match.groups()[0]
            monkey_data['test'] = int(value)
            continue
        true_match = re.search('If true: throw to monkey (\d+)', line)
        if true_match:
            value = true_match.groups()[0]
            monkey_data['throw_to_map'][True] = int(value)
            continue
        false_match = re.search('If false: throw to monkey (\d+)', line)
        if false_match:
            value = false_match.groups()[0]
            monkey_data['throw_to_map'][False] = int(value)
            continue

        monkeys.append(Monkey(monkey_data))
        monkey_data = {'id': None, 'items': None, 'operation': None, 'test': None, 'throw_to_map': {True: None, False: None}}
    return monkeys


def monkey_simulator(total_rounds, monkeys, worry_operation):
    for monkey in monkeys:
        monkey.worry_operation = worry_operation
    for i in range(total_rounds):
        print(f"Round {i+1} ------------")
        for monkey in monkeys:
            monkey.monkey_business(monkeys)
        
        # if i in [0, 19, 999, 1999, 2999, 3999, 4999, 5999, 6999, 7999, 8999, 9999]:
        #     for monkey in monkeys:
        #         monkey.pprint()
        #         print(f"End of Round {i+1} -----")
        #     input()

def part_1():
    monkeys = build_monkeys(read_from_file(get_filename(11, is_sample=False), lambda x: x.strip()))
    monkey_simulator(20, monkeys, lambda x: int(x / 3))
    inspections = list(reversed(sorted([monkey.total_inspections for monkey in monkeys])))
    print(f"Part 1: Most inspections were {inspections[:2]} total monkey business was {inspections[0] * inspections[1]}")


def part_2():
    monkeys = build_monkeys(read_from_file(get_filename(11, is_sample=False), lambda x: x.strip()))
    lowest_common_multiple = math.lcm(*[monkey.test for monkey in monkeys])
    # ok, so without some kind of limiting factor, some of these numbers get to be thousands of digits, and any arithmeticic operations on them are
    # slow AF. We know all of our test divisors though, so we also know that when our worry value is divisible by ALL of them, that we can reduce back
    # to the lowest common multiplier. Conveniently, python added an lcm function in 3.9, which makes finding that value (without my gross nonsense math)
    # incredibly easy :tada
    worry_fn = lambda x: x % lowest_common_multiple
    monkey_simulator(10000, monkeys, worry_fn)
    inspections = list(reversed(sorted([monkey.total_inspections for monkey in monkeys])))
    print(f"Part 1: Most inspections were {inspections[:2]} total monkey business was {inspections[0] * inspections[1]}")


part_1()
part_2()
