"""Day 7."""
from pathlib import Path
from collections import Counter
from functools import cmp_to_key

card_values = {
    # "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

new_card_values = {
    "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    # "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

hand_types = {
    "high": 1,
    "pair": 2,
    "two pair": 3,
    "three": 4,
    "full house": 5,
    "four": 6,
    "five": 7,
}


def compare(first, second):
    first_set = Counter(first)
    second_set = Counter(second)

    first_type = getType(first_set)
    second_type = getType(second_set)

    if first_type > second_type:
        return 1
    elif first_type < second_type:
        return -1
    else:
        cur_idx = 0
        while True:
            if card_values[first[cur_idx]] > card_values[second[cur_idx]]:
                return 1
            elif card_values[first[cur_idx]] < card_values[second[cur_idx]]:
                return -1
            else:
                cur_idx += 1


def getType(hand):
    if not isinstance(hand, Counter):
        hand = Counter(hand)

    if len(hand) == 5:
        # This is a high card
        return hand_types["high"]
    elif len(hand) == 4:
        # This is a pair
        return hand_types["pair"]
    elif len(hand) == 3:
        # Either a two pair, or a three
        if 3 in hand.values():
            return hand_types["three"]
        else:
            return hand_types["two pair"]
    elif len(hand) == 2:
        # Either a full house, or a four
        if 2 in hand.values():
            return hand_types["full house"]
        else:
            return hand_types["four"]
    elif len(hand) == 1:
        # This is a five
        return hand_types["five"]


def customSort(input_list, comparefn):
    return sorted(input_list, key=cmp_to_key(comparefn))


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_7.txt", "r") as f:
        raw_data = f.read().strip().split("\n")
        raw_data = [i.split(" ") for i in raw_data]

    return raw_data


def part_1():
    raw_data = get_data()

    hand_to_bid = {h: b for h, b in raw_data}

    sorted_data = customSort(list(hand_to_bid.keys()), compare)

    result = 0
    for i, hand in enumerate(sorted_data):
        result += (i + 1) * int(hand_to_bid[hand])

    print(result)


def makeHighestHand(hand):
    if "J" not in hand:
        return hand

    # Create a depth-first search to fill the wildcard J with every possible
    # card value
    possible_hands = []

    def dfs(cur_hand, cur_idx=0):
        if cur_idx == 5:
            possible_hands.append(cur_hand)
            return

        if cur_hand[cur_idx] == "J":
            for card in card_values.keys():
                if card == "J":
                    continue
                dfs(cur_hand[:cur_idx] + card + cur_hand[cur_idx + 1 :], cur_idx + 1)
        else:
            dfs(cur_hand, cur_idx + 1)

    dfs(hand)

    possible_hands = customSort(possible_hands, compare)
    return possible_hands[-1]


def compareNew(first_tuple, second_tuple):
    first, first_orig = first_tuple
    second, second_orig = second_tuple

    first_set = Counter(first)
    second_set = Counter(second)

    first_type = getType(first_set)
    second_type = getType(second_set)

    if first_type > second_type:
        return 1
    elif first_type < second_type:
        return -1
    else:
        cur_idx = 0
        while True:
            if (
                new_card_values[first_orig[cur_idx]]
                > new_card_values[second_orig[cur_idx]]
            ):
                return 1
            elif (
                new_card_values[first_orig[cur_idx]]
                < new_card_values[second_orig[cur_idx]]
            ):
                return -1
            else:
                cur_idx += 1


def part_2():
    raw_data = get_data()

    new_data = {}

    for hand, bid in raw_data:
        new_hand = makeHighestHand(hand)
        new_data[
            (
                new_hand,
                hand,
            )
        ] = int(bid)

    sorted_data = customSort(list(new_data.keys()), compareNew)
    result = 0
    for i, hand in enumerate(sorted_data):
        result += (i + 1) * new_data[hand]

    print(result)


if __name__ == "__main__":
    print("Part 1:")
    # part_1()

    print("\nPart 2:")
    part_2()
