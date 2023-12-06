"""Day 5."""
from pathlib import Path


def get_data():
    cur_dir = Path(__file__).parent.absolute()
    with open(cur_dir / "day_5.txt", "r") as f:
        raw_data = f.read().strip().split("\n\n")

    # Get the seeds
    seeds = raw_data[0].strip().split(": ")[1].split(" ")
    seeds = [int(seed) for seed in seeds]

    # Get the rule sets
    rule_sets = [i.split("\n")[1:] for i in raw_data[1:]]

    return seeds, rule_sets


class Converter:
    def __init__(self, rule_sets):
        self.rule_sets = rule_sets
        self.next = None
        # Each interval is a tuple.
        # (source_start, length, target_offset)
        # Where if target_offset is 5 and source_start is 0, then
        # 0 -> 5
        self.intervals = self._populateIntervals()

    def _populateIntervals(self):
        result = []
        for rule_set in self.rule_sets:
            dest, source, length = [int(i) for i in rule_set.split(" ")]
            result.append((source, length, dest - source))

        result = sorted(result, key=lambda x: x[0])

        # Fill in the gaps from 0
        additions = []
        if result[0][0] != 0:
            additions.append((0, result[0][0], 0))

        for i in range(len(result) - 1):
            if result[i][0] + result[i][1] != result[i + 1][0]:
                additions.append(
                    (
                        result[i][0] + result[i][1],
                        result[i + 1][0] - result[i][0] - result[i][1],
                        0,
                    )
                )

        result += additions
        result = sorted(result, key=lambda x: x[0])

        return result

    def setNext(self, next):
        self.next = next

    def setLast(self, last):
        if self.next is None:
            self.setNext(last)
        else:
            self.next.setLast(last)

    def convert(self, seed):
        if seed >= self.intervals[-1][0] + self.intervals[-1][1]:
            return seed

        for source, length, offset in self.intervals:
            if seed >= source and seed < source + length:
                return seed + offset

    def convertLast(self, seed):
        if self.next is None:
            return self.convert(seed)
        else:
            return self.next.convertLast(self.convert(seed))

    def getIntervalsFromRange(self, seed_start, seed_length):
        """Given a start seed and a length, return the intervals that are
        relevant to that range.
        """
        result = []
        if seed_start >= self.intervals[-1][0] + self.intervals[-1][1]:
            return [
                (
                    seed_start,
                    seed_length,
                    0,
                )
            ]
        for source, length, offset in self.intervals:
            if seed_length <= 0:
                break
            if seed_start >= source and seed_start < source + length:
                # We are in the correct interval. Now get the start (incl) and
                # the end (excl) of the internal range.
                cur_start, cur_end = (
                    seed_start,
                    min(seed_start + seed_length, source + length),
                )
                cur_length = cur_end - cur_start
                result.append(
                    (
                        cur_start,
                        cur_length,
                        offset,
                    )
                )
                seed_length -= cur_length
                seed_start += cur_length
        if seed_length > 0:
            result.append(
                (
                    seed_start,
                    seed_length,
                    0,
                )
            )
        return result

    def getLastIntervalsFromRange(self, input_intervals):
        """Given a start seed and a length, return the intervals that are
        relevant to that range.
        """
        source_intervals = []
        dest_intervals = []

        for seed_start, seed_length in input_intervals:
            source_intervals += self.getIntervalsFromRange(seed_start, seed_length)

        for source, length, offset in source_intervals:
            dest_intervals.append(
                (
                    source + offset,
                    length,
                )
            )
        dest_intervals = sorted(dest_intervals, key=lambda x: x[0])

        if self.next is None:
            return dest_intervals
        else:
            return self.next.getLastIntervalsFromRange(dest_intervals)


def part_1():
    seeds, rule_sets = get_data()
    c = Converter(rule_sets[0])
    for rule_set in rule_sets[1:]:
        c.setLast(Converter(rule_set))

    results = [c.convertLast(seed) for seed in seeds]
    print(min(results))


def part_2():
    seeds, rule_sets = get_data()
    c = Converter(rule_sets[0])
    for rule_set in rule_sets[1:]:
        c.setLast(Converter(rule_set))

    results = [c.convertLast(seed) for seed in seeds]

    print(c.getLastIntervalsFromRange(zip(seeds[0::2], seeds[1::2]))[0][0])


if __name__ == "__main__":
    print("Part 1:")
    part_1()

    print("\nPart 2:")
    part_2()
