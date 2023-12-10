import functools

FIVE_OF_A_KIND = 6
FOUR_OF_A_KIND = 5
FULL_HOUSE = 4
THREE_OF_A_KIND = 3
TWO_PAIR = 2
ONE_PAIR = 1
HIGH_CARD = 0

def get_counts(hand):
    counts = {}
    jokers = 0
    for card in hand:
        if card == 1:
            jokers += 1
        else:
            counts[card] = counts.get(card, 0) + 1
    return list(counts.values()), jokers

def get_type(hand):
    counts, jokers = get_counts(hand)

    # five of a kind
    if jokers == 5 or max(counts) + jokers == 5:
        return FIVE_OF_A_KIND

    # four of a kind
    if max(counts) + jokers == 4:
        return FOUR_OF_A_KIND

    # full house
    if (3 in counts and 2 in counts) or (counts.count(2) == 2 and jokers > 0):
        return FULL_HOUSE

    # three of a kind
    if max(counts) + jokers == 3:
        return THREE_OF_A_KIND

    # two pair
    if counts.count(2) == 2 or (2 in counts and jokers > 0):
        return TWO_PAIR

    # one pair
    if 2 in counts or jokers > 0:
        return ONE_PAIR

    return HIGH_CARD

def compare_hands(hand1, hand2):
    hand1 = hand1[0] # remove bid
    hand2 = hand2[0]
    type1 = get_type(hand1)
    type2 = get_type(hand2)
    if type1 > type2:
        return 1
    elif type1 < type2:
        return -1

    if hand1 == hand2:
        return 0
    elif hand1 > hand2:
        return 1
    else:
        return -1

def sort_hands(hands):
    hands.sort(key=functools.cmp_to_key(compare_hands))

def to_card_num(card):
    nums = {
        'T': 10,
        'J': 1,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    if card in nums:
        return nums[card]
    return int(card)

def parse_hand(string):
    # returns ([card, card, ...], bid)
    hand, _, bid = string.partition(' ')
    hand = [to_card_num(card) for card in hand]
    bid = int(bid)
    return hand, bid

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        hands = []
        for line in file.readlines():
            hands.append(parse_hand(line))

        sort_hands(hands)
        answer = 0
        for rank, (hand, bid) in enumerate(hands, 1):
            answer += rank * bid
        print(answer)
