"""Day 22."""


def get_data():
    with open("day_22.txt", "r") as f:
        data = f.read().rstrip().split("\n")
        directions = data[-1]
        data = data[:-2]
        # Expand the data by one in each direction
        data = [" " + i + " " for i in data]
        data = [" " * len(data[0])] + data + [" " * len(data[0])]
        max_len = max([len(i) for i in data])
        data = [i.ljust(max_len, " ") for i in data]
        data = [[i for i in ii] for ii in data]
    directions = directions.replace("R", ",R,")
    directions = directions.replace("L", ",L,")
    directions = [i for i in directions.split(",") if i]
    return directions, data


dirs = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}


def findStartingLocation(data):
    for i in range(len(data[0])):
        if data[1][i] == ".":
            return (1, i)


def getOppositeLocation(loc, cur_dir, data):
    new_loc = None
    if cur_dir == 0:
        # Facing right, search from left to right in this row
        for i in range(0, loc[1] + 1):
            if data[loc[0]][i] in [".", "#"]:
                new_loc = (
                    loc[0],
                    i,
                )
                break
    elif cur_dir == 1:
        # Facing down, search from top to bottom in this column
        for i in range(0, loc[0] + 1):
            if data[i][loc[1]] in [".", "#"]:
                new_loc = (
                    i,
                    loc[1],
                )
                break
    elif cur_dir == 2:
        # Facing left, search from right to left in this row
        for i in range(len(data[0]) - 1, loc[1] - 1, -1):
            if data[loc[0]][i] in [".", "#"]:
                new_loc = (
                    loc[0],
                    i,
                )
                break
    elif cur_dir == 3:
        # Facing up, search from bottom to top in this column
        for i in range(len(data) - 1, loc[0] - 1, -1):
            if data[i][loc[1]] in [".", "#"]:
                new_loc = (
                    i,
                    loc[1],
                )
                break
    else:
        raise ValueError("Invalid direction")

    return new_loc, cur_dir


def getBoxLocation(temp_loc, temp_dir, data):
    pass


def tryMove(cur_loc, cur_dir, steps, data, use_box: bool = False):
    temp_loc = cur_loc
    temp_dir = cur_dir
    i = 1
    while i <= steps:
        new_attempt = (
            temp_loc[0] + dirs[temp_dir][0],
            temp_loc[1] + dirs[temp_dir][1],
        )
        if data[new_attempt[0]][new_attempt[1]] not in [".", "#"]:
            # We're off the board, need to circle back
            if not use_box:
                new_loc, new_dir = getOppositeLocation(temp_loc, temp_dir, data)
            else:
                new_loc, new_dir = getBoxLocation(temp_loc, temp_dir, data)
        else:
            new_loc = new_attempt
            new_dir = temp_dir

        # Now that we've landed, let's see what we have
        if data[new_loc[0]][new_loc[1]] == "#":
            # We've hit a wall, do nothing
            pass
        elif data[new_loc[0]][new_loc[1]] == ".":
            # We can move forward, do so
            temp_loc = new_loc
            temp_dir = new_dir

        i += 1

    return temp_loc, temp_dir


def part_1():
    directions, data = get_data()
    cur_loc = findStartingLocation(data)
    print(f"Starting location: {cur_loc}")
    cur_dir = 0

    print(directions)

    for i in directions:
        if i.isnumeric():
            # Try to move forward for as many steps as possible
            cur_loc, _ = tryMove(cur_loc, cur_dir, int(i), data)
        else:
            cur_dir = (cur_dir + (1 if i == "R" else -1)) % 4

        print(cur_loc)
    print(
        f"Answer: 1000*{cur_loc[0]} + 4*{cur_loc[1]} + {cur_dir} =",
        1000 * cur_loc[0] + 4 * cur_loc[1] + cur_dir,
    )


def part_2():
    pass


if __name__ == "__main__":
    part_1()
    # part_2()
