from collections import defaultdict
from utils import read_from_file, d_print
import enum
import itertools


class Section(enum.Enum):
    CONDITIONS = 1
    MY_TICKET = 2
    OTHER_TICKETS = 3


class Condition():
    def __init__(self, name, r_min, r_max):
        self.name = name
        self.min = r_min
        self.max = r_max

    def __repr__(self):
        return "{}: {} - {}".format(self.name, self.min, self.max)

    def is_valid(self, value):
        return self.min <= value <= self.max

def format_condition(condition_str):
    name, ranges = condition_str.split(': ')
    ranges = ranges.split(' or ')
    conditions = []
    for r in ranges:
        r_min, r_max = r.split('-')
        conditions.append(Condition(name, int(r_min), int(r_max)))
    return conditions


def format_ticket(ticket_str):
    return tuple(int(ticket_field) for ticket_field in ticket_str.split(','))


format_section_fn_map = {
    Section.CONDITIONS: format_condition,
    Section.MY_TICKET: format_ticket,
    Section.OTHER_TICKETS: format_ticket
}


def format_input(lines):
    data = {
        Section.CONDITIONS: [],
        Section.MY_TICKET: [],
        Section.OTHER_TICKETS: [],
    }
    current_section = Section.CONDITIONS 
    for line in lines:
        if not line:
            continue
        elif line == 'your ticket:':
            current_section = Section.MY_TICKET
            continue
        elif line == 'nearby tickets:':
            current_section = Section.OTHER_TICKETS
            continue

        data[current_section].append(format_section_fn_map[current_section](line))
    data[Section.CONDITIONS] = list(itertools.chain(*data[Section.CONDITIONS]))
    return data


def is_valid_ticket_field(ticket_field, conditions):
    d_print("Validating {} for {}".format(ticket_field, conditions))
    for condition in conditions:
        if condition.is_valid(ticket_field):
            d_print("{} is valid".format(ticket_field))
            return True
    return False


def solve_1(filename):
    validation_cache = {}
    ticket_data = format_input(read_from_file(filename))
    invalid_field_values = []
    d_print(ticket_data)
    for ticket in ticket_data[Section.OTHER_TICKETS]:
        for ticket_field in ticket:
            if ticket_field not in validation_cache:
                conditions = ticket_data[Section.CONDITIONS]
                validation_cache[ticket_field] = is_valid_ticket_field(ticket_field, conditions)
            if not validation_cache[ticket_field]:
                invalid_field_values.append(ticket_field)
    return sum(invalid_field_values), invalid_field_values


# This guy's a constraint satisfaction problem - strategy will be
# 1. map each possible field value to which constraints it satisfies. 
# 2. disregard all tickets that don't satisfy any constraint.
# 3. see if we can find any tickets with fields that only satisfy a single constraint and
#   work backwards form there as much as possible
# 4. guess the next field, and repeat 3-4 until we find a working combo
# 5. get the appropriate values from my ticket now that we know how the field map
#
# Then hopefully it's down to a semi-reasonable number of tickets to consider...
# Use as many o(1) data structures as possible here. Don't want to have to perform
# more lookups than are absolutely necessary
def solve_2(filename):
    _, invalid_fields = solve_1(filename)
    ticket_data = format_input(read_from_file(filename))
    
    condition_map = defaultdict(list)
    # we'll just group all of the conditions by name to keep track of which fields are valid for 
    # which conditions
    for condition in ticket_data[Section.CONDITIONS]:
        condition_map[condition.name].append(condition)

    invalid_fields = set(invalid_fields)
    d_print(invalid_fields)
    valid_tickets = [
        ticket for ticket in ticket_data[Section.OTHER_TICKETS] 
        if not set(ticket).intersection(invalid_fields)
    ]

    constrained_fields = defaultdict(list)
    for condition_name, conditions in condition_map.items():
        for index in range(len(valid_tickets[0])):
            all_fields_pass = True
            for ticket in valid_tickets:
                if not is_valid_ticket_field(ticket[index], conditions):
                    all_fields_pass = False
                    break
            if all_fields_pass:
                constrained_fields[condition_name].append(index)
    
    condition_to_index_map = {}
    unique_conditions = len(condition_map.keys())
    while len(condition_to_index_map.keys()) < unique_conditions:
        for k, v in constrained_fields.items():
            if len(v) == 1:
                value = v[0]
                d_print("{}={}".format(k, value))
                condition_to_index_map[k] = value
                # remove that entry from every other possible field and then exit the loop
                for values_list in constrained_fields.values():
                    try:
                        values_list.remove(value)
                    except ValueError:
                        pass
                break
     
    my_ticket = ticket_data[Section.MY_TICKET][0]
    total = 1
    for k, v in condition_to_index_map.items():
        if k.startswith('departure'):
            d_print("{}={}".format(k, my_ticket[v]))
            total *= my_ticket[v]
    return total


 
