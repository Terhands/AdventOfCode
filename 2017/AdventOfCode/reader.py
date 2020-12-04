
def get_lines_from_file(filename):
  return [line.replace('\n', '') for line in open(filename, 'r').readlines()]
