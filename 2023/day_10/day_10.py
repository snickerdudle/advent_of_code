"""Day 10."""
from pathlib import Path
import queue


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_10.txt", "r") as f:
        raw_data = f.read().strip().split("\n")
    return raw_data


raw_data = get_data()

allowed_dirs = {
    "|": [(-1, 0), (1, 0)],  # up and down
    "-": [(0, -1), (0, 1)],  # left and right
    "7": [(0, -1), (1, 0)],  # left and down
    "J": [(0, -1), (-1, 0)],  # left and up
    "L": [(0, 1), (-1, 0)],  # right and up
    "F": [(0, 1), (1, 0)],  # right and down
    "S": [(0, -1), (1, 0)],  # left and down, same as 7
}

pipe_to_touching = {
    "|": [(0, -1), (0, 1)],  # left and right
    "-": [(-1, 0), (1, 0)],  # up and down
    "7": [(-1, 0), (-1, 1), (0, 1), (1, -1)],  # up, up-right, right, down-left
    "J": [(1, 0), (1, 1), (0, 1), (-1, -1)],  # down, down-right, right, up-left
    "L": [(1, 0), (1, -1), (0, -1), (-1, 1)],  # down, down-left, left, up-right
    "F": [(-1, 0), (-1, -1), (0, -1), (1, 1)],  # up, up-left, left, down-right
    "S": [(-1, 0), (-1, 1), (0, 1), (1, -1)],  # same as 7
}

dir_change = {
    # Pipe: direction-in: rotation
    "L": {(1, 0): -1, (0, -1): 1},
    "7": {(-1, 0): -1, (0, 1): 1},
    "J": {(0, 1): -1, (1, 0): 1},
    "F": {(0, -1): -1, (-1, 0): 1},
}


def bfs_furthest(cur_pos=(0, 0), cur_max=0):
    q = queue.Queue()
    q.put((cur_pos, cur_max))
    visited = {}

    while not q.empty():
        cur_pos, cur_max = q.get()
        for dir in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if dir not in allowed_dirs[raw_data[cur_pos[0]][cur_pos[1]]]:
                continue
            # Up, right, down, left
            new_pos = (cur_pos[0] + dir[0], cur_pos[1] + dir[1])
            if 0 <= new_pos[0] < len(raw_data) and 0 <= new_pos[1] < len(raw_data[0]):
                # The pipe could possibly work
                if new_pos in visited:
                    continue
                visited[new_pos] = cur_max + 1
                q.put((new_pos, cur_max + 1))
    return max(visited.values())


def dfs_label(start_pos):
    cur_pos = start_pos
    visited = {}

    while True:
        # Get the current position
        visited[cur_pos] = len(visited)
        for dir in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if dir not in allowed_dirs[raw_data[cur_pos[0]][cur_pos[1]]]:
                continue
            # Up, right, down, left
            new_pos = (cur_pos[0] + dir[0], cur_pos[1] + dir[1])
            if 0 <= new_pos[0] < len(raw_data) and 0 <= new_pos[1] < len(raw_data[0]):
                # As opposed to the bfs, we don't care about the max and
                # will chose this path, ignoring others.
                if new_pos in visited:
                    continue
                cur_pos = new_pos
                break
        else:
            break
    return visited


def add_pos(pos1, pos2):
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])


def label_sides(start_pos, my_pipe):
    LeftSide = set()
    RightSide = set()
    orientation = 0
    sorted_pos = sorted(my_pipe.items(), key=lambda x: x[1])
    dirs = {(-1, 0): 0, (0, 1): 1, (1, 0): 2, (0, -1): 3}
    movement = []
    orientation = 0
    old_delta = None

    for i in range(len(sorted_pos)):
        cur_pos, new_pos = sorted_pos[i][0], sorted_pos[(i + 1) % len(sorted_pos)][0]
        delta = (new_pos[0] - cur_pos[0], new_pos[1] - cur_pos[1])
        if old_delta is None:
            old_delta = delta
        rotation = dirs[old_delta] - orientation
        movement.append(rotation)
        orientation += rotation

        cur_pipe = raw_data[cur_pos[0]][cur_pos[1]]
        if cur_pipe == "S":
            continue
        if cur_pipe in ["|", "-"]:
            # We are on a straight pipe, so we assume when moving up or right
            # that the touching points are A, B, and when moving down or left
            # that the touching points are B, A.
            if orientation % 4 <= 1:
                LeftSide.add(add_pos(cur_pos, pipe_to_touching[cur_pipe][0]))
                RightSide.add(add_pos(cur_pos, pipe_to_touching[cur_pipe][1]))
            else:
                LeftSide.add(add_pos(cur_pos, pipe_to_touching[cur_pipe][1]))
                RightSide.add(add_pos(cur_pos, pipe_to_touching[cur_pipe][0]))
        else:
            # We are on a corner pipe, so we need to figure out which turn we
            # have (right turn or left turn). If right turn, the corner is B and
            # the rest is A. Otherwise, the corner is A and the rest is B.
            if dir_change[cur_pipe][old_delta] == 1:
                for i in pipe_to_touching[cur_pipe][:-1]:
                    LeftSide.add(add_pos(cur_pos, i))
                RightSide.add(add_pos(cur_pos, pipe_to_touching[cur_pipe][-1]))
            else:
                LeftSide.add(add_pos(cur_pos, pipe_to_touching[cur_pipe][-1]))
                for i in pipe_to_touching[cur_pipe][:-1]:
                    RightSide.add(add_pos(cur_pos, i))

        old_delta = delta
    return LeftSide, RightSide


def bfs_flood(start_pos, my_pipe, visited=None):
    q = [start_pos]
    if visited is None:
        visited = set()
    touches_outer = False

    while q:
        cur_pos = q.pop()
        visited.add(cur_pos)
        for dir in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            # Up, right, down, left
            new_pos = (cur_pos[0] + dir[0], cur_pos[1] + dir[1])
            if new_pos in my_pipe:
                continue
            if new_pos in visited:
                continue
            if 0 <= new_pos[0] < len(raw_data) and 0 <= new_pos[1] < len(raw_data[0]):
                q.append(new_pos)
            else:
                touches_outer = True
                return True
    return touches_outer


def floodfill(point_set, my_pipe):
    final_set = set()
    touches_outer = False

    for pos in point_set:
        if pos in final_set:
            continue
        t = bfs_flood(pos, my_pipe, final_set)
        touches_outer = touches_outer or t
        if touches_outer:
            break
    return final_set, touches_outer


def part_1():
    map = get_data()
    for r in range(len(map)):
        for c in range(len(map[0])):
            if map[r][c] == "S":
                start_pos = (r, c)
                break

    print(bfs_furthest(start_pos))


def part_2():
    map = get_data()
    for r in range(len(map)):
        for c in range(len(map[0])):
            if map[r][c] == "S":
                start_pos = (r, c)
                break

    my_pipe = dfs_label(start_pos)

    # Now we need to start labeling either side of the pipe as A or B.
    LeftSide, RightSide = label_sides(start_pos, my_pipe)

    for pos in my_pipe:
        if pos in LeftSide:
            LeftSide.remove(pos)
        if pos in RightSide:
            RightSide.remove(pos)

    # Now we need to perform floodfill on the A and B sides to find the
    # distance from each of them to the start.
    final_left, left_touch = floodfill(LeftSide, my_pipe)
    final_right, right_touch = floodfill(RightSide, my_pipe)

    if left_touch:
        print("Left touches outer")
        print("Right inner:", len(final_right))
    else:
        print("Right touches outer")
        print("Left inner:", len(final_left))


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
