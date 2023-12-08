"""Day 8."""
from pathlib import Path
import math


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_8.txt", "r") as f:
        raw_data = f.read().strip().split("\n")

        directions = raw_data[0]

        operations = raw_data[2:]
        operations = [op.split(" = ") for op in operations]
        operations = {op[0]: (op[1][1:4], op[1][6:9]) for op in operations}

    return directions, operations


def part_1():
    directions, operations = get_data()

    dir_idx = 0
    cur_pos = "AAA"
    steps = 0
    while cur_pos != "ZZZ":
        steps += 1
        cur_dir = directions[dir_idx]
        cur_pos = operations[cur_pos][0 if cur_dir == "L" else 1]
        dir_idx = (dir_idx + 1) % len(directions)

    print(steps)


def findZs(cur_pos):
    directions, operations = get_data()

    dir_idx = 0
    steps = 0
    new_pos = operations[cur_pos][0 if directions[dir_idx] == "L" else 1]
    dir_idx = 1
    zs = []

    while new_pos[-1] != "Z":
        steps += 1
        cur_dir = directions[dir_idx]
        new_pos = operations[new_pos][0 if cur_dir == "L" else 1]
        dir_idx = (dir_idx + 1) % len(directions)

    return new_pos, steps + 1


def part_2():
    directions, operations = get_data()

    dir_idx = 0
    cur_pos = [i for i in operations if i[-1] == "A"]

    zs = [findZs(start) for start in cur_pos]
    print([z[1] for z in zs])
    print(math.lcm(*[z[1] for z in zs]))


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
