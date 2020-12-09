from utils import read_from_file, d_print


class Program():

    def __init__(self, instructions):
        self.accumulator = 0
        self.instruction_pointer = 0
        self.instructions = instructions
        self.executed_instructions = set()

    def jmp(self, value):
        self.instruction_pointer += value

    def nop(self, _):
        self.instruction_pointer += 1

    def acc(self, value):
        self.accumulator += value
        self.instruction_pointer += 1

    def execute(self):
        self.executed_instructions.add(self.instruction_pointer)
        command_name, value = self.instructions[self.instruction_pointer]
        getattr(self, command_name)(value)

    def is_in_loop(self):
        return self.instruction_pointer in self.executed_instructions

    def is_completed(self):
        return self.instruction_pointer >= len(self.instructions)


def format_input(lines):
    instructions = []
    for line in lines:
        if not line:
            continue  # skip blank lines for this one
        command, value = line.split(' ')
        instructions.append((command, int(value)))
    return instructions


def solve_1(filename):
    program = Program(format_input(read_from_file(filename)))
    while not program.is_in_loop():
        program.execute()
    return program.accumulator


def switch_command(command):
    return 'jmp' if command == 'nop' else 'nop'


def solve_2(filename):
    instructions = format_input(read_from_file(filename))
    for index in range(len(instructions)):
        command, value = instructions[index]
        if command in ['nop', 'jmp']:
            instructions[index] = (switch_command(command), value)
        else:
            continue
        
        program = Program(instructions)
        while not program.is_in_loop():
            program.execute()
            if program.is_completed():
                return program.accumulator
        
        # switch the command back before trying the next command
        instructions[index] = (command, value) 

