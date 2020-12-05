from utils import *


def get_formatted_data(lines):
    return [int(line) for line in lines if line]


def part_1(expense_list):
    for expense in expense_list:
        for other_expense in expense_list:
            d_print('{} + {}'.format(expense, other_expense))
            if expense + other_expense == 2020:
                return expense * other_expense
    print("Oh no!")


def part_2(expense_list):
    for expense_1 in expense_list:
        for expense_2 in expense_list:
            for expense_3 in expense_list:
               _sum = expense_1 + expense_2 + expense_3
               d_print('{} + {} + {} = {}'.format(expense_1, expense_2, expense_3, _sum))
               if _sum == 2020:
                   return expense_1 * expense_2 * expense_3
    print("Oh no!")


def solve_1(filename):
  expense_list = get_formatted_data(read_from_file(filename))
  return part_1(expense_list)


def solve_2(filename):
  expense_list = get_formatted_data(read_from_file(filename))
  return part_2(expense_list)
