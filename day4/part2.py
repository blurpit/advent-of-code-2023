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

if __name__ == '__main__':
    copies = []
    with open('input.txt', 'r') as file:
        for i, card in enumerate(file.readlines()):
            # Get matching numbers
            winners, numbers = parse_card(card)
            matches = get_matching_numbers(winners, numbers)

            # Add needed slots into the copies array
            while len(copies) <= i + len(matches):
                copies.append(0)

            # Add original
            copies[i] += 1

            # Add copies
            for j in range(len(matches)):
                copies[i + j + 1] += copies[i]

    print(sum(copies))
