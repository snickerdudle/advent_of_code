"""Day 2."""
from pathlib import Path


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_2.txt", "r") as f:
        data = f.read().strip().split("\n")
        data = [i.split(":", 1) for i in data]
        data = {int(i[5:]): v.split(";") for i, v in data}
        for i in data:
            rounds = [j.strip() for j in data[i]]
            # The rounds are comma-separated lists of 4 green, 3 red etc
            cleaned_rounds = []
            # The order is red, green, blue
            for round_ in rounds:
                nums = [0, 0, 0]
                colors = [j.strip() for j in round_.split(",")]
                for color in colors:
                    if "red" in color:
                        num = int(color.split(" ")[0])
                        nums[0] = num
                    elif "green" in color:
                        num = int(color.split(" ")[0])
                        nums[1] = num
                    elif "blue" in color:
                        num = int(color.split(" ")[0])
                        nums[2] = num
                cleaned_rounds.append(nums)
            data[i] = cleaned_rounds
    return data


def part_1():
    data = get_data()
    # data is keyed at game number. The values are a list of rounds, each round
    # is a list of 3 numbers, red, green, blue
    max_nums = [12, 13, 14]
    final_result = 0

    def all_le(round_):
        for i in range(3):
            if round_[i] > max_nums[i]:
                return False
        return True

    final_result = sum(
        [
            game_num
            for game_num in data
            if all(all_le(round_) for round_ in data[game_num])
        ]
    )
    print(final_result)


def part_2():
    data = get_data()
    # data is keyed at game number. The values are a list of rounds, each round
    # is a list of 3 numbers, red, green, blue
    results = 0

    for game_num, rounds in data.items():
        min_nums = [-1, -1, -1]
        for round_ in rounds:
            for i in range(3):
                min_nums[i] = max(min_nums[i], round_[i])
        results += min_nums[0] * min_nums[1] * min_nums[2]

    print(results)
    return results


if __name__ == "__main__":
    part_1()
    part_2()
