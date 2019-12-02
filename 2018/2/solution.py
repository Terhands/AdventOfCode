import collections


def read_input(filename):
  with open(filename) as f:
    return [x.replace('\n', '') for x in f.readlines() if x.strip() != ""]


def char_count(line):
  counts = collections.defaultdict(int)
  for char in line:
    counts[char] += 1
  return counts


def part1(filename):
  box_ids = read_input(filename)
  exact_counts = {2: 0, 3: 0}
  for box_id in box_ids:
    char_counts = char_count(box_id)
    if 2 in char_counts.values():
      exact_counts[2] += 1
    if 3 in char_counts.values():
      exact_counts[3] += 1
  print exact_counts
  return exact_counts[2] * exact_counts[3]


def part2(filename):
  box_ids = read_input(filename)
  sorted_box_ids = sorted(box_ids)
  for i in range(len(sorted_box_ids) - 1):
    num_different = 0
    matching = []
    for x in range(len(sorted_box_ids[i])):
      if sorted_box_ids[i][x] == sorted_box_ids[i+1][x]:
        matching.append(sorted_box_ids[i][x])
      else:
        num_different += 1
        if num_different > 1:
          continue
    if num_different == 1:
      return matching



