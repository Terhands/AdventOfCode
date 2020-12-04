import collections


def solve(lines):
  bags = [collections.defaultdict(int) for i in range(8)]
  for line in lines:
    for i in range(len(line)):
      bags[i][line[i]] += 1

  decoded = ''
  for bag in bags:
    decoded += decode(bag)
  #print bags
  return decoded

def decode(chars):
  char, max_val = '', 100000
  for k, v in chars.iteritems():
    if v < max_val:
      char = k
      max_val = v
  return char

