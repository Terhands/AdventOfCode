import aoc_utils

# A = Rock (1) B = Paper (2) C = Scissors (3)
# X = Rock (1) Y = Paper (2) Z = Scissors (3)
# tie = 3 + play value, win = 6 + play value, loss = 0 + play value
TIE_SCORE = 3
WIN_SCORE = 6

conversions = {
    'A': 'R', 
    'X': 'R', 
    'B': 'P', 
    'Y': 'P',
    'C': 'S',
    'Z': 'S',
}

winning_combos = {
    'R': 'P',
    'P': 'S',
    'S': 'R',
}

play_to_score = {
    'R': 1,
    'P': 2,
    'S': 3,
}


def parse_round_1(round_str):
    opponent_play, my_play = round_str.strip().upper().split(' ')
    return conversions[opponent_play], conversions[my_play]


def compute_score(opponent_play, my_play):
    score = play_to_score[my_play]
    if opponent_play == my_play:
        score += TIE_SCORE
    elif winning_combos[opponent_play] == my_play:
        score += WIN_SCORE
    return score



def calculate_score_per_round(filename, parser, score_calculator):
    rounds = aoc_utils.read_from_file(filename, parser)
    return [score_calculator(opponent_play, my_play) for opponent_play, my_play in rounds]


def part_1():
    scores_per_round = calculate_score_per_round('2/input.txt', parse_round_1, compute_score)
    print(f"Part 1: Total score is {sum(scores_per_round)}")


# New meanings:
# X = Lose Y = tie Z = win
def parse_round_2(round_str):
    opponent_play, my_play = round_str.strip().upper().split(' ')
    return conversions[opponent_play], my_play


def compute_score_2(opponent_play, decision):
    options = {'R', 'P', 'S'}
    if decision == 'X':  # lose
        play = (options - {winning_combos[opponent_play], opponent_play}).pop()
        return play_to_score[play]
    if decision == 'Y':  # tie
        return TIE_SCORE + play_to_score[opponent_play]
    if decision == 'Z':  # win
        return WIN_SCORE + play_to_score[winning_combos[opponent_play]]


def part_2():
    scores_per_round = calculate_score_per_round('2/input.txt', parse_round_2, compute_score_2)
    print(f"Part 2: Total score is {sum(scores_per_round)}")


part_1()
part_2()