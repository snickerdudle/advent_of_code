"""Day 14."""
from pathlib import Path
from tqdm import tqdm


visited = {}


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_14.txt", "r") as f:
        raw_data = f.read().strip().split("\n")
        raw_data = [list(line) for line in raw_data]

    return raw_data


def printMap(data):
    s = ""
    for row in data:
        s += "".join(row) + "\n"
    print(s)


def tiltNorth(data):
    for c in range(len(data[0])):
        next_rock_idx = 0
        for r in range(len(data)):
            if data[r][c] == "O":
                # Move the rock
                if next_rock_idx != r:
                    data[next_rock_idx][c] = "O"
                    data[r][c] = "."
                next_rock_idx += 1
            elif data[r][c] == "#":
                next_rock_idx = r + 1
            else:
                pass
    return data


def tiltWest(data):
    for r in range(len(data)):
        next_rock_idx = 0
        for c in range(len(data[0])):
            if data[r][c] == "O":
                # Move the rock
                if next_rock_idx != c:
                    data[r][next_rock_idx] = "O"
                    data[r][c] = "."
                next_rock_idx += 1
            elif data[r][c] == "#":
                next_rock_idx = c + 1
            else:
                pass


def tiltSouth(data):
    for c in range(len(data[0])):
        next_rock_idx = len(data) - 1
        for r in range(len(data) - 1, -1, -1):
            if data[r][c] == "O":
                # Move the rock
                if next_rock_idx != r:
                    data[next_rock_idx][c] = "O"
                    data[r][c] = "."
                next_rock_idx -= 1
            elif data[r][c] == "#":
                next_rock_idx = r - 1
            else:
                pass
    return data


def tiltEast(data):
    for r in range(len(data)):
        next_rock_idx = len(data[0]) - 1
        for c in range(len(data[0]) - 1, -1, -1):
            if data[r][c] == "O":
                # Move the rock
                if next_rock_idx != c:
                    data[r][next_rock_idx] = "O"
                    data[r][c] = "."
                next_rock_idx -= 1
            elif data[r][c] == "#":
                next_rock_idx = c - 1
            else:
                pass


def getWeight(data):
    result = 0
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == "O":
                result += len(data) - row
    return result


def customHash(data):
    return hash("".join(["".join(row) for row in data]))


def part_1():
    raw_data = get_data()
    tiltNorth(raw_data)

    print(f"Weight: {getWeight(raw_data)}")


def part_2():
    raw_data = get_data()

    visited[customHash] = 0

    iteration = 0
    while iteration < 1_000_000_000:
        tiltNorth(raw_data)
        tiltWest(raw_data)
        tiltSouth(raw_data)
        tiltEast(raw_data)

        ch = customHash(raw_data)
        if ch in visited:
            last_seen = visited[ch]
            period = iteration - last_seen
            remaining = 1_000_000_000 - iteration
            remaining %= period
            iteration = 1_000_000_000 - remaining

        visited[ch] = iteration
        iteration += 1

    print(f"Weight: {getWeight(raw_data)}")


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
