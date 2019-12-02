class Recipes(object):

    def __init__(self):
        self.size = 0
        self.first_recipe = None

    def __repr__(self):
        return "%s" % self.scores

    def scores(self):
        curr = self.first_recipe
        scores = []
        for _ in range(self.size):
             scores.append(curr.score)
             curr = curr.next
        return scores

    def add_to_end(self, score):
        if self.first_recipe is None:
            self.first_recipe = Recipe(score, None, None)
        else:
            last_recipe = self.first_recipe.prev
            new_recipe = Recipe(score, last_recipe, self.first_recipe)
            last_recipe.next = new_recipe
            self.first_recipe.prev = new_recipe
        self.size += 1

    def print_last_x(self, x):
        print_from = self.first_recipe
        to_print = []
        for _ in range(x):
            print_from = print_from.prev
            to_print.append(print_from.score)
        to_print.reverse()
        print to_print

    def last_x(self, x):
        print_from = self.first_recipe
        sequence = ""
        for _ in range(x):
            print_from = print_from.prev
            sequence = str(print_from.score) + sequence
        return sequence


class Recipe(object):

    def __init__(self, score, prev, next):
        self.score = score
        self.prev = prev or self
        self.next = next or self

    def __repr__(self):
        return "%s" % self.score

    def move_ahead(self, distance=1):
        to = self
        for _ in range(distance):
            to = to.next
        return to


def split_digits(digits):
    scores = []
    if digits == 0:
        return [0]
    while digits > 0:
        scores.append(digits % 10)
        digits //= 10
    scores.reverse()
    return scores

def add_new_recipes(scores, recipes):
    scores = split_digits(scores)
    for score in scores:
        recipes.add_to_end(score)

def part1(num_recipes):
    recipes = Recipes()
    add_new_recipes(37, recipes)

    elf1_recipe = recipes.first_recipe
    elf2_recipe = elf1_recipe.next
    while recipes.size < (num_recipes + 10):
        s1, s2 = elf1_recipe.score, elf2_recipe.score
        new_scores = s1 + s2
        add_new_recipes(new_scores, recipes)
        elf1_recipe = elf1_recipe.move_ahead(s1 + 1)
        elf2_recipe = elf2_recipe.move_ahead(s2 + 1)
    return ''.join(map(str, recipes.scores()[num_recipes:num_recipes+10]))

# wow did part 2 ever not need these data structures... thought I was doing myself a solid building those XD
def part2(sequence):
    recipes = Recipes()
    add_new_recipes(37, recipes)
    check_size = len(sequence) + 2

    elf1_recipe = recipes.first_recipe
    elf2_recipe = elf1_recipe.next
    finished = False
    while not finished:
        s1, s2 = elf1_recipe.score, elf2_recipe.score
        new_scores = s1 + s2
        add_new_recipes(new_scores, recipes)
        elf1_recipe = elf1_recipe.move_ahead(s1 + 1)
        elf2_recipe = elf2_recipe.move_ahead(s2 + 1)

        if sequence in recipes.last_x(check_size):
            finished = True
    print recipes.size
    recipes.print_last_x(check_size)


