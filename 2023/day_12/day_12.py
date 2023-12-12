"""Day 12."""
from pathlib import Path
from tqdm import tqdm
from collections import Counter


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
        cur_pos, cur_order = generateAllPossibleCombinations(data)
        f = filterByOrder(cur_pos, order)
        return_val += len(f)

    print(f"Result: {return_val}")


def part_2():
    pass


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
