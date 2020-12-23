from utils import read_from_file, d_print
from collections import defaultdict


# map the allergen strings to their potential matches (removing any that are impossible)
def format_input(lines):
    allergen_mystery_word_lists_map = defaultdict(list)
    all_ingredients = []
    for line in lines:
        if not line:
            continue
        mystery_words_str, allergens_str = line.split(' (contains ')
        allergens = allergens_str.replace(')', '').replace(',', '').split(' ')
        mystery_words = mystery_words_str.split(' ')
        all_ingredients += mystery_words
        for allergen in allergens:
            allergen_mystery_word_lists_map[allergen].append(set(mystery_words))
    return allergen_mystery_word_lists_map, all_ingredients


def solve_1(filename):
    allergen_mystery_word_lists_map, all_ingredients = format_input(read_from_file(filename))
    allergen_to_all_potential_ingredients = {}
    for allergen, ingredient_lists in allergen_mystery_word_lists_map.items():
        potential_ingredients = ingredient_lists[0]
        for ingredient_list in ingredient_lists:
            potential_ingredients &= ingredient_list
        allergen_to_all_potential_ingredients[allergen] = potential_ingredients
        d_print('{}: {}'.format(allergen, potential_ingredients))

    confirmed_allergens = set()
    while len(allergen_to_all_potential_ingredients.keys()) > 0:
        keys_to_delete = []
        for k, v in allergen_to_all_potential_ingredients.items():
            v -= confirmed_allergens
            if len(v) == 1:
                keys_to_delete.append(k)
                confirmed_allergens.add(list(v)[0])
        for key in keys_to_delete:
            del allergen_to_all_potential_ingredients[key]

    d_print(confirmed_allergens)
    total = 0
    for ingredient in all_ingredients:
        if ingredient not in confirmed_allergens:
            total += 1
    return total


def solve_2(filename):
    allergen_mystery_word_lists_map, all_ingredients = format_input(read_from_file(filename))
    allergen_to_all_potential_ingredients = {}
    for allergen, ingredient_lists in allergen_mystery_word_lists_map.items():
        potential_ingredients = ingredient_lists[0]
        for ingredient_list in ingredient_lists:
            potential_ingredients &= ingredient_list
        allergen_to_all_potential_ingredients[allergen] = potential_ingredients
        d_print('{}: {}'.format(allergen, potential_ingredients))

    confirmed_allergens = set()
    allergen_to_ingredient_tuples = []
    while len(allergen_to_all_potential_ingredients.values()) > 0:
        keys_to_delete = []
        for k, v in allergen_to_all_potential_ingredients.items():
            v -= confirmed_allergens
            if len(v) == 1:
                ingredient = list(v)[0]
                keys_to_delete.append(k)
                confirmed_allergens.add(ingredient)
                allergen_to_ingredient_tuples.append((k, ingredient))
        for key in keys_to_delete:
            del allergen_to_all_potential_ingredients[key]

    sorted_allergen_to_ingredient = sorted(allergen_to_ingredient_tuples, key=lambda x: x[0])
    d_print(sorted_allergen_to_ingredient)
    return ','.join(ingredient for _, ingredient in sorted_allergen_to_ingredient)

