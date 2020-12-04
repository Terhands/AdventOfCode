import collections


bot_config = {}
values_map = collections.defaultdict(list)
instructions = []

def parse(line):
  if line.startswith('bot'):
    configure_bot(line)
  elif line.startswith('value'):
    instructions.append(line)
  else:
    print "Error: %s" % line 

def configure_bot(bot_configuration):
  bot, low_dest, high_dest = bot_configuration.replace(' gives low to ', ',').replace(' and high to ', ',').split(',')
  bot_config[bot] = (low_dest, high_dest)

def move_chip(line):
  value, bot = line.replace('value ', '').replace(' goes to ', ',').split(',')
  values_map[bot].append(int(value))
  propagate(bot)

def propagate(bot):
  if len(values_map[bot]) == 2:
    high = max(values_map[bot])
    low = min(values_map[bot])
    if high == 61 and low == 17:
      print bot
#      return
    low_dest, high_dest = bot_config[bot]
    values_map[bot] = []
    values_map[low_dest].append(low)
    values_map[high_dest].append(high)
    propagate(high_dest)
    propagate(low_dest)

def solve(lines):
  for line in lines:
    parse(line)
  for i in instructions:
    move_chip(i)



