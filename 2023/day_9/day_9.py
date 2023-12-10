"""Day 9."""
from pathlib import Path


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_9.txt", "r") as f:
        raw_data = f.read().strip().split("\n")
        raw_data = [[int(x) for x in i.split(" ")] for i in raw_data]

    return raw_data


def getDerivative(data):
    derivative = [data[i + 1] - data[i] for i in range(len(data) - 1)]
    return derivative


def part_1():
    raw_data = get_data()

    results = []
    for data in raw_data:
        derivatives = [data]
        while True:
            cur_derivative = getDerivative(data)
            derivatives.append(cur_derivative)
            if all([i == 0 for i in cur_derivative]):
                break
            data = cur_derivative

        # Now we have all the derivatives. We start going backwards and adding\
        # the derivatives to the previous data.
        cur_num = derivatives[-1][-1]
        for i in range(len(derivatives) - 2, -1, -1):
            # Starting at the second to last derivative, we add the current
            # number to the previous data.
            cur_num += derivatives[i][-1]
        results.append(cur_num)

    print(sum(results))


def part_2():
    raw_data = get_data()

    results = []
    for data in raw_data:
        derivatives = [data]
        while True:
            cur_derivative = getDerivative(data)
            derivatives.append(cur_derivative)
            if all([i == 0 for i in cur_derivative]):
                break
            data = cur_derivative

        # Now we have all the derivatives. We start going backwards and adding\
        # the derivatives to the previous data.
        cur_num = derivatives[-1][0]
        for i in range(len(derivatives) - 2, -1, -1):
            # Starting at the second to last derivative, we add the current
            # number to the previous data.
            cur_num = derivatives[i][0] - cur_num
        results.append(cur_num)

    print(sum(results))


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
