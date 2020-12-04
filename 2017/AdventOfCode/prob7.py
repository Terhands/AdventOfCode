

def is_valid_palindrome(sequence):
  is_proper_length = len(sequence) == 4
  is_palindrome = sequence[:2] == sequence[2:][::-1]
  print '%s : %s' % (sequence[:2], sequence[2:][::-1])  
  is_different_characters = not all([s == sequence[0] for s in sequence])
  print '%s, %s, %s' % (is_proper_length, is_palindrome, is_different_characters)
  return is_proper_length and is_palindrome and is_different_characters

def is_valid_palindrome_v2(s):
  is_proper_length = len(s) == 3
  return is_proper_length and s[0] == s[2] != s[1]

def solve_for_line_v2(line):
  is_in_brackets = False
  abas = []
  babs = []
  for i in range(len(line)):
    if line[i] == '[':
      is_in_brackets = True
      continue
    if line[i] == ']':
      is_in_brackets = False
      continue

    is_valid_sequence = is_valid_palindrome_v2(line[i:i+3])
    if is_valid_sequence and is_in_brackets:
      babs.append(line[i:i+3])
    elif is_valid_sequence:
      abas.append(line[i:i+3])
  is_valid = any([bab[1] + bab[0] + bab[1] in abas for bab in babs])
  print "%s: (%s, %s)" % (is_valid, babs, abas)
  return is_valid

def solve_for_line(line):
  is_in_brackets = False
  could_be_valid = False
  for i in range(len(line)):
    if line[i] == '[':
      is_in_brackets = True
      continue
    if line[i] == ']':
      is_in_brackets = False
      continue

    is_valid_sequence = is_valid_palindrome(line[i:i+4])
    # print "%s - %s" % (line[i:i+4], is_valid_sequence)
    if is_valid_sequence and is_in_brackets:
      print "Is not valid: " + line
      return False
    if is_valid_sequence:
      could_be_valid = True
  print ("Is valid: " if could_be_valid else "Is not valid: ") + line
  return could_be_valid
    

def solve(lines):
  print sum([1 for l in lines if solve_for_line_v2(l)])



