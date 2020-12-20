from utils import read_from_file, d_print
import re


# take the rules strings and build up a regex?
def format_input(lines):
    rules_lines = []
    message_lines = []
    is_rules_section = True
    for line in lines:
        if not line:
            is_rules_section = False
            continue

        if is_rules_section:
            rules_lines.append(line)
        else:
            message_lines.append(line)
    return rules_lines, message_lines


def get_rules_map(rule_lines):
    rules_dict = {}
    for rule_line in rule_lines:
        rule_key, rules = rule_line.split(': ')
        if '"' in rules:
            rules_dict[rule_key] = rules.replace('"', '')
        else:
            rules_dict[rule_key] = []
            d_print(rules)
            ored_rules = rules.split(' | ')
            for ored_rule in ored_rules:
                rules_dict[rule_key].append(ored_rule.split(' '))
    return rules_dict


def rules_regex_for_key(key, rules_dict, cache, is_part_2=False):
    # convert each key into it's piece of the regex - store that in a cache since it looks like there
    # is a lot of repetition in the keys, so performance could be problematic in building this.
    # for the sample this is the regex string that should be produced: r'^a((aa|bb)(ab|ba)|(ab|ba)(aa|bb))b$'
    rules = rules_dict[key]
    d_print("{}: {}".format(key, rules))
    # case 0: the key has already been solved and is in the cache - don't bother recomputing it
    if key in cache:
        return cache[key]

    # case 1: the base case where we have one of our characters
    if isinstance(rules, str):
        str_pattern = '({})'.format(rules)
        cache[key] = str_pattern
        return str_pattern

    # This is a little gross, I'm sure there's a sensible way to build the 11 case wildcard, but this is easier
    if is_part_2 and key == '8':
        rule_str = rules_regex_for_key('42', rules_dict, cache, is_part_2)
        str_pattern = '({})+'.format(rule_str)
        cache[key] = str_pattern
        return str_pattern

    # The original regex only matches 24 characters. The longest string in the input is 96 characters.
    # So the repeating pattern here can be something like:  ab | aabb | aaa(ab)*bbb so since regexes
    # don't really count very well, we'll have to add in the possibilities manually, which totally sucks.
    # so our regex should follow this pattern (but be more ginormous) ab | a(ab)+b | aa(ab)+bb | ... up
    # to 36 a's and b's on either side to be safe. Bleh. I'm going to want to do this in a loop :P
    if is_part_2 and key == '11':
        rule_42 = rules_regex_for_key('42', rules_dict, cache, is_part_2)
        rule_31 = rules_regex_for_key('31', rules_dict, cache, is_part_2)
        
        rules_strs = ['({}{})'.format(rule_42, rule_31)]
        repeating = '({}{})+'.format(rule_42, rule_31)
        for i in range(36):
            str_42 = '{}'.format(rule_42)*(i+1)
            str_31 = '{}'.format(rule_31)*(i+1)
            rule_str = '({}{}{})'.format(str_42, repeating, str_31)
            rules_strs.append(rule_str)
        str_pattern = '({})'.format('|'.join(rules_strs))
        return str_pattern
    # end of the part 2 grossness.

    if isinstance(rules, list):
        rules_strs = []
        for subrules in rules:
            rule_str = ''
            for rule in subrules:
                rule_str += rules_regex_for_key(rule, rules_dict, cache, is_part_2)
            rules_strs.append(rule_str)
        str_pattern = '({})'.format('|'.join(rules_strs))
        cache[key] = str_pattern
        return str_pattern


def solve_1(filename):
    rules_lines, message_lines = format_input(read_from_file(filename))
    rules_dict = get_rules_map(rules_lines)
    regex_str = rules_regex_for_key('0', rules_dict, {})
    # because we wrap every expression in parens we get an extra set. But we want to set a start/end anyway, 
    # so we can just overwrite them
    regex_str = r'^{}$'.format(regex_str[1:-1])
    pattern = re.compile(regex_str)
    d_print(regex_str)
    matches = 0
    for line in message_lines:
        if pattern.match(line):
            d_print('Match Found: {}'.format(line))
            matches += 1
    return matches


def solve_2(filename):
    rules_lines, message_lines = format_input(read_from_file(filename))
    rules_dict = get_rules_map(rules_lines)
    regex_str = rules_regex_for_key('0', rules_dict, {}, is_part_2=True)
    # because we wrap every expression in parens we get an extra set. But we want to set a start/end anyway, 
    # so we can just overwrite them
    regex_str = r'^{}$'.format(regex_str[1:-1])
    pattern = re.compile(regex_str)
    d_print(regex_str)
    matches = 0
    for line in message_lines:
        if pattern.match(line):
            d_print('Match Found: {}'.format(line))
            matches += 1
    return matches


