

def parse_line(line):
  i, count = 0, 0
  while i < len(line):
    if line[i] == '(':
      decompressed_size, new_i = get_mult_info(line, i)
      #print "%s decompressed: %s" % (line[i:new_i+1], decompressed_size) 
      if new_i > 0:
        count += decompressed_size
        i = new_i
      #print line[i]
    else:
      count += 1
     # print "Counting: %s" % line[i]
    i += 1
    #print "Count: %d" % count 
  return count
        
def get_mult_info(line, index):
  assert line[index] == '('
  try:
    a, b = line[index+1:].split(')')[0].split('x')
    offset = len(line[index:].split(')')[0]) 
    print "Recursing on: %s" % line[index+offset+1:index+offset+int(a) + 1]
    recursive_count = parse_line(line[index+offset+1:index+offset+int(a) + 1])
    print "Recursive Count: %s" % recursive_count

    #total_count = int(a) * int(b)
    #if recursive_count > int(a):
    total_count = int(b) * recursive_count
    print "%s x %s = %s" % (int(b), recursive_count, total_count)
    
    #print line[index + offset:index+offset + int(a)]* (int(a)*int(b))
    return total_count, index + offset + int(a) 
  except:
    return 0, 0




