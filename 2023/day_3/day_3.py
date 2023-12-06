"""Day 3."""
from pathlib import Path
from collections import defaultdict


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_3.txt", "r") as f:
        data = f.read().strip().split("\n")

    return data


def part_1():
    data = get_data()
    result = 0

    for row_idx, line in enumerate(data):
        cur_on_num = None
        idx_map = defaultdict(int)
        # First, assemble a map of all the numbers. This is keyed at the index
        # of the number, and the value is the length of the number.
        for idx, char in enumerate(line):
            if char.isnumeric():
                if cur_on_num is not None:
                    idx_map[cur_on_num] += 1
                else:
                    cur_on_num = idx
                    idx_map[cur_on_num] = 1
            else:
                cur_on_num = None

        # Now, we have a map of where all the numbers are. We need to find
        # whether there is a symbol around each of these numbers.
        # We start at the top, then left, then right, and then bottom.
        def has_symbol(row_idx, col_idx):
            if row_idx < 0 or row_idx >= len(data):
                return False
            line = data[row_idx]
            if col_idx < 0 or col_idx >= len(line):
                return False
            return line[col_idx] != "." and not line[col_idx].isnumeric()

        for idx, length in idx_map.items():
            number = int(line[idx : idx + length])
            # Top
            if any(has_symbol(row_idx - 1, idx - 1 + i) for i in range(length + 2)):
                result += number
                continue
            # Left
            if has_symbol(row_idx, idx - 1):
                result += number
                continue
            # Right
            if has_symbol(row_idx, idx + length):
                result += number
                continue
            # Bottom
            if any(has_symbol(row_idx + 1, idx - 1 + i) for i in range(length + 2)):
                result += number
                continue
    print(result)


def part_2():
    data = get_data()
    result = 0
    gear_nums = defaultdict(list)

    for row_idx, line in enumerate(data):
        cur_on_num = None
        idx_map = defaultdict(int)
        # First, assemble a map of all the numbers. This is keyed at the index
        # of the number, and the value is the length of the number.
        for idx, char in enumerate(line):
            if char.isnumeric():
                if cur_on_num is not None:
                    idx_map[cur_on_num] += 1
                else:
                    cur_on_num = idx
                    idx_map[cur_on_num] = 1
            else:
                cur_on_num = None

        # Now, we have a map of where all the numbers are. We need to find
        # all the gears
        def label_gears(row_idx, col_idx, number):
            if row_idx < 0 or row_idx >= len(data):
                return
            line = data[row_idx]
            if col_idx < 0 or col_idx >= len(line):
                return
            if line[col_idx] == "*":
                gear_nums[(row_idx, col_idx)].append(number)

        for idx, length in idx_map.items():
            number = int(line[idx : idx + length])
            # Top
            for i in range(length + 2):
                label_gears(row_idx - 1, idx - 1 + i, number)
            # Left
            label_gears(row_idx, idx - 1, number)
            # Right
            label_gears(row_idx, idx + length, number)
            # Bottom
            for i in range(length + 2):
                label_gears(row_idx + 1, idx - 1 + i, number)

    # Now, we have a map of all the gears. We need to find the one that has
    # exactly 2 numbers.
    for gear, numbers in gear_nums.items():
        if len(numbers) == 2:
            result += numbers[0] * numbers[1]

    print(result)
    return result


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
