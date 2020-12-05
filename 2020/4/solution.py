from utils import read_from_file, d_print


class Passport():

    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    optional_fields = ['cid']

    def __init__(self, passport_info):
        d_print(passport_info)
        fields = passport_info.split(' ')
        for field in fields:
            k, v = field.split(':')
            setattr(self, k, v)

    def is_valid(self):
        for field in self.required_fields:
            if not hasattr(self, field):
                return False
        return True

    def is_valid_2(self):
        for field in self.required_fields:
            if not hasattr(self, field):
                return False
            if not getattr(self, '{}_is_valid'.format(field))():
                return False
        return True

    def byr_is_valid(self):
        return 1920 <= int(self.byr) <= 2002

    def iyr_is_valid(self):
        return 2010 <= int(self.iyr) <= 2020

    def eyr_is_valid(self):
        return 2020 <= int(self.eyr) <= 2030

    def hgt_is_valid(self):
        height = int(self.hgt[:-2])
        units = self.hgt[-2:]
        if units == 'cm':
            return 150 <= height <= 193
        else:
            return 59 <= height <= 76

    def hcl_is_valid(self):
        colour_code = self.hcl[1:]
        for c in colour_code:
            if c not in '0123456789abcdef':
                return False
        return self.hcl[0] == '#'

    def ecl_is_valid(self):
        return self.ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

    def pid_is_valid(self):
        try:
            int(self.pid)
            return len(self.pid) == 9
        except ValueError:
            pass
        return False


def format_input(lines):
    passports = []
    current_passport_data = ''
    for line in lines:
        if line:
            current_passport_data += ' ' + line
        else:
            passports.append(Passport(current_passport_data.strip()))
            current_passport_data = ''  # clear this out for the next round
    return passports


def solve_1(filename):
    passports = format_input(read_from_file(filename))
    valid_passports = [passport for passport in passports if passport.is_valid()]
    return len(valid_passports)


def solve_2(filename):
    passports = format_input(read_from_file(filename))
    valid_passports = [passport for passport in passports if passport.is_valid_2()]
    return len(valid_passports)

