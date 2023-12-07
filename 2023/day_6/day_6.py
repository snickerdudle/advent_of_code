"""Day 6."""
from pathlib import Path
import math


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_6.txt", "r") as f:
        raw_data = f.read().strip().split("\n")
        t = [int(i.strip()) for i in raw_data[0].split(" ")[1:] if i]
        dist = [int(i.strip()) for i in raw_data[1].split(" ")[1:] if i]

    return t, dist, {t: d for t, d in zip(t, dist)}


def part_1():
    _, _, raw_data = get_data()
    result = 1
    for t, d in raw_data.items():
        solution = []
        min_num = (-t + (t**2 - 4 * d) ** 0.5) / -2
        if min_num.is_integer():
            solution.append(int(min_num) + 1)
        else:
            solution.append(math.ceil(min_num))

        max_num = (-t - (t**2 - 4 * d) ** 0.5) / -2
        if max_num.is_integer():
            solution.append(int(max_num) - 1)
        else:
            solution.append(math.floor(max_num))
        print(f"t: {t}, d: {d}, solution: {solution}")
        result *= solution[1] - solution[0] + 1

    print(result)
    return result


def part_2():
    t, d, _ = get_data()
    result = 1
    t = int("".join([str(i) for i in t]))
    d = int("".join([str(i) for i in d]))

    solution = []
    min_num = (-t + (t**2 - 4 * d) ** 0.5) / -2
    if min_num.is_integer():
        solution.append(int(min_num) + 1)
    else:
        solution.append(math.ceil(min_num))

    max_num = (-t - (t**2 - 4 * d) ** 0.5) / -2
    if max_num.is_integer():
        solution.append(int(max_num) - 1)
    else:
        solution.append(math.floor(max_num))
    print(f"t: {t}, d: {d}, solution: {solution}")
    result *= solution[1] - solution[0] + 1

    print(result)
    return result


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
