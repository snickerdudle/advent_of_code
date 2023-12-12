"""Day 11."""
from pathlib import Path
import numpy as np


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_11.txt", "r") as f:
        raw_data = f.read().strip().split("\n")
        raw_data = np.array([list(line) for line in raw_data])
        raw_data = raw_data == "#"

    return raw_data


galaxy_scale = 2


def part_1():
    raw_data = get_data()
    # Get the rows where there are all False
    rows = np.all(~raw_data, axis=1)
    empty_rows = np.where(rows)[0]

    # Now same for columns
    cols = np.all(~raw_data, axis=0)
    empty_cols = np.where(cols)[0]

    # Now we get all the galaxies
    cur_galaxy = 1
    galaxies = {}
    for r in range(raw_data.shape[0]):
        for c in range(raw_data.shape[1]):
            if raw_data[r][c]:
                galaxies[cur_galaxy] = (
                    r,
                    c,
                )
                cur_galaxy += 1
    print(f"Found {len(galaxies)} galaxies")

    # Now assemble a list of pairwise links
    final_result = 0
    galaxy_pairs = set(
        tuple(
            sorted(
                (
                    g1,
                    g2,
                )
            )
        )
        for g1 in galaxies.keys()
        for g2 in galaxies.keys()
    )

    # Now we need to find the manhattan distance between each pair
    for g1, g2 in galaxy_pairs:
        if g1 == g2:
            continue
        r1, c1 = galaxies[g1]
        r2, c2 = galaxies[g2]

        r1, r2 = sorted((r1, r2))
        c1, c2 = sorted((c1, c2))

        dist = abs(r2 - r1) + abs(c2 - c1)

        # It is possible to have an empty row, so check
        for row in empty_rows:
            if r1 < row < r2:
                dist += galaxy_scale - 1
                # print(f"Adding row {row} between {r1} and {r2}")

        for col in empty_cols:
            if c1 < col < c2:
                dist += galaxy_scale - 1
                # print(f"Adding col {col} between {c1} and {c2}")

        final_result += dist

    print(f"Final result: {final_result}")


def part_2():
    global galaxy_scale
    galaxy_scale = 1_000_000
    part_1()


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
