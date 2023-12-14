"""Day 13."""
from pathlib import Path


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_13.txt", "r") as f:
        raw_data = f.read().strip().split("\n\n")
        raw_data = [i.split("\n") for i in raw_data]

    return raw_data


def hammingDistance(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


def getReflectionHorizontal(image, row, col):
    # If we have a 10x10 image, and are given row 2 and col 3 (0-indexed), we
    # will return the values in columns (0, 1, 2, 3) and (7, 6, 5, 4) (the same
    # number of cols on both sides.
    # If we are given column number 8, will will give back (8), (9)
    image_size = len(image[0])
    if not (0 <= col < image_size):
        raise ValueError("Column number is out of bounds.")
    if not (0 <= row < len(image)):
        raise ValueError("Row number is out of bounds.")

    mirror_size = min(col + 1, image_size - col - 1)
    left = image[row][col + 1 - mirror_size : col + 1]
    right = image[row][col + 1 : col + 1 + mirror_size][::-1]
    return left, right


def getReflectionVertical(image, row, col):
    image_size_vert = len(image)
    if not (0 <= col < len(image[0])):
        raise ValueError("Column number is out of bounds.")
    if not (0 <= row < image_size_vert):
        raise ValueError("Row number is out of bounds.")

    mirror_size = min(row + 1, image_size_vert - row - 1)
    top = image[row + 1 - mirror_size : row + 1]
    bottom = image[row + 1 : row + 1 + mirror_size]

    top = "".join([i[col] for i in top])
    bottom = "".join([i[col] for i in bottom[::-1]])
    return top, bottom


def findHorizontalReflections(image, smudge=0):
    image_size = len(image[0])
    total_set_hor = set([i for i in range(image_size - 1)])
    to_remove = set()

    for col in range(len(image[0])):
        cur_h = 0
        for row in range(len(image)):
            left, right = getReflectionHorizontal(image, row, col)
            cur_h += hammingDistance(left, right)
        if cur_h != smudge:
            to_remove.add(col)

    total_set_hor.difference_update(to_remove)
    return total_set_hor


def findVerticalReflections(image, smudge=0):
    image_size_vert = len(image)
    total_set_vert = set([i for i in range(image_size_vert - 1)])
    to_remove = set()

    for row in range(len(image)):
        cur_h = 0
        for col in range(len(image[row])):
            top, bottom = getReflectionVertical(image, row, col)
            cur_h += hammingDistance(top, bottom)
        if cur_h != smudge:
            to_remove.add(row)

    total_set_vert.difference_update(to_remove)
    return total_set_vert


def printHorizontalReflections(image, col):
    print(" " * col + "><")
    for i in image:
        print("".join(i))
    print(" " * col + "><")


def printVerticalReflections(image, row):
    for i, r in enumerate(image):
        if i == row:
            print("v ", end="")
        elif i == row + 1:
            print("^ ", end="")
        else:
            print("  ", end="")
        print("".join(r))
    print()


def part_1():
    raw_data = get_data()
    results = 0

    for image in raw_data:
        h = findHorizontalReflections(image)
        for i in h:
            # printHorizontalReflections(image, i)
            results += i + 1
        v = findVerticalReflections(image)
        for i in v:
            # printVerticalReflections(image, i)
            results += (i + 1) * 100
        if h and v:
            print("Both")

    print(results)


def part_2():
    raw_data = get_data()
    results = 0

    for image in raw_data:
        h = findHorizontalReflections(image, smudge=1)
        for i in h:
            # printHorizontalReflections(image, i)
            results += i + 1
        v = findVerticalReflections(image, smudge=1)
        for i in v:
            # printVerticalReflections(image, i)
            results += (i + 1) * 100
        if h and v:
            print("Both")

    print(results)


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
