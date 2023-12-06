"""Day 1."""
from pathlib import Path


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_1.txt", "r") as f:
        data = f.read().strip().split("\n")

    return data


def part_1():
    data = get_data()
    cur_val = 0

    # For every line
    for line in data:
        # Get all the numerics
        nums = [int(i) for i in line if i.isnumeric()]
        # Now get the first and the last
        cur_val += nums[0] * 10 + nums[-1]

    print("Final value:", cur_val)
    return cur_val


def part_2():
    letters = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    data = get_data()
    cur_val = 0

    # For every line
    for line in data:
        nums = []
        # Start iterating through the line
        idx = 0
        while idx < len(line):
            # If the letter is numeric, skip it
            if line[idx].isnumeric():
                nums.append(int(line[idx]))
            else:
                # Check to see if the next N characters match the letter
                for letter in letters:
                    if line[idx : idx + len(letter)] == letter:
                        nums.append(letters[letter])
                        break
            idx += 1
        # Now get the first and the last
        cur_val += nums[0] * 10 + nums[-1]

    print("Final value:", cur_val)
    return cur_val


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
