"""Day 4."""
from pathlib import Path


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_4.txt", "r") as f:
        raw_data = f.read().strip().split("\n")
        clean_data = []
        for line in raw_data:
            winning, mine = line.split("|")
            winning = winning.split(":")[1].strip().split(" ")
            winning = [int(i) for i in winning if i]
            mine = [int(i) for i in mine.split(" ") if i]
            clean_data.append((winning, mine))
    return clean_data


def part_1():
    cleaned_data = get_data()
    result = 0

    for winning, mine in cleaned_data:
        intersection = set(winning) & set(mine)
        if intersection:
            result += 2 ** (len(intersection) - 1)
    print(result)


def part_2():
    cleaned_data = get_data()
    num_cards = {i: 1 for i in range(1, len(cleaned_data) + 1)}

    for card_idx, (winning, mine) in enumerate(cleaned_data):
        card_num = card_idx + 1
        intersection = set(winning) & set(mine)
        result = len(intersection)

        # Make the copies
        for next_card_num in range(card_num + 1, card_num + 1 + result):
            num_cards[next_card_num] += num_cards[card_num]

    print(sum(list(num_cards.values())))


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
