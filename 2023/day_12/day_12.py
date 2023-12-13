"""Day 12."""
from pathlib import Path
from tqdm import tqdm
from collections import Counter
from functools import cache


hashed_possibilities = {}
hashed_order = {}


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_12.txt", "r") as f:
        raw_data = f.read().strip().split("\n")
        raw_data = [i.split(" ") for i in raw_data]
        raw_data = [(i[0], [int(ii) for ii in i[1].split(",")]) for i in raw_data]

    return raw_data


def generateAllPossibleCombinations(question):
    # Data is a collection of regular symbols (#) and ? for unkowns
    # '#' -> ('#') -> {(1): 1}
    # '??' -> ('..', '#.', '.#', '##') -> {(0): 1, (1): 2, (2): 1}
    # '???' -> ('...', '#..', '.#.', '..#', '#.#', '##.', '.##', '###') -> {(0): 1, (1): 3, (1, 1): 1, (2): 2, (3):1}

    if question not in hashed_possibilities:
        possible = []
        if "?" not in question:
            possible.append(question)
        else:
            idx = 0
            while question[idx] != "?":
                idx += 1
            before = question[:idx]
            afters, _ = generateAllPossibleCombinations(question[idx + 1 :])
            if not afters:
                possible.append(before + "#")
                possible.append(before + ".")

            else:
                for after in afters:
                    possible.append(before + "#" + after)
                    possible.append(before + "." + after)

        order = [getOrderFromData(i) for i in possible]
        order = Counter(order)
        hashed_possibilities[question] = list(set(possible))
        hashed_order[question] = order
    return hashed_possibilities[question], hashed_order[question]


def getOrderFromData(data):
    return tuple([len(i) for i in data.split(".") if i])


def filterByOrder(data, order):
    order = tuple(order)
    return [i for i in data if getOrderFromData(i) == order]


def part_1():
    raw_data = get_data()
    return_val = 0

    for data, order in tqdm(raw_data, leave=False):
        return_val += iterative_approach(data, tuple(order))

    print(f"Result: {return_val}")


@cache
def iterative_approach(data, order, cur_count=0, last="."):
    data = data + "." if data[-1] != "." else data
    perms = 0
    cur_idx = 0

    while cur_idx < len(data) and order:
        if cur_count > order[0]:
            # We have overcounted on this group
            return 0

        cur_char = data[cur_idx]
        if cur_char == "#":
            if last == ".":
                # if last[-1] == ".":
                # We are entering a new group
                cur_count = 1
            else:
                cur_count += 1
        elif cur_char == ".":
            # if last[-1] == "#":
            if last == "#":
                if cur_count != order[0]:
                    # We have over/undercounted on the latest group
                    return 0
                order = order[1:]
                cur_count = 0
        elif cur_char == "?":
            # Here we have to try both options
            # First we try with a #
            perms += iterative_approach(
                data[cur_idx + 1 :],
                order,
                cur_count=(1 if last == "." else cur_count + 1),
                last="#",
            )
            # Then we try with a . - here we need to check that the previous
            # group is not undercounted
            if last == "#":
                # Make sure the count is correct
                if cur_count != order[0]:
                    return perms
                else:
                    perms += iterative_approach(
                        data[cur_idx + 1 :], order[1:], 0, last="."
                    )
            else:
                perms += iterative_approach(data[cur_idx + 1 :], order, 0, last=".")

            return perms
        cur_idx += 1
        last = cur_char
        # last = cur_char

    if not order:
        return 1 if "#" not in data[cur_idx:] else 0
    else:
        return 1 if len(order) == 1 and cur_count == order[0] else 0


def part_2():
    raw_data = get_data()
    result = 0

    for data, order in tqdm(raw_data, leave=False):
        data = "?".join([data for _ in range(5)])
        order = tuple(order * 5)
        result += iterative_approach(data, order)

    print(f"Result: {result}")


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
