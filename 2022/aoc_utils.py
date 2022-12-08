
def read_from_file(filename, line_transform_fn=None):
    line_transform_fn = line_transform_fn or (lambda x: x)
    with open(filename) as f_in:
        contents = []
        for line in f_in.readlines():
            contents.append(line_transform_fn(line))
    return contents


def get_filename(day, is_sample=False):
    return f'inputs/day{day}_{"sample" if is_sample else "input"}.txt'
