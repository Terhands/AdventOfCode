from utils import read_from_file, d_print


class Password():
    def __init__(self, min_required, max_required, character, password):
        self.min_required = min_required
        self.max_required = max_required
        self.character = character
        self.password = password

    def is_valid(self):
        total = self.password.count(self.character)
        return self.min_required <= total <= self.max_required

    def is_valid_2(self):
        pos_1, pos_2 = self.password[self.min_required - 1], self.password[self.max_required - 1]
        result = self.character in [pos_1, pos_2] and pos_1 != pos_2
        d_print("Password '{}' is {}.".format(self.password, "valid" if result else "invalid"))
        return result

def format_input(lines):
    passwords = []
    for line in lines:
        if not line:
            continue  # skip blank lines
        required_range, character, password = line.split(' ')
        min_required, max_required = required_range.split('-')
        character = character[:-1]  # strip of the colon. They might be tricky bastards and use the colon character as the requirement...
        passwords.append(Password(int(min_required), int(max_required), character, password))
    return passwords


def solve_1(filename):
    passwords = format_input(read_from_file(filename))
    return len([p for p in passwords if p.is_valid()])


def solve_2(filename):
    passwords = format_input(read_from_file(filename))
    return len([p for p in passwords if p.is_valid_2()])

