import re

def parse_card(card):
    """ Returns (winning numbers, your numbers) """
    # Remove "Card 123: " prefix
    _, _, card = card.partition(': ')

    # Split into winning numbers and your numbers
    winners, _, numbers = card.partition(" | ")

    # Split strings into lists
    winners = re.split(r'\s+', winners.strip())
    numbers = re.split(r'\s+', numbers.strip())

    # Convert to ints
    winners = [int(n) for n in winners]
    numbers = [int(n) for n in numbers]

    return winners, numbers

def get_matching_numbers(winners, numbers):
    """ Returns the set of your numbers that are winning numbers """
    return set(winners).intersection(set(numbers))

def get_points(card):
    winners, numbers = parse_card(card)
    matches = get_matching_numbers(winners, numbers)
    if len(matches) > 0:
        return 2 ** (len(matches) - 1)
    return 0

if __name__ == '__main__':
    answer = 0
    with open('input.txt', 'r') as file:
        for line in file.readlines():
            answer += get_points(line)
    print(answer)
