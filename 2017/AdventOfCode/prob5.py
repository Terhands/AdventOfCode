import md5


def solve(base_hash):
  code = ['-' for _ in range(8)]
  i = 0
  while '-' in code:
    curr_hash = ''
    while not curr_hash.startswith('00000'):
      curr_hash = md5.new(base_hash + str(i)).hexdigest()
      i += 1
    if curr_hash[5].isdigit():
      index = int(curr_hash[5])
      if index < 8 and code[index] == '-':
        code[index] = curr_hash[6]
        print code

  return code

