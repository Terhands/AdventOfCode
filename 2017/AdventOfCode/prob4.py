import collections

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def parse_line(line):
  checksum = line[line.find('['):line.find(']')].replace('[', '').replace(']', '')
  sector = line[:line.find('[')].split('-')[-1]
  room_name = ' '.join(line[:line.find(sector)-1].split('-'))
  return room_name, int(sector), checksum

def is_room_real(room_name, checksum):
  char_counts = collections.defaultdict(int)

  for char in room_name:
    if char != ' ':
      char_counts[char] += 1

  for i in range(len(checksum) - 1):
    if char_counts[checksum[i]] < char_counts[checksum[i+1]]:
      return False
    if char_counts[checksum[i]] == char_counts[checksum[i+1]] and checksum[i] > checksum[i+1]:
      return False
    if char_counts[checksum[i]] != sorted(char_counts.itervalues(), reverse=True)[i]:
      return False  
  return True

def decrypt_room_name(room_name, sector):
  return ''.join([c if c == ' ' else alphabet[(alphabet.find(c) + sector) % len(alphabet)] for c in room_name])
  

def solve(lines):
  total = 0
  for line in lines:
    room_name, sector, checksum = parse_line(line)
    total += sector if is_room_real(room_name, checksum) else 0
    if is_room_real(room_name, checksum):
      print "%s: %s" % (decrypt_room_name(room_name, sector), sector)  
  print total
