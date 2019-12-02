
def read_input(filename):
    with open(filename) as f:
        return f.readlines()[0].replace('\n', '')

def part1(input):
    had_reaction = True
    polymer = input
    while(had_reaction):
        new_polymer = ''
        had_reaction = False
        i = 0
        while i < (len(polymer) - 1):
            if polymer[i] != polymer[i+1] and polymer[i].lower() == polymer[i+1].lower():
                # print polymer[i], polymer[i+1]
                i += 2  # skip to the next
                had_reaction = True
            else:
                # print polymer[i], polymer[i+1]
                new_polymer += polymer[i]
                i += 1
                if i == (len(polymer) - 1):
                    # don't skip the last element
                    new_polymer += polymer[i]
        # print "-----"
        polymer = new_polymer
    return polymer


def part2(input):
    shortest_reulting_polymer = input
    for letter in 'qwertyuioplkjhgfdsazxcvbnm':
        cleaned_polymer = input.replace(letter, '').replace(letter.upper(), '')
        result_polymer = part1(cleaned_polymer)
        # print cleaned_polymer, result_polymer
        if len(result_polymer) < len(shortest_reulting_polymer):
            shortest_reulting_polymer = result_polymer
            
    return shortest_reulting_polymer
