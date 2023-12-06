"""Day XXX."""
from pathlib import Path


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_XXX.txt", "r") as f:
        data = f.read().strip().split("\n")

    return data


def part_1():
    data = get_data()


def part_2():
    pass


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
