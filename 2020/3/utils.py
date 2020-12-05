
def read_from_file(filename):
    with open(filename) as f_in:
        lines = [line.strip() for line in f_in.readlines()]
    return lines


def d_print(message):
    if d_print.debug:
        print(message)
d_print.debug = False
