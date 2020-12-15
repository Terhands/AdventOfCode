from utils import read_from_file, d_print
from collections import OrderedDict


def format_input(lines):
    mask_to_directives_map = OrderedDict()
    current_mask = None
    for line in lines:
        if not line:
            continue
        elif "mask" in line:
            current_mask = line.split(' = ')[-1]
            mask_to_directives_map[current_mask] = []
        else:
            address, value = line.split(' = ')
            address = address[4:-1]
            mask_to_directives_map[current_mask].append((int(address), int(value)))
    return mask_to_directives_map


def apply_mask(mask, value):
    masked_value = ''
    for i in range(len(mask)):
        if mask[-(i+1)] != 'X':
            masked_value = '{}{}'.format(int(mask[-(i+1)]), masked_value)
        else:
            masked_value = '{}{}'.format(value >> i & 1, masked_value) 
    d_print('{} -> {}'.format(masked_value, int(masked_value, 2)))
    return int(masked_value, 2)


def solve_1(filename):
    memory = {}
    mask_to_directives = format_input(read_from_file(filename))
    for mask, directives in mask_to_directives.items():
        d_print("{}: {}".format(mask, directives))
        for address, value in directives:
            memory[address] = apply_mask(mask, value)
    return sum(memory.values())


def apply_mask_to_address(mask, address):
    masked_address = ''
    for i in range(len(mask)):
        if mask[-(i+1)] != 'X':
            masked = int(mask[-(i+1)]) | (address >> i) & 1
            masked_address = '{}{}'.format(masked, masked_address)
        else:
            masked_address = '{}{}'.format(mask[-(i+1)], masked_address) 
    d_print('{} -> {}'.format(address, masked_address))
    return masked_address


def add_digit_to_address(address, digit):
    return '{}{}'.format(address, digit)


def expand_masked_address(masked_address):
    addresses = ['']
    for digit in masked_address:
        if digit == 'X':
            expanded_addresses = []
            for address in addresses:
                expanded_addresses.append(add_digit_to_address(address, 0))
                expanded_addresses.append(add_digit_to_address(address, 1))
            addresses = expanded_addresses
        else: 
            addresses = [add_digit_to_address(address, digit) for address in addresses]
    return addresses


def solve_2(filename):
    memory = {}
    mask_to_directives = format_input(read_from_file(filename))
    for mask, directives in mask_to_directives.items():
        d_print("{}: {}".format(mask, directives))
        for address, value in directives:
            masked_address = apply_mask_to_address(mask, address)
            for expanded_address in expand_masked_address(masked_address):
                memory[expanded_address] = value
    return sum(memory.values())






