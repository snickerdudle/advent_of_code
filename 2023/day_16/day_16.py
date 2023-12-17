"""Day 16."""
from pathlib import Path


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_16.txt", "r") as f:
        raw_data = f.read().strip().split("\n")

    return raw_data


dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # N, E, S, W


def light_dfs(data, start_pos=(0, 0), start_dir=1):
    stack = []
    stack.append((start_pos[0], start_pos[1], start_dir))  # (row, col, direction)
    visited = set()

    def continuePath(row, col, direction):
        new_pos = (row + dirs[direction][0], col + dirs[direction][1])
        if 0 <= new_pos[0] < len(data) and 0 <= new_pos[1] < len(data[0]):
            if (new_pos[0], new_pos[1], direction) in visited:
                return
            stack.append((new_pos[0], new_pos[1], direction))

    def maybeAddNewPos(new_pos, direction):
        if 0 <= new_pos[0] < len(data) and 0 <= new_pos[1] < len(data[0]):
            if (new_pos[0], new_pos[1], direction) not in visited:
                stack.append((new_pos[0], new_pos[1], direction))

    while stack:
        row, col, direction = stack.pop()
        visited.add((row, col, direction))

        cur_tile = data[row][col]
        if cur_tile == ".":
            # Do nothing except continue in the same direction
            continuePath(row, col, direction)
        elif cur_tile == "|":
            # Need to check if we are East or West
            if direction == 1 or direction == 3:
                # Add North
                new_pos = (row - 1, col)
                direction = 0
                maybeAddNewPos(new_pos, direction)
                # Add South
                new_pos = (row + 1, col)
                direction = 2
                maybeAddNewPos(new_pos, direction)
            else:
                continuePath(row, col, direction)
        elif cur_tile == "-":
            # Need to check if we are North or South
            if direction == 0 or direction == 2:
                # Add East
                new_pos = (row, col + 1)
                direction = 1
                maybeAddNewPos(new_pos, direction)
                # Add West
                new_pos = (row, col - 1)
                direction = 3
                maybeAddNewPos(new_pos, direction)
            else:
                continuePath(row, col, direction)
        elif cur_tile == "\\":
            # If East or West, add +1 to direction (south and north)
            # If North or South, add -1 to direction (west and east)
            if direction == 1 or direction == 3:
                direction += 1
            elif direction == 0 or direction == 2:
                direction -= 1
            direction %= 4
            new_pos = (row + dirs[direction][0], col + dirs[direction][1])
            maybeAddNewPos(new_pos, direction)
        elif cur_tile == "/":
            # If East or West, add -1 to direction (north and south)
            # If North or South, add +1 to direction (west and east)
            if direction == 1 or direction == 3:
                direction -= 1
            elif direction == 0 or direction == 2:
                direction += 1
            direction %= 4
            new_pos = (row + dirs[direction][0], col + dirs[direction][1])
            maybeAddNewPos(new_pos, direction)
        else:
            raise ValueError("Unknown tile: {}".format(cur_tile))
    return len(set([(r, c) for r, c, d in visited]))


def part_1():
    raw_data = get_data()
    print(light_dfs(raw_data))


def part_2():
    raw_data = get_data()
    max_energized = 0
    for row in range(len(raw_data)):
        # left side to the right
        max_energized = max(max_energized, light_dfs(raw_data, (row, 0), 1))
        # right side to the left
        max_energized = max(
            max_energized, light_dfs(raw_data, (row, len(raw_data[0]) - 1), 3)
        )
    for col in range(len(raw_data[0])):
        # top to bottom
        max_energized = max(max_energized, light_dfs(raw_data, (0, col), 2))
        # bottom to top
        max_energized = max(
            max_energized, light_dfs(raw_data, (len(raw_data) - 1, col), 0)
        )
    print(max_energized)


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
